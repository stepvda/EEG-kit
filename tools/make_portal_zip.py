#!/usr/bin/env python3
"""
make_portal_zip.py -- pack the KiCad 10 layout-input set as one archive for upload to
the JLCPCB portal at design.jlcpcb.com/quote.

**Nothing here uploads anything.**  It writes a file into `dist/`.  Stephane uploads it.

**The PACKING is deterministic.**  Every member is stored with a fixed timestamp and
fixed permissions, in sorted order, so packing the same directory twice gives the same
bytes; without that a zip records the mtime of the files that made it and differs from
itself run to run.

**Re-emitting the directory is not.**  `kicad-cli` mints a fresh random UUID for every
element it upgrades, so a new emission changes the `.kicad_pcb` and `.kicad_sch` files --
in UUIDs only, measured, nothing else -- and the DRC report carries the time it ran.  So
the archive's own checksum identifies THIS emission and is not a fingerprint of the
design.  The manifest inside it says the same thing in the same words.

`dist/` is a build directory and is not tracked.  The repository does carry two Gerber
zips under `kicad/`, so there is precedent for an archive in the tree, but a layout input
set is rebuilt by `tools/emit_all.py` in a minute and a 3 MB binary that duplicates
51 tracked files earns nothing by being committed.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import hashlib
import os
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import design as D          # noqa: E402

DIST = os.path.join(PKG, "dist")
SRC = os.path.join(PKG, "kicad", "RevC_layout_inputs_kicad10")
NAME = "EEG-CAR-01_RevC_layout_inputs_kicad10"

# A fixed DOS timestamp so the archive is byte-identical run to run: 1 January 1980,
# which is the earliest a zip can express.
FIXED = (1980, 1, 1, 0, 0, 0)

# The portal's practical ceiling.  Above this, say so and propose a split rather than
# deciding one.
SOFT_LIMIT = 100 * 1024 * 1024


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def members(src):
    """(absolute path, name inside the archive), sorted, so the order is stable."""
    out = []
    for root, dirs, files in os.walk(src):
        dirs.sort()
        for f in sorted(files):
            p = os.path.join(root, f)
            out.append((p, os.path.join(NAME, os.path.relpath(p, src))))
    return sorted(out, key=lambda t: t[1])


def build(src=SRC, dist=DIST, verbose=True):
    if not os.path.isdir(src):
        raise SystemExit(f"{os.path.relpath(src, PKG)} does not exist; run "
                         f"tools/emit_all.py first")
    os.makedirs(dist, exist_ok=True)
    out = os.path.join(dist, f"{NAME}.zip")
    mem = members(src)
    raw = sum(os.path.getsize(p) for p, _ in mem)

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path, arc in mem:
            zi = zipfile.ZipInfo(arc, date_time=FIXED)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            with open(path, "rb") as f:
                z.writestr(zi, f.read())

    packed = os.path.getsize(out)
    if verbose:
        print(f"    {os.path.relpath(out, PKG)}")
        print(f"    {len(mem)} files, {raw:,} bytes uncompressed, "
              f"{packed:,} bytes compressed ({100 * packed / raw:.1f} %)")
        print(f"    sha256 {sha256(out)}")
        if packed > SOFT_LIMIT:
            print(f"    ** {packed / 1e6:.0f} MB exceeds the ~100 MB the portal "
                  f"accepts comfortably. It needs splitting; that is a decision, not "
                  f"something this tool takes.")
    return out, raw, packed, len(mem)


def verify(zip_path=None, verbose=True):
    """Extract the archive to a scratch directory and check every file against the
    SHA256SUMS.txt that travels inside it.  An archive that does not reproduce its own
    manifest is worse than no archive."""
    import tempfile
    zip_path = zip_path or os.path.join(DIST, f"{NAME}.zip")
    with tempfile.TemporaryDirectory() as td:
        with zipfile.ZipFile(zip_path) as z:
            z.extractall(td)
        root = os.path.join(td, NAME)
        man = os.path.join(root, "SHA256SUMS.txt")
        if not os.path.exists(man):
            raise SystemExit("the archive carries no SHA256SUMS.txt")

        # the manifest lists, per file: "  <name>", a description, then "  <sha>  <n> bytes"
        want, name = {}, None
        for line in open(man):
            s = line.rstrip("\n")
            if s.startswith("  ") and not s.startswith("      ") and s.strip():
                name = s.strip()
            elif s.startswith("      ") and name:
                parts = s.split()
                if len(parts) >= 3 and len(parts[0]) == 64:
                    want[name] = (parts[0], int(parts[1]))
                    name = None
        bad, missing = [], []
        for n, (sha, size) in sorted(want.items()):
            p = os.path.join(root, n)
            if not os.path.exists(p):
                missing.append(n)
                continue
            got = sha256(p)
            if got != sha or os.path.getsize(p) != size:
                bad.append(f"{n}: manifest {sha[:16]}.. / {size} B, "
                           f"extracted {got[:16]}.. / {os.path.getsize(p)} B")
        extracted = sum(len(fs) for _r, _d, fs in os.walk(root))
        if verbose:
            print(f"    extracted {extracted} files; {len(want)} carry a checksum in "
                  f"the manifest")
            print(f"    checksum mismatches: {len(bad)}   missing: {len(missing)}")
            for b in bad[:10]:
                print("      " + b)
            for m in missing[:10]:
                print("      missing " + m)
        if bad or missing:
            raise SystemExit(f"the archive does not reproduce its own manifest: "
                             f"{len(bad)} mismatch(es), {len(missing)} missing")
    return len(want)


def main(verbose=True):
    print(f"== EEG-CAR-01 Rev {D.REV_C} -- portal archive, KiCad 10 set ==")
    out, raw, packed, n = build(verbose=verbose)
    ok = verify(out, verbose=verbose)
    if verbose:
        print(f"    the archive reproduces all {ok} checksums in its own manifest")
    return out


if __name__ == "__main__":
    main()

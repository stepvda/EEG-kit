#!/usr/bin/env python3
"""
kicad_fmt.py -- emit the Rev C layout-input set in more than one KiCad file format.

The JLCPCB layout desk runs KiCad 10.  The set is written by this programme's own
s-expression writers in the KiCad 8 dialect (`tools/kicad_pcb8.py`,
`tools/kicad_sch.py`), and opening a KiCad 8 project in KiCad 10 can silently alter the
net classes, the custom rules and the DRC severities -- which is where most of the
layout specification lives.  So the set is emitted for both, and the two are diffed.

**How the second format is produced, and why not by a second writer.**  KiCad's own
`kicad-cli ... upgrade` rewrites a file in the running KiCad's native format.  That is
used here rather than teaching the Python writers a second dialect, for one reason: the
KiCad 10 s-expression schema is KiCad's to define and not ours to infer.  A hand-written
`(version 20260206)` would be a guess at a format we cannot read from a specification,
and a guess in the net classes or the rules is exactly the failure this whole exercise
exists to prevent.  KiCad's upgrader is authoritative about KiCad's format.

So there is still ONE source -- `tools/design.py` -- and one set of writers.  The KiCad
10 target is the KiCad 8 emission passed through KiCad's own converter, which makes the
two sets equivalent by construction rather than by assertion, and leaves nothing to keep
in step by hand.

**The version numbers below were measured, not remembered.**  They were read out of
files that KiCad 10.0.6 had just written, by upgrading the released set in a scratch
directory and reading the tokens back.  `verify()` re-reads them on every emission, so a
different KiCad silently producing a third format is an error and not a surprise.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
sys.path.insert(0, HERE)


# --------------------------------------------------------------------------- profiles
@dataclass
class Format:
    key: str
    label: str                 # what to call it in a README
    pcb_version: int           # the (version N) token of a .kicad_pcb
    sch_version: int           # the (version N) token of a .kicad_sch
    generator_version: str     # the (generator_version "N") token
    cli_major: str = ""        # kicad-cli must report this major version
    needs_cli: bool = False    # whether producing it requires KiCad installed
    measured_on: str = ""      # the KiCad build the tokens were read from


# KiCad 8: what tools/kicad_pcb8.py and tools/kicad_sch.py write directly.
KICAD8 = Format(
    key="kicad8", label="KiCad 8",
    pcb_version=20240108, sch_version=20231120, generator_version="8.0",
    needs_cli=False,
    measured_on="written directly by tools/kicad_pcb8.py and tools/kicad_sch.py")

# KiCad 10: read out of files kicad-cli 10.0.6 wrote on 9 September 2026.
KICAD10 = Format(
    key="kicad10", label="KiCad 10",
    pcb_version=20260206, sch_version=20260306, generator_version="10.0",
    cli_major="10", needs_cli=True,
    measured_on="kicad-cli 10.0.6")

FORMATS = {f.key: f for f in (KICAD8, KICAD10)}


# --------------------------------------------------------------------------- the cli
CLI_CANDIDATES = (
    os.environ.get("KICAD_CLI", ""),
    os.path.expanduser("~/Applications/KiCad.app/Contents/MacOS/kicad-cli"),
    "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli",
    "/Applications/KiCad.app/Contents/MacOS/kicad-cli",
    shutil.which("kicad-cli") or "",
)


def find_cli():
    """The kicad-cli to use, or None.  None is not an error here: it is an error only
    when a target that needs it is asked for, and the caller says so in its own words."""
    for c in CLI_CANDIDATES:
        if c and os.path.isfile(c) and os.access(c, os.X_OK):
            return c
    return None


def cli_version(cli=None):
    cli = cli or find_cli()
    if not cli:
        return None
    r = subprocess.run([cli, "version"], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


# --------------------------------------------------------------------------- reading
_VER = re.compile(r"\(version\s+(\d{8})\s*\)")
_GEN = re.compile(r'\(generator_version\s+"([^"]+)"\s*\)')


def read_tokens(path):
    """(version, generator_version) from the head of a KiCad s-expression file."""
    with open(path, errors="replace") as f:
        head = f.read(4096)
    v = _VER.search(head)
    g = _GEN.search(head)
    return (int(v.group(1)) if v else None, g.group(1) if g else None)


def verify(directory, fmt, verbose=True):
    """Every .kicad_pcb and .kicad_sch in `directory` carries `fmt`'s tokens.

    This is the check that a format target actually happened.  `kicad-cli sch upgrade`
    does NOT recurse into hierarchical sheets -- it rewrites the file it is given and
    nothing else -- so a set whose root sheet upgraded and whose nine children did not
    would open, look right, and be half one format and half the other.
    """
    bad = []
    for name in sorted(os.listdir(directory)):
        p = os.path.join(directory, name)
        if name.endswith(".kicad_pcb"):
            want = fmt.pcb_version
        elif name.endswith(".kicad_sch"):
            want = fmt.sch_version
        else:
            continue
        got, gen = read_tokens(p)
        if got != want:
            bad.append(f"{name}: (version {got}), expected {want}")
        elif gen != fmt.generator_version:
            bad.append(f'{name}: (generator_version "{gen}"), '
                       f'expected "{fmt.generator_version}"')
    if bad:
        raise SystemExit(f"{fmt.label} format check failed on {len(bad)} file(s):\n  "
                         + "\n  ".join(bad))
    n = sum(1 for f in os.listdir(directory)
            if f.endswith((".kicad_pcb", ".kicad_sch")))
    if verbose:
        print(f"    {n} file(s) carry the {fmt.label} tokens "
              f"(pcb {fmt.pcb_version}, sch {fmt.sch_version}, "
              f'generator_version "{fmt.generator_version}")')
    return n


# --------------------------------------------------------------------------- emitting
def convert_tree(directory, fmt, cli=None, verbose=True):
    """Rewrite the KiCad files in `directory` in `fmt`'s format, in place.

    `directory` is expected to be a COPY of the KiCad 8 emission; nothing here reads or
    writes the source tree.  Returns the list of files rewritten.
    """
    if not fmt.needs_cli:
        return []
    cli = cli or find_cli()
    if not cli:
        raise SystemExit(
            f"the {fmt.label} target needs kicad-cli and none was found. Set KICAD_CLI "
            f"to it, or install KiCad {fmt.cli_major}. Looked in:\n  "
            + "\n  ".join(c for c in CLI_CANDIDATES if c))
    ver = cli_version(cli)
    if not ver or not ver.startswith(fmt.cli_major + "."):
        raise SystemExit(
            f"the {fmt.label} target needs kicad-cli {fmt.cli_major}.x; {cli} reports "
            f"{ver!r}. Emitting with a different KiCad would write a format this "
            f"programme has not measured and cannot check.")

    done = []
    pcbs = sorted(f for f in os.listdir(directory) if f.endswith(".kicad_pcb"))
    schs = sorted(f for f in os.listdir(directory) if f.endswith(".kicad_sch"))
    syms = sorted(f for f in os.listdir(directory) if f.endswith(".kicad_sym"))

    def run(args, what):
        r = subprocess.run([cli] + args, capture_output=True, text=True,
                           cwd=directory)
        if r.returncode != 0:
            raise SystemExit(f"kicad-cli {' '.join(args[:2])} failed on {what}:\n"
                             f"{r.stdout}\n{r.stderr}")
        return r.stdout.strip()

    for f in pcbs:
        run(["pcb", "upgrade", f], f)
        done.append(f)
    # every sheet individually: `sch upgrade` rewrites one file and does not follow
    # the hierarchy, so the root sheet alone would leave the nine children at KiCad 8.
    for f in schs:
        run(["sch", "upgrade", f], f)
        done.append(f)
    for f in syms:
        run(["sym", "upgrade", "--force", f], f)
        done.append(f)
    if verbose:
        print(f"    {len(pcbs)} board, {len(schs)} schematic and {len(syms)} symbol "
              f"file(s) rewritten as {fmt.label} by kicad-cli {ver}")
    return done


def run_drc(directory, pcb, out_name="drc_kicad10.txt", cli=None):
    """`kicad-cli pcb drc` in `directory`.  Returns (ok, text, path) or (None, why, None)
    when there is no KiCad to run it with -- the caller reports that as NOT PERFORMED
    rather than as a pass."""
    cli = cli or find_cli()
    if not cli:
        return None, "kicad-cli not found on this machine", None
    r = subprocess.run(
        [cli, "pcb", "drc", "--severity-all", "--format", "report",
         "-o", out_name, pcb],
        capture_output=True, text=True, cwd=directory)
    path = os.path.join(directory, out_name)
    if r.returncode != 0 or not os.path.exists(path):
        return False, (r.stdout + r.stderr).strip(), None
    return True, open(path).read(), path


def run_erc(directory, sch, out_name="erc_kicad10.txt", cli=None):
    """`kicad-cli sch erc`, same contract as run_drc()."""
    cli = cli or find_cli()
    if not cli:
        return None, "kicad-cli not found on this machine", None
    r = subprocess.run(
        [cli, "sch", "erc", "--severity-all", "--format", "report",
         "-o", out_name, sch],
        capture_output=True, text=True, cwd=directory)
    path = os.path.join(directory, out_name)
    if not os.path.exists(path):
        return False, (r.stdout + r.stderr).strip(), None
    return True, open(path).read(), path


def report(fmt, cli=None):
    """A line for a README or an equivalence report saying what produced this format."""
    if not fmt.needs_cli:
        return f"{fmt.label}: written directly by this programme's writers."
    return (f"{fmt.label}: produced from the {KICAD8.label} emission by "
            f"`kicad-cli {cli_version(cli) or '?'}` "
            f"(`pcb upgrade`, `sch upgrade`, `sym upgrade`).")


if __name__ == "__main__":
    cli = find_cli()
    print(f"kicad-cli : {cli or 'NOT FOUND'}")
    print(f"version   : {cli_version(cli) or '--'}")
    for f in FORMATS.values():
        print(f"\n{f.key}: {f.label}")
        print(f"  pcb (version {f.pcb_version}), sch (version {f.sch_version}), "
              f'generator_version "{f.generator_version}"')
        print(f"  measured on: {f.measured_on}")
    if len(sys.argv) > 2 and sys.argv[1] == "--verify":
        verify(sys.argv[2], FORMATS[sys.argv[3] if len(sys.argv) > 3 else "kicad8"])

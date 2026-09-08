#!/usr/bin/env python3
"""
revision_bump.py -- advance the revision letter of every document a change touched, and
bring every cross-reference to it up to date.

ECO-EEG-016 section 3 step 6 says to bump the revision of every document a change
touches, and section 1.5 says that an older letter in a cross-reference is a defect and
not a synonym -- Rev A's escape clause, that an older letter "means the same document as
corrected in this release", is withdrawn.  Doing that by hand across twenty documents and
two hundred citations is how the package came to have sixty disagreements in the first
place.

`tools/finalise_docs.py` already does the same job as part of a full release.  This is a
narrower tool for one round: it takes an explicit list of documents and letters, so that
nothing moves that the round did not touch, and it says what it changed.

    python3 revision_bump.py --dry     say what would change
    python3 revision_bump.py           do it

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
DOCS = os.path.join(PKG, "docs")

# The documents this round changed, and the letter each moves to.  A document not on this
# list is not touched, and its citations are not rewritten.
BUMP = {
    "DSN-EEG-003": ("C", "D"),
    "ECO-EEG-016": ("B", "C"),
    "ICD-EEG-006": ("B", "C"),
    "FW-EEG-001": ("C", "D"),
    "JIG-EEG-009": ("B", "C"),
    "AVL-EEG-017": ("B", "C"),
    "ASM-EEG-023": ("A", "B"),
    "RUL-EEG-021": ("A", "B"),
}

# Files outside docs/ that cite a document by identifier and letter.
OTHER = ["tools/DESIGN_FACTS.md", "tools/RULINGS.md", "constraints/nets.md",
         "README.md", "README_package_index.txt", "KNOWN_ISSUES.txt"]

# Tools that hard-code a document FILE NAME, which the rename breaks.
TOOLS = ["tools/simulate_production.py", "tools/finalise_docs.py",
         "tools/check_consistency.py", "tools/emit_workbooks.py",
         "tools/emit_costed_bom.py"]


def _text_files():
    out = []
    for f in sorted(os.listdir(DOCS)):
        if f.endswith(".md"):
            out.append(os.path.join(DOCS, f))
    for rel in OTHER + TOOLS:
        p = os.path.join(PKG, rel)
        if os.path.exists(p):
            out.append(p)
    return out


def bump_front_matter(dry=False):
    """The `**Document:** X **Revision:** Y` line each document declares itself with."""
    changed = []
    for f in sorted(os.listdir(DOCS)):
        if not f.endswith(".md"):
            continue
        p = os.path.join(DOCS, f)
        t = open(p).read()
        m = re.search(r"\*\*Document:\*\*\s*([A-Z]+-EEG-\d+)\s+\*\*Revision:\*\*\s*"
                      r"\*{0,2}([A-Z])\*{0,2}", t)
        if not m:
            continue
        did, old = m.group(1), m.group(2)
        if did not in BUMP:
            continue
        want_old, new = BUMP[did]
        if old == new:
            continue
        if old != want_old:
            raise SystemExit(f"{f} declares Rev {old}; expected Rev {want_old}")
        t2 = t[:m.start(2)] + new + t[m.end(2):]
        if not dry:
            open(p, "w").write(t2)
        changed.append((f, did, old, new))
    return changed


def rewrite_citations(dry=False):
    """Every `XXX-EEG-nnn Rev <letter>` for a document on the list."""
    hits = {}
    for p in _text_files():
        t = open(p).read()
        o = t
        for did, (old, new) in BUMP.items():
            # `Rev A.2` is a package v1 sub-revision and is never a citation of a
            # current letter, so the letter must not be followed by a dot and a digit.
            t, k = re.subn(rf"{did}(\s+)Rev(\s+)\*{{0,2}}[A-Z]\*{{0,2}}(?!\.\d)\b",
                           rf"{did}\g<1>Rev\g<2>{new}", t)
            if k:
                hits[(os.path.relpath(p, PKG), did)] = k
        if t != o and not dry:
            open(p, "w").write(t)
    return hits


def rename_files(dry=False):
    """The file name carries the letter the document declares."""
    moves = []
    for f in sorted(os.listdir(DOCS)):
        m = re.match(r"([A-Z]+-EEG-\d+)_Rev([A-Z])_(.+)\.(md|docx|pdf)$", f)
        if not m:
            continue
        did, old, stem, ext = m.groups()
        if did not in BUMP:
            continue
        _o, new = BUMP[did]
        if old == new:
            continue
        dst = f"{did}_Rev{new}_{stem}.{ext}"
        moves.append((f, dst))
        if dry:
            continue
        src_p, dst_p = os.path.join(DOCS, f), os.path.join(DOCS, dst)
        r = subprocess.run(["git", "mv", src_p, dst_p], cwd=PKG, capture_output=True)
        if r.returncode != 0:
            os.rename(src_p, dst_p)
    if not dry and moves:
        for p in _text_files():
            t = open(p).read()
            o = t
            for old_f, new_f in moves:
                t = t.replace(old_f, new_f)
            if t != o:
                open(p, "w").write(t)
    return moves


def main(dry=False):
    fm = bump_front_matter(dry)
    print(f"front matter: {len(fm)} document(s)")
    for f, did, old, new in fm:
        print(f"  {did}  Rev {old} -> Rev {new}")
    hits = rewrite_citations(dry)
    total = sum(hits.values())
    print(f"citations rewritten: {total} in {len({k[0] for k in hits})} file(s)")
    for (path, did), k in sorted(hits.items()):
        print(f"  {path:70s} {did} x{k}")
    moves = rename_files(dry)
    print(f"files renamed: {len(moves)}")
    for a, b in moves:
        print(f"  {a}\n    -> {b}")
    if dry:
        print("\n(dry run -- nothing written)")
    return fm, hits, moves


if __name__ == "__main__":
    main(dry="--dry" in sys.argv)

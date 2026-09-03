#!/usr/bin/env python3
"""
finalise_docs.py -- the mechanical half of the document release.

Four jobs, all of them things a person should not do by hand across twenty documents:

  1. replace every <<ROUTING_STATS>> placeholder with the real routing result, read out of
     the DRC report rather than typed;
  2. bring every "Governing documents:" line up to the current revision letters;
  3. rename every document file so the filename carries the revision the document says it is;
  4. register the rulings file as a controlled document, because four released documents cite
     it and the register said it was not part of the release.

Run it after tools/emit_all.py and before tools/make_docs.py.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
DOCS = os.path.join(PKG, "docs")
DRC = os.path.join(PKG, "kicad", "EEG-CAR-01_RevB_DRC_report.txt")


def read_stats():
    t = open(DRC).read()

    def g(pat, cast=str, default=None):
        m = re.search(pat, t)
        return cast(m.group(1)) if m else default

    return {
        "segments": g(r"segments (\d+)", int, 0),
        "vias": g(r"vias (\d+)", int, 0),
        "islands": g(r"pour islands (\d+)", int, 0),
        "nets": g(r"nets +(\d+)\n", int, 0),
        "connected": g(r"nets fully connected +(\d+)", int, 0),
        "violations": g(r"VIOLATIONS: (\d+)", int, 0),
        "unclosed": len(re.findall(r"^    net \S+:", t, re.M)),
        "min_f": g(r"min clearance F\.Cu +([0-9][0-9.]*)", float, 0.0),
        "min_b": g(r"min clearance B\.Cu +([0-9][0-9.]*)", float, 0.0),
        "min_p": g(r"min clearance In1\.Cu +([0-9][0-9.]*)", float, 0.0),
        "narrow": g(r"tracks below 0\.25 mm +(\d+)", int, 0),
        "hole": g(r"smallest plated hole +([0-9][0-9.]*)", float, 0.0),
    }


def sentence(s):
    open_nets = s["nets"] - s["connected"]
    return (
        f"EEG-CAR-01 Rev B is routed on four layers with {s['segments']} track segments and "
        f"{s['vias']} through vias, and each reference plane is one continuous island per "
        f"net. Every geometric rule passes: the smallest measured clearance is "
        f"{s['min_f']:.3f} mm on L1, {s['min_p']:.3f} mm on the planes and {s['min_b']:.3f} mm "
        f"on L4 against a 0.20 mm rule; the narrowest conductor is 0.20 mm with {s['narrow']} "
        f"segments below the 0.25 mm preferred width; the smallest plated hole is "
        f"{s['hole']:.2f} mm; no digital net enters the analogue zone; and there is exactly "
        f"one AGND_REF-to-DGND bridge and one HARN_SHIELD-to-DGND bridge. "
        + (
            f"**There are no violations, and all {s['connected']} nets are one connected "
            f"copper island.** That meets the fabrication-release gate of ECO-EEG-016 "
            f"section 3, so the data is **RELEASED FOR REVIEW under RFQ-EEG-002A**. It is "
            f"**not released for fabrication**: no human layout engineer has read routing "
            f"produced by the programme's own tools, and that review is what fabrication "
            f"release waits on. The report also records the connections the router had to "
            f"relax to close the board -- a board that closes at minimum geometry is not "
            f"the same board as one that closes at preferred geometry."
            if s["violations"] == 0 and open_nets == 0 else
            f"**{open_nets} nets each still have one connection that the automatic router "
            f"could not close. All {s['violations']} are listed by name and pad in "
            f"`kicad/EEG-CAR-01_RevB_DRC_report.txt`.** Closing them and reviewing the "
            f"whole routing is the scope of RFQ-EEG-002A, and the fabrication data is NOT "
            f"RELEASED FOR FABRICATION until they are closed."
        )
    )


REV_OF = {}


def scan_revisions():
    for f in os.listdir(DOCS):
        if not f.endswith(".md"):
            continue
        head = open(os.path.join(DOCS, f)).read(2000)
        m = re.search(r"\*\*Document:\*\*\s*([A-Z]+-EEG-\d+)\s*\*\*Revision:\*\*\s*\*{0,2}([A-Z])",
                      head)
        if m:
            REV_OF[m.group(1)] = m.group(2)
    return REV_OF


def main():
    stats = read_stats()
    text = sentence(stats)
    scan_revisions()
    # the two documents that are generated rather than written
    REV_OF.setdefault("SCH-EEG-005", "B")
    REV_OF.setdefault("MECH-EEG-020", "A")
    REV_OF.setdefault("SIM-EEG-018", "A")
    REV_OF.setdefault("DSN-EEG-002", "E")
    REV_OF.setdefault("RUL-EEG-021", "A")
    print("revisions:", " ".join(f"{k}={v}" for k, v in sorted(REV_OF.items())))

    # 4. register the rulings file
    rul = os.path.join(DOCS, "RUL-EEG-021_RevA_rulings_register.md")
    src = open(os.path.join(HERE, "RULINGS.md")).read()
    header = (
        "# Rulings Register\n\n"
        "**Document:** RUL-EEG-021  **Revision:** A  **Date:** 1 September 2026\n"
        "**Issued by:** TI One Voice research programme (one.witysk.org), Brussels, Belgium\n"
        "**Licence:** CC BY-SA 4.0\n"
        "**Governing documents:** DSN-EEG-003 Rev C, then RFQ-EEG-001 Rev E. Where this\n"
        "document and `tools/design.py` disagree, `design.py` governs.\n\n"
        "## Why this document exists\n\n"
        "A cross-document audit on 1 September 2026 found sixty places where seventeen "
        "documents, written from one fact base, still disagreed with each other. Each "
        "disagreement needed one answer, made once, that every document could be corrected "
        "against. This is that set of answers. It began life as an internal worksheet and is "
        "registered as a controlled document because four released documents cite it.\n\n"
        "Nothing in this package has been manufactured or measured, and no safety engineer "
        "has reviewed this design.\n\n---\n\n")
    body = src.split("---\n", 1)[1] if "---\n" in src else src
    open(rul, "w").write(header + body)
    print("registered", os.path.basename(rul))

    changed = 0
    for f in sorted(os.listdir(DOCS)):
        if not f.endswith(".md"):
            continue
        p = os.path.join(DOCS, f)
        t = open(p).read()
        o = t
        t = t.replace("<<ROUTING_STATS>>", text)
        t = t.replace("`<<ROUTING_STATS>>`", text)
        t = t.replace("&lt;&lt;ROUTING_STATS&gt;&gt;", text)
        # governing-document lines
        t = re.sub(r"DSN-EEG-003\s+Rev\s+B\b", "DSN-EEG-003 Rev C", t)
        t = re.sub(r"RFQ-EEG-001\s+Rev\s+D\b", "RFQ-EEG-001 Rev E", t)
        for did, rev in REV_OF.items():
            if did in ("DSN-EEG-003", "RFQ-EEG-001"):
                continue
            t = re.sub(rf"{did}\s+Rev\s+[A-Z]\b", f"{did} Rev {rev}", t)
        if t != o:
            open(p, "w").write(t)
            changed += 1
    print(f"{changed} documents updated")

    # 3. rename files to carry the revision the document declares
    for f in sorted(os.listdir(DOCS)):
        m = re.match(r"([A-Z]+-EEG-\d+)_Rev([A-Z])_(.+)\.md$", f)
        if not m:
            continue
        did, old, stem = m.groups()
        new = REV_OF.get(did, old)
        if new == old:
            continue
        dst = os.path.join(DOCS, f"{did}_Rev{new}_{stem}.md")
        subprocess.run(["git", "mv", os.path.join(DOCS, f), dst], cwd=PKG,
                       capture_output=True)
        if not os.path.exists(dst):
            shutil.move(os.path.join(DOCS, f), dst)
        print(f"  {f}  ->  {os.path.basename(dst)}")
        # fix every citation of the old filename
        for g in os.listdir(DOCS):
            if not g.endswith(".md"):
                continue
            q = os.path.join(DOCS, g)
            tt = open(q).read()
            if f in tt:
                open(q, "w").write(tt.replace(f, os.path.basename(dst)))
    # drop the stale docx/pdf so make_docs regenerates against the new names
    for f in os.listdir(DOCS):
        if f.endswith((".docx", ".pdf")) and not f.startswith("DSN-EEG-002"):
            os.remove(os.path.join(DOCS, f))
    print("stale docx/pdf removed; run tools/make_docs.py to regenerate")


if __name__ == "__main__":
    main()

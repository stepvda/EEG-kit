#!/usr/bin/env python3
"""
check_consistency.py -- refuse to release a package that contradicts itself.

Four audits of package v2 found the same class of defect over and over: a number, a part
name or a revision letter that one document had moved on from and another had not.  Every
one of them was cheap to find mechanically and expensive to find by reading.  This is that
check, so the fifth audit does not have to be a person.

It looks for three things:

  BANNED   a figure or a name that a ruling has superseded.  If it appears anywhere outside
           an explicit withdrawal notice, that is a document that missed a ruling.
  REVS     a cross-reference to DOC-nnn Rev X where the package ships Rev Y.  Historical
           references are legitimate ("Rev C said ..."), so a hit is only reported when the
           sentence does not read as one.
  AGREE    figures that must agree across the package -- the routing census, the simulation
           headline -- quoted with more than one value.

Exit status is 1 if anything is found, so it can gate a release.

Usage:  python3 tools/check_consistency.py [--quiet]
Licence: CC BY-SA 4.0.
"""
from __future__ import annotations

import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)

# A hit is forgiven when the line also says the value is dead.  These are the words the
# package actually uses when it withdraws something.
# A hit is forgiven when the surrounding sentence says the value is dead.
#
# These markers are deliberately UNAMBIGUOUS.  Earlier versions of this list held ordinary
# English -- "was", "were", "rather than", "instead of" -- and each one silently disabled
# the check over a widening area: "The routing WAS produced by the autorouter" and
# "asks for review RATHER THAN routing" each forgave a line that still read
# "VIOLATIONS: 25 ... NOT RELEASED FOR FABRICATION".  A document that withdraws a figure
# says so; if a legitimate line is flagged here, the fix is to make the withdrawal
# explicit in the prose, not to broaden this pattern.
WITHDRAWN = re.compile(
    r"withdraw|superseded|supersedes|no longer|used to|\*\*Was:?\*\*|"
    r"stale|obsolete|in error|transcription error|not approved|~~|"
    r"are gone|is gone|have gone|earlier issue|previous routing|former|"
    r"was first (?:written|issued|stated)|were first (?:written|issued|stated)|"
    r"was then|package v1|Rev A\.2|first issue|corrected from|and not the|"
    r"what were then|what was then|at the time|then-open|as it stood|"
    # A line that explains WHY something is dead is not the same as a line that still
    # relies on it.  These are the words the package uses when it argues the point:
    r"forbid|not settled|not permitted|is an AGC|OPEN:|open item|"
    r"lower bound|settles|single home|see PKG|per PKG|§3\.2|§2\.2", re.I)

# (pattern, what it should be now, why)
BANNED = [
    (r"\b340\s*[x×]\s*250\s*[x×]\s*210\b", "the case size PKG-EEG-015 §3.2 specifies",
     "the case grew; PKG §3.2 is the authority"),
    (r"\bNanuk\s*915\b", "the shell PKG-EEG-015 §3.2 names", "case shell decided once"),
    (r"\bPeli\s*1450\b", "the shell PKG-EEG-015 §3.2 names", "case shell decided once"),
    (r"two-layer\s+(?:PE\s+)?foam", "the foam layer count PKG-EEG-015 §2.2 specifies",
     "the foam insert was re-cut"),
    (r"\b6\s*cm2\b|\b6\s*cm²\b", "33.8 cm²",
     "150x130 - 130x124 = 33.8 cm², not 6"),
    (r"\b118\s*s(?:econds)?\b", "126 s of raw samples (124 s framed)",
     "6 MiB / 50.0 kB/s, ECO-EEG-025"),
    (r"MAX9814", "a fixed-gain preamp; the MAX9814 is NOT approved (E-14 forbids AGC)",
     "E-14 forbids automatic gain control"),
    (r"\(8,\s*8\)|\(142,\s*8\)|\(8,\s*122\)", "(12, 10), (144, 100) and (12, 120)",
     "fiducial positions, per design.py and the CPL"),
    (r"iSerial\w*\s*(?:=|from|populates? from)\s*(?:the\s*)?ATECC",
     "iSerialNumber = the unit serial TIOV-B-nnnn",
     "RUL-EEG-021 §B rules the format; the ATECC serial is a second identifier"),
    # --- added after the second review.  Each of these is a sentence that was true once
    # and is now false, and each survived a correction pass because nothing looked for it.
    (r"factory serial is the USB `?iSerialNumber",
     "the unit serial TIOV-B-nnnn is the iSerialNumber",
     "the ATECC serial is printed and in the Data Matrix, not in the descriptor"),
    (r"Through vias \| 502|\b502 through vias\b", "498",
     "the de-duplicated census"),
    (r"allows for that \(ECO-EEG-019\)",
     "E-11's 50 Hz +/-10 % half is not met with the approved parts; T12e measures 42-58 Hz",
     "no widened corner tolerance was ever written into TST"),
    (r"are written to match", "say what is actually true of each document",
     "DSN-EEG-002 Rev E was never re-issued, so it does not match"),
    (r"two-layer die-cut PE foam|two layers of grey foam",
     "the seven-layer Rev C stack of PKG-EEG-015 §2.2",
     "the two-layer insert cannot pack this kit"),
    (r"twenty or more people", "the fleet figure PKG-EEG-015 carries",
     "the old fleet arithmetic"),
    (r"ICD-EEG-006 section 9\b|ICD-EEG-006 §9\b", "ICD-EEG-006 section 2.7",
     "section 9 is verification and sign-off; 2.7 holds the current tally"),
    (r"\bbuilt and priced\b", "not built here -- JIG-EEG-009 says so and TST §16 agrees",
     "FIX-02/C, the artificial ear"),
    (r"288 mA on DVDD3V3", "the tally in ICD-EEG-006 section 2.7",
     "superseded current figure"),
    (r"92\.6 kOhm|92\.6 k\u03a9", "92.5 kOhm", "the corrected lead-off arithmetic"),
    # --- added 2 September 2026, when the board closed.  Every figure below described a
    # board with twenty-five open design-rule violations.  The board now has none, so each
    # of these is a sentence that was true on 1 September and false on 2 September.  They
    # are banned rather than merely corrected because the failure mode is a document that
    # missed the routing result, and that is exactly what this check exists to catch.
    (r"\b(?:twenty-five|25)[^\S\n]+(?:open[^\S\n]+)?(?:DRC[^\S\n]+)?"
     r"(?:violations|open[^\S\n]+items|design-rule[^\S\n]+violations)\b",
     "zero violations -- the DRC report is the authority",
     "the board closed on 2026-09-02; 25 violations is a withdrawn figure"),
    (r"\b(?:twenty-three|23)[^\S\n]+(?:nets|unclosed|open[^\S\n]+nets)\b",
     "0 unclosed nets; all 145 are one connected copper island",
     "the board closed on 2026-09-02"),
    (r"VIOLATIONS:[^\S\n]*(?!0\b)\d+", "VIOLATIONS: 0",
     "the DRC report's own headline; the board closed on 2026-09-02"),
    (r"not[^\S\n]+DRC-clean", "the board passes every rule in the DRC",
     "the board closed on 2026-09-02"),
    (r"0\.328[^\S\n]*mm", "the two electrode-clearance vias are gone",
     "both were removed when the board was re-routed"),
    (r"\b122[^\S\n]+of[^\S\n]+145\b|\b122/145\b", "145 of 145",
     "superseded connectivity census"),
    (r"0\.241[^\S\n]*mm[^\S\n]+on[^\S\n]+L1", "0.260 mm on L1",
     "superseded clearance measurement"),
    (r"0\.292[^\S\n]*mm", "0.285 mm on the planes",
     "superseded clearance measurement"),
    # The release status itself.  An unqualified "NOT RELEASED FOR FABRICATION" is no
    # longer the whole truth: the ECO-EEG-016 s3 gate is met and the data is released for
    # REVIEW.  A line may still say it is not released for fabrication -- that is true --
    # but only alongside the review status, which the forgiveness pattern below requires.
    (r"NOT[^\S\n]+RELEASED[^\S\n]+FOR[^\S\n]+FABRICATION",
     "RELEASED FOR REVIEW under RFQ-EEG-002A, and not for fabrication",
     "state both halves: the gate is met, the human review is not done"),
]

# Lines that legitimately say "not released for fabrication" say WHY in the same breath.
# Deliberately narrow.  An earlier version also forgave any line mentioning "a human
# layout engineer", which let tools/DESIGN_FACTS.md keep "VIOLATIONS: 25 ... NOT RELEASED
# FOR FABRICATION" through a whole pass: the line named the missing reviewer and so looked
# like it was stating the new status when it was stating the old one.  Only an explicit
# release-for-review phrase forgives.
RELEASE_OK = re.compile(r"RELEASED FOR REVIEW|released for review|"
                        r"review(?:ed)?\**[^\S\n]+under[^\S\n]+RFQ|"
                        r"not[^\S\n]+yet[^\S\n]+released", re.I)

# Figures that must be quoted identically wherever they appear.  Group 1 is the VALUE; the
# comparison is on the number alone, so that "twenty-five violations", "25 DRC violations"
# and "25 open violations" all count as the same figure.  Only a different NUMBER is a
# disagreement -- the package is allowed to vary its prose.
# NB: patterns use [^\S\n] rather than \s so a run of whitespace cannot cross a
# line break -- "pour islands 4\n\nVIOLATIONS: 25" is not "4 violations".
WORDS = {"twenty-three": "23", "twenty-five": "25", "twenty-four": "24",
         "three": "3", "four": "4", "two": "2", "one": "1"}
AGREE = [
    # \b...\b on the number, and no comma may intervene: "tracks on L1 and L4, through
    # vias" must not read as "4 through vias".
    ("routing census, track segments",
     r"\b(\d[\d\u202f\u00a0 ]*\d|\d)[^\S\n]+track segments\b"),
    ("routing census, through vias",
     r"\b(\d[\d\u202f\u00a0 ]*\d|\d)[^\S\n]+through vias\b"),
    ("simulation, checks passed", r"\b(\d+)[^\S\n]*(?:checks[^\S\n]*)?passed,[^\S\n]*\d+[^\S\n]*failed"),
    # The interop harness count drifted once already: eight CMD_LIGHTS checks were added on
    # 2026-09-02 and nine documents went on saying 49 for a while.  Anchor it so the next
    # person to add a check is told which files have to move with it.
    ("interop harness, checks",
     r"\b(\d+)[^\S\n]+(?:of[^\S\n]+\d+[^\S\n]+)?checks?(?:[^\S\n]+(?:green|all[^\S\n]+passing|now[^\S\n]+read|pin|read))"),
    ("open DRC items",
     r"\b(twenty-five|twenty-three|\d+)[^\S\n]+(?:open[^\S\n]+)?(?:DRC[^\S\n]+)?violations\b"),
    ("connections routed at relaxed geometry",
     r"\b(\d+)[^\S\n]+relaxed[^\S\n]+connections\b"),
    # "pads" alone is far too common a word: 406 stencil apertures and 211 designators are
    # not pad counts.  Anchor on the two phrasings the package actually uses for the census.
    ("pad census", r"\b(\d{3})\s+pads\b(?=[^\n]*(?:census|in total|on the board|netlist))"),
    ("simulation, total checks", r"ran\s+(\d+)\s+checks"),
    ("unclosed connections",
     r"\b(twenty-three|\d+)[^\S\n]+nets?[^\S\n]+(?:each[^\S\n]+)?(?:have|has|with)[^\S\n]+one\b"),
]

# Explicit, auditable exemptions.  A superseded figure has to be allowed to appear in the
# passage that supersedes it, and in the identifier of the open item that tracks it.  Each
# entry is (file suffix, substring that must be on the line, why).  Keep this list short:
# if it starts growing, the package has a real problem rather than a checker problem.
ALLOW = [
    ("PKG-EEG-015_RevB_packing_labelling_and_shipping.md", "Kit BOM Rev B item 34 said",
     "PKG 3.3 is the passage that withdraws the old case figures"),
    ("PKG-EEG-015_RevB_packing_labelling_and_shipping.md", "AVL-EEG-017 Rev B K21 restates",
     "same passage, quoting the transcription it corrects"),
    ("PKG-EEG-015_RevB_packing_labelling_and_shipping.md", "The named example models are a second problem",
     "same passage, naming the shells it rules out"),
    ("WH-EEG-008_RevB_harness_and_cable_assembly.md", "max9814-location-conflict",
     "the slug of the open item that tracks the unsettled preamplifier"),
    ("AVL-EEG-017_RevB_approved_vendor_list.md", "a gain that moves is not a gain",
     "the passage that argues the MAX9814 out; AVL is where the rejection is reasoned"),
    ("JIG-EEG-009_RevB_test_fixture_design.md", "Rev B of this document reported it as",
     "the sentence that withdraws the old 92.6 kOhm figure"),
    ("TST-EEG-004_RevC_production_test_specification.md",
     "designed, dimensioned, built and priced in",
     "this is about the fixture set as a whole, not FIX-02/C, which TST now says is not built"),
]


def _allowed(rel, line):
    return any(rel.endswith(f) and sub in line for f, sub, _ in ALLOW)


TEXT_EXT = (".md", ".txt", ".py", ".c", ".h", ".json", ".csv")
# reports/ is the dated routing-iteration log: drc_01.txt IS the record of the board as it
# stood at iteration 1, violations and all.  Rewriting it would destroy the evidence of how
# the board was closed, so it is excluded rather than corrected.
SKIP_DIRS = {"__pycache__", "reports"}
# the worksheets are allowed to hold history; the controlled register governs
SKIP_FILES = {"check_consistency.py"}
# A generator that branches on the DRC state necessarily contains the text for BOTH
# states.  The dead branch is not a claim about this board; the live one is checked
# through the file it writes.
BRANCHED_GENERATORS = {"tools/emit_extras.py", "tools/finalise_docs.py",
                       "tools/simulate_production.py"}


def _files():
    for root, dirs, names in os.walk(PKG):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for n in sorted(names):
            if n in SKIP_FILES or not n.endswith(TEXT_EXT):
                continue
            yield os.path.join(root, n)


def main(quiet=False):
    hits = []
    # A vacuous check is worse than no check: it prints PASS.  Refuse to grade the
    # package unless the rules still catch what they are for.
    broken = selftest(quiet)

    for path in _files():
        rel = os.path.relpath(path, PKG)
        try:
            lines = open(path, encoding="utf8").read().split("\n")
        except (UnicodeDecodeError, OSError):
            continue
        for i, line in enumerate(lines, 1):
            # A wrapped sentence is still one sentence.  Forgiveness is judged on the
            # line plus its neighbours, because "...is NOT RELEASED FOR FABRICATION /
            # because no human layout engineer has read it" is a correct statement whose
            # two halves land on different lines.
            window = "\n".join(lines[max(0, i - 2):i + 1])
            for pat, should, why in BANNED:
                # "not released for fabrication" is still true; it is only wrong when
                # stated ALONE, without the review status that now sits beside it.
                if "FABRICATION" in pat and RELEASE_OK.search(window):
                    continue
                if rel in BRANCHED_GENERATORS and "FABRICATION" in pat:
                    continue
                if (re.search(pat, line, re.I) and not WITHDRAWN.search(window)
                        and not _allowed(rel, line)):
                    hits.append(("BANNED", rel, i, line.strip()[:110], should, why))

    # Rendition freshness.  Every document ships as .md, .docx and .pdf, and the two
    # renditions are generated FROM the Markdown.  Nothing checked that they had actually
    # been regenerated, and the consequence was already in the package: TST-EEG-004's T30
    # existed in the Markdown and in neither rendition, so a test engineer reading the PDF
    # -- which is what a manufacturer is sent -- ran a sequence that was missing a step,
    # with all three files carrying the same revision letter C.
    stale = []
    docdir = os.path.join(PKG, "docs")
    if os.path.isdir(docdir):
        for md in sorted(glob.glob(os.path.join(docdir, "*.md"))):
            mtime = os.path.getmtime(md)
            for ext in (".docx", ".pdf"):
                other = md[:-3] + ext
                if not os.path.exists(other):
                    stale.append(f"{os.path.basename(other)} does not exist")
                elif os.path.getmtime(other) < mtime - 1:
                    stale.append(f"{os.path.basename(other)} is older than its .md")

    # figures that must agree
    seen = {}
    for path in _files():
        if not path.endswith((".md", ".txt")):
            continue
        rel = os.path.relpath(path, PKG)
        try:
            txt = open(path, encoding="utf8").read()
        except (UnicodeDecodeError, OSError):
            continue
        for label, pat in AGREE:
            for m in re.finditer(pat, txt, re.I):
                val = (m.group(1) if m.groups() else m.group(0)).strip().lower()
                val = WORDS.get(val, re.sub(r"[\s,]", "", val))
                if not val.isdigit():
                    continue
                # A figure quoted inside a withdrawal ("Was: ... 25 violations",
                # "superseded on 2 September") is history, not a competing claim.  Judge
                # that on the surrounding sentence, as the banned scan does.
                a = txt.rfind("\n", 0, max(0, m.start() - 120)) + 1
                b = txt.find("\n", m.end() + 120)
                if WITHDRAWN.search(txt[a:b if b > 0 else len(txt)]):
                    continue
                seen.setdefault(label, {}).setdefault(val, []).append(rel)

    disagreements = []
    for label, vals in seen.items():
        if len(vals) > 1:
            disagreements.append((label, vals))

    if not quiet:
        print(f"consistency check over {PKG}")
        print(f"  banned figures and names ... {len(hits)} hit(s)")
        for kind, rel, i, line, should, why in hits:
            print(f"    {rel}:{i}\n        {line}\n        -> {should}   ({why})")
        print(f"  figures that must agree .... {len(disagreements)} disagreement(s)")
        for label, vals in disagreements:
            print(f"    {label}:")
            for v, files in sorted(vals.items(), key=lambda kv: -len(kv[1])):
                print(f"        {v:>10}  in {len(files)} file(s): "
                      f"{', '.join(sorted(set(files))[:4])}")

    if not quiet:
        print(f"  document renditions ........ {len(stale)} stale")
        for t in stale[:6]:
            print(f"    {t}")
        if len(stale) > 6:
            print(f"    ... and {len(stale) - 6} more")

    bad = len(hits) + len(disagreements) + len(broken) + len(stale)
    if broken:
        print(f"\nFAIL: the check itself is broken -- {len(broken)} probe(s) graded "
              f"wrongly, so a PASS here would mean nothing")
        return 1
    print(f"\n{'FAIL' if bad else 'PASS'}: {bad} item(s) need attention")
    return 1 if bad else 0


# --------------------------------------------------------------------------- self-test
# This check reports PASS when it finds nothing, which is also what it reports when its
# own patterns have stopped working.  Twice they had: an over-broad forgiveness word
# ("was", then "rather than") silently disabled the routing-status rules while the tool
# still printed PASS.  These probes are the difference between the two.  --selftest runs
# them; a release run does too, and refuses to grade the package if they fail.
PROBES = [
    ("The DRC reports 25 violations and the data is NOT RELEASED FOR FABRICATION.", True),
    ("23 nets each have one connection the router could not close.", True),
    ("Two vias sit 0.328 mm from an electrode net.", True),
    ("`report.txt` reports VIOLATIONS: 25 so the board is not DRC-clean.", True),
    ("The routing was produced by the autorouter and reports VIOLATIONS: 25.", True),
    ("RFQ-EEG-002A asks for review rather than routing; VIOLATIONS: 25 remain.", True),
    ("The DRC reports zero violations; 145 of 145 nets are connected.", False),
    ("It is RELEASED FOR REVIEW under RFQ-EEG-002A and NOT RELEASED FOR FABRICATION.",
     False),
    ("**Was:** 122 of 145 nets, 25 violations.", False),
    ("The two electrode-clearance vias at 0.328 mm are gone.", False),
]


def selftest(quiet=False):
    """Return a list of probes the banned-scan grades wrongly."""
    bad = []
    for line, want in PROBES:
        got = any(re.search(pat, line, re.I) and not WITHDRAWN.search(line)
                  and not ("FABRICATION" in pat and RELEASE_OK.search(line))
                  for pat, _, _ in BANNED)
        if got != want:
            bad.append((line, want, got))
    if not quiet:
        print(f"  self-test ................... {len(PROBES) - len(bad)}"
              f"/{len(PROBES)} probes correct")
        for line, want, got in bad:
            print(f"    {'MISSED' if want else 'FALSE POSITIVE'}: {line[:78]}")
    return bad


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(1 if selftest() else 0)
    sys.exit(main(quiet="--quiet" in sys.argv))

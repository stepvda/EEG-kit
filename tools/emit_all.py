#!/usr/bin/env python3
"""
emit_all.py -- build every generated artifact of the package from design.py.

    python3 emit_all.py            write the Rev C layout-input set
    python3 emit_all.py --rev-b    refused; see below

**What this command does changed on 8 September 2026 (ECO-EEG-030), and it changed
because running it the old way would now destroy released data.**

Until Rev B was withdrawn, `emit_all.py` routed the board and wrote the Rev B
fabrication set: Gerbers, drill, CPL, BOM, the DRC report, the routed `.kicad_pcb`, the
drawings and the eight-sheet schematic PDF.  Rev B is withdrawn from fabrication and
`design.py` has moved on to Rev C -- corrected footprints (U1-U3 are TSSOP-14, not
SOIC-14) and corrected part numbers -- so re-running the Rev B path would write Rev B
file names from Rev C data and produce a set whose copper does not reach its own pads.
**The Rev B fabrication set is frozen.  It is recovered from git, not regenerated**, and
`--rev-b` refuses rather than silently doing damage.

Rev C has no routing of its own: the layout is bought.  What this writes is the input
set the contractor works from, and what checks it on the way back.

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import design as D          # noqa: E402
import emit_revc            # noqa: E402

REV_B_FROZEN = """
REFUSED.  The Rev B fabrication set is frozen and this tool will not rewrite it.

Rev B was withdrawn from fabrication on 4 September 2026 after an external layout
engineer read it, declined the review and advised a redesign (ECO-EEG-016 section 2,
ECO-EEG-030).  Its files stay in the tree as history under their own names:

    kicad/EEG-CAR-01_RevB_routed.kicad_pcb
    kicad/EEG-CAR-01_RevB_DRC_report.txt
    kicad/gerber/*
    schematic/SCH-EEG-005_RevB_schematic_set.pdf

design.py now describes Rev C.  Its footprints and part numbers are NOT Rev B's -- U1,
U2 and U3 moved from SOIC-14 to TSSOP-14 under ECO-EEG-031, because the quad OPA4376 is
not made in SOIC-14 -- so routing produced against Rev B's pad positions does not land on
Rev C's pads.  Regenerating Rev B from this source would write a set that looks released
and is not connected.

To read the Rev B set as released:   git show <commit>:kicad/...
To build the Rev C input set:        python3 emit_all.py
"""


def main(argv=()):
    if "--rev-b" in argv or "--cached" in argv:
        print(REV_B_FROZEN.strip())
        return 2
    print(f"EEG-CAR-01 Rev {D.REV_C} -- layout input set, {D.DATE_C}")
    print("Rev B is frozen history; see ECO-EEG-030.\n")
    emit_revc.main()
    print("\ndone")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

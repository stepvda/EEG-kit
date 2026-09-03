#!/usr/bin/env python3
"""
metrics.py -- the per-iteration scoreboard, from a DRC report plus routed.pkl.

    python3 tools/metrics.py reports/drc_04.txt          (routed.pkl beside this file)

Prints, and is meant to be pasted into reports/log.md verbatim: connectivity,
violations by kind, copper census, and the RELAXED-CONNECTION ledger two ways
-- as listed (the report repeats a connection each time the build re-routes
it) and as unique pad-to-pad connections, by net class, so the
manufacturability cost of closing nets is a visible number.
Licence: CC BY-SA 4.0.
"""
import collections
import math
import os
import pickle
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import design as D   # noqa: E402
import pcbgen        # noqa: E402


def main(report):
    t = open(report).read()
    d = pickle.load(open(os.path.join(HERE, "routed.pkl"), "rb"))
    tracks, vias = d["tracks"], d["vias"]
    unclosed = re.findall(r"net (\S+): (.*?) is not joined", t)
    viol = int(re.search(r"VIOLATIONS: (\d+)", t).group(1))
    kinds = re.findall(r"^  ([a-zA-Z][^(\n]*?)\s+\((\d+)\)\s*$", t[t.index("VIOLATIONS:"):
                                                                     t.index("CONNECTIONS THE ROUTER")], re.M)
    length = sum(math.hypot(x.x2 - x.x1, x.y2 - x.y1) for x in tracks)
    print(f"nets connected        {int(re.search(r'nets fully connected\s+(\d+)', t).group(1))}/145")
    print(f"unclosed nets         {len(unclosed)}  {[n for n, _ in unclosed]}")
    print(f"DRC violations        {viol}  " + ", ".join(f"{k.strip()} {n}" for k, n in kinds))
    print(f"segments / vias       {len(tracks)} / {len(vias)}   copper {length:.0f} mm")
    # relaxed ledger -- from the pickle, not the report: the report lists at
    # most 40 rows per block while its headline counts the raw list, and the
    # raw list repeats a connection every time the build re-routes it
    raw = list(d.get("narrowed", []))
    uniq = {}
    for net, a, b, w, c in raw:
        uniq.setdefault((net, tuple(sorted((a, b)))), []).append((float(w), float(c)))
    bycls = collections.Counter(D.netclass_of(n) for (n, _) in uniq)
    narrow = sum(1 for k, v in uniq.items()
                 if min(w for w, _ in v) < D.NETCLASS[D.netclass_of(k[0])][0])
    print(f"relaxed connections   {len(raw)} raw = {len(uniq)} unique pad-to-pad "
          f"(+{len(raw) - len(uniq)} re-listings of re-routed connections)")
    print(f"  unique by class     " + ", ".join(f"{k} {v}" for k, v in sorted(bycls.items())))
    print(f"  unique narrowed     {narrow}   unique reduced-gap-only {len(uniq) - narrow}")
    pw = [k[0] for k in uniq if D.netclass_of(k[0]) == "POWER_D"]
    print(f"  POWER_D nets hit    {dict(collections.Counter(pw))}")
    at_min = sum(1 for v in uniq.values() if min(w for w, _ in v) <= 0.201)
    print(f"  unique at 0.20 mm   {at_min}")
    mins = re.findall(r"min clearance (\S+)\s+([\d.]+)", t)
    print(f"measured minima       " + ", ".join(f"{l} {v}" for l, v in mins)
          + f", narrowest track {re.search(r'narrowest track\s+([\d.]+)', t).group(1)}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "drc_report.txt"))

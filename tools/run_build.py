import functools, pickle, sys
print = functools.partial(print, flush=True)
import builtins; builtins.print = print
import build_board as BB, drc
res = BB.build(verbose=True, plot="routed.png")
pickle.dump({k: v for k, v in res.items() if k != "board"}, open("routed.pkl", "wb"))
v, st = drc.write_report("drc_report.txt", res["board"], res["tracks"], res["vias"],
                         res["pours"], res["iso_box"], res.get("narrowed", []))
print("DRC violations:", len(v))
for k, val in st.items():
    print(f"  {k}: {val}")

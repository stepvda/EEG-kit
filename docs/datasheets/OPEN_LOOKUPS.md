# Open datasheet lookups — three figures a person has to fetch

Each of these is blocked because the manufacturer's site refuses an automated request, or
because no document could be obtained at all. **Each is one page, one number.** You should not
need to read anything else to work through this sheet.

Work them in the order given: the first unblocks EUR 2 530 of layout, the third is on the
critical path for a patient-safety part.

---

## 1. Omron **G6K-2F-Y** — the FIX-01 relay land pattern

**URL** — <https://components.omron.com/us-en/products/detail/G6K-2F-Y>
(HTTP 403 to an automated request; opens normally in a browser)

**The figure needed** — the **land pattern envelope in mm²**, from the recommended PCB
mounting pattern in the datasheet. Take overall length × width of the recommended pad
pattern, not the relay body.

**The number to compare it against** — **70.7 mm²**.

**Where to record it** — `tools/fixture_gen.py`, constant `RELAY_ENV_MM2`, which is currently
**70.0 mm² and marked ASSUMED**. Then run:

```
python3 tools/fixture_gen.py --check
```

which recomputes the area budget and prints the verdict.

**What it unblocks** — FIX-01's 160.0 × 100.0 mm outline. The budget closes at **60 %
occupancy against a 60 % working limit — a margin of 1.0 %**.

- **If ≤ 70.7 mm²**: the outline is confirmed and the FIX-01 and FIX-04 layout can be
  commissioned — **15 working days, EUR 3 355** (JIG-EEG-009 §6.1, §6.3).
- **If > 70.7 mm²**: the outline must grow **before** anyone routes it. JIG-EEG-009 §1.9 notes
  the Hammond 1590D enclosure at 188 × 119 mm has room for a larger board.

**Why it is first.** Routing FIX-01 against an unconfirmed envelope risks 46 hours and
EUR 2 530 against an outline that may not close. See
`reports/INVESTIGATION_fixture_pcb_copper.md` §4.

---

## 2. Omron **B3F-1052** — the tactile switch at SW1–SW3

**URL** — <https://components.omron.com/us-en/products/detail/B3F-1052>
(HTTP 403 to an automated request)

**The figures needed** — four, all from the first page:

| | Expected, per AVL-EEG-017 §1.4 and `design.py` |
|---|---|
| Body size | 6.0 × 6.0 mm |
| Operating force | **1.47 N {150 gf}** — the AVL row asks for 160 gf ± 50, so 150 gf is inside it |
| Plunger | **projected, 7.3 mm** — a 12 mm B32-series key top mounts only to a projected plunger, and the POD-P1 lid opening is cut at 12.4 mm for that cap |
| Terminals | **four, no ground terminal** |

**Where to record it** — confirm the row in `docs/datasheets/README_datasheets.md` §4 and mark
its *Checked* column **fetched** instead of **blocked**. If any figure differs from the table
above, **stop and raise it**: ECO-EEG-031 already corrected this line once, from the 12 × 12 mm
B3F-4055, and the footprint `SW_PUSH_6mm_H7.3mm` was renamed with it.

**What it unblocks** — nothing is waiting on it. It closes a line two manufacturers have
already queried and prevents the ECO-EEG-031 correction being undone by a well-meaning
substitution.

---

## 3. **NEUROSPEC** — a solderable 1.5 mm DIN 42802 touch-proof socket

**URL** — <https://shop.neurospec.com/products/adapters-connectors/1-5mm-adapters-connectors-din-42802-2>
(an automated request redirect-loops; opens normally in a browser)

**What to look for** — the listing described as **"DIN 1.5 mm Touch-Proof (TP) Sockets (for
soldering)"**. The words *for soldering* are the reason this is on the sheet: it is the only
description found anywhere of a 1.5 mm DIN 42802 socket that terminates on a board rather than
in a panel or on a cable.

**The figures needed** — a **dimensioned drawing**, and then:

| | Requirement it must meet |
|---|---|
| Termination | one Ø1.7 mm PCB pin on the footprint centre, two Ø1.5 mm retention posts at ±3.5 mm — **or a documented deviation with a drawing** |
| Body | within 9.8 × 7.8 mm, on a 14 mm pitch |
| Gender | instrument end: recessed **male** pin — but see `RISK-EEG-011` **SR-13**, which is open |
| Colours | three distinct, one per site |
| Rating | ≥ 1 A stated on the datasheet |
| Cycles | mating force stated, repeatable over ≥ 500 cycles |

**Where to record it** — `reports/INVESTIGATION_din42802_sockets_J15_J17.md` §3.1, the
**verified** table. Move it out of §3.2 only if a document is actually obtained.

**What it unblocks** — the highest-risk line in AVL-EEG-017: J15–J17 have **no qualified
vendor at all** and a **12-week first-article lead time**. More immediately, it bears on
whether the three sockets stay on the board or move to a panel — see
`reports/INVESTIGATION_din42802_sockets_J15_J17.md` §4, which argues that decision should be
taken **before the Rev C layout desk starts placement**.

**If the page yields nothing**, the fallback is the three suppliers AVL-EEG-017 §1.4.1 already
names — Stäubli (a PCB-terminated variant of the LB-I1,5 family, which would be bespoke),
Wuhan Greentek, and Plastics One / Bio-Medical Instruments — and Stäubli's own contact address
is `ec.ch@staubli.com`.

---

## Recording convention

Whatever is found, record it the way the index already does: the **manufacturer's canonical
URL**, the **document number and revision as printed on the document**, the **date retrieved**,
and the **page or table** the figure came from. A figure without those four is asserted, not
verified, and the index marks it so.

Licence: CC BY-SA 4.0. **The documents these links point to are not.**

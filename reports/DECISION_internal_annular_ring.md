# Decision paper — IQC-B11's internal annular ring

**Status: evidence and options. QP-EEG-010 has NOT been rewritten and no limit has been
changed.** Vendor answers are still arriving.

**Why it is live.** One fabricator has stated **in writing** that it cannot provide the
report. A second's microsection template does not carry the measurement. When two independent
houses say no to the same line, the requirement is the outlier, not the market.

---

## 1. What IQC-B11 and IQC-B12 each actually rely on

| Row | What it inspects | Evidence it names | Limit | Consequence |
|---|---|---|---|---|
| **IQC-B11** | Inner-layer registration: four layers in the order L1 signal / L2 plane / L3 plane / L4 signal; dielectric thicknesses within ±10 % of §1.1; **internal annular ring measured at a through via** | **Microsection, 1 coupon per fabrication lot**, report retained | four layers in the right order; **ring ≥ 0.025 mm** (IPC-6012 class 2) | Wrong layer order, a missing plane, or any ring below 0.025 mm — **hard reject, whole lot** |
| **IQC-B12** | Layer-to-layer misregistration | **Fabricator registration report *plus* the IQC-B11 coupon** | **≤ 0.125 mm** at every measured location | Above 0.125 mm |
| *IQC-B13* | *Plane continuity and the plane split* | *Artwork comparison every lot; 4-wire DMM on 2 boards; insulation tester at 250 V DC* | *≤ 0.10 Ω corner to corner; AGND_REF–DGND ≥ 100 MΩ* | *hard reject* |

Three things follow, and the third is the useful one.

1. **B11 has exactly one evidence source.** No coupon, no row. There is no alternative
   method written into it.
2. **B12 has two, and only one is the coupon.** A fabricator registration report satisfies
   half of B12 on its own. B12 is therefore *less* exposed than B11 to a house that will not
   microsection.
3. **IQC-B13 does not depend on the coupon at all** — artwork comparison, 4-wire resistance
   and a 250 V insulation test on finished boards. Whatever happens to B11, plane continuity
   and the plane split remain inspectable by methods nobody has objected to. The brief's
   framing that "IQC-B12 leans on the same coupon" is right; it is worth adding that **B13
   does not**, because that limits how much is actually at risk.

Also relevant to any decision: QP-EEG-010 §5 puts "any bare board that failed IQC-B11, B12 or
B13" in **quarantine, no rework**, and prohibits use-as-is concession "for any four-layer
characteristic in IQC-B11 to B13". So these rows are not merely reports — they are wired into
disposition.

## 2. The underlying concern, stated separately from the method

QP-EEG-010 §2.1 says why these rows exist: three characteristics that did not exist on a
two-layer board now have to be inspected — **inner-layer registration**, **plane continuity**,
and the **misregistration limit**.

The concern behind B11 specifically is: **did the inner layers land on the holes?**

This matters here more than on a general-purpose board because of what the inner layers *are*
on this design. DSN-EEG-003 §3.3 rule 2 pours **AGND_REF on L2 and L3 across the whole
analogue zone**, and rule 3 requires every electrode net to run on L1 **with the reference
plane continuous beneath it**. The inner layers are not a convenience — they are the reference
the front end measures against, and the stitching vias are how the two plane regions are tied.
A via that misses its inner land is a stitch that did not happen.

**Why electrical test cannot find it.** A 100 % netlist test to the supplied IPC-D-356A proves
every net is one connected island. A via with a reduced or absent internal annular ring can
still be electrically continuous — the barrel plating touches *some* of the land, or the net
reaches its destination another way. It fails later, thermally or mechanically, and it fails
in the field. That is precisely the defect class electrical test is blind to, and it is why
the requirement was written.

**So the question is not "can we drop B11". It is "what other evidence shows the inner layers
landed on the holes".**

## 3. The arithmetic — verified, and then a problem with it

### 3.1 Verified against DSN-EEG-003 Rev D

Checked against the source rather than taken from the brief:

- DSN-EEG-003 §3.2, vias row: *"0.60 mm pad, 0.30 mm finished hole, **0.15 mm annular ring**,
  tented both sides"* — the document states 0.15 mm directly. (0.60 − 0.30) / 2 = 0.15. ✓
- IPC-6012 class 2 internal annular ring minimum: **0.025 mm**.
- Misregistration budget: 0.15 − 0.025 = **0.125 mm**. ✓

QP-EEG-010 IQC-B12 and ASM-EEG-007 both carry the same 0.15 mm figure, so the package is
internally consistent. **The brief's arithmetic is correct as far as it goes.**

### 3.2 The problem: 0.15 mm is computed from the *finished* hole

Every statement of the 0.15 mm ring in this package derives it from the **0.30 mm finished
hole**. But the internal annular ring is not measured to the finished hole — it is measured to
the **drilled** hole wall, and the drilled hole is larger than the finished one by the plating
allowance, because the copper that makes the hole "finished" is plated *into* the barrel.

The inner-layer land is etched, the drill passes through it, and what is left of that land is
set by the **drill diameter**, not by what the barrel measures afterwards.

Worked, with the plating allowance as the variable:

| Plating per wall | Drill Ø | Internal ring (0.60 − drill)/2 | Budget to 0.025 mm |
|---|---:|---:|---:|
| 0 (the package's implicit assumption) | 0.30 mm | 0.150 mm | **0.125 mm** |
| 25 µm | 0.35 mm | 0.125 mm | **0.100 mm** |
| 50 µm | 0.40 mm | 0.100 mm | **0.075 mm** |

At a routine 25 µm the misregistration budget is **0.100 mm, not 0.125 mm — 20 % tighter than
the number in the plan.** At 50 µm it is 0.075 mm, 40 % tighter.

> **This is asserted, not verified.** It is the standard reading of how IPC-6012 measures
> internal annular ring, and it has **not** been read out of a copy of IPC-6012 by this
> programme. Confirm it before acting on it. If it is right, IQC-B12's stated limit is
> optimistic and the requirement is harder than the plan believes — which strengthens, not
> weakens, the fabricators' objection.

### 3.3 A package gap this exposed

**Nothing in this package states a drill size or a plating allowance.** Searched `design.py`
and DSN-EEG-003: every hole figure is given as a **finished** diameter, and `design.py`
fabrication note 7 reads "Smallest plated hole 0.30 mm (vias)". `wh_bus.py` is the only place
that touches the distinction, and only in passing — *"sizes below are FINISHED hole diameters;
add plating allowance for the tool"*.

So the package hands the fabricator a finished dimension and never states the tool size, and
the annular-ring figure it then quotes back is computed as though the two were the same. That
is a gap independent of what is decided about B11, and it should be closed either way.

## 4. The alternatives, and what each does and does not prove

The concern is *"the inner layers landed on the holes"*. Measured against that:

| | Option | Proves | Does **not** prove | Vendor friction |
|---|---|---|---|---|
| **1** | **Keep B11 as written** — microsection coupon per lot, ring measured at a through via | Directly and completely: layer order, dielectric thickness, and the ring itself, on a real hole | Nothing relevant is missing. It is the strongest evidence available | **Highest.** Two houses already cannot or do not |
| **2** | **Fabricator registration report** alone | Layer-to-layer registration as *the fabricator measures it*, usually optically on registration targets in the panel border, before or after lamination | **Does not prove the ring at a hole.** Registration targets are in the rails, not at your vias; it is a panel-level statistic, not a measurement of the worst hole. It also does not prove **layer order** | Low — most houses produce one routinely |
| **3** | **The ring added to a standard microsection**, which the house already does | Nearly everything option 1 does, on the house's own coupon and template | Depends on their coupon carrying a **through via of the right drill size**; a standard coupon often sections a plated through-hole of a *different* diameter | **Low to medium.** This is the option the second fabricator's objection actually points at — their template lacks the *measurement*, not the *capability* |
| **4** | **Process-capability declaration** — the house states its registration capability, e.g. ±0.05 mm | That the process is *nominally* capable | Nothing about **this lot**. It is a promise, not evidence, and IQC-B11 exists because promises are not lot evidence | Lowest |
| **5** | **Third-party measurement on the coupon** — the house supplies the coupon, an independent laboratory sections and measures it | The same as option 1, with independence | Adds cost and days per lot; needs the coupon to exist, so it does not help if the house will not carry one in the rails | Medium; moves the burden off the fabricator |
| **6** | **Combination: registration report every lot (B12) + ring-bearing microsection on first article and on any process change** | Layer order and ring at first article; drift caught by the registration report thereafter | A lot-specific defect arising between first article and the next microsection | Medium — a common industrial compromise |

**Two observations that are not recommendations:**

- Option 3 is the smallest change that keeps the evidence. It asks a house to add one
  measurement to a report it already produces, rather than to produce a report it does not.
  The second fabricator's objection was about the *template*, which is a different thing from
  a capability.
- Option 4 is the only one that proves nothing about the delivered lot. If the aim is to
  reduce friction rather than to keep evidence, it is worth being explicit that this is what
  it costs.

## 5. What is not decided here

- **QP-EEG-010 is unchanged.** No limit, method or disposition rule has been touched.
- The **0.025 mm** limit itself is IPC-6012 class 2's, not this programme's, and dropping
  below it would be a departure from the class the whole package is built to — a different
  and larger decision than changing the *evidence*.
- **§3.2 should be settled first.** If the ring is measured to the drilled hole, the real
  budget is 0.100 mm or less and every option above is being judged against the wrong number.
- The **drill-size / plating-allowance gap in §3.3** should be closed regardless of the
  outcome, because the fabricator is currently being given a finished dimension and asked to
  meet a ring figure derived as though no plating existed.
- Vendor answers are still arriving. A third and fourth data point change what "the
  requirement is the outlier" means.

---

*Sources: QP-EEG-010 Rev B §2.1 rows IQC-B11, B12, B13, B15, §4.3 rows FB-21/FB-22, §5
disposition; DSN-EEG-003 Rev D §3.2 and §3.3 rules 2–3; ASM-EEG-007 Rev B; `tools/design.py`
fabrication notes 6, 7, 13, 14; `tools/wh_bus.py`. The 0.15 mm / 0.125 mm arithmetic is
verified against DSN-EEG-003. The drilled-versus-finished-hole point in §3.2 is **asserted
from standard IPC practice and is not verified against a copy of IPC-6012**. Licence:
CC BY-SA 4.0.*

# Decision paper — the two `confirm` rows in `tools/rules.py`

**Status: evidence and options. NO VALUE IS CHOSEN HERE, and no governing document has been
changed.** Under-width critical nets was one of the seven deficiencies that withdrew Rev B;
this is not a number to invent.

**Why it is urgent.** LAY-EEG-034 is about to be uploaded into JLCPCB's *Layout Requirements*
field, where it becomes part of an order specification. A row marked "confirm" is a proposal,
and a proposal is what a vendor points at when refusing to treat a departure as their error.

---

## 1. First, a correction to the brief

The brief describes the open rows as "`confirm=True` on the ELECTRODE widths and on **the
whole ANALOGUE_REF row**". The source does not say that.

`tools/rules.py` uses `confirm` as a **tuple of columns**, not a flag, precisely so a row can
be part transcription and part proposal:

| Class | `confirm` | Meaning |
|---|---|---|
| `ELECTRODE` | `("width",)` | clearance, layers and vias are requirements; **only the widths are ours** |
| `ANALOGUE_REF` | `("width",)` | **also widths only** — not the whole row |

`ANALOGUE_REF` carries no `cites` string, so nothing else in that row is transcribed from a
governing document either — but the only column *flagged* as a proposal is the width pair.
**`rules.py` governs; the brief is wrong on this point.** What is open is two width pairs and
nothing else.

## 2. What the governing documents fix — the search, and its result

Searched: DSN-EEG-003 Rev D, RFQ-EEG-001 Rev E, RISK-EEG-011 Rev B, ICD-EEG-006 Rev C.

**No governing document fixes a conductor width for either class.** What they do fix:

| Source | What it fixes | Class |
|---|---|---|
| DSN-EEG-003 §3.3 rule 3 | electrode nets routed **on L1**, reference plane continuous beneath, **0.35 mm** clearance rather than 0.20 mm | ELECTRODE — layer, clearance, and by implication no vias |
| DSN-EEG-003 §3.2 | board **minimum track 0.20 mm**; "most conductors are 0.25 mm or wider" | whole board, not a class |
| DSN-EEG-003 §3.3 rule 2 | AGND_REF poured on **L2 and L3** across the analogue zone; joins DGND at R90 only | ANALOGUE_REF — topology, not width |
| ICD-EEG-006 §2.1 | analogue load **about 10 mA per rail** *(calculated: three OPA4376 at 3.04 mA plus the dividers)* | ANALOGUE_REF — current |

DSN-EEG-003 §3.2's "0.25 mm or wider" is a **description of the board**, not a class rule. It
is the sentence a reader is most likely to mistake for a requirement, and it is not one.

## 3. What the electrical requirement implies

### 3.1 Current is not the constraint on either class

IPC-2221, 35 µm outer copper, 10 °C rise — the figures LAY-EEG-034 §61 already uses:
**0.40 mm ≈ 1.29 A**, **0.25 mm ≈ 0.89 A**.

| Class | Actual current | Against 0.25 mm ≈ 0.89 A |
|---|---|---|
| ANALOGUE_REF | ~10 mA per rail (ICD-EEG-006 §2.1) | **89× margin** |
| ELECTRODE | 36.8 µA worst-case single fault (RFQ-EEG-001 E-024); ~300 pA bias in normal use | **24 000× margin** |

Current does not select a width here at any candidate value. Any argument for a wider track
on these two classes is about impedance, noise or robustness — never about heating.

### 3.2 IR drop, computed here

*Derived in this paper, not taken from a document.* 35 µm copper, ρ = 1.72 × 10⁻⁸ Ω·m →
sheet resistance **0.491 mΩ/square**. A 100 mm run is used as a representative worst case
across a 150 × 130 mm board.

| Width | Squares in 100 mm | Track R | Drop at 10 mA (ANALOGUE_REF) | Drop at 36.8 µA (ELECTRODE) |
|---|---:|---:|---:|---:|
| 0.20 mm | 500 | 246 mΩ | 2.46 mV | 9.0 µV |
| 0.25 mm | 400 | 196 mΩ | 1.96 mV | 7.2 µV |
| 0.30 mm | 333 | 164 mΩ | 1.64 mV | 6.0 µV |
| 0.40 mm | 250 | 123 mΩ | 1.23 mV | 4.5 µV |

**ELECTRODE:** the whole 0.20 → 0.40 mm range moves the drop by 4.5 µV, and the conductor is
in series with a **68 kΩ** protection resistor (R1–R16). 196 mΩ against 68 kΩ is **2.9 ppm**.
Track width is electrically irrelevant on this class. Whatever justifies a width here, it is
not the electrical requirement.

**ANALOGUE_REF:** the range moves the drop by ~1.2 mV. Against a ±2.5 V rail that is 0.05 %,
and it is a DC offset largely common to the channels. Not nothing, but not a limit either —
which is what `rules.py` already says: *"the width is for source impedance and for the
mid-rail's noise, not for current."*

### 3.3 The isolation strip and the analogue zoning impose nothing on width

- The isolation keep-out (DSN-EEG-003 §3.3 rule 4) is a **region** — x ≥ 141.0 mm,
  y = 2.0–22.0 mm — free of copper on all four layers. It constrains *where* copper may be,
  not how wide it is, and no ELECTRODE or ANALOGUE_REF net goes near it.
- The zoning rule (rule 1, split at x = 62 mm) is likewise a region rule.
- The **0.35 mm electrode clearance** is the real spatial constraint, and it interacts with
  width: at a fixed pitch, every 0.05 mm added to a track is 0.05 mm taken from the gap.
  `design.py` already records this as the binding constraint in the electrode ladder — "the
  rails, their vias and the sixteen row signals (each owed 0.35 mm)".

## 4. What promoting each row would actually cost — measured, not estimated

Computed from `kicad/EEG-CAR-01_RevB_routed.kicad_pcb`, 3745 segments, each segment's width
against the class minimum now in force. **The total reproduces the 322 under-width findings in
`kicad/EEG-CAR-01_RevB_regraded_ECO-EEG-032.txt` exactly**, which validates the method.

| Class | Min | Segments | Under width |
|---|---:|---:|---:|
| **ELECTRODE** | 0.25 | 492 | **0** |
| **ANALOGUE_REF** | 0.30 | 686 | **186** |
| ANALOGUE | 0.25 | 888 | 77 |
| POWER | 0.40 | 863 | 59 |
| USB, LED_DRIVE, DIGITAL, DEFAULT | — | 816 | 0 |
| **TOTAL** | | **3745** | **322** |

### 4.1 ELECTRODE costs nothing. It is already met at the *preferred* width

492 electrode segments, **narrowest 0.300 mm**. The class minimum is 0.25 mm and the
preferred is 0.30 mm, so the released Rev B geometry already satisfies **the preferred
figure, everywhere, with zero exceptions.**

Promoting ELECTRODE 0.25 / 0.30 from proposal to requirement therefore constrains no
geometry that has ever been drawn. It costs nothing and forecloses nothing.

### 4.2 ANALOGUE_REF is 58 % of every under-width finding on the board

186 of the 322. And the per-net breakdown inverts the class's own justification:

| Net | Segments | Under 0.30 mm | Narrowest |
|---|---:|---:|---:|
| AVSS | 351 | 70 | **0.200 mm** |
| AVDD | 255 | **116** | 0.280 mm |
| **AGND_REF** | 58 | **0** | 0.300 mm |
| AVSS2 | 13 | 0 | 0.400 mm |
| AVDD2 | 9 | 0 | 0.400 mm |

**Every one of the 186 is on AVDD or AVSS — the ±2.5 V rails. None is on AGND_REF.**

That matters, because the justification in `rules.py` for the 0.30 mm minimum is *"for source
impedance and for the mid-rail's noise"*. **The mid-rail already meets it and does not need
it; the rails do not meet it and the justification is not written about them.** The 0.30 mm
figure is binding on exactly the members its stated reason does not describe.

AGND_REF is also mostly **not a track**: rule 2 pours it on L2 and L3 across the whole
analogue zone. Its 58 segments are the stitching between pour and pads, not a distribution
path. A width rule aimed at the mid-rail is aimed at something that is largely a plane.

## 5. The options

### 5.1 ELECTRODE widths

| | Option | What it does | Cost | Against |
|---|---|---|---|---|
| **E1** | Promote **0.25 / 0.30** as-is to a requirement | Makes the rule sheet's electrode row wholly a requirement. Cites this analysis as the basis | **Zero.** Already met at preferred on all 492 segments | The number is still this programme's, now stated as a requirement without a document behind it |
| **E2** | Promote at the **board floor, 0.20 / 0.25** | Introduces no new figure: uses DSN-EEG-003 §3.2's own numbers | Zero | Permits a patient-connected conductor at the same minimum as a digital net. Rev B only reached 0.20 mm on these nets *by relaxing*, and Rev C's brief is not to repeat that |
| **E3** | Promote at **0.30 / 0.35** or wider | Matches what Rev B actually achieved (0.300 mm narrowest) and adds margin | Zero against Rev B geometry, but spends gap in the electrode ladder where 0.35 mm clearance is already binding | Buys nothing electrically (§3.2); may cost routability in the one place the board is tightest |
| **E4** | Leave as a proposal, and mark it as such in LAY-EEG-034 | Honest | Zero | This is the status quo, and it is the thing causing the problem: a vendor will read a "confirm" row as optional |

*What the evidence supports:* the electrical case is silent (§3.2), so this is a robustness
and process judgement, not a calculation. E1 and E3 are both free against the released
geometry. E2 is the only option that introduces no programme-invented number, and is also the
only one that lets a patient-connected conductor sit at the board floor.

### 5.2 ANALOGUE_REF widths

| | Option | What it does | Cost | Against |
|---|---|---|---|---|
| **A1** | Promote **0.30 / 0.40** as-is | Keeps the current figures | **186 relaxations to fix in Rev C** — the single largest geometry cost on the board | Binds hardest on the two nets its own justification does not describe |
| **A2** | Promote at **0.20 / 0.25** (board default) | 10 mA needs 0.20 mm eighty-nine times over (§3.1) | Would clear all 186 | Abandons the source-impedance and noise argument entirely, without having tested it |
| **A3** | **Split the class**: keep AGND_REF at 0.30 / 0.40, put AVDD/AVSS/AVDD2/AVSS2 in their own class at a width chosen for rails | Aligns the rule with the reason. AGND_REF already meets 0.30 at all 58 segments, so that half costs nothing | Clears most or all of the 186 depending on the rail figure chosen | A new class is a change to `rules.py` structure and to the rule sheet; needs its own justification |
| **A4** | Keep as a proposal | Honest | Zero | Same vendor problem as E4 |

*What the evidence supports:* **A3 is the option the measurements point at**, because the
justification and the binding constraint are currently attached to different nets. It is also
the only option that requires a second decision — what width the rails get — rather than
settling the row in one move.

## 6. What is not decided here, and who decides

- **No value is chosen.** Every option above is left open.
- The ELECTRODE row touches a **patient-connected** conductor, so the safety reviewer who
  owns RISK-EEG-011 has an interest even though §3.2 shows the electrical case is empty.
- The ANALOGUE_REF row is an **analogue performance** judgement — source impedance and
  mid-rail noise — which needs whoever owns the front-end design, not a layout engineer.
- **A3 cannot be decided from the documents at all**, because no document has ever stated a
  width requirement for the ±2.5 V rails separately from the mid-rail.

Until a decision is made, `confirm=("width",)` should stay on both rows and LAY-EEG-034
should keep saying so, because that statement is currently true.

---

*Sources: `tools/rules.py`; DSN-EEG-003 Rev D §3.2 and §3.3 rules 1–4; RFQ-EEG-001 Rev E
E-024; ICD-EEG-006 Rev C §2.1; LAY-EEG-034 Rev A; `kicad/EEG-CAR-01_RevB_routed.kicad_pcb`;
`kicad/EEG-CAR-01_RevB_regraded_ECO-EEG-032.txt`. Sheet resistance and IR-drop arithmetic in
§3.2 and the segment tallies in §4 are derived in this paper; the tallies reproduce the
regrade tool's total of 322 exactly. Licence: CC BY-SA 4.0.*

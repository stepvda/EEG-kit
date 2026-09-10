# Stage-one investigation — copper for the fixture boards

**Status: investigation only. No routing has been attempted and no file under `fixtures/` has
been changed.** Stage two is not merely un-started — it is blocked, and by something WP1 was
already looking at. That is the finding.

A manufacturer has asked directly whether they build the fixture boards or we consign them.
**Neither is possible today**, and the reason is not that the work was overlooked.

---

## 1. Which of FIX-01 to FIX-04 are PCBs at all?

Answered from JIG-EEG-009 Rev C, not from the shape of the `fixtures/pcb/` directory.

| Fixture | Is it a PCB? | Evidence |
|---|---|---|
| **FIX-01** | **Yes.** 160.0 × 100.0 mm, two layers | §1.9 outline; `fixtures/pcb/FIX-01/` holds outline, zoning, legend, NPTH drill, constraints and a **217-net, 772-pin** netlist |
| **FIX-02** | **Has a circuit; has no board, and no board was ever specified** | §2.4 BOM is U201 (TLV3201), R201–R205 precision resistors, C201, plus a Pico, a PCM5102A and a TPA6132 breakout, two 47 Ω loads and a TRS plug, **in a Hammond 1590B enclosure**. §6.1 prices **no** "Fixture PCB" line for it |
| **FIX-03** | **No. Not an electronic assembly at all** | §3.3 is a printed PA12 nest plus bought items — USB-C pigtail, P75-B1 pogo block, barcode scanner, powered hub — and "no keys, no secrets, and no ability to sign anything". §6.1 prices no PCB line |
| **FIX-04** | **Yes.** Two layers | `fixtures/pcb/FIX-04/` holds the same file set and a **61-net, 208-pin** netlist; §6.1 prices a PCB line at EUR 72 |

**So the fixture index naming FIX-01 to FIX-04 does not imply four boards. It implies four
fixtures, two of which are boards.** `fixtures/pcb/` containing exactly FIX-01 and FIX-04 is
correct and complete for what the document specifies. Nothing is missing there.

**FIX-02 is the one worth a second look, and it is a design question, not a gap.** It has real
electronics — a comparator, five 0.1 % resistors, a threshold network — presently described as
parts in a box. Whether that becomes a small PCB or stays point-to-point in the 1590B has
never been decided, and JIG-EEG-009 does not decide it. It should not be decided by a
generator quietly emitting a board for it.

## 2. Why copper was deliberately omitted

This was a decision, and both the tool and the released data state it plainly.

`tools/fixture_gen.py`:

> **The fixture PCBs are NOT a fabrication release, and this file does not pretend one.**
> […] What is released is everything that does not need a layout engineer — the outline, the
> mounting holes, the zoning and keep-out artwork, the panel legend, the drill programme for
> the non-plated holes, the complete netlist and the constraint set — because those are
> derivable from JIG-EEG-009 and **the netlist is the thing a layout house cannot start
> without.** Copper is not derivable: laying out 83 relays and 144 precision resistors on two
> layers with a driven guard pour is a person's job […] **Inventing a copper layer against a
> footprint nobody has measured would produce a file a fabricator would build and a board
> nobody could assemble.**

`fixtures/pcb/FIX-01/README_fixture_pcb_data.txt` says the same to the reader who only has the
directory: *"a board fabricated from what is here would be a bare piece of FR-4 with four
holes in it […] The copper is a layout engineer's work and is priced in JIG-EEG-009 §6.1 and
scheduled in §6.3."*

**The work is already costed and scheduled**, which is the strongest evidence that it was
planned rather than forgotten:

| | Hours | EUR |
|---|---:|---:|
| FIX-01 schematic capture, land patterns, placement, routing, DRC and outputs | 46 | 2 530 |
| FIX-04 schematic capture, land patterns, placement, routing, outputs, 500 V creepage check | 15 | 825 |
| *(Controller firmware bring-up on the first boards — related, not layout)* | *24* | *1 320* |
| **One-off engineering, first set only** | **85** | **4 675** |

§6.3 puts the layout leg at **15 working days** and says it is "the only long-lead item […]
the layout-then-fabricate leg is now the longest one at 25 days". All figures are stated in
that document as **calculated estimates at EUR 55/hour, not quotations**.

## 3. Can `tools/fixture_gen.py` emit copper?

**No, and it should not be extended to until §4 is resolved.**

- The generator has no copper machinery of any kind — no track, pour, via, paste or plated-
  drill writer. Every Gerber it emits carries a `G04 NOT A FABRICATION SET` line and the NPTH
  writer states "there is no copper layer".
- It has no autorouter, and adding one would be the wrong instrument. FIX-01 needs a **driven
  GUARD pour** and the §1.3 ratio-leg rule; those are the judgements the 20 priced routing
  hours exist to buy.
- It does have `--check`, which computes the area budget against a **stated** land-pattern
  envelope. That is the honest half of the job and it is already done.

Extending it is therefore not a small job and not obviously the right one. The netlists exist
in both human and machine form specifically so a **layout house** can start.

## 4. The blocker, which is a datasheet

**FIX-01's outline is provisional until one number is read off one datasheet.**

From `fixtures/pcb/FIX-01/README_fixture_pcb_data.txt`:

| | |
|---|---|
| Board area | 16 000 mm² (160.0 × 100.0) |
| Occupied | 9 540 mm² — **60 %**, against a 60 % working limit for a two-layer board of this density |
| 83 relays at | **70.0 mm² each — ASSUMED envelope, not a datasheet figure** |
| Largest land pattern the outline can carry | **70.7 mm²** |
| **Margin** | **1.0 %** |

> "A board that closes only if the relay is at or under the size assumed for it is a board
> that does not close if the assumption is 2 mm out on one axis, so this outline is
> provisional until the datasheet is opened."

The part is the **Omron G6K-2F-Y**, and `tools/fixture_gen.py` names it as "a datasheet this
package does not carry". It is section 7 of the new `docs/datasheets/README_datasheets.md`,
and it is **not resolved there either**: `components.omron.com` refuses automated requests
(HTTP 403), so a person has to open the page.

**Routing FIX-01 before that number is known would spend 46 hours and EUR 2 530 against an
outline that may not close.** JIG-EEG-009 §1.9 notes the enclosure — a Hammond 1590D at
188 × 119 mm — has room for a larger board if one is needed, so the fallback exists; but
changing the outline after routing means routing again.

## 5. What stage two should be, and it is not what the brief describes

The brief's stage two is: *"route the fixture boards from their existing netlists through
`tools/fixture_gen.py`, with the same discipline as the carrier — generated from source, DRC
run in KiCad, rule count asserted, nothing hand-edited."*

Three things about that do not survive contact with the source:

1. **`fixture_gen.py` cannot route and should not learn to.** The carrier's own machine
   routing is exactly what an independent layout engineer rejected — vias in pads, stubs,
   off-centre pad entry, under-width conductors — and it is being redone by a human layout
   desk as Rev C. Applying "the same discipline as the carrier" to the fixtures would mean
   repeating the process that produced the withdrawal, on boards that carry 500 V relay maps
   and a driven guard.
2. **The one dimension it turns on is unknown** (§4). This is the hard blocker.
3. **The programme has already decided this is a person's job, priced it and scheduled it.**
   Reversing that is a decision, not a task, and the evidence in §2 argues for keeping it.

**Recommended shape for stage two, for a decision rather than as a plan to execute:**

| | Step | Depends on |
|---|---|---|
| a | Open the G6K-2F-Y datasheet; read the land pattern; check against **70.7 mm²** | a person, WP1 §7 |
| b | If it does not fit: re-size the outline in `fixture_gen.py` (the outline **is** derivable) and re-run `--check` | (a) |
| c | Decide whether FIX-02's circuit becomes a board or stays in the 1590B | JIG-EEG-009 owner |
| d | Commission FIX-01 and FIX-04 layout from a layout house against the released netlists — the 15-day, EUR 3 355 leg already in §6.3 | (a), (b) |
| e | Take the returned copper back in as released data with checksums, as `kicad/gerber/` does | (d) |

Step (a) costs one person ten minutes and unblocks a EUR 3 355 commitment. **Nothing else in
this work package should start before it.**

## 6. What can be answered to the manufacturer today

They asked whether they build the fixture boards or we consign them. The answerable parts:

- **FIX-03 is not a board.** Printed nest plus bought items; nothing to quote as a PCB.
- **FIX-02 has no board and may never have one.** Quote it as an assembled box if they quote
  it at all.
- **FIX-01 and FIX-04 are boards, and the copper does not exist**, so they cannot be built by
  anyone yet — not by them, not by us. What exists is the netlist, the outline, the zoning,
  the legend, the NPTH drill and the constraints, which is what a layout house needs to
  start and is deliberately everything short of a fabrication set.
- If they have a layout capability, **the 15-day leg in §6.3 is a thing they could quote**,
  and that is probably the most useful question to put back to them.

---

*Sources: JIG-EEG-009 Rev C §0, §1.9, §2.1, §2.4, §3.3, §6.1, §6.2, §6.3, §8.8;
`tools/fixture_gen.py`; `fixtures/pcb/FIX-01/README_fixture_pcb_data.txt`;
`fixtures/pcb/FIX-04/`; `docs/datasheets/README_datasheets.md` §7. All euro and hour figures
are JIG-EEG-009's own calculated estimates at EUR 55/hour, not quotations, and nothing in this
package has been built. Licence: CC BY-SA 4.0.*

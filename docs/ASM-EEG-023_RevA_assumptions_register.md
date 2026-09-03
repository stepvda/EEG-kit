# ASM-EEG-023 Rev A -- register of programme assumptions

**Document:** ASM-EEG-023  **Revision:** A  **Date:** 2 September 2026  
**Status:** every entry below is a DECISION taken by the programme, not an approval.


## What this document is

The completeness audit of 2 September 2026 found thirty-two things a contract manufacturer
could not do from this package alone. Twenty-eight were closed by writing the missing files.
The remaining questions were not missing files but missing **decisions** -- a threshold
voltage nobody had fixed, a fastener nobody had chosen, a termination method nobody had
drawn -- and this register holds them.

Each was decided three times over. A first pass proposed a decision from the package's own
numbers. An independent reviewer then attacked it, on technical grounds or as a
manufacturing engineer who had to build to it. **Not one of the twenty-two survived that
attack unchanged.** A third pass re-decided each against its attack, with instructions to
verify the attack before conceding to it -- because an attacker can be wrong too, and
conceding to a bad attack damages the package as surely as ignoring a good one. Several
attacks were partly refuted on exactly that basis, and those are recorded here as kept.

**Nothing in this register is a sign-off.** Every entry names who must sign it. A decision
with reasoning attached is worth having because a reviewer reviews a proposal far faster
than a blank page, and because it makes the assumption visible instead of leaving it to be
discovered by a manufacturer at the point it costs money. It is not worth confusing with an
approval, and the programme does not confuse the two.

## How to read an entry

| Field | Meaning |
|---|---|
| **Confidence: derived** | It follows from numbers already in the package. Check the arithmetic and it is settled. |
| **Confidence: judgement** | A defensible engineering call where the package did not determine the answer. |
| **Confidence: cannot-decide-here** | The question cannot be answered from what exists. The entry says what must happen instead. This is a legitimate answer and there are three of them. |
| **Blocks a build** | A manufacturer literally cannot proceed. Ten do. |
| **What the attack changed** | What was conceded and what was kept, specifically. This is the most useful field for a reviewer. |
| **What would change it** | The measurement or fact that overturns the decision. |


## Summary

- **22 assumptions** decided.
- **8 derived**, **11 judgement**, **3 cannot be decided here**.
- **10 block a build**: D2-FIX01-OUTLINE, D3-CAL-COMMUTATOR, MECH-D1, MECH-D5, D2-EAR-REFERENCE-COUPLER, D3-BIAS-FPZ-TERMINATION, D4-D11-C11-PATIENT-SIDE, D1-ATECC-CONFIG, D1-HM04-CROWN-AND-LEAF, D5-K12-SPRING-ENVELOPE.
- **All 22 require a human sign-off.** None is approved by this document.


---

# Cannot be decided here


## D5-FIX04-EMG-SHARE

**Question.** The FIX-04 head-sharing rule: the EMG head paralleled onto channels 1 to 3 and never mated with the scalp head.

**Decision.**

Two halves, and they get different answers. DECIDED — the paralleling stands, unchanged. J403
ways 1-3 stay on COND1_E1 / COND2_E2 / COND3_E3 alongside J401 ways 1-3
(fixture_gen.py:288-292). 12 + 10 + 3 = 25 conductors on 24 relays; channels 23/24 stay spare on
J407; no fourth TPIC6B595 and no eight further relays. Corrected cost of the rejected
alternative: EUR 55 / 24 = EUR 2.29 per relay, so ~EUR 18 of relays plus the register and the
board area, not "about EUR 25". FIX-04 stays at 61 nets, 208 pins, 35 reference designators, so
JIG §6.1 and §8.8 need no re-issue. DECIDED — the justification is replaced outright. The alias
is NOT a false PASS. It is (a) a false FAIL on H2 — with WH-06 mated at J403 its three leads sit
on the same nodes as E_Fz, E_Cz and E_Pz, so any contact between the three loose snap ends reads
as an electrode-cable short across 3 of the 66 pairs — and (b) a 500 V DC exposure at H4, where
"bundle to any exposed metal" puts the tester's output onto three un-touch-proof 4 mm female
snap cups hanging loose on the bench. H2 and H4 do not even apply to WH-06 (WH-EEG-008 §9
table), so the hazardous state is purely a leftover from the previous H1 — exactly the operator
error the legend rule is for. Refusing HV ARM is the half that matters; continuity was never
single-barrier, because H9 is a 100 % second-person pin-by-pin read-back on every harness.
DECIDED — buildable today, EUR 0 in parts, no netlist change, no creepage question. In fix_m3.c
add a declared-head verb: HEAD [ELECTRODE|LIGHT|EMG|NONE], default NONE at fx_role_init(),
refused with ERR 5 INTERLOCK while hv_armed so it cannot change under voltage. HV ARM refused
with ERR 5 unless HEAD is ELECTRODE or LIGHT (the only cables H4 and H10 apply to). SCAN <n> and
SCANMASK refused with ERR 5 while HEAD is NONE. SCAN OFF, HV SAFE, STATE, LID and fx_role_safe()
are ALWAYS allowed — the new gate goes after the "OFF" branch at fix_m3.c:130, never at the
existing switching_allowed() call at :128. fx_role_state() gains head=<declared> beside the
existing lid_interlock line. WH-EEG-008 §9's QP-EEG-010 record gains a "cable mated at the
fixture" field across H1-H6 and H10 — the range it actually records; H7/H8 are FAI and H9 is a
signature — and §9 states that an H2 or H4 result taken with a second cable mated is void. This
is a declaration, not a sense: it does not stop a lying operator, but it moves the rule off the
silkscreen into a step the operator must take, that STATE reports and that the record carries.
NOT DECIDABLE HERE — the sensed interlock (three presence loops, three GPIOs, "under EUR 5"). It
is withdrawn as specified, and I will not respecify it, because the package does not establish
whether there is anything to sense. The released artwork calls the board connector the head
("J403 EMG HEAD IS NEVER MATED WITH J401", fixture_gen.py:498) and JIG §4.1 defines each head by
the cable it Mates — on that reading the heads never come off, a presence loop reads "both
present" forever, and the card cannot run H1 at all. Against that, §6.1 buys "screened
multicore" and EUR 20 of printed parts for FIX-04, and §8.9 releases seven printed parts of
which none is a FIX-04/D head — so the heads may be flying assemblies whose bodies have simply
never been drawn. Those two released facts contradict each other, and neither WH-01 (12 ways, 12
conductors) nor WH-02 (10 for 10) has a spare way to sense the cable instead.

**What the attack changed.**

CONCEDED, all verified in the files: 1. The false-PASS story is gone. WH-EEG-008:1435 gives H1
as "site terminal to its connector pin"; the EMG lead hangs on the fixture-side node as an open
stub and its far end is a snap socket, not the Fz cup. A broken E_Fz reads open either way. The
whole load-bearing sentence of the reasoning was wrong. 2. "H1 is the only test the electrode
harness ever gets... nothing downstream catches it" is false twice. WH-01 also gets H2, H3, H4,
H5, H6 and H9 — and H9 (:1443) is a second-person pin-by-pin read-back, 100 % match, applies to
all. T9c (TST-EEG-004:622-630) is fitted-harness; it is a type test, so the honest claim is "no
per-unit step", not "no later step at all". 3. Present is not mated. I checked further than the
attack did and it is worse than "unstated": the released silkscreen string at fixture_gen.py:498
calls J403 itself the EMG head. The decision's interlock senses the wrong variable, and may
sense a variable that does not move. 4. The three pull-ups are unbuildable. fixture_gen.py has
only V5 and DGND on either fixture; RP2040 inputs are not 5 V tolerant; the package's own idiom
for this exact input is internal — hal_rp2040.c:109 gpio_pull_up(PIN_LID_INTERLOCK). Deleted,
along with the "under EUR 5". 5. Creepage and §5b unaddressed. FIX-04_constraints.txt §5a
demands 3.0 mm from anything carrying the tester's output; §5b keeps the common bus off DGND on
purpose. A DGND-referenced pair entering the electrode head and crossing the SCANNER MATRIX zone
was never argued against either rule, on the one card that switches a lethal voltage. 6. No head
body exists. JIG §8.9 lists seven printed parts and none is a FIX-04/D head, so "two ways in the
head housing strapped together" has nowhere to live. 7. Record wording wrong. WH-EEG-008:1463
records H1-H6 and H10, not H1-H10, and records/ carries no harness schema at all (T00..T30,
additionalProperties:false at both levels). 8. SCAN OFF. fix_m3.c calls switching_allowed() at
:128, before the "OFF" branch at :130, so the decision's gate would have refused the one command
that drops all 24 channels to the common bus. The gate moves below the branch. Minors conceded:
~EUR 18 of relays, not 25 (EUR 55 / 24 = 2.29 each). KEPT, because the attack did not break it
and the files back it: - The paralleling itself: 25 conductors on 24 relays, one cable at a
time, channels 23/24 genuinely spare (22 is L10, so the re-map alternative does spend both),
fourth register rejected. - That a silkscreen line is not enough — the attack agrees, and argues
the stronger case. - M3, ERR 5 INTERLOCK and the lid-open drop in fx_role_poll() as the correct
model and place. REJECTED — one correction back at the attack: - "The harness is tested loose,
before the helmet-end terminations" is imprecise. WH-EEG-008:1427 defers only the terminations
to the contact-light LEDs; the HM-04A electrode terminations are made and H6 pull-tests them at
15 N. So H1's far end for WH-01 really is the crown contact. This does not change the attack's
conclusion — there is still no path through a broken conductor — but the reason is the stub's
location, not an unterminated cable. - WH-06's far end is a 4 mm FEMALE snap socket (Staubli
SLS425-SEK/N), not a "loose stud". Still un-touch-proof metal at 500 V; state it as the cup, not
as a stud. NOT TAKEN from the attack's correction: its instruction to wire the loops lid-switch
style and price them as three connectors and three leads. That presumes the heads unplug, which
is the fact nobody has established.

**Reasoning.**

The decision reached a defensible conclusion through a chain of reasoning that does not survive
the files. H1 measures site terminal to connector pin, so the paralleled EMG lead — an open stub
on the fixture side — cannot carry the measurement, and the false PASS the whole decision was
built on does not exist. Meanwhile H9 puts a second person pin-by-pin across every conductor of
every harness, so continuity was never the single barrier it was claimed to be. A conclusion
resting on a mechanism that is not real has to be re-founded before it can be kept. Re-founded,
the case is still good and is arguably stronger: the real consequence of the alias is a false
FAIL on 3 of H2's 66 pairs and, at H4, 500 V DC on three loose un-touch-proof snap cups. Neither
H2 nor H4 applies to WH-06, so the hazardous state is never a state anyone needs — it is purely
a leftover EMG lead from a previous H1. That is precisely the error a legend cannot catch and an
interlock can. But the decision's interlock cannot be specified from released data. Its sense
loop needs a head that comes off the card and a housing to strap two ways in. The released
legend calls the connector the head; §8.9 releases no head body; §6.1 buys multicore and printed
parts that imply one exists. Those cannot all be true, and the answer changes completely
depending on which is: if the heads are captive the interlock is dead on arrival and would
refuse SCAN forever; if they are separable it works but silently rewrites the shop rule into an
extra J403 mate cycle per unit and still owes an answer on DGND inside a head that carries 500
V. Choosing between those from here would be inventing the fact, and the fact is a mechanical
property of a part that has never been drawn. So I took the floor that needs no missing fact.
FIX-04 already knows the moment that matters — it owns HV ARM — and fix_m3.c already has
hv_armed, FX_ERR_INTERLOCK, fx_role_state() and the lid-open drop path. A declared-head verb
gating HV ARM and the scanning verbs, with SCAN OFF and fx_role_safe carved out, costs one verb,
no parts, no nets, no creepage argument, and it puts the head state into STATE and into the
harness record where the legend could never put it. It is weaker than a sense — an operator can
declare wrongly — and I am saying so rather than dressing it up. It is strictly better than a
silkscreen line, and it is buildable from the files as they stand today.

**Confidence:** cannot-decide-here  |  **Blocks a build:** no  |  **Signed off by:** Programme engineer, who owns JIG-EEG-009 and must settle the one open fact (are the FIX-04/D heads separable from the card at J401/J402/J403, or are J401/J402/J403 themselves the heads as the released legend says). Plus the safety engineer the package repeatedly records as never having reviewed anything (JIG §4.3, DESIGN_FACTS §8 item 1), because this is the card that switches 500 V DC and the finding is a live exposed-metal hazard at H4 on leads that are patient-applied parts. Plus the QC inspector who signs H4 and H10, because the void condition added to WH-EEG-008 §9 changes what they are certifying. The declared-head firmware gate and the WH-EEG-008 §9 record wording can go in under the programme engineer alone; the 500 V finding and any sensed interlock cannot.

**What would change it.**

One determinate fact decides the sensed interlock, and it is a drawing question, not a
measurement: state in JIG §4.1 whether the FIX-04/D heads are flying assemblies that unplug at
J401/J402/J403, or are the board connectors themselves. - If they unplug: the sense-loop
interlock becomes the right answer, wired exactly like the lid switch (J40x way 1 to a free M3
GPIO, way 2 to DGND, strap in the head, internal gpio_pull_up() — no external resistors, since
there is no 3V3 rail on this card), and it then also needs three head bodies released as printed
parts under §8.9, a FIX-04_constraints.txt §5 note bringing the sense pairs under the 3.0 mm 500
V rule and answering §5b on controller ground inside a head that carries 500 V, and re-issued
net and pin counts in JIG §6.1 and §8.8. The shop rule also changes to "unplug the head you are
not using", which adds a J403 mate cycle per unit and should be priced. - If they are the board
connectors: sensing is off the table permanently, and the declared-head gate plus a legend that
names the hazard rather than just the rule is the final answer. Separately: if WH-EEG-008 §9 is
ever revised so a step needs the electrode head and the EMG head live together, the whole share
is wrong and the fourth TPIC6B595 (~EUR 18 of relays plus the register and area) becomes the
right spend, as §4.1 already says. And if the 4 mm snap ends of WH-06 are ever specified as
touch-proof shrouded, the H4 half of the hazard drops and only the H2 false-FAIL remains.

**Files this touches:** `docs/JIG-EEG-009_RevB_test_fixture_design.md`, `docs/WH-EEG-008_RevB_harness_and_cable_assembly.md`, `fixtures/firmware/src/fix_m3.c`, `fixtures/firmware/test/host_test.c`, `tools/fixture_gen.py`, `records/README.txt`


## D1-HM04-CROWN-AND-LEAF

**Question.** How does WH-01 conductors 1-8 attach electrically to the Ag/AgCl cup at each of the eight HM-04 electrode assemblies, given a cup that is released on a service bayonet at every turnaround and replaced every ~25 sessions?

**Decision.**

HOLD the joint; split the decision in three and issue only the part that is derived and safety-
free. A. ISSUE NOW — the bayonet run only (clause (c)). This is a literal build stop and is pure
mechanism. HM-04 entry slots re-cut 1.70 mm wide x r 4.60-5.55 x 3.20 mm deep; a 90-degree
circumferential run at z 0.80-3.20 with a 0.80 mm retaining lip at the cup face, ending in a
0.35 mm detent, clockwise viewed from the cup face; HM-05B lugs re-cut 1.40 mm wide x r
4.55-5.40 x z 0.95-2.95. Float stays 0.40 mm (down 0.15 / up 0.25). TWO CONDITIONS the original
decision did not carry: (i) FIT-01 must gain the slot, run and lug. `fit01()`
(tools/mech_gen.py:646-655) is three plain bores 9.20/9.35/9.15 and nothing else, despite a
docstring claiming it "carries the cup bayonet"; it gates no bayonet feature today. (ii) The re-
cut moves the up-stop from the carrier face on the bore roof to two 1.40 mm lugs on a printed
run roof, and creates a down-stop that did not exist at all (the released entry slot is open at
the cup face and retains nothing). SVC R10's 10 N retention and H6's 15 N must be demonstrated
on that coupon before the run is called released. B. ISSUE AS VENDOR CRITERIA ONLY, not as
released geometry — (a) crown annulus OD 5.20 / ID 3.20 x 0.50 mm thick, let flush in the HM-05B
spigot top at z 11.60-12.10, gold >= 0.76 um over nickel on the upper face (nickel thickness to
the plater's standard; the "3-6 um" and the "same rule AVL 1.4 already imposes" citation are
both struck); (e) 0.60 x 0.50 mm axial tail groove in the HM-05B OD at 45 degrees to lugs and
drive notches, potted flush; (f) the field-replaceable unit is the HM-05A + HM-05B + HM-05C
assembly joined once in the shop — this is correct and is what keeps a soldering iron out of SVC
5.4 and the joint out of the 40 kHz bath; K1 (10), K26 (8+2) and the SVC R11 consumable schedule
move with it in the same change; (g) K1 purchase criterion: 20 mm +3/-0 of 7/0.1 mm pre-tinned 3
mm, or a welded tab — a PO criterion, not a released dimension, because HM-05A's "modified for
the service bayonet" has never been drawn. C. DO NOT ISSUE — (h) at all, (b) as dimensioned, (d)
as dimensioned, and the K12 line. The electrical termination itself cannot be closed from this
package, for three reasons that no value can paper over: (1) the volume it must live in is an
undivided, gel-flushed through-cavity that the LED also occupies, and SF-9 says in terms that
physical separation is the only possible control — that is a safety disposition nobody has made;
(2) the free band left for crown + leaf + spring is 1.15-1.55 mm under the decision's own stops,
and no 302 coil at ~7.5 N/mm (3 N -> 6 N over 0.40 mm) has a solid height under 1.15 mm, so K12
is not merely unspecified but arguably not realisable in the released envelope; (3) HM-05A, the
cup this joint terminates, has never been drawn. The crown-and-leaf PRINCIPLE stands and is not
overturned — only the values are held.

**What the attack changed.**

CONCEDED, all five points, after checking each against source. (1) Clause (h) is withdrawn
entirely. Verified: `hm04()` cuts the side opening as ONE box, `win = box(3.2, w+2, 2.6)` at z
11.70-14.30 through a 12.40 mm body (mech_gen.py:577-578) — the "inboard" and "outboard"
openings are two ends of one undivided cavity. The gel port is `circle(1.25).cutThruAll()`,
entirely inside the window's |x| <= 1.6, so from z 14.30 down the port is not a bore: it vents
sideways into that slot and out both faces. RISK-EEG-011:322 SF-9 reads exactly as quoted ("No
series resistance can control this fault ... The control is physical separation and its
verification, nothing else"); H-05 at :192 is 3/1/3 with separation as its sole control; ASM-
EEG-007:1288 open item 20 already records the exclusion as unsupported by the frame as built;
SR-01's 53.2 uA vs 50 uA is confirmed at :190. The attack is also right that R1-R16 are not in
this fault path — they sit between the conductor and the ADC, not between a 3.3 V / 1 kOhm LED
source and the cup. And "raised and shielded" is geometrically false: a crown face at z 12.10 is
0.40 mm ABOVE the slot floor at 11.70, i.e. inside the slot, in line of sight of both openings.
R6's two 10 ml passes plus 1 bar of air, and IFU step 1's per-session syringe of gel, both run
through that volume. (2) Clause (d) is held. WH-EEG-008:1440 H6 reads "acts on HM-04A's
anchorage in the body AND on the solder joint to the conductor"; AVL K25 (:564) still requires
"an anchorage in printed PA12 that holds 15 N". (d) takes both out of the load path and re-
issues neither, so H6 would afterwards pass by pulling a strain relief while a dry solder joint
goes untested. The keyhole is genuinely not buildable as written — no lobe/throat, no depth, no
z, no lip — and a 2.0 mm bulb in a 2.00 mm feature is zero nominal clearance in MJF PA12. (3)
K12 is struck from the re-cut line. AVL:551 carries only "3-6 N at working length, stainless
302" — no bore, no rate, no solid height. WH §3.1.1's released row says "Spring | K12, unchanged
| It bears on the crown"; with crown OD 5.20 inside a Ø6.80 seat the spring necessarily lands on
the 0.70 mm PA12 land at r 2.60-3.30, not on the crown. The decision reversed a released row
silently. I ran the attack's spring arithmetic myself and it holds. (4) "A seated cup is by
construction a connected cup" is struck from the reasoning. The leaf and the spring both act
between HM-04 and HM-05B — parallel, not series — so the interface force is the leaf's >= 0.5 N
alone, on a part (K25) with no vendor and no sample. Note this error is inherited verbatim from
released §3.1.1 and is echoed in H6's own parenthetical ("designed to part at 3 to 6 N"), so the
correction propagates to both documents, not just to this decision. (5) Plating citation
corrected; K1/K26/SVC consumable lines added to the change. WHERE THE ATTACK IS WRONG OR
OVERSTATED, and I did not concede: - "about 3 mm apart" is wrong. The cavity is 3.2 mm wide in x
and runs the full 12.4 mm through in y; the two openings are 12.4 mm apart. The defect is the
shared, undivided, gel-flushed volume with no partition and no creepage figure — not the
spacing. Stating it as 3 mm invites a reviewer to "fix" it by spacing, which fixes nothing. -
"clause (h) ... does so deliberately", as if the decision invented the arrangement. It did not.
WH §3.1.1's own "must gain" table already asks HM-04 for "a seat and two lead passages for the
contact-light LED at the outboard opening". The decision inherited it. That does not rescue (h)
— §3.1.1 is marked "a PROPOSAL, not a released design" whose safety reviewer has not answered,
and issuing it as a value is precisely what converts an open proposal into a released control-
less arrangement — but the fault is the package's, not this decision's alone. - The attack
UNDERSTATES FIT-01. It says the new load path "FIT-01's 9.20/9.35/9.15 coupon does not gate"; in
fact `fit01()` is three plain cylindrical bores with no slot, no lug and no run, so it gates no
bayonet feature whatever, and its own docstring is wrong about that. KEPT, and independently re-
derived: the two model findings. `hm05b()` lugs are `box(1.05, 1.40, 2.10)` at r 4.875 -> r
4.35-5.40, z 0.15-2.25; `hm04()` slots are `rect(2.2, 1.4)` at r 4.20 -> r 3.10-5.30 x 1.40 wide
x 2.40 deep. 0.10 mm radial interference, zero tangential clearance, no circumferential run: the
released parts do not assemble. `hm09()` tip lugs `box(2.0, 1.2, 2.2)` at r 4.2 -> r 3.20-5.20 x
1.20 do fit, so the defect really is invisible from the key side. The 1.40 mm free band (spigot
top 12.10 -> seat roof 13.50) and the 0.40 mm float (bore 9.00 - body 8.60) are right. The
rejections check out: `hm11a_halo()` is 11.93 mm at the front against SECTION_W_MIN 12.20
(mech_gen.py:761-762, 849-853), the flank pocket is enclosed by 0.05 mm of radial clearance, K12
is 302 stainless.

**Reasoning.**

The attack lands its main blow and I checked every citation it made; all of them hold. But the
reason this becomes "cannot decide here" rather than "issue the correction" is narrower than the
attack's list and worth stating precisely. The decision was asked for the electrical attachment.
That attachment has to live in the 1.15-1.55 mm band above the HM-05B spigot. Three separate
things already own that band and none of them can be moved from here: - The gel path owns it.
The Ø2.50 port is inside the through-slot's |x| <= 1.6, so below z 14.30 the port is not a bore.
Participant gel goes in there every session and 20 ml of water plus 1 bar of air goes through it
every turnaround. - The LED owns the other end of the same cavity, by the released proposal's
own request, against a hazard (H-05 / SF-9) whose only stated control is physical separation and
whose exclusion ASM open item 20 already records as unsupported. - K12 owns what is left, and
cannot: 3 N at 1.55 mm rising to 6 N at 1.15 mm is ~7.5 N/mm with a solid height under 1.15 mm,
which no 302 coil delivers. Any one of those is a re-cut. Together they mean the joint's
geometry is not determined by this decision at all — it is determined by whichever way the
safety reviewer disposes of the LED, and by whether the band can be opened up. Issuing crown and
leaf values now would fix dimensions to a cavity that is about to change shape. One finding
neither side has, which points at the cheapest fix. `hm04()` builds a solid `b`, cuts a one-
sided 4.0 x 3.0 light window into it at z 13.5 — and then throws `b` away. `body` is rebuilt
from scratch (mech_gen.py:568-577) and only the through-slot `win` is cut. So the released
through-slot is the residue of an abandoned code path; the AUTHORED intent was a blind one-sided
window, which is also what ASM §4.2 describes and what WH §3.1.1 flags as not matching the
model. That reframes the safety fix: restoring a blind outboard LED seat and cutting a SEPARATE
inboard entry for the electrode conductor, with full-thickness PA12 between them, is a return to
the drawing's intent rather than a new invention — and it is the option that preserves H-05's
exclusion as written. It still needs both reviewers and it still leaves the gel path to be re-
drawn, because with the slot blinded the port becomes a real bore again and the flush has
somewhere to go. That is a good thing, not a complication. What I am NOT holding: the principle,
and the bayonet run. The principle — the quarter-turn already in SVC R4 is the disconnect, a
rotation-invariant annulus so nothing twists, no connector mated at a site with wet gloves —
survives the attack untouched; the attack concedes it. And the run is a different question from
the joint. The released HM-04/HM-05B pair does not assemble: 0.10 mm of radial interference,
zero tangential clearance, no circumferential run at all, and an entry slot open at the cup face
so there is no retention either. That is a defect in a released model, independent of every
electrical question, and it is worth issuing on its own so the mechanical reviewer is not
waiting on the safety reviewer to fix a plug fit that cannot turn. Two smaller things the attack
got right that change the shape of the change order rather than the answer: H6 and K25 have to
be re-issued in the SAME change as any strain relief, or the 15 N test silently stops testing
the solder joint; and H6's parenthetical "designed to part at 3 to 6 N" is wrong for the same
parallel-load reason as the reasoning's "seated is connected", so both documents get the same
correction.

**Confidence:** cannot-decide-here  |  **Blocks a build:** yes  |  **Signed off by:** Order matters, and it is not the order the original decision gave. 1. SAFETY REVIEWER FIRST, not second. Re-run H-05 and SF-9 against a chosen HM-04 geometry and record the disposition beside RISK-EEG-011 §4 and SR-01. This has to come first because its outcome DETERMINES the HM-04 cavity the mechanical reviewer would otherwise cut; cutting the crown and leaf pockets before it is answered means cutting them twice. The two options to rule between: a blind outboard LED seat with two lead passages, separated from the inboard termination volume by a full-height printed web (the abandoned-code-path intent, and the option that preserves H-05's exclusion as written), or the LED out of the HM-04 body entirely, lit through a light pipe from a frame-mounted source, which keeps WH-02 out of the electrode body altogether. Either way the gel path is re-drawn in the same breath, or R6's flush exits through the window instead of the cup. 2. MECHANICAL REVIEWER owning MECH-EEG-020 sheet 8, for the re-cut of HM-04, HM-05B and FIT-01, and for the new lug-on-run load path. May proceed on section A (the bayonet run) immediately and in parallel — it is independent of the safety question. 3. AVL-EEG-017 for K25 and K26 against the corrected criteria, for K12 (or its replacement by a wave washer, which is the only form that fits 1.15-1.55 mm at that rate), and for K1's tail and quantity. 4. ECO-EEG-016. WH §3.1.1 is explicitly not yet in the change register; nothing here can be issued outside an ECO. No sample can be judged before 1 and 2 have both signed.

**What would change it.**

Four things, and the first two are gates rather than experiments. 1. A written safety
disposition of SF-9 and H-05 against a named HM-04 geometry, recorded beside RISK-EEG-011 §4 and
SR-01. Until that exists there is no answer to give, whatever geometry anyone draws. If it
chooses the frame-mounted LED and light pipe, the whole inboard cavity becomes the termination's
alone and clauses (b) and (d) can be dimensioned immediately. 2. HM-05A drawn. The cup is bought
as "modified for the service bayonet" and the modification has never existed on paper; the
crown's tail joint, K1's purchase line and the free-state protrusion all hang off it. 3. A K12
that exists in 1.15-1.55 mm at ~7.5 N/mm with a solid height under 1.15 mm — realistically a
wave washer or a conical washer, not a 302 coil. If no such part is found, the band itself has
to be opened up, which re-opens HM-04's height and the seat roof at z 13.50, and every value in
(a) and (b) moves with it. 4. A FIT-01 coupon re-cut to carry the slot, run and lug, printed in
the batch, and pulled. If the bayonet does not turn and retain against SVC R10's 10 N, or a
contact sample cannot hold 0.5 N across the full 0.40 mm of float, the joint reverts to the
leaded-cup-into-the-channel fallback — and HM-01's parametric redraw then has to carry a pocket
for it, on a frame that is already 11.93 mm against the 12.20 mm its own harness document needs.
Also overturning: an input-referred noise run (TST-EEG-004 T8, inputs shorted, 1.0 uV RMS) that
degrades with the joint fitted; or a first-article H6 that damages a strain-relief keyhole
rather than the body, which moves the relief outboard onto the channel cover.

**Files this touches:** `docs/RISK-EEG-011_RevB_risk_analysis_and_safety_review_pack.md`, `tools/mech_gen.py`, `docs/WH-EEG-008_RevB_harness_and_cable_assembly.md`, `docs/ASM-EEG-007_RevB_assembly_work_instructions.md`, `docs/SVC-EEG-013_RevB_service_and_refurbishment_manual.md`, `docs/AVL-EEG-017_RevB_approved_vendor_list.md`, `docs/PARTS-EEG-019_RevB_part_identifier_register.md`, `docs/DSN-EEG-003_RevC_manufacturing_design_package.md`, `docs/ECO-EEG-016_RevB_change_control_and_document_register.md`, `KNOWN_ISSUES.txt`


## D5-K12-SPRING-ENVELOPE

**Question.** AVL K12 buys a "3-6 N stainless 302 compression spring" selected against the HM-04 outline (12.4 x 12.4 x 18.0 mm). What spring actually fits, and what stops it from becoming part of the electrical joint?

**Decision.**

Re-issue K12 as a FINDING plus a partial specification. Do NOT issue a dimensioned envelope, and
do not re-cut HM-04 on this decision. FINDING (this part survives and is confirmed against the
released solids). "3-6 N stainless 302 compression spring" cannot be bought. hm04() cuts the
seat Ø6.80 z 9.00-13.50; hm05b() gives a Ø9.10 x 8.60 body and a Ø6.60 x 3.50 spigot, so the
spigot top is z 12.10. The seat/spigot annulus is 0.10 mm on the RADIUS (0.20 diametral) and no
coil occupies it. The only free volume is the ~1.40 mm band above the spigot, and the 3.20 mm
through-slot (z 11.70-14.30) opens straight into it. That band is a wave-spring band. WHAT K12
MAY SAY NOW: - Form: multi-turn crest-to-crest wave spring, stainless. NOT a coil (no annulus).
NOT a Belleville (OD 6.50 / ID 5.40 is De/Di = 1.20 against a normal 1.7-2.5, on 0.55 mm of
radial width — a ~75 deg cone, i.e. a tube). NOT a single-turn wave washer (I re-ran Smalley: E
193 GPa, b 0.55, Dm 5.95, N 3, K 2.4 → 7.5 N/mm needs t = 0.076 mm, and 3*pi*P*Dm/(4*b*t^2*N^2)
at 6 N = 2,930 MPa, ~1.6x the tensile of 302 spring temper; it sets on first compression). -
Material: stainless 316 spring temper, REQUIRED, not offered as an alternate to 302. The seat is
a chloride crevice under wave crests that is never immersed, never scrubbed and never fully
dried. - Diameters (these ARE derivable from released solids): OD <= 6.50 mm, ID >= 5.40 mm,
bearing on the PA12 spigot rim between r 2.70 and 3.30. - Heights: SYMBOLIC, not numeric.
working_height_rest = seat_roof_z - (spigot_top_z at the run's retaining datum);
working_height_min = the same at the run's roof datum. Both are undefined until HM-04's
circumferential bayonet run is drawn. - Solid height as a RELATION, not a number: solid_height
<= working_height_min - 0.25 mm, so the spring can never stack solid inside travel. - Force: 3-6
N carried forward unchanged as AVL K12's own stated target, explicitly not derived. - No-gold
rule as a RELATION, not two independent limits: (ID_min - crown_OD_max)/2 >= (seat_bore_max -
spring_OD_min)/2 + 0.05 mm. Do not fix HM-05C's OD from a purchase spec. - Qualification: 25
cycles of SVC R6 (two 10 ml warm-water passes, demineralised rinse, <=1 bar air) + 70% IPA wipe
+ conductive-paste dwell — the K25 regime. NOT the cups' 40 kHz R5 bath: ASM 4.2 bonds HM-04
into HM-01, and SVC R5 lists HM-01 as "Wipe, never immersed". - Status: SAMPLE ONLY, five pieces
measured on a printed HM-04/HM-05B pair. No fleet order. - Also required and absent today: a
retention/capture feature for the ring, an ASM fitting step and an SVC handling step
(KNOWN_ISSUES.txt lines 256-258 record that no assembly step fits the cups, carriers or springs
at all). WHAT IS NOT DECIDABLE AND MUST NOT BE INVENTED: 1.80 mm at rest / 1.40 mm at full
travel, free height 2.20 mm, solid <= 1.40 mm, and rate 7.5 N/mm. Also withdrawn: "the HM-05C
crown OD of 5.20 mm" as a fact, the HM-04 seat re-cut to roof 13.90 + Ø7.60 at 13.90-14.30 as a
spring change, and the claim that the spring being clear of gold satisfies WH 3.1.1(2) "out of
the gel".

**What the attack changed.**

CONCEDED (checked, and all of it holds): 1. The rest datum does not exist. mech_gen.py hm05b()
says in bold "**The bayonet does not yet turn.** hm04() cuts a straight 2.40 mm entry pocket and
no circumferential run behind it... it is a plug fit, not a bayonet." PARTS-EEG-019 OA-14 and
the HM-04/HM-05B register rows carry it, and WH-EEG-008 open item 22 blocks on it. 9.00 - 8.60 =
0.40 mm is plug-fit float, not spring stroke. I went further than the attack: measured against
sibling D1's OWN proposed run (HM-04 run z 0.80-3.20 against HM-05B lugs z 0.95-2.95), the
carrier sits 0.15 mm low at rest and rises 0.25 mm, so with roof 13.90 the band is 1.95 / 1.55
mm, not 1.80 / 1.40. A spring built to the issued envelope (free 2.20, 7.5 N/mm) then delivers
1.9 N at rest — under its own 3 N floor — and 4.9 N at full travel. The envelope is wrong even
against the decision it claims to coordinate with. 2. The physics of the "hard rule" is wrong. A
stainless ring seated on PA12 at one end and touching gold at the other is a dead-end stub, not
"a second metal junction in parallel". And the safeguard does not achieve WH 3.1.1(2)'s "same
plating on both mating faces, and out of the gel": AVL K12 itself says "the spring is inside the
electrode body and is exposed to gel and saline", the Ø2.50 gel port delivers into that volume
and SVC R6 flushes it. A 0.10 mm air gap in conductive paste is not isolation. Conceded and
rewritten: the real reasons to keep stainless off the crown are galling of the gold-over-nickel
plating K25/K26 require, under the 90 deg turn SVC R4 performs at eight sites every turnaround,
and PA12 rim wear at 3-6 N on a 0.70 mm annulus that has to hold the crown flush at z 12.10. 3.
The rule was unenforceable as written. OD 6.50 in a Ø6.80 seat is 0.15 mm radial float against a
0.10 mm radial gap over a 5.20 crown — and MJF is +0.15/-0.05 (FIT-01 gates 9.20/9.35/9.15), so
at a 6.95 bore the float is 0.225. Float exceeds gap; the ring lands on the gold. The attack
understated this. Replaced with a relation. 4. Crown OD 5.20 is not in the package — K26 says
only "outside diameter to suit the Ø6.60 mm spigot; centre clear of Ø2.40 mm", and grep finds no
5.20 anywhere in docs/, mech/ or tools/. Conceded with a correction to the attack (below). 5.
The spring form was wrong. Belleville at that ratio is a tube; a single-turn wave washer sets on
first compression. Only a multi-turn crest-to-crest wave spring reconciles rate, stroke and
stress, and the decision never said so. My own Smalley calc reproduces the attack's t = 0.08 mm
and ~2,900 MPa within a percent. 6. Solid height <= 1.40 mm equalled the minimum working height,
so the spring could stack solid exactly at 6 N and, at the tight end of the fit, hand the scalp
whatever the helmet presses with for a 2 h session — on a patient-applied part whose whole
justification (AVL K12) is that the force is the one thing the participant cannot adjust.
Conceded, and expressed as a relation rather than the attack's 1.10 mm. 7. The accept/reject
discriminator was false. WH 3.1.1 states "The side slot, at z 11.70 to 14.30, opens straight
into that band." The released seat is already breached over 11.70-13.50, and at roof 13.90 the
whole spring band 12.10-13.90 is still inside the slot. "Visible and dislodgeable" is true of
the accepted option too. Objection dropped and replaced with the real requirement: a capture
feature, plus an ASM step and an SVC step. 8. "Costs nothing" was wrong, and doubly so. The slot
removes only |x| <= 1.6 of the 7.60 mm width, so Ø7.60 at z 13.90-14.30 cuts new material on all
four shoulders; ASM 4.3 already fits a bicolour LED into that exact window with no seat, and
WH's must-gain table owes three more features into the same band. Worse, the Ø7.60 z 13.90-14.30
relief is sibling D1's leaf run, already proposed there — so "to make that envelope exist" is
circular twice over. The re-cut is dropped from this decision and handed to one MECH-EEG-020
sheet 8 that allocates the band once. 9. Wrong qualification regime. SVC R5 immerses "8 cups, 2
ear clips" only; HM-01 is wipe-never-immersed and HM-04 is bonded into it (ASM 4.2, 100 N pull-
off, unrepairable). The spring never sees the bath. Regime corrected to R6 + IPA + paste, and
316 made mandatory. 10. No retention and no loss control. Confirmed at KNOWN_ISSUES.txt:256-258
— no ASM step fits the springs, carriers or cups; SVC line 187 handles the cup and never the
spring. Under D1 a lost or mis-seated ring is a silent open electrode. Smaller items conceded:
"0.10 mm of diametral clearance" is 0.10 radial / 0.20 diametral by the package's own convention
(mech_gen.py calls 9.20-9.10 "0.10 mm diametral"); the reasoning's claim that a washer fits in
1.40 mm is contradicted by then needing 1.80; and the label "D1" collides with RUL-EEG-021's
released D1-D16 ruling (BAV99, not BAT54S). WHERE THE ATTACK IS WRONG OR OVERSTATED, AND I DID
NOT CONCEDE: - "It silently reverses RELEASED text." WH-EEG-008 3.1.1 opens "**Nothing in this
section is released.** It specifies a joint that does not exist", and AVL carries K25/K26 as
OPEN WITH CRITERIA. The K12 "bears on the crown" line is a proposal, not released design. The
defect is real but lesser in kind: the decision contradicted a live proposal without flagging
it. It still has to be raised as a change to 3.1.1 and to K25/K26. - "Crown OD 5.20 is
invented." It is not conjured — it is sibling decision D1(a) in this same batch, which D5
explicitly coordinates with. The actual defect is that D5 states a proposal (itself graded WEAK)
as an established fact and hangs a vendor purchase spec on it, constraining an undesigned
patient-path part from the wrong document. - The attack's own fix, "solid height <= 1.10 mm", is
pinned to the very datum it convicts the decision of using. I replaced it with a relation to
working_height_min. WHAT SURVIVES FROM THE ORIGINAL DECISION: the finding itself — K12 as
written is unbuyable, this is geometry and not sourcing, the only volume is the band above the
spigot, and the preload member must not become the conductor (which WH 3.1.1 had already ruled
out on its "spring is the conductor" line). That is kept. Everything numeric below it is
withdrawn.

**Reasoning.**

The decision's diagnosis is right and its prescription is not derivable. I confirmed the
geometry directly: hm04() gives bore Ø9.20 z 0-9.00, seat Ø6.80 z 9.00-13.50, gel port Ø2.50,
slot 3.20 wide z 11.70-14.30 cut right through, top fillet at 16.80; hm05b() gives body Ø9.10 x
8.60 and spigot Ø6.60 x 3.50, so spigot top z 12.10. A 0.10 mm radial annulus takes no coil, and
the 1.40 mm band above the spigot is the only free volume. That much is solid and is worth
issuing. Everything the decision built on top of it fails a check. The working heights need a
rest position for the carrier, and the feature that sets it — HM-04's circumferential bayonet
run — does not exist in any model; mech_gen.py, PARTS-EEG-019 OA-14 and WH-EEG-008 open item 22
all say so in as many words. The decision's own phrase "derived from the released solids" is
therefore false for the two numbers a vendor would actually quote against. My arithmetic against
D1's proposed run shows the error is not academic: the spring as specified would be 1.9 N at
rest, below its own floor. The form is wrong on physics I re-derived rather than accepted: OD
6.50 / ID 5.40 is a 1.20 diameter ratio on 0.55 mm of radial width, which is no disc spring, and
a single-turn wave washer at 7.5 N/mm needs 0.076 mm strip running at ~2,930 MPa at 6 N. The one
honest answer to "what form" is a multi-turn crest-to-crest wave spring, and that much can be
said today. The "hard rule" fails twice: its stated mechanism is wrong (dead-end stub, not a
parallel path), and its numbers do not enforce it (0.15-0.225 mm float against a 0.10 mm gap).
The hazard it names is real but different — galling of gold plating under the quarter-turn at
every service — and the hazard it does not name, a stainless preload member inside a gel volume,
is left unresolved by the fix and must be recorded as open rather than closed. Two safety items
make this more than a paperwork correction. Solid height set equal to minimum working height
lets a rigid metal stack transmit unbounded helmet force into the scalp for a 2 h session on a
patient-applied part. And nothing in ASM or SVC handles the spring at all, so under the crown-
and-leaf principle a dropped ring is a silent open electrode with a cup that still looks fitted
— precisely the failure WH 3.1.1 says the design exists to prevent. Finally the HM-04 re-cut
does not belong to this decision. The 0.40 mm at z 13.90-14.30 is contested by D1's leaf run, an
LED seat and two lead passages that ASM 4.3 already assumes, a dressed conductor exit, and the
HM-04A anchorage. It has to be allocated once on MECH-EEG-020 sheet 8, not claimed piecemeal by
a spring spec that calls it free.

**Confidence:** cannot-decide-here  |  **Blocks a build:** yes  |  **Signed off by:** Sequential, and the order matters. (1) The mechanical reviewer on MECH-EEG-020 sheet 8 first: the circumferential bayonet run — without it the rest and full-travel datums do not exist and no envelope can be quoted — together with the one-time allocation of the z 11.70-14.30 band across HM-04A's anchorage, the LED seat and its two lead passages, the dressed conductor exit and D1's leaf relief, plus a dimension for HM-05C so the no-gold relation becomes a number and a capture feature for the ring. (2) The safety reviewer: this is a patient-applied part, the solid-height bound is what keeps the force bounded, and "stainless preload member inside the gel volume" has to be signed as an accepted open item or designed out. (3) AVL-EEG-017 with a wave-spring maker (Smalley, Lee Spring, Gutekunst) against five measured samples on a printed HM-04/HM-05B pair, as K12 already requires, and only after (1). (4) ECO-EEG-016 to carry the change to WH-EEG-008 3.1.1's K12 row and to AVL K25/K26, since this contradicts a live proposal rather than silently overwriting it.

**What would change it.**

A drawn circumferential bayonet run on MECH-EEG-020 sheet 8 makes the whole envelope derivable
in an afternoon: it fixes spigot_top_z at both the retaining and the roof datum, and the
symbolic heights above become two numbers. A dimensioned HM-05C turns the no-gold relation into
a pair of limits. Five measured wave springs at the quoted rate either confirm 3-6 N over the
real stroke or show the stroke cannot be had at that rate in 316, in which case the seat roof
rises and the band is re-allocated with the LED rather than around it. A measured cup contact
force on a head form showing 3-6 N is the wrong target overturns the force, not the form. A
25-cycle R6 + IPA + paste run showing relaxation below 3 N or crevice pitting sends the line
from 316 to Elgiloy. And if no maker will quote a multi-turn wave spring at OD 6.50 / ID 5.40,
the fallback is the one WH 3.1.1 already names — a leaded cup with the joint in the frame
channel — which removes the spring from the electrical question entirely.

**Files this touches:** `docs/AVL-EEG-017_RevB_approved_vendor_list.md`, `docs/WH-EEG-008_RevB_harness_and_cable_assembly.md`, `docs/PARTS-EEG-019_RevB_part_identifier_register.md`, `docs/ASM-EEG-007_RevB_assembly_work_instructions.md`, `docs/SVC-EEG-013_RevB_service_and_refurbishment_manual.md`, `docs/ECO-EEG-016_RevB_change_control_and_document_register.md`, `KNOWN_ISSUES.txt`


---

# Blocks a build


## D2-FIX01-OUTLINE

**Question.** Can the FIX-01 board outline of 160.0 x 100.0 mm (section 1.9) hold its bill of materials, and what to do if it cannot?

**Decision.**

No, and neither can the 160.0 x 170.0 mm replacement. BOTH outlines are withdrawn. I opened the
one document both the decision and the attack deferred to — Omron's own G6K datasheet
(omronfs.omron.com/en_US/ecb/products/pdf/en-g6k.pdf, p.6). G6K-2F-Y: body 10.0 +/-0.2 x 6.5
+/-0.2 x 5.2 +/-0.2 mm; recommended land pattern 0.8 x 1.8 mm pads, four per row, outer centres
7.6 mm apart, rows 7.0 mm centre-to-centre. Copper extent 8.4 (X) x 8.8 (Y); part-plus-copper
extent 10.0 (X, body) x 8.8 (Y, copper) = 88.0 mm2 bare, ~98 mm2 at a 0.25 mm/side courtyard.
WHAT THAT SETTLES. 1. 160.0 x 100.0 mm is dead twice over. Fed into the package's own
area_budget(), the real relay puts FIX-01 at 69.0 % (bare) to 79.2 % (0.5 mm/side courtyard)
occupancy against its own 60 % limit — NOT FEASIBLE, not marginal. The generator's 70.7 mm2
ceiling and "THE MARGIN IS 1.0 %" were computed against an assumed 70.0 mm2 that is 26-57 % too
small. The decision's zoning proof (16 x 7.0 = 112 mm on a 100 mm board) was right, and the
datasheet independently confirms the verdict. 2. 160.0 x 170.0 mm is dead too, on the axis the
attack flagged. The decision's 9.0 mm row pitch against 8.8 mm of real copper leaves 0.2 mm
between adjacent rows — exactly the board's minimum clearance, with nothing at all for the
driven GUARD pour that rule (b) requires between rows, and less than the +/-0.1 mm land-pattern
tolerance. It is not buildable. 3. The width survives. Real body 10.0 mm into the decision's
12.0 mm cell leaves 2.0 mm; 5 x 12.0 + 4 x 3.0 + 3.0 = 75.0 mm row; 5 + 45 + 75 + 30 + 5 = 160.0
mm. "The width was right, the height was wrong" holds — the height was just more wrong than the
decision knew. ISSUE AT 160.0 x 200.0 mm, two-layer, same stack-up, finish and class. M3 NPTH at
(5,5), (155,5), (5,195), (155,195), 6 mm keep-out. - Row pitch 11.0 mm, relay cell 12.0 (X) x
11.0 (Y) mm: 2.0 mm X and 2.2 mm Y clear of the real land pattern. Floor is 10.5 mm (8.8 copper
+ 0.25/side courtyard + ~1.0 mm of rule-(b) guard channel); 16 x 11.0 = 176.0 mm + 12.0 mm end
bands = 200.0 mm. 200 is also a standard panel dimension — as 160 x 100 was, which is very
likely where the original single-Eurocard number came from rather than from any count. - Zones
tile the board, usable width in brackets: guarded x 0-50 [5-50, holding the 40 x 60 can at x
5-45, y 70-130], relay matrix and reference field x 50-125 [75], logic x 125-160 [usable 125-155
= 30.0 mm, with 155-160 edge and M3 keep-out margin]. One boundary, one number, everywhere. -
Occupancy at the real envelope 34.5 % (bare) to 39.6 % (0.5 mm/side); largest carryable envelope
186.4 mm2. - LAND-PATTERN RULE, now a measurement and not a permission: relay land pattern 10.0
x 8.8 mm, cell 12.0 x 11.0 mm max, long axis along X, courtyard included. Goes in
FIX-01_constraints.txt section 5. - Cost, section 6.1: PCB 5-off 32000/16000 x EUR 120 = EUR 240
(+120). Enclosure line: the EUR 35 uplift is WITHDRAWN as uncostable — see below. - Enclosure:
1590D withdrawn with the outline. Requirement pending a named part — internal floor >= 190 x 215
mm (>= 25 mm at the left end for the J101/J102 bulkhead BNC bodies, ~10 mm at the front for the
WH-KEY-01 shrouds, 5 mm elsewhere) with a written internal-height stack budget in the AVL K24
style (board 1.6 + standoff + 15 mm can + shroud and Pico headroom + lid clearance). This is now
an OPEN item in section 7, listed the way section 7 already lists the unchosen voice
preamplifier, not a closed one. - Exposure corrected: 46 h / EUR 2 530 of FIX-01 layout.

**What the attack changed.**

I checked all six attack points against the files. Five stand, one stands with a correction, and
one of them turned out to be far more serious than the attacker could show. CONCEDED — A, and it
is fatal rather than editorial. The attack said the decision re-creates the error it convicts
the package of: a 12.0 x 9.0 mm grid is a hard dimensional cap, so advertising 151.7 mm2 of
headroom and declaring "the datasheet risk disappears" is false. Correct — and the attack's
invented counter-example (12.6 x 8.4) guessed the wrong shape but the right axis. The real part
is 10.0 x 8.8. It passes the area test easily and breaks the 9.0 mm pitch with 0.2 mm to spare
against a 0.20 mm minimum clearance and a +/-0.1 mm tolerance. So I do not merely delete the
headroom sentence as the attack asked — I withdraw the 170.0 mm height it was attached to. The
attack's remedy (state the cap, keep the outline provisional) is superseded by simply opening
the datasheet, which is what it also offered as the alternative and which is an hour's work.
CONCEDED — B, and there is more. Verified: section 2.4 buys a Hammond 1590B for FIX-02, so "no
enclosure family beyond the 1590D is in this package" is false. Section 1.9's table puts
J101/J102 on the LEFT END PANEL, outside the outline, so board-plus-5-mm cannot hold them. AVL-
EEG-017 K24 is verbatim as cited — POD-P1 named with 163.0 x 143.0 x 58.0 external AND 158.0 x
138.0 x 55.5 internal, stack 2.5+6.0+1.6+18.0+3.0+18.0 = 49.1 against 55.5, margin 6.4 — so a
named part with real internals and an itemised stack is the package's own standard, and a bare
"at least 35 mm" is a regression. Section 7 does treat spec-only parts as open items. BEYOND THE
ATTACK: section 1.9's reassurance that "the Hammond 1590D enclosure is 188 x 119 mm inside"
misreads section 1.8's bare triple "188 x 119 x 37 mm" — a 37 mm-tall box cannot also be 37 mm
inside. That misreading is repeated in section 7, fixture_gen.py:846, FIX-01_constraints.txt:70
and README_fixture_pcb_data.txt:64. The "1590D has room for a larger board" fallback the whole
package leans on was never real, which strengthens the case for growing the board and kills the
EUR 35 estimate outright. CONCEDED — C. Confirmed by arithmetic on the decision's own text:
"logic x 125-160" is 35 mm, the same sentence calls it 30 mm, and 5+45+75+30+5 implies 125-155.
Same split for the guard band, 0-50 versus 5-50. Fixed by tiling the zones across the full board
and stating the usable width separately, which also matches the existing convention where the
released zones run 0..160. CONCEDED — D. Verified: 16000 - 7040 - 2400 = 6560 mm2 remains
against roughly 3300 mm2 of Pico, twelve ICs, resistors and connectors, so "nowhere to go" is
checkable and wrong; and at a 12 x 9 cell the 8 x 10 tiling is 96 x 90 mm and 90 + 13 = 103 >
100. The decision did silently use an 11 x 8 cell for the option it rejected and 12 x 9 for the
one it adopted. The rejection outcome survives on rule (b) — breaking each channel's relays away
from its own reference resistors lengthens the guarded low-level node — but the stated reason is
withdrawn. CONCEDED — E. Section 6.1 reads 8+4+8+20+6 = 46 h / EUR 2 530 for FIX-01 and 13+2 =
15 h for FIX-04, a separate 120 x 80 board. The 61 h in section 7 is the sum of both. Exposure
corrected. CONCEDED — F, and I reproduced it. I copied tools/ to a scratch directory and changed
only w, h and the four mount coordinates: the three zone tuples stayed at y 0..100 on a 170 mm
board, the can stayed at y 20..80, and every connector stayed in the bottom 100 mm, while the
silkscreen and zoning artwork bounds did scale (y to 165 and 168). So the re-issue is a data
edit — zones, can rect, CONNECTORS y-positions, mount coordinates — and then a regeneration,
exactly as the attack listed. KNOWN_ISSUES.txt:283 is stale verbatim as quoted ("ten
TPIC6B595s", "80 precision resistors" against the corrected eleven and 77). FOUND WHILE
CHECKING, neither party raised it: the released FIX-01_netlist.txt says "218 nets, 773 pins, 193
reference designators" while JIG-EEG-009 says 217 nets and 772 pins in three places (lines 592,
1282, 1369). Fix in the same pass. KEPT. The headline and its price direction. The attack
conceded them and the datasheet now proves them independently: 160.0 x 100.0 runs 69-79 %
occupancy at the real land pattern. The 160.0 mm width, the 12.0 mm X cell, the withdrawal of
the 1590D, and the rejection of both a two-board split and holding 160 x 100 all survive. What
does not survive is the specific 170.0 mm height, the 9.0 mm pitch, the "risk disappears" claim,
the EUR 35 enclosure line, the EUR 120 total and the 61 h figure.

**Reasoning.**

The decision, the attack and the package all deferred to one document — "settled by opening one
datasheet", "an hour's work". So I opened it rather than arguing around it, and it is decisive
in a way neither party anticipated. Everything I could verify from the files reproduced.
fixture_gen.py:137-141 gives RELAY_ENV_MM2 = 10.0*7.0, IC_SOIC20W_MM2 = 13.0*8.0, PICO_MM2 =
51.0*21.0; the zone tuples at :90-96 and constraints section 3 give GUARDED 0-40, MATRIX 40-150
"5 columns of 16 relays", LOGIC 150-160, all y 0..100. Running --check on the unmodified package
reproduces 83 relays, 77 resistors, 16 ICs, exactly 60 % occupancy, 70.7 mm2 and "THE MARGIN IS
1.0 %". Editing a scratch copy to 160 x 170 reproduces 35.1 % and 151.7 mm2 to the decimal, and
27200/16000 x 120 = 204.0. The direction was sound and the attack's reproduction was honest. The
decisive number is the axis, not the area. The package's whole test is an area test — 60 %
occupancy, "the largest relay land-pattern envelope the outline can carry is X mm2" — and the
decision's own best insight was that a strict row-and-column grid fails on geometry before it
fails on area. It then made precisely that mistake itself, setting a 9.0 mm pitch and claiming
the area headroom made the datasheet irrelevant. The real land pattern is 8.8 mm across that
pitch. At 160 x 170 the area test passes comfortably (40.6 %) and the board still cannot be laid
out. That is the same failure mode, one revision later, and it is why I withdrew the replacement
rather than patching its prose as the attack proposed. Note what the datasheet does to the
package's escape hatch. The generator prints, at 160 x 170, "the largest relay land-pattern
envelope the outline can carry is 151.7 mm2, roughly 14.7 x 10.3 mm". Had the outline been re-
issued as the decision wrote it, the regenerated constraints file would have shipped a written
permission for a 14.7 x 10.3 mm land pattern into a grid that physically caps at 12.0 x 9.0 — a
contradiction inside a released file that a layout contractor would find at placement, after the
46 h had been commissioned. That is the concrete harm the attack's point A was pointing at. On
the enclosure I went further than the attack. Its arithmetic assumed the package's "188 x 119 mm
inside", but section 1.8 gives 188 x 119 x 37 as a bare triple in the way a catalogue quotes an
external size, and 37 mm cannot be both outside and inside. So the reassurance repeated in five
places — section 1.9, section 7, fixture_gen.py:846, constraints:70, README:64 — that the 1590D
has room for a larger board rests on a dimension read as internal that cannot be internal. That
is independent of anything I fetched: it is provable from the package alone. It is also why I
refuse to carry a EUR 35 enclosure uplift. A 160 x 200 board needing roughly 190 x 215 mm of
internal floor is nowhere near the 1590 family, and the package's own standard (AVL K24 /
POD-P1) is a named part with external and internal dimensions and an itemised stack budget.
Naming that part is a purchasing action, not an engineering one, and it should be listed open
rather than guessed at EUR 35. On the one number I did not close: the 11.0 mm row pitch. Its
floor is derived — 8.8 mm of copper is measured, 0.25 mm/side is the IPC-7351 nominal gull-wing
courtyard, and rule (b) needs about 1.0 mm of channel and gap between rows — which puts the
floor at 10.5 mm and makes 9.0 mm impossible. Within that floor, 11.0 is a judgement that lands
the board on a standard 200 mm panel dimension; 12.0 would give 218 mm. I state it as the single
number the layout engineer confirms rather than presenting it as measured, because the courtyard
convention and the inter-row guard allowance are the two things this package has never written
down. Confidence is 'derived' rather than 'cannot-decide-here' because the missing measurement
is no longer missing: the vendor's own drawing is now in hand, every occupancy figure comes from
the package's own area_budget(), and the ripple list was reproduced by experiment rather than
asserted. It is not 'judgement' because the two load-bearing conclusions — both outlines
withdrawn, width 160.0 holds — follow from measured dimensions and the package's own arithmetic
with no discretion in them. Source for the land pattern:
https://omronfs.omron.com/en_US/ecb/products/pdf/en-g6k.pdf (Omron G6K series, "Dimensions",
G6K-2F-Y, Mounting Dimensions TOP VIEW, tolerance +/-0.1 mm). It must be attached to the package
and cited from section 1.8, so that the next revision argues from the drawing instead of from an
assumption — that is the durable fix here, more than any single outline number.

**Confidence:** derived  |  **Blocks a build:** yes  |  **Signed off by:** The FIX-01 fixture design owner for JIG-EEG-009 signs the outline, the zoning and the withdrawal of the Hammond 1590D, with the change raised through ECO-EEG-016 because released artwork (Edge_Cuts, Zoning, NPTH, silkscreen), a released constraints file and two cost lines in section 6.1 are being re-cut. The layout engineer who takes the 46 h confirms the 11.0 mm row pitch against their courtyard convention and the rule-(b) guard channel before the outline is frozen — that is the one number this decision hands over rather than fixes. Purchasing names the replacement enclosure part and returns its real internal dimensions, at which point the section 6.1 enclosure line can be costed and section 7's new open item closed. No safety engineer is required: FIX-01 is a bench fixture, it carries no patient-applied part, and the 500 V DC work is on FIX-04, which this decision does not touch.

**What would change it.**

The row pitch is the live number. Below a 10.5 mm floor nothing is buildable (8.8 mm of copper
plus courtyard plus the rule-(b) guard channel); at 11.0 mm the board is 200.0 mm tall, at 12.0
mm it is 218.0 mm. A layout engineer who states a courtyard convention and an inter-row guard
allowance settles the height in one line, and the width and the 12.0 mm X cell do not move with
it. If purchasing cannot find an enclosure with roughly 190 x 215 mm of internal floor at an
acceptable price, the decision inverts into a two-board FIX-01 and must be re-taken from the
top, not fudged — that trade was rejected here on a EUR 120 delta which is now EUR 240 plus an
uncosted box, so the balance has genuinely shifted and the earlier rejection should not be
treated as settled. If the fitted relay is ever changed from the G6K-2F-Y, every number above is
void: they are all derived from that one land pattern, and the package should carry the drawing
so the next reviewer can see that at a glance. Finally, if anyone proposes reverting to 160 x
100 on the grounds that the area budget once passed: it passed only against an assumed 70.0 mm2
envelope that the vendor drawing shows is 26-57 % too small. At the real part the same generator
returns NOT FEASIBLE.

**Files this touches:** `tools/fixture_gen.py`, `docs/JIG-EEG-009_RevB_test_fixture_design.md`, `fixtures/pcb/FIX-01/FIX-01_constraints.txt`, `fixtures/pcb/FIX-01/FIX-01-Edge_Cuts.gbr`, `fixtures/pcb/FIX-01/FIX-01-NPTH.drl`, `fixtures/pcb/FIX-01/FIX-01-Zoning.gbr`, `fixtures/pcb/FIX-01/FIX-01-F_Silkscreen.gbr`, `fixtures/pcb/FIX-01/README_fixture_pcb_data.txt`, `fixtures/MANIFEST.json`, `KNOWN_ISSUES.txt`, `docs/ECO-EEG-016_RevB_change_control_and_document_register.md`


## D3-CAL-COMMUTATOR

**Question.** Contact assignment of K101 and K102, and does U3 have to float (JIG-EEG-009 section 1.2 / section 8.8: the one thing to settle before schematic capture)?

**Decision.**

Yes, U3 floats, and the released commutator is a build-blocker that must be replaced before
capture. The contact assignment and the floating requirement stand exactly as decided; five
things are added or corrected around them, and one of them is itself a blocker. 1. CONTACT
ASSIGNMENT (unchanged, now recorded as a ruling against a named rival). K101, both poles
paralleled, is the CAL_HI selector: C1,C2 -> CAL_HI; NC1,NC2 -> REF_HI; NO1,NO2 -> REF_LO. K102,
both poles paralleled, is the return selector: C1,C2 -> FIX_COM; NC1,NC2 -> REF_LO; NO1,NO2 ->
REF_HI. POL A = both de-energised = CAL_HI - FIX_COM = +5.0000 V. POL B = both energised =
-5.0000 V. One coil only = 0.000 V with one reference leg left open: no short across U3. The
rival that must be recorded as rejected is NOT the one the decision listed. It is two
IDENTICALLY wired paralleled crossovers (K101.C1 = K102.C1 = REF_HI, K101.C2 = K102.C2 = REF_LO,
NC1/NO2 -> CAL_HI, NC2/NO1 -> FIX_COM). It delivers the same +/-5 V and the same halved contact
resistance, and it is what the fix_m1.c cmd_pol comment actually describes, because under it a
half-driven pair genuinely shorts U3. It is rejected because of that: 100 mOhm contacts across
an ADR4550 on a single-coil failure, versus a benign 0 V. Record the reason; do not present the
firmware comment as agreeing with the chosen assignment, because it does not. 2. U3 FLOATS
(unchanged). Delete U3.GND from FIX_COM and U3.VIN from V5. U3.GND -> REF_LO. VIN from an
isolated DC-DC off J107 whose secondary return bonds to REF_LO and to nothing else. 3. NEW AND
BLOCKING - U1 AND U2 NEED A NEGATIVE RAIL, in the same edit. Add net V5N = -5.0 V +/-5 %,
referenced to FIX_COM (this rail does NOT float; it is the amplifier supply for a FIX_COM-
referenced divider). Move U1.VS- and U2.VS- off FIX_COM onto V5N; VS+ stays on V5. Source: a
regulated inverting supply (isolated 5 V -> +/-5 V module or regulated inverting charge pump),
placed outside the can. Without this, polarity B puts SRC_MID at -50 mV and U1's output cannot
follow below its own negative rail: GRD_DRV clamps at ~0, SRC_LO comes out near 0 instead of
-5.000 mV, and the +/- substitution silently returns about half the A-minus-B differential while
polarity A looks perfect. FIX-01 then has three domains and section 1.2 must say so: V5/FIX_COM
for logic and coils, +/-5 V about FIX_COM for U1/U2, and the floating domain for U3. 4. K103
SENSE FLIPPED to match the firmware: K103.NO1 = CAL_HI, K103.NC1 = GEN_IN (energised = CAL, per
fix_m1.c:206). This settles the netlist-versus-firmware contradiction in the safe direction,
keeps the permanently live CAL_HI on an open contact inside the can, and preserves section 8.4's
"SRC, source OFF = 3300 x 18 / 10018 = 5.9 mV" row. Then either add K104 in series with SRC_HI
for a genuine three-position OFF, or re-word section 8.3 from "every relay open, no source
connected" to "every relay open, the calibration reference disconnected, generator input
selected". K103's second pole cannot do this job - both poles follow one coil. 5. ISOLATED
SUPPLY, PROPERLY SPECIFIED. Regulated output, 9.0 V nominal (6-9 V band, final value once the
ADR4550BRZ minimum input is read), >= 1 kV isolation, barrier capacitance <= 20 pF, >= 0.25 W.
The barrier capacitance is the load-bearing number, not the voltage rating: REF_LO is a
measurement node and the module's dV/dt couples into it. Pi filter on the SECONDARY (mandatory;
a primary-side filter is optional and does not protect U3). Module placed OUTSIDE the can in the
relay-matrix zone, secondary entering through feedthrough capacitors. If an unregulated module
is used, preload it to its stated minimum load and put the preload outside the can - U3 draws
~1.5 mA, ~1.7 % of a 1 W module, and an unloaded unregulated module can rise toward twice
nominal. 6. U3.GND_SENSE IS DELETED. The netlist currently asserts two ground pins on two
different nets. The package's own rule (netlist header, section 8.8) forbids inventing pinouts
and the ADR4550BRZ datasheet is not in this package. Capture resolves it; if the part has one
ground pin, the net carries U3.GND on REF_LO alone. Decoupling is a separate, package-wide gap -
the netlist carries no capacitors for any device - and is not a reason to hold this ruling. 7.
SECTION 1.2/1.3 TEXT. State the reason for the reversal that survives arithmetic: the +/- DC
substitution cancels the DUT's own input offset and its bias-current offset at constant source
impedance, so the F-18 absolute-gain constant that section 1.1 says FIX-01 produces from the
internal DC substitution source is offset-free. Reprint the RSS: the ten terms sum to 2.658e-4,
giving 0.0163 % 1 sigma and 0.0326 % expanded, TUR 15.3:1 (not 2.558e-4 / 0.0160 / 0.0320 /
15.6:1). Fix section 1.9's "217 nets and 772 pins" to 218 and 773.

**What the attack changed.**

CONCEDED, and one of these is decisive. (a) The rails. Verified at FIX-01_netlist.txt lines 289,
300, 771, 782: U1.VS- and U2.VS- are on FIX_COM, VS+ on V5. Polarity B needs GRD_DRV at -50 mV,
which a 0-5 V op-amp cannot produce. This is derived, not arguable, and it means the decision as
written did NOT close the section 7 / section 8.8 item: settling K101/K102 alone does not
unblock capture. V5N is now part of the ruling. (b) The justification. The 0.0020 % row is the
residual AFTER differencing; undifferenced it is 1 uV / 5 mV = 0.02 %. I re-ran the RSS:
6.618e-4, 0.0257 % 1 sigma, 0.0515 % expanded, TUR 9.7:1 - inside the programme's 0.100 % rule
by 1.9x. So the budget does NOT force the reversal, and the decision's central "the budget takes
credit for it" argument is wrong. The reason was restated as DUT offset and bias-current
cancellation. By-catch confirmed: the printed RSS sum 2.558e-4 should be 2.658e-4, and section
1.9's net/pin counts disagree with the netlist header. (c) The safe state. Confirmed: putting
CAL_HI on K101's commons makes the reference live in every state, and with the released K103
(NC1 = CAL_HI) the divider input sits at +5.0000 V at power-up, so section 8.3's "no source
connected" becomes false and section 8.4's 5.9 mV row becomes 10.9 mV. The decision destroyed
that property without noticing. Fixed by flipping K103 rather than by hand-waving. (d) The
firmware comment, the supply spec, U3.GND_SENSE and the area pressure: all conceded and all now
carry values. KEPT, because the attack did not break them: the contact assignment (the attack
concedes it gives +5 / -5 / 0 / 0), the floating requirement, and the finding that the released
netlist is a build-blocker - I re-derived the short in both states directly from the file rather
than taking either party's word. REJECTED - the attack is wrong twice. (1) It says the cmd_pol
comment "describes the released broken netlist". It does not: the released netlist shorts the
reference in BOTH states, so a half-driven pair is not a distinct failure there. The comment
describes a coherent THIRD assignment - K101 and K102 wired identically as paralleled crossovers
- which neither the decision nor the attack names, and under which a half-driven pair really
does short U3. That makes the comment evidence of a design intent that must be explicitly
overruled in the rulings register, not a mistake to be silently rewritten. (2) Its remedy 3,
"use K103's second pole to break the CAL leg when K103 is released", is unbuildable: both poles
follow one coil, so pole 2 cannot open while pole 1 selects CAL. Only its parenthetical "add a
fourth relay" works, and the cheaper fix is the K103 flip. FOUND INDEPENDENTLY, neither party
has it. (i) The attack's proposal to put the isolated module in the LOGIC zone is unavailable: x
150-160 is 1000 mm2 and the constraints file already assigns it 11 TPIC6B595 (~1144 mm2), U20
(~104 mm2) and the Pico (1071 mm2) - over-subscribed 2.3x before this edit. The zoning, not just
the 60 % board figure, is what fails; the outline is already flagged provisional in section 1.9
and the 1590D has room, so the module does not decide the outline. It goes in the relay-matrix
zone. (ii) Section 1.1 says FIX-01 produces the F-18 absolute-gain constant "from an internal DC
substitution source, not from the generator", while T7's procedure prints a 10 Hz sine from the
function generator. That contradiction has to be resolved in the same ECO, because it decides
whether the broken polarity B corrupts F-18 at all. (iii) The isolated module's barrier
CAPACITANCE, not its voltage rating, is the specification that protects REF_LO.

**Reasoning.**

The commutator answer is derivable from the released files and I re-derived it rather than
accepting either party's account. K101.C1/C2 on REF_HI with NC1 on REF_LO closes REF_HI onto
REF_LO de-energised; energised, K101.NO1/K102.NO2 tie them again through CAL_HI and
K101.NO2/K102.NO1 tie them through FIX_COM. No state delivers 5 V, so section 1.12 step 4 ("U3
reference re-measured, +/-0.005 %") could never pass on the released design. Build-blocker, not
a topology preference. The decision's assignment is the right one and is slightly better than
its nearest rival. Both give CAL_HI - FIX_COM = +5 V de-energised and -5 V energised with two
contacts in the loop and both poles paralleled at 50 mOhm each, so contact resistance is
identical; the split assignment differs only on the single-coil failure, where it gives 0 V with
a reference leg open instead of a hard short across the ADR4550. That is worth choosing and
worth writing down. The section 1.3 design rule survives either way: K102's 100 mOhm sits in
series with the 0.5 mA source current, 50 uV on 5 V, and the J102 monitor (J102H.1 = SRC_HI,
J102H.2 = FIX_COM) measures the divider input downstream of it, outside the calibrated ratio.
Floating is forced by the same topology. In polarity B K102 connects REF_LO to FIX_COM's
counterpart REF_HI, so a hard-tied U3 ground would short the divider input to common through the
reference's ground pin. Nothing in the attack touches that. What the attack broke is the claim
that this ruling closes the item. The rails do not support the function being ruled on: to
deliver -5 mV to a FIX_COM-referenced DUT, some element must swing below FIX_COM, and the only
element that can is U1's output. Moving the commutator downstream is not available either - a
contact in the A2 legs is a 100 mOhm in 20 Ohm error, 0.5 %, which section 1.3 forbids by name.
So V5N is not an improvement, it is a precondition, and it belongs in this edit. The budget
argument the decision leaned on does not survive its own arithmetic, and I checked that by re-
running the table. That matters practically: a reviewer who redoes the RSS and finds 9.7:1
without the reversal will delete K101/K102 and the isolated supply, and the decision gives them
no answer. The answer that holds is DUT offset and bias-current cancellation at constant source
impedance - the SHORT position cannot substitute for it because it changes the source impedance
from 18 Ohm to 0. The safe-state regression is real and is the kind of thing that gets
discovered on a bench at 2 a.m. Flipping K103 to agree with fix_m1.c fixes three things at once
- the documented contradiction, the power-up state, and section 8.4's readback row - which is
why I chose it over the attack's version. I did not invent the two datasheet numbers the package
does not carry. The ADR4550BRZ minimum input and pin list, and the G6K-2F-Y land pattern, stay
open and are named as such.

**Confidence:** judgement  |  **Blocks a build:** yes  |  **Signed off by:** The FIX-01 fixture designer / schematic owner signs the netlist change (assignment, V5N, K103 sense, U3 floating domain). TST-EEG-004's owner co-signs, because the change decides how the F-18 absolute-gain constant is produced and rewrites the section 1.3 uncertainty budget and its TUR. The CM quality manager signs the section 5.2 calibration-schedule consequence (U3 and the A1/U1/A2 ratios are now measured in two polarities on a three-domain fixture). Raised as an ECO under ECO-EEG-016 with the assignment and the K103 sense recorded in RUL-EEG-021. Section 7 also records that no safety engineer has reviewed FIX-01; adding two isolated supplies and a negative rail is the point at which that review should happen.

**What would change it.**

1. The ADR4550BRZ datasheet. Its minimum input voltage sets the isolated secondary (a lower,
quieter 6 V is preferable if it is met); its pin list settles whether GND_SENSE exists. Neither
is in this package. 2. A programme decision to drop polarity reversal. That is a legitimate
build and the arithmetic supports it: delete K101 and K102, ground U3 to FIX_COM, feed it from a
non-isolated 9-12 V, delete V5N and the isolated module, and reprint section 1.3 with the
thermal-EMF row at 0.02 % - 0.0257 % 1 sigma, 0.0515 % expanded, TUR 9.7:1, still 1.9x inside
the 0.100 % rule. It costs two relays, three U22 outputs, the POL verb, the isolated supply, the
bipolar rail and the can crowding, and it loses DUT offset and bias-current cancellation in the
F-18 substitution. This is the one choice I would not make alone, and it must be made in writing
before capture. 3. Resolution of the section 1.1 / T7 contradiction. If T7's 10 Hz generator
sine, not the DC substitution, is what actually produces the F-18 constant, the consequence of a
broken polarity B shrinks to the fixture's own shift-start checks and the cost/benefit in item 2
shifts toward deleting the reversal. 4. The Omron G6K-2F-Y land pattern. It governs whether
160.0 x 100.0 mm closes at all, and the LOGIC zone is already over-subscribed 2.3x, so the
outline is likely to be re-cut regardless of this ruling. 5. A measurement on a built board.
Nothing in FIX-01 has been built, and section 7 says so.

**Files this touches:** `tools/fixture_gen.py`, `fixtures/pcb/FIX-01/FIX-01_netlist.txt`, `fixtures/pcb/FIX-01/FIX-01_netlist.json`, `fixtures/pcb/FIX-01/FIX-01_constraints.txt`, `fixtures/firmware/src/fix_m1.c`, `docs/JIG-EEG-009_RevB_test_fixture_design.md`, `docs/TST-EEG-004_RevC_production_test_specification.md`, `docs/RUL-EEG-021_RevA_rulings_register.md`, `docs/ECO-EEG-016_RevB_change_control_and_document_register.md`, `KNOWN_ISSUES.txt`


## MECH-D1

**Question.** What vendor part sits behind every line of mech/HARDWARE_SCHEDULE.md (H-1 to H-9), so a purchase order can be raised against the released POD-P1 geometry?

**Decision.**

The engineering stands; the closure strategy and two numbers change. Rule I am applying
uniformly, which is what §4 actually asks for: a line closes on a STANDARD (the standard is the
datasheet) or on a datasheet held on file — never on a distributor part number alone. CLOSED ON
A STANDARD (purchasable today, Class C, CoC + lot codes per AVL §9): - H-3: ISO 7045 (DIN 7985)
M3 x 12, A2-70, cross recess H, 4/pod. Head dk 5.6 clears the Ø3.40 lid hole and sits inside the
Ø8.00 boss footprint. 0.60 N.m, diagonal, two passes. - H-3a (NEW ROW): ISO 7089 form A M3, A2,
Ø7.0 x 0.5 mm plain washer, 4/pod. Bearing area goes 15.55 -> 29.40 mm2, so 43-64 MPa becomes
23-34 MPa at the 667-1000 N preload. - H-5: ISO 7045 M3 x 6, PA6.6 natural, 4/pod (not 8). -
H-6: unchanged; ASM-EEG-007 §3.3 owns it. - H-9 (POD-P1-03): silicone VMQ O-cord Ø1.50 +/-0.08,
60 +/-5 Shore A, bought by the metre, 1 m/pod, cut 602.0 mm, butt-bonded with a Loctite
406-class cyanoacrylate. OPEN WITH CRITERIA — dimensions fixed and final, vendor NOT closed: -
H-1 (H-2 merged into it): ONE M3 brass thermal insert, 8/pod. Maker's recommended hole Ø4.00 mm
— this is the acceptance criterion that actually pins the choice, not OD alone; OD 4.60 mm (hard
max 5.00 by the 1.5 mm boss-wall rule); length 5.70 mm; knurled with undercut. Datasheet,
installation data (tip temperature, set depth, blind-hole displacement allowance) and CoC per
lot ON FILE before the line closes — on the specified part, not only on an alternate. ruthex
RX-M3x5.7 is a candidate to evaluate, NOT the specified part; it is a maker-channel brand with
no distributor line and no per-lot CoC, and closing on it would be exactly what §4 forbids. -
H-4: M3 x 18 mm hex spacer, MALE-FEMALE, PA6.6, body 18.00 mm, stud 6 mm (window 4.6-7.1,
engaging 4.40 mm), A/F 5.5 mm, 4/pod. No vendor. Carries a PROHIBITION line: AVL-EEG-017 §1.6's
Würth 970200321 / Mouser 710-970200321 is the FEMALE-FEMALE part and must not be ordered against
this line. Decided jointly by AVL and the safety reviewer, per §4, because SR-08 creepage rests
on the material. - H-7: M3 x 8 thread-forming screw for plastics, 30-degree or trilobular, steel
or A2, 2/pod, into the printed Ø2.50 pilot, ~0.3 N.m. EJOT DELTA PT 30 x 8 named as the
candidate class; proprietary thread form, so it closes on a datasheet, not on a catalogue
number. GEOMETRY (three generator edits, not one): - FLOOR_INSERT_DEPTH 5.50 -> 6.30 (not 6.20):
5.70 insert + 0.30 set-below-flush that ASM §5.1 item 1 expressly permits + 0.30 displacement.
floor_under = 2.20 mm, so the >= 2.0 assert at mech_gen.py:362 still passes; boss_wall stays
2.00. - The H-1 allowance term splits into two named constants (set-below 0.30 + displacement
0.30) so H-1 regenerates as "insert length at most 5.7 mm" — naming the bought part exactly
instead of licensing a 5.9 and reopening the two-length ambiguity. - WASHER_T = 0.5 added and
used: lid_engage = 12.0 - 6.0 - 0.2 - 0.5 = 5.30 mm, all inside a 5.70 insert, tip 1.70 mm clear
of the 7.00 bore. SEQUENCING, and this is the load-bearing part: this is POD-P1-01 Rev C under
ECO-EEG-016, not a regenerate. New STL/STEP, new sha256, volume ~144.38 cm3. DO NOT RELEASE THE
INSERT PO UNTIL THE RE-RELEASE IS ON FILE. Sheet 18's first-article insert pull-out at 0.60 N.m
stays open verbatim.

**What the attack changed.**

I checked all six and the minor. Five land, one is half right, and the spine survives. CONCEDED
IN FULL: (1) 6.20 is wrong. ASM-EEG-007 line 861 says "flush to 0.3 mm below it", so a 5.70
insert can bottom 6.00 mm down, leaving 0.20 mm — under the 0.30 the schedule's own H-1 formula
assumes. 6.30. And 6.20 regenerates H-1 as "at most 5.9 mm", re-licensing the second length the
whole decision exists to kill. My "5.70 + 0.50 of allowance" was only true if the insert is set
dead flush, which the ASM does not require. (2) "One constant, one regenerate" was false and I
own it. mech_gen.py:2250 is lid_engage = 12.0 - lid_stack - lid_gap = 5.80, with no washer term.
I did the 5.30 arithmetic in my reasoning and then never put it in the generator. Ship my change
as written and HARDWARE_SCHEDULE.md — generated, hand-editing forbidden — regenerates demanding
a 5.8-6.7 mm insert while the PO buys 5.70. Goods-in rejects the part I specified. Confirmed
stale too: mech_drawings.py:55 "D4.0 x 5.5 mm", mech_drawings.py:99 "6.0 mm into the brass
insert", ASM line 850 "5.50 mm deep in the floor bosses" in .md/.docx/.pdf. (3) It is an ECO on
a released part. MANIFEST.json carries POD-P1-01 Rev B, 144.42 cm3, sha e11302a8… (STL) /
aed60513… (STEP); PARTS-EEG-019 quotes 144.42 at §2.2 line 274, §6 line 668 as a CLOSED cross-
document audit item, and §7 line 715; AVL K24 quotes the bureau against those files. 4 x π/4 x
4.0^2 x 0.80 = 40.2 mm3, so both SHAs and the volume move. Raising the insert PO before the re-
release lands 5.70 inserts against 5.50 bores — the mixed-length failure wearing a different
hat. (5) The H-4 vendor pointer was actively dangerous. AVL §1.6 line 305 is "M3 x 18 mm nylon
hex, FEMALE-FEMALE, Würth 970200321, Mouser 710-970200321" — the exact part §3 of the schedule
says cannot be used. "Wuerth, the family already approved on §1.6" walks a buyer to the wrong
part. Prohibition line added. My "cannot be decoded under one rule" rationale is dropped: no
Würth catalogue is in the package, so the honest reason is that none was read. (6) H-1 was
closed the way §4 forbids. §4's preamble: "none of them may be closed by picking a part number
off a distributor's site without checking the criteria against its datasheet." There is no
insert datasheet in docs/ and no "ruthex" string anywhere in the package. My validation was
circular — the part matched to mech_gen.py:249's comment, and that comment cited back as
validation, when the comment itself says "the exact figure is the insert maker's and is settled
at first article". CoC moved onto the specified part. Recommended hole Ø4.00 promoted to the
acceptance criterion, because industrial knurled inserts at OD 4.7-4.8 want ~4.3 and are not
drop-in — "any insert to the same three dimensions" was a narrower set than it sounded. MINOR:
conceded. MH = [(5,5),(145,5),(5,125),(145,125)] at mech_gen.py:67, and ICD-EEG-006 line 863
reads "MP-01 is non-conductive and carries no earthed plate, no metal standoffs and no metal
screws left of x = 62 mm" — the subject is MP-01, and the stated reason is a conductive plate 18
mm above high-impedance nodes. Brass inserts in pod floor bosses sit below the carrier. My
blanket rejection banned my own H-1. Rescoped. CONCEDED IN SUBSTANCE, NOT AS ARGUED: (4) The
attack is right that I dropped sheet 18's open item — mech_drawings.py:69 does say "0.60 N.m is
itself at the top of what a 5.7 mm insert in PA12 will hold, so first article measures pull-out
or the torque comes down" — and right that the washer does not reduce demand on that interface.
It is NOT established that the washer lowers K. Adding it replaces steel-on-PA12 with steel-on-
steel at the head (μ comparable, not clearly lower) while pushing the plastic-bearing interface
out to a larger mean radius, which pushes K the other way; whichever branch slips first decides,
and neither is measured. The firmer version, which the attack missed: the washer costs 0.50 mm
of penetration, so engaged insert thread at the ASM's worst-case set depth goes 5.50 -> 5.00 mm
at unchanged-or-higher preload. That is a real ~9 % cut in engagement on the joint the drawing
already calls marginal. So: FA pull-out stays open verbatim and the cost is stated. WHAT I KEPT:
one insert not two, deepened floor bore, the washer, male-female nylon standoff, four M3x6,
thread-forming P-clip screw, 602.0 mm cord. The attack conceded all of it. The washer earns its
place twice, and the attack's own concession proves the second: without it the released schedule
demands a >=5.8 insert at the lid, which forces a second length back into the pod. Rejecting the
washer means re-opening the merge.

**Reasoning.**

The attack's central service was showing that my answer was a document change I had described as
a constant change. Three of the six generator/prose edits I needed were invisible to me, and one
of them (lid_engage with no washer term) would have produced a released, do-not-hand-edit
schedule that rejects at goods-in the exact part the PO buys. That is a worse failure than the
one I was fixing, because it looks like everything worked until a box of inserts is on the
bench. On 6.30 over 6.20: the whole argument for one insert is that a single named length is
unambiguous. 6.20 regenerates the H-1 criterion as "at most 5.9 mm", which is an invitation to
buy a 5.9 for the floor and a 5.7 for the lid — precisely the two-length hazard I rejected. 6.30
with the allowance split into its two real terms regenerates as "at most 5.7 mm" and the
document then names the part it buys. It costs 0.10 mm of floor margin (2.20 against the >= 2.0
assert) and buys the unambiguity the decision exists for. Worth it. On leaving H-1 and H-4 open:
my brief was to put a vendor part behind every line, and I have not done that for two of nine. I
am choosing that deliberately rather than filling the box. §4 is not a formality here — it says
the criteria are what the released geometry can accept, and for the insert the governing
criterion is the maker's own recommended hole and blind-hole allowance, which is the number 6.30
is computed from. Closing that line on a brand with no datasheet in the package would make the
bore depth rest on an assumption I had just dressed up as a part number. The dimensional
engineering is decided and is the part that was actually missing; the vendor closure is a
bounded, named procurement action with an owner, not an unknown. On the ECO: this is the one
item that can still cause the damage the decision was written to prevent. Rev B floor bores at
5.50 physically cannot take the 5.70 insert every other document in the package assumes, so the
geometry itself is wrong, not merely under-specified — KNOWN_ISSUES line 237 already says the
eight Ø4.00 bores "hold no thread at all". Nothing has been printed, so this is caught in time,
but only if the PO waits for the re-release.

**Confidence:** judgement  |  **Blocks a build:** yes  |  **Signed off by:** Three signatures, and they are not interchangeable. (1) Mechanical design owner plus the ECO-EEG-016 change board, for POD-P1-01 Rev B -> Rev C: regenerated STL/STEP, new sha256 and volume in mech/MANIFEST.json, and the reopening of PARTS-EEG-019 §6's closed cross-document item at 144.42 cm3. A released model is being re-cut and a bureau (AVL K24) is quoted against the old files. (2) AVL-EEG-017 owner / buyer, for H-1 and H-7, on the insert maker's datasheet, installation data and CoC per lot being on file before either line closes. (3) AVL-EEG-017 owner AND the safety reviewer together for H-4, which is what §4 already assigns, because RISK-EEG-011 SR-08's creepage rests on the standoff material. QP-EEG-010's quality owner books the first-article insert pull-out at 0.60 N.m as an FA acceptance item.

**What would change it.**

Three first-article measurements, each safe-if-wrong in the direction chosen. (a) The chosen
insert maker's stated blind-hole displacement allowance and recommended hole. 6.30 assumes 0.30
displacement on top of the ASM's 0.30 set-below-flush. If displacement exceeds 0.50 the insert
must SHORTEN, not the bore deepen — at 6.30 only 0.20 mm of margin remains before the
floor_under >= 2.0 assert bites. If the maker's recommended hole is not Ø4.00, the part is out
regardless of its OD. (b) MJF PA12 compressive yield on a coupon or FIT-01: above ~65 MPa the
washer is optional — but dropping H-3a returns lid_engage to 5.80 and re-imposes a >= 5.8 mm
insert at the lid, which reopens the H-1/H-2 merge. The washer and the single insert stand or
fall together; that coupling was not visible before the attack. (c) First-article insert pull-
out at 0.60 N.m per sheet 18. If it fails, the remedy is the drawing's own — the torque comes
down — which also relieves the bearing case and may retire H-3a. Measured torque coefficient K
above ~0.35 would likewise make the bare head acceptable.

**Files this touches:** `tools/mech_gen.py`, `tools/mech_drawings.py`, `mech/HARDWARE_SCHEDULE.md`, `mech/MANIFEST.json`, `mech/MECH_RELEASE_STATUS.md`, `mech/stl/POD-P1_prototype_enclosure_base.stl`, `mech/step/POD-P1_prototype_enclosure_base.step`, `mech/drawings/MECH-EEG-020_RevA_printed_part_drawings.pdf`, `docs/ASM-EEG-007_RevB_assembly_work_instructions.md`, `docs/ASM-EEG-007_RevB_assembly_work_instructions.docx`, `docs/ASM-EEG-007_RevB_assembly_work_instructions.pdf`, `docs/AVL-EEG-017_RevB_approved_vendor_list.md`, `docs/PARTS-EEG-019_RevB_part_identifier_register.md`, `docs/ECO-EEG-016_RevB_change_control_and_document_register.md`, `docs/EEG_kit_BOM_for_bidders_RevC.xlsx`, `docs/EEG_kit_BOM_INTERNAL_RevC_costed.xlsx`, `KNOWN_ISSUES.txt`


## MECH-D5

**Question.** What identifiers do the new items take under PARTS-EEG-019 numbering — the entry plate, the glands, and the fastener lines?

**Decision.**

HM-12 is CONFIRMED for the occipital umbilical entry plate. §1.2 is re-cut to "HM-13 to HM-19
reserved for Phase 2" — ONE number taken, not two. POD-P1-06 is ISSUED for the harness-entry
cable gland, ONE part, 4 per kit, two at each end of the two umbilicals. HM-13 is NOT issued
today. POD-P1-05 stays withdrawn and its number is not reused. NO FASTENER GETS A PART
IDENTIFIER. §1.3 rule 4 is re-cut, but with a CLASS exclusion, not a geometric test. New
wording: "Bought-in catalogue items get no identifier unless (a) the programme modifies them, or
(b) they mate with a printed part of this programme — a dedicated carrier or adapter, or a seat,
bore, groove or anchorage cut into a printed part for them. Standard threaded fastening hardware
is excluded by class whatever printed feature receives it: screws, nuts, washers, threaded
inserts, standoffs, and their pilots, insert bores and clearance holes. The ear-reference
coupler, the Harwin M20 housings and the JST PHR-2 mate with nothing printed and fall outside
limb (b) as well (OA-16)." AVL-EEG-017 §4 new lines, SIX of them, K47 to K52 (K46 verified as
the highest issued), all OPEN WITH CRITERIA, no distributor part numbers: K47 M3 brass heat-set
insert, floor bosses (H-1), 4/pod — 4.00 mm recommended hole, overall length at most 5.20 mm, OD
at most 5.00 mm. K48 M3 brass heat-set insert, lid bosses (H-2), 4/pod — same hole, length 5.8
to 6.7 mm. K49 M3 x 12 A2 pan screw (H-3), 4/pod — pan or cheese head under a 3.40 mm clearance
hole, head OD clearing the 8.00 mm boss footprint. NO WASHER under this head. K50 M3 x 8 thread-
forming screw for plastics (H-7), 2/pod — for a 2.50 mm pilot in PA12, 30-degree or trilobular,
A2 or steel. K51 cable gland M12 x 1.5 = POD-P1-06 (H-8/H-10), 4/kit — clamping 3.0 to 6.5 mm;
panel range covering 3.50 and 4.40 mm; locknut at most 17.00 mm across flats; at least IP54;
retention at least 15 N; polyamide. K52 silicone O-cord 1.5 mm 60 Shore A, 602.0 mm cut =
POD-P1-03, 1/pod. No washer line is issued at all. K24 GAINS HM-12, or the print bureau is not
quoted for it. AVL §1.6 "Carrier-to-plate standoff" and kit BOM item 31 are corrected to male-
female with FOUR M3 x 6 nylon screws — description AND the Würth 970200321 / Mouser
710-970200321 MPN, which is a female-female part — and the line reverts to OPEN WITH CRITERIA.
The correction is written into tools/RULINGS.md FIRST, then RUL-EEG-021 is regenerated. The
18.00 mm body is unchanged, so RISK-EEG-011 SR-08's creepage and the 49.1 mm stack budget are
untouched. PARTS-EEG-019:278 and SVC-EEG-013:593 are corrected: two gland features DO exist in
POD-P1-01 and they are not POD-P1-05. MARKING: HM-12 gains its row and is engraved "HM-12 A" per
§4.1, on the exposed downward face between the two Ø22 seats. That re-cuts a released model.

**What the attack changed.**

CONCEDED, all verified against the files: (3) K47 cannot be one insert line.
HARDWARE_SCHEDULE.md:31-32 gives H-1 "at most 5.2 mm" and H-2 "5.8 to 6.7 mm" — disjoint — and
§3 says "A 5.7 mm insert ... does not fit this bore." §4 carries them as two OPEN WITH CRITERIA
rows. Split into K47/K48; everything after shifts. (4) The K49 washer has no origin. The only
non-silicone washer in the package is mech_gen.py:1348, an M12 locknut washer at the helmet, and
that line says in terms "it is not taken here." An ISO 7089 M3 under the H-3 head is 0.5 mm and
eats the 5.80 mm engagement that H-2's own 5.8 mm minimum is derived from. Washer DROPPED. Also
conceded: "ISO 7045 M3 x 12 A2" and "EJOT DELTA PT 30 x 8" are distributor picks with no
datasheet in the package, which HARDWARE_SCHEDULE §4 forbids in terms. Rewritten as criteria.
(5) The rulings register was left uncorrected and self-heals. tools/RULINGS.md:82 and docs/RUL-
EEG-021:80 both carry "female–female ... eight M3 x 6". finalise_docs.py:112-113 regenerates
RUL-EEG-021 from RULINGS.md, and RUL-EEG-021:42-43 says a hand edit "is reverted, without a
warning, on the next run." And AVL §1.6:305 still carries a female-female MPN. Both files added;
the MPN is now explicitly in scope. (6) HM-12 confirmed and nobody prints it.
MECH_RELEASE_STATUS.md:84 verbatim: "AVL-EEG-017 K24 | print set of twelve items | the set in
section 1 above, plus HM-12; everything not in K24 is unquoted." K24's list omits HM-12. Added.
Line 46 shows its MECH-EEG-020 sheet as "none", and the CSV has 25 sheets — so the sheet is owed
either way and my cost argument was wrong on that point. (7) PARTS-EEG-019:278 still reads "no
gland feature exists in POD-P1-01." Verbatim. SVC-EEG-013:593 says the same. Both corrected;
HARDWARE_SCHEDULE §5 items 4 and 5 already asked for exactly this. (2) PARTIALLY CONCEDED, and
this is the substantive change. HM-13 is WITHDRAWN from this decision. mech_gen.py:1253 reads
"OE_BORE_D = ENTRY_BORE_D # 12.50: the same gland as the pod entries, deliberately"; line 288
says "the same gland is fitted at the helmet end of both umbilicals"; HARDWARE_SCHEDULE.md:53
says "H-8 and H-10 are the same part, which is deliberate: one gland type, one AVL line, one
spare"; and §4 says the two ends "may end up different parts; that is a decision, and it has not
been taken." PARTS-EEG-019's header makes design.py/mech_gen govern on disagreement. Issuing
HM-13 writes an answer into the register ahead of the source file. The split is now a recorded
open item: if MECH-D2 lands and the ends become different parts, the helmet end takes HM-13 and
the pod end keeps POD-P1-06, and K51 splits. The attack was WRONG on two things and I did not
follow it: (2, second half) "MECH-D2 does not exist ... a citation to nothing." As a package
document, correct — `grep -rI "MECH-D"` over package_v2.3 and the whole documentation/Study -
EEG/ tree returns nothing. But MECH-D2 is a sibling decision in this same batch, so it is a
citation to an unlanded sibling, not to nothing. The right response is to make the split
conditional, which I have done, not to pretend the question is unasked. (1) The attack is RIGHT
that my rule-4 wording contradicted itself — mech_gen.py:429 _harness_entry() cuts the Ø12.50
bore straight through the POD-P1-01 wall and raises a locknut pad and a P-clip boss on it, so no
printed part is dedicated to the pod gland, and my "not a printed feature that merely receives
it" would have excluded it. But the attack's replacement is worse and I REJECT it. Its rule — "a
seat, boss, pilot or bore raised or cut in a part that exists for another purpose is not an
interface part" — strips two identifiers the register has already allocated: POD-P1-03, a
bought-in O-cord seated in a groove cut in POD-P1-01/02 (line 279), which the attack's own
correction keeps as K52; and HM-04A, whose register row at line 243 says in terms "It gets an
identifier under rule 4 of §1.3 because it is a bought part with a printed interface part" — an
anchorage cut into HM-04, a part that exists for five other purposes. The attack also asks for
NO gland identifier at all, against HARDWARE_SCHEDULE §4 ("POD-P1-06 is proposed for the
harness-entry gland") and §5 item 4, which ask PARTS-EEG-019 for exactly that number. So the
discriminator cannot be geometric. It is a class exclusion, which is what the register actually
practises: fasteners are out (AVL §1.6, H-1 to H-7); functional fittings that mate with
something printed are in (POD-P1-03, HM-04A, HM-05A, WH-ADP-03/04, HM-12, POD-P1-06); items that
mate with nothing printed are out (OA-16, Harwin M20, JST PHR-2). That wording is consistent
with every allocation in §2, which neither my first version nor the attack's was.

**Reasoning.**

HM-12 is not a free choice and survives untouched.
mech/stl/HM-12_occipital_umbilical_entry_plate.stl and .step exist, mech/MANIFEST.json carries
part_id "HM-12" on both, MECH_RELEASE_STATUS.md:46 lists it, mech_gen.py carries it in PARTS,
REGISTER, MANIFEST and UNMARKED, and §1.3 rule 2 makes the filename carry the identifier. The
Phase 2 block has nothing allocated in it. Renaming costs a regenerate and a re-hash against a
reservation holding nothing. POD-P1-06 for the gland is what the package asks for, in writing,
twice (HARDWARE_SCHEDULE §4's identifier row and §5 item 4), and POD-P1-05 is the precedent that
a gland takes a POD-P1 number. One number, because the governing source file says one gland —
mech_gen.py:1253 and 288, HARDWARE_SCHEDULE:53 — and because the file that would justify two
says the decision "has not been taken." A register does not get to settle a hardware question
its own source file has left open; it records the number the package can defend today and
carries the split as an open item. The fastener ruling is the load-bearing part and it needed to
be re-cut, because rule 4's current positive limb ("a printed interface part exists for them")
is genuinely ambiguous: every insert bore, tapped boss and 2.50 mm pilot in POD-P1-01 is
arguably a printed interface, and read that way roughly a dozen catalogue fasteners acquire
numbers in a namespace whose stated purpose is to stop two things sharing one. But the exclusion
has to be by class, because a geometric test cannot separate the H-1 insert bore from HM-04A's
anchorage or POD-P1-03's groove, and the register has already given both of those numbers.
Naming the excluded class outright — screws, nuts, washers, inserts, standoffs and the features
that receive them — is the only wording that reproduces every allocation §2 already carries and
still keeps a shop from numbering its screws. K47 is derived, not chosen: K46 is the highest
K-line in AVL §4 Rev B. Six lines rather than seven because the two inserts are two purchasable
items with disjoint length windows and the washer is not a part of this package. The standoff
correction is the one item here that a buyer can act on wrongly today, which is why the MPN and
the worksheet both had to come into scope.

**Confidence:** judgement  |  **Blocks a build:** yes  |  **Signed off by:** PARTS-EEG-019's register owner signs the identifiers and the §1.3 rule 4 re-cut (HM-12, POD-P1-06, the fastener class exclusion, the POD-P1-05 row correction). AVL-EEG-017's owner signs K47 to K52 and the K24 addition; the §1.6 standoff line is signed by AVL-EEG-017's owner TOGETHER WITH the safety reviewer, because HARDWARE_SCHEDULE §4 makes that line jointly owned — RISK-EEG-011 SR-08's creepage rests on the standoff's material and its 18 mm length. Mechanical signs the HM-12 re-cut, the added mark and the new MECH-EEG-020 sheet 26. ECO-EEG-016 records the change. WH-EEG-008's owner is consulted on the gland retention figure and holds the open item on the two-ends split.

**What would change it.**

The gland split. If MECH-D2 lands and HARDWARE_SCHEDULE §4's H-8/H-10 row closes as "two
different parts", HM-13 issues for the helmet end, POD-P1-06 narrows to the pod end at 2/kit,
K51 splits into two lines, and §1.2's reservation re-cuts again to HM-14 to HM-19. Until
mech_gen.py stops saying "the same gland as the pod entries, deliberately", the register carries
one gland. Phase 2 allocations. If Phase 2 has already committed HM-12 to an occipital-shell
part, the plate takes the next free HM number: a key change in mech_gen.py's
PARTS/REGISTER/MANIFEST tables, a manifest re-hash and two filenames. No dimension moves, and
the plate is unmarked today precisely so an unissued number cannot reach hardware. Further
K-lines. If AVL-EEG-017 issues any K-line before these are written in, the block moves off K47.
The insert lengths. If the insert maker's blind-hole allowance is not the assumed 0.3 mm, K47's
"at most 5.20 mm" moves with it — that figure is HARDWARE_SCHEDULE's assumption, not a datasheet
value. The gland locknut. If the approved gland's across-flats exceeds 17.00 mm, this stops
being a numbering question: ENTRY_PAD_D, OE_SEAT_D and the 32.00 mm axis spacing all move,
_pod_holds() and _oe_holds() fail the build, and HM-12 is re-cut in geometry and not just in
marking.

**Files this touches:** `docs/PARTS-EEG-019_RevB_part_identifier_register.md`, `docs/AVL-EEG-017_RevB_approved_vendor_list.md`, `tools/RULINGS.md`, `docs/RUL-EEG-021_RevA_rulings_register.md`, `tools/mech_gen.py`, `mech/HARDWARE_SCHEDULE.md`, `mech/MECH_RELEASE_STATUS.md`, `mech/MANIFEST.json`, `mech/drawings/MECH-EEG-020_sheet_index.csv`, `docs/SVC-EEG-013_RevB_service_and_refurbishment_manual.md`, `docs/EEG_kit_BOM_for_bidders_RevC.xlsx`, `docs/ECO-EEG-016_RevB_change_control_and_document_register.md`


## D2-EAR-REFERENCE-COUPLER

**Question.** WH-01 conductors 9 and 10 are described by three documents as three incompatible joints (bare crimp onto a clip / a leaded electrode with a plug and no socket / a joint that must part without a tool twice per turnaround). What is the clip, what is the conductor termination, and how does it stay touch-proof?

**Decision.**

THE RULING STANDS, WITH ITS SUPPORTING PROVISIONS REPLACED. CLIP (unchanged, derived): AVL-
EEG-017 K2 exactly as written — Wuhan Greentek Ag/AgCl ear clip, finished, leaded, with its own
DIN 42802 touch-proof plug. The part does not change; its purchase order gains one field (see 2
below). TERMINATION (unchanged, derived): WH-01 conductors 9 and 10 terminate in a free-hanging
1.5 mm touch-proof cable SOCKET to DIN 42802-1 — AVL line K27 — crimped or soldered onto the 250
mm temple tail at the point the crimp used to be. No cut length moves: 2140 mm stands (1500 +
120 + 20 + 195 + 40 + 15 + 250). K27 is placed on the same purchase order as K2 so retention and
finger-safety when mated are one supplier's responsibility; Stäubli LB-I1,5 cable-socket family
is the approved alternate, exact order code including colour suffix read off the catalogue and
not constructed here. TOUCH-PROOFNESS — the decision's four provisions are replaced by five,
with values: 1. PACKING RULE (the load-bearing one, and the decision's real gap). The ear clips
travel MATED and captive. PKG-EEG-015 §1.1 line 2.1 becomes "2 fitted | HELMET HM-01"; the (408,
162) 94 × 100 bay becomes EMG LEADS only; IFU-EEG-014 §1 table and §9 step 1 are re-issued; SVC-
EEG-013 R12 gains an explicit "ear clips left mated, dressed inside the helmet bay" line to
close the R10/R12 gap. Without this the participant unmates and re-mates both couplers every
session, unsupervised, out of one 94 × 100 mm hollow holding five identical 1.5 mm DIN 42802
male plugs, and IFU §8 ("You dismantle nothing") is false. 2. K2 LEAD LENGTH. Apply the K1
correction verbatim to K2: the PO states lead length and termination. Set plug-to-jaw at 150–200
mm — a stated number, not the catalogue 1.0–1.5 m. Record the total unscreened reference run
(250 mm tail + ≤200 mm clip lead = ≤450 mm) as an extension of DEV-WH-01 to REF_L/REF_R, and re-
measure T8 (≤1.0 µV RMS, an RTS-1 release criterion) on a built unit carrying the real lead
before that deviation is accepted. 3. INSULATION OF THE FREE TAIL. A materials row in WH §4, not
a label citation. Extruded PTFE or FEP sleeve, or 3:1 heat-shrink supplied ≥1.5 mm / RECOVERED
≤0.70 mm, over the whole 250 mm free length, resistant to 70 % IPA and to the 40 kHz bath. The
PS-187-2-WT citation is deleted: it is a white thermal-transfer marker sleeve at 1.6 mm
recovered and cannot grip a 0.70 mm OD conductor. 4. STRAIN RELIEF — NOT SPECIFIED AT THIS
ISSUE, CARRIED OPEN. The 2.0 mm adhesive-lined bulb "at the temple channel mouth, captured
behind the cover strip" is deleted. The released HM-01 mesh has no temple channel mouth
(mech_gen.py defines exactly three, all occipital: HM01_N1_MOUTH (0.00, −95.38, roof) and
HM01_HALO_MOUTH (±45.41, −82.41, −11.25)), and CH_BORE is a constant 3.80 mm, so a 2.0 mm bulb
has no shoulder to react against. The H6 15 N leg is therefore NOT applied to the ear couplers,
and the gap is carried open beside the identical OE-1/OE-2 anchor entry already in KNOWN_ISSUES,
until a temple wire exit (a mouth stepped below 2.0 mm, or a moulded-in anchor) is added to
mech_gen.py and registered. 5. TESTS. Drop H3 (single-pole, no screen terminal, tail outside the
screen after step 6, and redundant against H3's existing drain-to-every-conductor leg). Add the
couplers to H4 — 500 V DC, 60 s, conductor bundle to any exposed metal with the plug withdrawn,
socket body and shroud counted as exposed metal, 100 MΩ minimum. Add them to H8 at 100 cycles
minimum, run as-built after step 15, with H1 repeated; the per-unit leg lives in step 19's
existing as-built repeat. Add ONE first-article-only check that H4 cannot give and the package
has nowhere: IEC 60601-1 / IEC 61032 test-probe B on the unmated socket, recorded in the FAI
pack. 6. RETENTION WINDOW — the binding criterion, and K27 has none. Add to K27: separation
force 5 to 15 N, stated and repeatable, beside the existing "mating force stated and repeatable
over ≥500 cycles". High enough not to part on a snag on the one net whose partial loss WH §3.1
itself calls "electrically almost invisible"; low enough for SVC R4's tool-free release. 7.
COLOUR. GY and PK on the sockets stands — it meets K27's actual criterion, "a colour distinct
from the three EMG sockets". The "§10 one-table rule" justification is dropped (that is a
conductor-colour labelling rule). Because K2 is bought unchanged, the K2 PO gains: plug colour
to match, or a printed GY/PK marker sleeve on the clip lead within 25 mm of the plug. 8. LIFE.
With (1) adopted: ~100 operator mate cycles over 5 years (20 turnarounds/kit-year × 5) against
≥500 — 5× margin, cycle count not binding. If (1) is REFUSED, the participant adds ~250 (SVC §3:
25 sessions ≈ 10 turnarounds ≈ half a year → ~50 sessions/kit-year) for ~350 total — 1.4×, not
5× — and then K27's cycle spec goes to ≥1000 and the mis-mate must be killed mechanically, by
gender reversal or keying, not by a colour. 9. OPEN ITEM 24 restated in BOTH directions: an EMG
lead mates an ear socket, AND the K2 clip's own plug mates J15–J17. With (1) both are operator
errors at R10, caught by R4's existing count-out (8 cups, 2 ear clips). Without (1) neither is.

**What the attack changed.**

CONCEDED — five things, all verified against the files. (1) The decision's one new safety claim
is false as the package stands. PKG-EEG-015 §1.1 line 2.1 reads "Ag/AgCl ear-clip references | 2
| EAR CLIPS + EMG LEADS" — bare "2", while every fitted line on that list reads "N fitted" (1.5,
1.7, 1.8, 1.11, 1.15, 1.16). The §2.2 bay schedule puts HELMET HM-01 at (14, 14) 197 × 236 and
EAR CLIPS + EMG LEADS at (408, 162) 94 × 100, with line 2.2's three EMG DIN leads in the same
hollow; IFU §1 renders it ("Two ear clips on a lead, and three coloured leads for the face
pads"), §2 step 3 has the participant clipping them on, and §9 step 1 sends them back to that
hollow. So the participant does mate the couplers, every session, from a bay of five identical
DIN plugs — the exact fault the decision claimed to have removed. "Operator-only and countable"
is withdrawn; it is recovered only by re-issuing PKG and IFU, which is now provision (1) of the
ruling. (2) "It does not change what is bought" was false and unbounded the reference. AVL K1
carries a verbatim correction for this exact defect one line above K2 — "The '1.5 m lead' in
this line is a catalogue description and is not what the kit needs... The purchase order must
state the tail length and its termination" — and K2 has no such note and no length. WH §4 argues
at length why WH-01 must be screened, and DEV-WH-01 accepts unscreened only for the three EMG
channels. The decision silently propagated that deviation onto REF_L/REF_R with no bound. Now
bounded at ≤450 mm total with T8 re-measured. (3) The sleeve cited the wrong section and could
not be built. §10 is Labelling; PS-187-2-WT is a white thermal-transfer wire-MARKER sleeve, 1.6
mm recovered for pigtails, against §4's "PTFE, 0.15 mm wall, OD 0.70 mm" conductor. It recovers
to more than twice the wire OD. Replaced with a §4 materials row, recovered ≤0.70 mm. (4) The
strain relief named geometry the released frame does not have. mech_gen.py records exactly three
channel mouths, all occipital, and CH_BORE = 3.80 constant. Provision deleted; the H6 15 N leg
is withdrawn from the couplers and the anchor carried open. (5) H3 was the wrong test and there
is no retention number. H3 is drain-referenced, §3.6 states a DIN socket is single-pole with
nowhere for a screen to land, and step 6 cuts the WH-01 screen back at the helmet end. K27's
criteria carry a mating-force/cycle line and no separation force, while every other separable
interface in the kit has a window (bayonet 3–6 N / >10 N, H8 0.15 N per contact, boom 30 N).
Both fixed, with values. KEPT — the attack is wrong or overstated in five places, and none of
them recovers the decision's original text. (a) Point 4's cover-strip citation is misapplied.
HM-11A DOES run through the temple — hm11a() sweeps azimuth −55° to +235°, the whole halo band
except the 70° occipital arc — and line 694's "no cover strip can run there" is a comment on
that occipital arc (HM01_SHELL_T0/T1 = 235–305°), not on the temple. The attack's conclusion
survives for a different and worse reason: the released frame has no temple MOUTH at all, and
hm11a()'s own docstring says "The released HM-01 cannot take this strip" (10.91 mm band against
the 12.20 mm the two-channel section needs, no rebate). Its quotation of the mech_gen comment as
"Every channel that reaches the occiput opens into the shell cavity, and nothing opens anywhere
else" is a paraphrase, not verbatim text. (b) "Unrunnable in sequence" is overstated. Step 19
already repeats continuity and screen isolation as an as-built check, so a coupler leg is
runnable there. H3 is dropped because it is redundant and screen-referenced, not because it
cannot be run. (c) H4 does not evidence finger-safety. It is a 500 V DC insulation-resistance
measurement; finger-safety to the IEC 60601-1 test finger is a gauge/type check, which the
package has nowhere. So H4 is added for "no accessible conductive part" AND a separate first-
article test-probe-B check is added. The attack was right that a supplier declaration was being
substituted for a measurement, and wrong that H4 alone closes it. (d) Gender reversal (the
attack's fallback (b)) is not cost-neutral. The temple-tail plug form (LM-I1,5) is a catalogue
cable part; a socket-ended ear clip is not a Greentek catalogue line and would be a bespoke
Class A patient-contact electrode. The rejection stands, but is downgraded from "will not" to
"second choice, if the programme refuses provision (1)". (e) The decision's reading was not
invented. RISK-EEG-011 H-20 states the mitigation "Participant touches nothing removable" and
H-30 states "Electrodes permanently mounted, so there are no placements to get wrong". The
package contradicts itself between the risk file's intent and the packer's and participant's
documents. The attack is right that PKG and IFU are the operative ones, so the fix is a re-issue
the risk file already assumes — not a reversal of the ruling. (f) The colour values survive.
K27's actual criterion is "a colour distinct from the three EMG sockets", which GY/PK meets.
Only the "one-table rule" justification is dropped, plus a PO line for the mating plug half.

**Reasoning.**

The three-way disagreement is still resolvable in exactly one direction, and the attack never
touched that. A permanent crimp cannot satisfy SVC R4/R5, which release and bath the clips twice
per turnaround for the kit's life. A finished leaded electrode with a plug and no socket cannot
be connected. A free-hanging DIN 42802-1 cable socket on the temple tail satisfies K2, R4/R5 and
touch-proofness at once, moves no cut length, and is the one form of this part catalogued as a
cable part — so it does not carry the 12-week first-article risk AVL §1.4.1's PCB-mount line
does. That half is derived from the files and survives intact. What the attack destroyed is
everything the decision stacked on top. The load-bearing failure is that the decision reasoned
from RISK-EEG-011's stated mitigations ("Participant touches nothing removable") and from IFU
§13.2 ("the only electrodes you position yourself" are the three face pads) without opening PKG-
EEG-015 §1.1 and §2.2, which are what a packer actually ticks. Those put the clips loose in a
hollow 197 mm of foam away from the helmet, on a 250 mm tail that cannot span it, alongside
three more identical DIN plugs. So the participant mates them, every session — and the mis-mate
the decision called "operator-only and countable" is the per-session participant error it
claimed to have eliminated, in both directions (an EMG lead into an ear socket, and the ear
clip's plug into J15–J17), on the one net the harness document itself calls electrically almost
invisible when it partly fails. That is a packing ruling, not a connector ruling, and it is
decidable here: rule the clips mated and captive in transit. Doing so makes RISK H-20's existing
mitigation true rather than aspirational, keeps IFU §8's "You dismantle nothing" honest, reduces
open item 24 to an operator error at R10 caught by R4's count-out, and — because it removes ~250
participant cycles — restores the 5× life margin the decision claimed. It requires provision
(2), a stated short K2 lead, or the clip cannot travel dressed inside the helmet bay. The other
three concessions are straightforward specification errors, and each has an obvious correct
value: a marker sleeve is not insulation (§4 row, recovered ≤0.70 mm); a bulb in a constant 3.80
mm bore reacts nothing and there is no temple mouth to put it in anyway (deleted, carried open
beside the identical OE anchor gap KNOWN_ISSUES already holds); and a screen-referenced test on
a single-pole socket outside the screen measures nothing (H4 + H8 + a first-article test-finger
check). The retention window is the attack's best original contribution: this is the only
separable interface in the kit with no force window, it hangs 40 mm from a participant's face,
and it sits on the silent net. 5–15 N is set by the two constraints the package already states —
above the snag, below SVC R4's tool-free release. I did not concede the temple cover strip, the
"unrunnable" premise, H4-as-finger-safety, or the cost-free gender reversal, because the files
do not support them. None of those recover the decision's original text; three of them make the
underlying defect worse, not better.

**Confidence:** judgement  |  **Blocks a build:** yes  |  **Signed off by:** The safety reviewer, for the patient-applied touch-proof interface itself — K27 against its criteria including the new 5–15 N separation window, the H4 leg, and the first-article IEC 61032 test-probe-B check on the unmated socket — and for accepting the extension of DEV-WH-01 to REF_L/REF_R after T8 is re-measured on a built unit. The programme lead, for provision (1), the packing rule, because it changes PKG-EEG-015 §1.1 and §2.2, IFU-EEG-014 §1 and §9, SVC-EEG-013 R12 and the RISK-EEG-011 H-20/H-30 mitigations together, and it is the change the whole safety argument rests on. The mechanical reviewer plus the PARTS/MECH owner, for the temple wire exit in tools/mech_gen.py — a released model must gain a feature and be re-cut before the H6 15 N leg can be written. The AVL-EEG-017 owner, to place K27 on the same purchase order as K2 and to add the lead-length and plug-colour fields to K2. ECO-EEG-016 carries the change record for all of it.

**What would change it.**

A submitted K27 sample that is not finger-safe to IEC 61032 probe B with the plug withdrawn, or
whose separation force is not repeatably inside 5–15 N over 500 cycles, kills the vendor and not
the ruling — go to the Stäubli LB-I1,5 alternate. If no maker supplies a cable socket that mates
the K2 clip's plug with a stated retention force, the fallback is to buy clip and coupler as one
assembled leaded pair, which makes the temple tail a permanent joint and forces SVC R4/R5/R10 to
be rewritten around releasing at the clip jaw. If the programme REFUSES provision (1) and the
clips travel loose, three things change together and the ruling must be re-opened: K27's cycle
criterion goes from ≥500 to ≥1000 (about 350 cycles over 5 years is 1.4× margin, not 5×); the
colour code is no longer an adequate defence against a participant mating one of five identical
plugs in one 94 × 100 mm bay, so the mis-mate must be killed mechanically by gender reversal or
keying — accepting that a socket-ended ear clip is a bespoke Class A patient-contact part and
not a Greentek catalogue line; and open item 24's residual has to be re-scored in RISK-EEG-011
as a per-session participant error rather than an operator error at R10. A T8 measurement above
1.0 µV RMS on a built unit carrying the real K2 lead means the unscreened reference run is not
acceptable at any length, and the clip lead must be screened or the coupler moved to the earlobe
end. A temple wire exit added to tools/mech_gen.py and registered closes provision (4) and lets
the H6 15 N leg be written against a real anchor; until then it stays open and is not tested.

**Files this touches:** `docs/WH-EEG-008_RevB_harness_and_cable_assembly.md`, `docs/AVL-EEG-017_RevB_approved_vendor_list.md`, `docs/PKG-EEG-015_RevB_packing_labelling_and_shipping.md`, `docs/IFU-EEG-014_RevB_participant_quick_start_and_placement_guide.md`, `docs/SVC-EEG-013_RevB_service_and_refurbishment_manual.md`, `docs/RISK-EEG-011_RevB_risk_analysis_and_safety_review_pack.md`, `docs/ECO-EEG-016_RevB_change_control_and_document_register.md`, `docs/PARTS-EEG-019_RevB_part_identifier_register.md`, `tools/mech_gen.py`, `KNOWN_ISSUES.txt`


## D3-BIAS-FPZ-TERMINATION

**Question.** Conductor 11 (BIAS_EL) lands on an "Fpz bias pad, solder tag" with no part number, no drawing and no feature on any model. What does it land on?

**Decision.**

The bias pad is deleted as a helmet feature. Conductor 11 terminates at the HM-01 halo-front
channel mouth in a free-hanging 1.5 mm touch-proof SOCKET to DIN 42802-1 — K27 class, Stäubli
LB-I1,5 family or the Wuhan Greentek DIN 42802 cable range, both of which AVL-EEG-017 K27
already records as catalogued cable parts — in TQ turquoise, conductor 11's own colour under the
section 10 one-table rule and distinct from the red/yellow/green EMG set. Same gender as the two
ear couplers and the three panel sockets: after this change no plug exists anywhere on the
instrument side. It mates WH-10 / WH-EEG-008-10, a new 150 mm ±10 mm snap-to-touch-proof-PLUG
lead of the K3 class (reference Stäubli SLS425-SEK/N, Greentek equivalent approved), TQ
turquoise — the form suppliers actually build and the form K3 is already bought in. The
electrode is a fourth disposable pre-gelled Ag/AgCl snap pad off the existing K4 pack (Ambu
BlueSensor N, 30 per pack), placed on prepped forehead skin below the HM-02A brow pad, one per
session. Three values that changed, and two that cannot be set here: CUT LENGTH: not 1980 mm. A
free-hanging coupler needs a free tail; 1980 = 1500+120+20+285+40+15 has none. Cut =
1500+120+20+285+15+F, with the 40 mm site service loop DELETED (there is no site left to coil it
at) and F the free tail. F must be stated explicitly on the wire list and is set at the first
fitting trial — bounded below by the clearance needed to mate by hand clear of the HM-02A brow
pad and above by the 250 mm the ears carry. Do not carry 1980 forward. PULL TEST: not H6's 15 N.
H6's 15 N is defined as acting on HM-04A's anchorage in the body and on the solder joint; a
free-hanging coupler has no body. Either draw an HM-01 anchorage that takes 15 N (which returns
this to open items 22/26 with the mechanical reviewer) or set the coupler retention at or below
H5's 13 N minimum for 28 AWG, and give it the mating-force and 500-cycle criteria K27 already
carries. CROSS-MATE: stated, not designed out. Open item 24 grows from five interfaces to six
sockets and six plugs, and gains a consequence RISK-EEG-011 has not analysed: a K2 ear clip or a
K3 EMG lead will enter the bias socket, putting an electrode on BIAS_EL — the one patient node
whose clamp sits on the patient side of its resistor, SF-1a bound 183.6 µA — at a site RISK-
EEG-011 works only at Fpz. If genuine non-interchangeability of the driven output is wanted, the
answer is connector CLASS or a keyed shroud, not gender; costed and referred to the safety
reviewer. FRAME: this does not leave HM-01 untouched. A dressed channel mouth against 0.70 mm OD
PTFE and a strain relief at the halo front are new features on the same carried-over STL that no
source file generates (PARTS-EEG-019 OA-1). Open item 26 is narrowed, not closed. SR-12 STAYS
OPEN. Touch-proofing an interface does not alter the 183.6 µA that flows out through the
electrode into the person. RISK-EEG-011's three options for SR-12 are move D11/C11 to the module
side, add a second series element, or accept the topology with a written justification. None of
them is a connector. Say this in the same paragraph as the 183.6 µA so no reviewer closes SR-12
on this change.

**What the attack changed.**

CONCEDED — the attack's central claim is true and it kills the primary. WH-EEG-008 §3.1.2 (line
416) reads verbatim: "The kit then has five 1.5 mm touch-proof interfaces -- three EMG sockets
on the pod panel and two ear sockets on the helmet temples". All five are SOCKETS. A 1.5 mm DIN
42802 plug mates every one of them. The decision counted the five LEADS (which are plugs) and
wrote its conclusion about the five INTERFACES. "The bias interface cannot mate any of the five
other 1.5 mm interfaces" is exactly inverted, and it was the whole rationale for the gender
reversal. CONCEDED — the hazard is reachable by hand. §3.1 rows 9/10 give the ear couplers "195
+ 250 free"; §3.1.2 makes them free-hanging sockets on the 250 mm temple tails. The halo ellipse
is a=81.10 / b=96.80 (mech_gen.py:844), so temple to halo front is roughly 126 mm straight — a
250 mm tail reaches with slack. A helmet-mounted bias plug into an ear socket is a two-handed
action between two things already on the helmet, needing no lead at all. It is precisely the
fault WH-EEG-008's own mis-mate table lists as a defect to prevent: "WH-01 offset -1 | BIAS_EL
onto REF_R; the driven common-mode return lands on the reference node." And it is invisible:
§3.1 says R9/R10 are hard-paralleled onto SRB1 so "one clip falling off is electrically almost
invisible", and §3.1.2 says T10 cannot catch it because "a mis-plugged electrode is still an
electrode". CONCEDED — 1980 mm and "free-hanging" cannot both be true. Verified against the row
and the formula: conductor 8 at 250 in-frame cuts 1945, conductors 9/10 at 195+250 free cut
2140, conductor 11 at 285 cuts 1980 with zero free tail. CONCEDED — H6 at 15 N is unachievable
as written. Line 1440 defines the 15 N as acting on HM-04A's anchorage in the body; line 1439
qualifies 28 AWG crimps at 13 N minimum. Specifying a 15 N pull on an unanchored coupler puts
the load on a joint qualified at 13 N. CONCEDED — the 12.55-vs-11.93 argument proves far too
much. Both numbers are real (ASM-EEG-007:710; mech_gen.py:852), but mech_gen.py:761 records the
same frame at 10.91 mm across the temple against the 12.20 mm its own harness document needs,
and hm11b_sagittal() records the arch as a Ø9.20 mm rod — 3.35 mm short of the same pocket. The
0.62 mm at Fpz is the SMALLEST deficit in the package. Dropped as a reason; the real reasons
stand on their own (no ninth cup, carrier, crown, spring, gel port or contact light; no
reprocessing argument; and SVC R5 confirms the 25-cycle disinfection compatibility protocol has
never been run). CONCEDED — "put nothing on the frame at all" was false. hm11a_halo() records
the released mesh as having ONE fully enclosed 3.80 mm bore per section, no second channel and
no rebate; mech_gen.py:1150 records that anchor pockets are not in the v1 mesh either. CONCEDED
— the paperwork is not free. SVC §3.3 already carries "EMG snap-to-DIN leads (WH-06) | 3 | The
lead is the wear item, not the pad"; WH-10 needs the same row. SVC R4 step 6 count-out needs a
line. PKG §1.1 gives every fitted assembly a line (WH-09 is 1.17). And every IFU §13.2 quote the
attack made is verbatim in the file: the title "The three face pads", "These are the only
electrodes you position yourself", "Match colour to colour and you cannot get them the wrong way
round", and "Thirty are supplied, which is ten sessions' worth" — which at four pads is 7.5, not
ten. All four have to be re-issued. CONCEDED — SR-12 is untouched. RISK-EEG-011 line 883 lists
the three real options and a connector is not among them. REJECTED — the attack's counting
argument. "The primary adds a sixth interface and a seventh" is wrong. Both configurations end
with exactly six sockets and six plugs; 36 combinations either way. The count is identical. The
real asymmetry, which does favour the socket, is not how many but WHICH half: with the helmet
side all sockets, the unprotected driven node cannot be carried into anything, because a socket
cannot be inserted. REJECTED — the fallback is not clean of the earlobe-current path. The attack
implies inverting the gender removes it. It does not: a K2 ear clip plug still enters the bias
socket and puts an earlobe on BIAS_EL under the same SF-1a bound. What inverting removes is the
helmet-to-helmet mis-mate that needs no lead at all. The residual must be written into RISK-
EEG-011, not assumed away. REJECTED (minor) — SVC R4's "4 pads" are the four HM-02 TPU comfort
pads, discarded at step 4, not electrode pads. WH-10 still needs a count-out line, but not for
the reason given. KEPT — deleting the pad as a helmet feature, the disposable K4 pad on prepped
forehead skin, a controlled coupler in place of a solder tag, TQ turquoise, and WH-10 as the
next free number (PARTS-EEG-019 §2 confirms WH-01–07 and WH-09 in use, WH-08 withdrawn and not
reused).

**Reasoning.**

I opened every file the attack cited and the load-bearing ones all check out verbatim. The
decision's guard is inverted: the five interfaces it claimed the bias plug could not mate are
all sockets, and a plug mates a socket. That is not a wording slip — it was the entire argument
for putting the male half on the helmet, and once it fails, the reversal is not free, it is the
one place a reversal costs something. The kit's driven output is the one node whose clamp sits
on the patient side of its resistor (KNOWN_ISSUES 0a: D11/C11 on BIAS_EL, 2.5 V / 13.615 kΩ =
183.6 µA against S-02's 50 µA), and the primary made that node the mobile, insertable half,
within easy reach of two free-hanging ear sockets on 250 mm tails, available to the participant
by hand at every session. The document's own mis-mate table already names that exact event as a
factory defect to be prevented. So the correction stands: take the decision's own stated
fallback as the primary. That is also the manufacturable half — K3 is already bought as a snap-
to-DIN-plug lead, whereas a snap-to-socket lead is not a catalogue form — so the fallback
removes the supply risk the primary carried as well. Everything else in the decision survives
and is worth keeping. The bias site genuinely should not be a ninth HM-04, but for the reasons
that do not depend on 0.62 mm: no ninth cup, carrier, crown, spring, gel port or contact light
exists, a disposable pad needs no retention and no reprocessing argument, and SVC's 25-cycle
disinfection compatibility protocol has never been run. A fourth K4 pad reuses a pack the kit
already buys. WH-10 is the right number. Turquoise is right and satisfies K27's existing
"distinct from the three EMG sockets" criterion. Three claims in the decision had to be
withdrawn rather than adjusted, because each would have let a reviewer sign something untrue.
The cut length cannot stay at 1980 while the coupler is free-hanging — the arithmetic is right
but it contains no free tail and a 40 mm loop with nowhere to sit. H6's 15 N is defined against
a body anchorage the coupler does not have, and sits above H5's 13 N crimp qualification. And
touch-proofing does not close SR-12 — it fixes a bare accessible conductive part, which is real
and worth fixing, but the 183.6 µA flows out through the intended electrode, and the decision
put "the cheapest thing that fixes it" three clauses after the number. Two numbers I have
deliberately not filled in. The free tail F is a fitting dimension, and the bias coupler's
retention value depends on whether HM-01 gains an anchorage. Both are stated as what must be
determined and by whom rather than guessed, because a guessed tail length and a guessed pull
value are exactly the kind of thing that gets built.

**Confidence:** judgement  |  **Blocks a build:** yes  |  **Signed off by:** The safety reviewer first, on three things together: that a K27-class touch-proof socket is the correct patient-side form for the driven output, that the residual cross-mate (a K2 ear clip or K3 EMG lead entering the bias socket, putting an electrode on the one unresisted patient node at SF-1a's 183.6 µA bound) is accepted and stated rather than mitigated, and that SR-12 remains open and is not read as closed by this change. Then the mechanical reviewer, with open items 22 and 26, because the halo-front channel mouth, the dressed exit and the strain relief are new features on the carried-over HM-01 STL that no source file generates (PARTS-EEG-019 OA-1), and because the coupler retention value depends on whether an anchorage is drawn. Then PARTS-EEG-019 and ECO-EEG-016 to issue WH-10 / WH-EEG-008-10, and AVL-EEG-017 to open the lead line (K47 proposed) and to carry the bias socket as a third unit against K27's existing criteria. Then IFU-EEG-014's owner, because §13.2 must be re-issued: the title, "the only electrodes you position yourself", the "match colour to colour and you cannot get them the wrong way round" guarantee, and "thirty are supplied, which is ten sessions' worth" all break at four pads with one coupler on the helmet.

**What would change it.**

A vendor sample measured against K27's criteria — if no supplier will build a 1.5 mm touch-proof
socket to those criteria as a cable part, the whole coupler line reopens, not just this site. A
first fitting trial: it sets F, the free tail, and it is where a clash between the pad and the
HM-02A brow pad shows up (a fit finding, moving the pad down or the brow pad up, not a
redesign). A safety-reviewer ruling that the driven output must be genuinely non-interchangeable
rather than merely stated — that replaces the K27-class socket with a different connector class
or a keyed shroud, and the socket-class decision above is withdrawn. A decision on SR-12 that
moves D11 and C11 to the module side removes the reason this site is the most urgent of the
three open terminations, though it does not change the termination itself. And if the mechanical
reviewer draws the HM-01 anchorage, the coupler retention goes to 15 N and aligns with H6; if
not, it is capped at H5's 13 N.

**Files this touches:** `docs/WH-EEG-008_RevB_harness_and_cable_assembly.md`, `docs/AVL-EEG-017_RevB_approved_vendor_list.md`, `docs/PARTS-EEG-019_RevB_part_identifier_register.md`, `docs/ECO-EEG-016_RevB_change_control_and_document_register.md`, `docs/RISK-EEG-011_RevB_risk_analysis_and_safety_review_pack.md`, `docs/IFU-EEG-014_RevB_participant_quick_start_and_placement_guide.md`, `docs/SVC-EEG-013_RevB_service_and_refurbishment_manual.md`, `docs/PKG-EEG-015_RevB_packing_labelling_and_shipping.md`, `KNOWN_ISSUES.txt`


## D4-D11-C11-PATIENT-SIDE

**Question.** D11 and C11 sit on BIAS_EL, the patient side of R11, alone among the sixteen protection networks (RISK-EEG-011 SR-12, KNOWN_ISSUES 0a). Move them, add a second series element, or accept the topology?

**Decision.**

MOVE BOTH, FIT BOTH, CHANGE NO VALUES. Delete tools/design.py:501-503 and let channel 11 fall
through the generic loop at :497-500, so the row becomes identical to the other fifteen: R11.1 =
BIAS_EL (patient), R11.2 = BIASOUT (module), D11.3 = BIASOUT, C11.1 = BIASOUT, C11.2 = AGND_REF.
C11 stays a fitted 10 nF C0G 50 V Murata GCM1885C1H103JA16D. The DNP rider of the original
decision is withdrawn. Values after the change: SF-1a (shorted D11 half) collapses into the
ordinary SF-1 — 2.5 V / 47 kOhm = 53.2 uA bound A and 2.5 V / 60.615 kOhm = 41.2 uA bound B
today, and 2.5 V / 68 kOhm = 36.8 uA once ECO-EEG-024 lands — instead of 183.6 uA bound B /
unbounded bound A. SF-6a collapses into SF-6 (shorted C11 now ties the Fpz electrode to AGND_REF
through the full 47 kOhm: no injection, dead bias drive, a Pass row that already exists). E-07
stays met word for word: sixteen networks, C1-C16 all 10 nF C0G. constraints/nets.md pad counts
invert, BIAS_EL 4 -> 2 and BIASOUT 2 -> 4 (regenerate with emit_netclass_table.py, do not hand-
edit). Three things the original edit instruction omitted, all confirmed and all mandatory. (1)
State in the ECO that deleting :501-503 also swaps R11's pads, and that this is expected to
retire the relaxed-geometry connection "BIASOUT J2.10 -> R11.1" recorded twice at
tools/drc_report.txt:59 and :67. (2) Re-run the full emit chain, not only drc.py and netcheck.py
— the netclass table, the CPL, the assembly drawings and the schematic sheets are all generated.
(3) Re-route BIAS_EL and BIASOUT with tools/rerun_subset.py and re-verify 145 of 145 nets,
VIOLATIONS: 0. The one thing the package genuinely cannot compute — whether the module's bias
amplifier is stable driving 10 nF at its own pin, now that the 47 kOhm no longer isolates it —
is not resolved by guessing a capacitor value. It is declared where this package already
declares everything it assumes about a module it has not yet bought: add a row to ICD-EEG-006
Rev B section 2.1's assumption table, beside "Inputs tolerate the series protection resistance",
reading "Bias amplifier stable driving 10 nF C0G at BIASOUT, with 47 kOhm (68 kOhm after ECO-
EEG-024) in series to the electrode" with the consequence-if-untrue "bias loop peaks or
oscillates; common-mode rejection degrades on all sixteen channels". That is an incoming-
qualification condition on the module and a first-article scope check, not a carrier defect.
Note the exposure is bounded and functional, not a patient-current fault: an oscillating bias
amp is rail-limited and reaches the forehead only through the 47 kOhm, i.e. <= 53 uA AC, inside
the 100 uA AC normal-condition allowance for a type BF applied part. If first article shows
peaking, C11 is depopulated or dropped to the 4.7 nF C0G same-series alternate that AVL-
EEG-017:149 already approves "only on a written ECO" — the pad is there either way, and that
direction of change is cheap. The reverse is not, which is why fitted is the default. Assign the
whole change an ECO number under ECO-EEG-016 and record SR-12's disposition as the safety
reviewer's per RISK-EEG-011 section 11. Correct two sentences of the recorded rationale: SF-6a
is closed by the move alone, and "removing it restores the symmetry" is withdrawn.

**What the attack changed.**

CONCEDED — the whole C11 depopulation rider, on five findings I checked and confirmed in the
files. 1. E-07 conflict is real and was never mentioned. docs/RFQ-
EEG-001_RevE_EEG_kit_specification.md:336 is priority M and reads "**Sixteen** series protection
networks ... and a 10 nF **C0G** filter to AGND_REF (C1-C16, Murata GCM1885C1H103JA16D) ...
Value confirmed at safety review". A DNP C11 makes the board non-conformant to a mandatory line
of the top-level spec, silently, in a package that raises an ECO for a 1 mm placement shift. 2.
The symmetry argument was false as I wrote it. The other fifteen DO carry a 10 nF shunt — at the
module node. What is symmetric is the position (nothing patient-side), not the presence. DNP
would have made channel 11 the only patient conductor on the board with no RF termination at
either end, with its far end an amplifier output — the node that rectifies RF into DC, which
then lands on the common mode of all sixteen channels. 3. The SF-6a claim was a non-sequitur.
Move-and-fit closes SF-6a too: RISK-EEG-011:318 rates a shorted C_n as SF-6 "no source ... Pass.
Dead channel", and at BIASOUT a shorted C11 is exactly that, with the full 47 kOhm in the
patient path. DNP bought nothing on safety that the move had not already bought. 4. The edit
instruction was incomplete in three ways, all verified. Deleting :501-503 marks nothing DNP. The
package runs TWO uncoupled DNP mechanisms — the dnp=True kwarg (design.py:34-37, used once at
:300, surfacing at :732 and emit_extras.py:145) and the literal "DNP" substring in the value
string (gerber.py:464 CPL Fit column, emit_workbooks.py:237, drawings.py:243 and :252); R89
carries both ("2k2 1% -- DNP" at :298 plus dnp=True at :300). Setting one and not the other
ships a CPL that says fit. And deleting :501-503 swaps R11's pads, which my description of the
edit did not contain. 5. The stencil finding is correct. tools/gerber.py:213-236 gates paste on
the pad's own F.Paste/B.Paste layer and has no DNP exclusion anywhere; ASM-EEG-007:372 only says
R89's feeder is not loaded. A DNP C11 would have shipped a printed aperture on two unpopulated
0603 pads bridging BIASOUT to AGND_REF. I do downgrade the attack's heading: a bead there is
SF-6, a dead bias drive, a functional fault, not the patient-current fault it is filed under.
Real, worth fixing, not a patient hazard. Scope: "a two-net change" was true of the netlist and
false of the package, as charged. The DNP would additionally have falsified "153 surface-mount,
of which 152 are fitted because R89 is DNP" in AVL-EEG-017:112, DSN-EEG-003:253, ASM-
EEG-007:196/:352/:1130, QP-EEG-010:59, SIM-EEG-018:131, simulate_production.py:416, ECO-EEG-016
C-05:1027, RFQ:515 and records/TST-EEG-004_RevC_unit_test_record.schema.json:868 — nine
documents I avoid entirely by fitting. KEPT — the core call, which the attack also verified and
did not contest. D11 must move, and it must move before the bare board is ordered. PROT row 11
at design.py:63 is (11, "BIAS_EL", "BIASOUT", ...); the generic loop puts Dn.3 and Cn.1 on dst;
:501-503 overrides only channel 11 via last-write-wins in wire() (design.py:422-424). The
arithmetic at RISK-EEG-011:306-319 stands: 183.6 uA against S-02's 50 uA, 3.7x over on bound B
and unbounded on bound A, on the one lead that reaches a forehead. "Released for review, not for
fabrication" is confirmed at RISK section 7 and section 11. The three rejected alternatives stay
rejected for the reasons given. REJECTED — the attack's own replacement. Its (b) "fit 1 nF
instead" trades one unsupported number for another: it drops the 10 kOhm isolation resistor that
the same paragraph concedes is the right configuration, names no MPN, and nothing in the package
establishes that 1 nF direct on the pin is safe where 10 nF direct is not. Its (a) "fetch the
datasheet" is right as engineering hygiene and I endorse doing it, but it does not close the
question either — the ADS1299 is on a PIEEG-8-class module (ICD-EEG-006:215, "BIASOUT is
likewise an output of the module"), the bias loop closes inside that module (BIASIN undriven on
the carrier, ICD:221), and no TI datasheet figure tells you what a third-party module's bias
output tolerates. Hence the ICD assumption row, which is a mechanism the package already uses
and neither side proposed.

**Reasoning.**

The decision splits cleanly into a half that the package settles and a half that it does not,
and the original error was answering both halves with the same confidence. The D11 half is
arithmetic, and it is already in the file. RISK-EEG-011 section 4.4 rows SF-1a and SF-6a exist
precisely because someone noticed the override, and SF-1a's own number, 183.6 uA on bound B
against S-02's 50 uA, is 3.7x a mandatory limit on a driven conductor that terminates on a
forehead. Moving the clamp to the module side makes channel 11 the sixteenth ordinary channel
and folds it into ECO-EEG-024, the fix that is already planned. Nothing in the attack touched
this and I keep it unchanged, including the timing: it is a source-and-netlist change today and
a re-spin after the first bare-board order. The C11 half is a stability question about a part
that has not been bought, and my error was to answer it by removing the component. That
converted an unknown I could not close into a certainty I could not defend: a silent breach of a
mandatory spec line, an EMC exposure on the one node whose DC offset lands on all sixteen
channels' common mode, a second and undocumented DNP in a codebase with two DNP mechanisms that
do not talk to each other, a printed stencil aperture on an unpopulated pad pair bridging the
bias drive to the analogue mid-rail, and nine documents' worth of "152 fitted" made false. All
five verified in the files. That is a worse package than the one I started with. Fitting C11 at
its specified value is the only option that closes SF-1a and SF-6a while touching no
requirement, no AVL line, no placement count and no DNP machinery. What it costs is exactly one
honest unknown, and this package has a place to put those: ICD-EEG-006 section 2.1's assumption
table, which already carries rows like ">= 25 mA on each rail" and "Inputs tolerate the series
protection resistance", each with its consequence if untrue. A BIASOUT capacitive-load row
belongs there and is conspicuously missing — the table has no row for it in either topology,
which means the current design's assumption about the bias output is undeclared too. Two things
make fitting the safe default rather than a gamble. The exposure if the assumption is wrong is
bounded and functional: an unstable rail-limited bias amp reaches the participant only through
47 kOhm, at most about 53 uA AC, inside the type BF normal-condition allowance, and it shows up
as degraded CMRR on a bench, not as a hazard on a head — and RISK section 7 already forbids any
unit going on a head before a signed safety review. And the change is reversible in the cheap
direction: depopulating a fitted cap at first article is a CPL line and an ECO with the pad
already on the board, while re-populating a part that has been deleted from E-07, the AVL and
nine placement counts is the expensive direction. The original decision's own contingency logic
pointed this way and I ran it backwards. I considered cannot-decide-here and reject it. The
attack does not show the question unanswerable; it verified the arithmetic that answers the
larger half of it, and the smaller half is answerable without a number by naming it as an
interface requirement on a module that has not been selected. Inventing 1 nF to fill the box, as
the attack's fallback proposes, is the thing this method warns against.

**Confidence:** judgement  |  **Blocks a build:** yes  |  **Signed off by:** The electrical safety reviewer of RISK-EEG-011 section 7 — the independent chartered engineer that section 7.1 defines and that section 7 records as not yet started — as the named owner of SR-12, SF-1a and SF-6a, who signs the disposition of SR-12 per section 11. Then DSN-EEG-003 Rev C's owner, because this changes the schematic, the netlist and a routed board that is released for review under RFQ-EEG-002A. The new ICD-EEG-006 section 2.1 assumption row is additionally the module-qualification owner's to accept, since it becomes a condition on a supplier not yet chosen, and it must be in the RFQ pack before any PIEEG-8-class module is qualified.

**What would change it.**

On C11's value, not its position. An ADS1299 datasheet figure, a module vendor statement, or a
first-article bench measurement on BIASOUT showing the bias amplifier peaks or oscillates into
10 nF — then depopulate C11, or drop to the 4.7 nF C0G same-series alternate that AVL-
EEG-017:149 already approves on written ECO, or fit <=1 nF behind a 10 kOhm isolation resistor
as a schematic change. All three are cheap once the pad exists, which is why the pad is
populated now. A CISPR 11 / IEC 61000-4-3 pre-scan under REG-EEG-012 section 4 showing RF
demodulating on the bias node argues the same way and argues for keeping the filter, not
removing it. Note that the pre-scan has no date anywhere in the package, so it cannot be leaned
on as a future gate. Nothing would put D11 or C11 back on BIAS_EL. The only finding that would
reopen the position is a demonstration that the ESD event at the connector, which no requirement
in RFQ-EEG-001 asks for, exceeds what the module survives through 47 kOhm — and the answer to
that is a TVS at the harness entry under ECO, not a clamp in front of the safety resistor. If
the safety reviewer prefers to close SF-1a alone and defer SF-6a, the minimal variant is to keep
lines 501-503 and re-point only D11.3 to BIASOUT. That is a one-pin change, leaves E-07 and the
amplifier loading exactly as they are today, and closes the 183.6 uA breach — at the cost of
leaving SF-6a open. It is a legitimate reviewer's call and is recorded here as such, but it is
not recommended: it preserves the special case in the source that produced this defect in the
first place.

**Files this touches:** `tools/design.py`, `tools/schematic.py`, `tools/DESIGN_FACTS.md`, `constraints/nets.md`, `kicad/EEG-CAR-01_RevB_routed.kicad_pcb`, `tools/drc_report.txt`, `docs/RISK-EEG-011_RevB_risk_analysis_and_safety_review_pack.md`, `docs/ICD-EEG-006_RevB_interface_control_document.md`, `docs/WH-EEG-008_RevB_harness_and_cable_assembly.md`, `docs/JIG-EEG-009_RevB_test_fixture_design.md`, `docs/DSN-EEG-003_RevC_manufacturing_design_package.md`, `docs/ECO-EEG-016_RevB_change_control_and_document_register.md`, `KNOWN_ISSUES.txt`


## D1-ATECC-CONFIG

**Question.** Is the proposed ATECC608B configuration-zone template (firmware/tools/ATECC608B_CONFIG_TEMPLATE.md + atecc608b_config.bin) right, and what must a security reviewer check before a part is locked?

**Decision.**

SPLIT. Adopt the template bytes unchanged. Reject the sequence ruling and replace it. KEEP — the
four bytes and the mask, verified byte-for-byte against the shipped binaries: - offset 20 =
0x81, offset 21 = 0x20 → SlotConfig[0] = 0x2081 (ReadKey = 0x1 external signatures only; NoMac
0; LimitedUse 0; EncryptRead 0; IsSecret 1; WriteKey 0x0; WriteConfig 0x2) - offset 96 = 0x33,
offset 97 = 0x00 → KeyConfig[0] = 0x0033 (Private 1; PubInfo 1; KeyType = (0x33>>2)&7 = 4 =
P-256; Lockable 1; ReqRandom/ReqAuth 0; AuthKey 0; PersistentDisable 0; X509id 0) - mask 0xFF on
exactly bytes 20, 21, 96, 97 and 0x00 on the other 124 (confirmed: mask non-zero indices are
exactly [20, 21, 96, 97]) Also keep, unchanged: reject FW-EEG-001 §7.3's GenKey-at-step-3 /
lock-at-step-8 order; reject a full 128-byte template; refuse to self-close checklist item 1
(the WriteConfig nibble must be read off the 608B's own table by a named person); ban
ATECC608B-TNGTLS; and record the J11 die marking per lot at T00 (AVL-EEG-017 M5 names "Adafruit
4314", which has carried both 608A and 608B, while ASM-EEG-007 §3 requires 608B-SSHDA). DROP —
the mandated data-zone lock as step 2d between the config lock and GenKey. Do not mandate it
now, and do not put it before GenKey. NEW ITEM 9, OPCODE ALLOCATION — blocks any write, not
merely any lock. 0x4A is double-allocated: - firmware/main/main.c:321 `CMD_READ_CALIBRATION =
0x4A`, implemented at main.c:435 and exempted from the g_prov_open gate at main.c:374-375 -
firmware/tools/provision.py:116-117 `CMD_ATECC_WRITE_CONFIG = 0x4A` / `CMD_READ_CALIBRATION =
0x4B` - docs/FW-EEG-001_RevC:470 documents 0x4A as CMD_READ_CALIBRATION — the governing document
sides with the firmware. Resolution: keep 0x4A = READ_CALIBRATION (firmware and FW-EEG-001
already agree), move provision.py's CMD_READ_CALIBRATION 0x4B → 0x4A and CMD_ATECC_WRITE_CONFIG
0x4A → 0x4B. Note 0x4B is currently occupied in provision.py, so this is a two-line swap, not a
one-line move. Re-check every new opcode against main.c's enum, never against provision.py's.
UNTIL THAT IS DONE, `provision.py --write-config --lock` IS UNSAFE ON ANY UNIT THAT HOLDS A
CALIBRATION BLOB. Verified arithmetic: write_config_zone() sends block 0 as
[0x4A][blk=0][msk[0:32]][img[0:32]] and block 3 as [0x4A][blk=3][msk[96:128]][img[96:128]]
(blocks 1 and 2 are skipped by `if not any(msk[...])`). main.c's READ_CALIBRATION reads off =
c[1] | c[2]<<8, want = c[3], i.e. block 0 → off = 0x0000, want = 0; block 3 → off = 0xFF03, want
= 255 → clamped. With "calib" present, block 0 memcpys zero bytes and block 3 trips `off >=
clen`; BOTH return status 0x00, rlen 0. write_config_zone() returns True,
rec["config_zone_written"] = True, the "STOPPING BEFORE THE LOCK" guard at provision.py:605 is
bypassed, and 0x47 irreversibly locks a FACTORY-DEFAULT configuration zone — with a record that
falsely carries the template sha256. Gate the lock on positive evidence instead of on the
write's ACK: expose an ATECC Read (opcode 0x02, zone 0, word 5 for bytes 20-23 and word 24 for
bytes 96-99), diff the four masked bytes against atecc608b_config.bin, and refuse 0x47 unless
the read-back matches. DATA-ZONE LOCK — leave as template checklist item 4, open. If a named
reviewer confirms Sign requires it, place it AFTER GenKey, after pubkey read, and after any
data-slot write: lock config → GenKey → pubkey → write data → lock data. CMD_ATECC_LOCK_DATA /
drv_atecc_lock_data() with Lock opcode 0x17, mode 0x81, param2 0x0000 is the right shape; 0x4C
is genuinely free in both tables (main.c uses 0x40-0x4A + 0x4F, provision.py 0x40-0x4B + 0x4F),
so that number survives — but take it from the table fixed in item 9. Resolve FW-EEG-001:1108
first ("writes the string unchanged into the USB iSerialNumber, the ATECC608B data zone and the
provisioning record"): the code writes NVS only (CMD_WRITE_UNIT_SERIAL →
drv_nvs_set_str("unit_serial")), so either the document is stale and must be corrected, or the
data lock must come after that write. KEEP, with a correction — extending
CMD_READ_PROVISION_STATE (0x48) to report LockValue (config byte 86 = word 21 byte 2) beside
LockConfig (byte 87) is worth doing and is wire-compatible (provision.py tests `len(state) >=
1`). It needs a named drv_atecc_data_locked() sibling reading w[2] of word 21, mirroring
drv_atecc_config_locked()'s w[3]; without it the change is not buildable as stated. ALSO
REQUIRED, found in verification and in neither the decision nor the attack: -
firmware/tools/provision_selftest.py:69-70 models the shipped firmware as one "which has no 0x4A
and no 0x4B and answers status 0x01 for both". That is false against main.c:321, so the
package's own self-test can never catch this collision — it validates a fiction. The simulator
must model the real 0x4A. - The "STOPPING BEFORE THE LOCK" guard sits INSIDE `if write_config:`,
while step 2c sits under a separate `if lock:`. So `--lock` without `--write-config` reaches the
irreversible 0x47 with no guard at all, on a zone that was never written. Guard 2c
unconditionally. - Move the NVS constants (0x44, 0x45, 0x49, 0x46, 0x4A-serial) BEFORE the
irreversible steps. They have no ATECC dependency, and main.c:381-386 refuses CMD_ENTER_PROV
once the config zone is locked, so any interruption after 2c leaves a board that cannot be re-
entered to finish. - Add an item for the absent signing path: drivers.c exposes only
genkey/pubkey/config_locked/lock_config/present — no Sign, no Nonce — and main.c:739-740 marks
the signing task "not shown". T16 cannot pass on any unit regardless of lock state, so the data-
zone-lock question should be decided together with that implementation, not ahead of it. No part
is written or locked until items 1-9 are signed by a named reviewer.

**What the attack changed.**

CONCEDED — the attack is right on every point I could check, and I verified each cited line
rather than taking it on trust. 1. The 0x4A collision is real and I confirmed all three
citations: main.c:321 defines CMD_READ_CALIBRATION = 0x4A (implemented at main.c:435, gate-
exempt at main.c:374-375); provision.py:116-117 assigns 0x4A to CMD_ATECC_WRITE_CONFIG and 0x4B
to CMD_READ_CALIBRATION; FW-EEG-001:470 documents 0x4A as READ_CALIBRATION. My original survey
("0x40-0x4B and 0x4F are taken in provision.py") checked the host table only and never opened
main.c's enum. That was the method error, and it propagated: I ratified the template's §4 claim
that "main.c has no 0x4A case", provision.py's error text "implements 0x40-0x49 and 0x4F only",
and README_provisioning.md item 7 — all three are false against this package. 2. I ran the
framing arithmetic rather than accepting the attack's word for it, and it lands exactly as
described: block 0 → off = 0x0000/want = 0; block 3 → off = 0xFF03/want = 255. Both return
status 0x00 with rlen 0 when "calib" exists, so the write silently no-ops, the guard passes, and
0x47 locks a factory-default zone. 3. I went further than the attack on reachability, which it
asserted but did not pin down. Inside a single fresh run the hazard is NOT live: provision.py
locks at 2c before writing calibration at step 7, and on a virgin part drv_nvs_get_blob("calib")
fails, so 0x4A returns status 0x06 and the run dies safely (misdiagnosed, but safe). The live
route is the ATECC swap. SVC-EEG-013 §5.8 item 1 requires a replacement J11 module to be re-
provisioned including "calibration constants, configuration-zone lock", and item 4 keeps the
TIOV-B-nnnn serial with the unit — i.e. the ESP32 and its `calib` NVS blob are retained while a
fresh, unlocked ATECC is fitted. That is precisely "calib present, config zone unlocked". TST-
EEG-004:741 routes T16 failures down the same path. Running --write-config --lock there destroys
the new breakout. So the attack's conclusion holds and is better supported than it argued. 4.
The "safe-if-wrong" ordering inference was invalid, and I concede it. On the 608 the slot
permissions are enforced against the data-zone lock state — the unlocked data zone is the
permissive one — so "GenKey permitted before the data lock" does not imply "permitted after". My
order converted checklist item 1, the WriteConfig nibble I explicitly refused to close, into an
irreversible fleet-wide dependency and deleted the fallback. Reversed. 5. Conceded: the data-
zone lock is verbatim checklist item 4 of the very document under review, not a new finding, so
there was no urgency justifying a second irreversible step in an unverified order. 6. Conceded:
FW-EEG-001:1108 does say the serial is written into the ATECC data zone. My "this design writes
no data slot" is true of the CODE (CMD_WRITE_UNIT_SERIAL lands in NVS via drv_nvs_set_str) but
the document says otherwise, and that contradiction must be resolved before any data lock, not
after. 7. Conceded: drivers.c has no Sign and no Nonce; main.c:739-740 marks the signing task
"not shown". T16 cannot pass today for reasons that precede any lock. KEPT — the attack did not
touch these, and I re-verified them independently. The four bytes and the mask: img[20,21] =
0x81,0x20 and img[96,97] = 0x33,0x00, mask non-zero at exactly [20,21,96,97]. The decode holds
bit for bit, including KeyType = (0x33>>2)&7 = 4 = P-256. LimitedUse clear stays load-bearing
(one signature per 2048 samples ≈ every 2.05 s at 1000 Hz would exhaust a monotonic counter mid-
session); PubInfo set stays load-bearing (GenKey mode 0x00 and the M-03 label fingerprint). Also
kept: rejecting FW-EEG-001 §7.3's order, rejecting a 128-byte template, refusing to self-close
item 1, banning -TNGTLS, the 0x48/LockValue extension, and the AVL/ASM die-marking item.
CORRECTED IN THE ATTACK — two places. Its fix (a) says "move CMD_ATECC_WRITE_CONFIG to 0x4B"
without noting 0x4B is already CMD_READ_CALIBRATION in provision.py; it is a two-line swap. And
its dismissal of "0x4C-0x4E are free" as "right only by luck" concedes too little to itself: I
checked both tables and 0x4C-0x4E are in fact free in each, so the LOCK_DATA number stands even
though the method that produced it was wrong. ADDED — two defects neither side caught.
provision_selftest.py:69-70 hard-codes the fiction that the shipped firmware "has no 0x4A and no
0x4B and answers status 0x01 for both", so the package's own regression test structurally cannot
catch this collision. And the "STOPPING BEFORE THE LOCK" guard is nested inside `if
write_config:` while step 2c hangs off a separate `if lock:`, so `--lock` without `--write-
config` reaches the irreversible 0x47 with no guard whatsoever.

**Reasoning.**

I treated the attack as a hypothesis and opened every file and line it cited. All of them held:
main.c:321, 374-375, 381-386, 435, 739-740; provision.py:116-117, 487, 577-612; drivers.c:431
(atecc_cmd(0x17, 0x80, 0x0000)) and 422-429 (config_locked reads w[3] = byte 87, so byte 86 =
w[2] is the right sibling for LockValue); FW-EEG-001:470 and :1108. I also independently decoded
the two binaries rather than trusting either party's transcription, and reproduced the
write_config_zone → READ_CALIBRATION framing collision numerically. The four-byte half of my
original decision survives untouched because it is checkable and I re-checked it. The sequence
half does not survive, and it fails for a reason that indicts the method rather than the
conclusion: I surveyed opcode allocation in the host tool and treated that as the allocation
table. The device is the authority on what an opcode does, and the device disagrees. Everything
downstream of that survey — "0x4A write config" in the ratified order, the claim that an absent
opcode fails safe with an unknown-opcode refusal, the confidence that the "STOPPING BEFORE THE
LOCK" guard protects the irreversible step — inherits the error. The severity turns on
reachability, so I chased it rather than asserting it. Within one run on a virgin part the
sequence is self-protecting: the lock at 2c precedes the calibration write at step 7, and with
no `calib` key drv_nvs_get_blob fails and 0x4A answers 0x06, killing the run. The hazard needs a
board whose ESP32 NVS holds a calibration blob while its ATECC is fresh and unlocked. SVC-
EEG-013 §5.8 creates exactly that state as routine service work: swap the J11 module, keep the
unit and therefore its NVS, re-provision. That makes this a live scrap path on spares that SVC
§6 stocks precisely two of, not a theoretical one. On the ordering, the attack's physics is
better than mine. The permissive state on a 608 is the unlocked data zone; the restrictive state
is the locked one, where SlotConfig.WriteConfig governs. Mandating lock-data-before-GenKey
therefore bets the whole fleet on WriteConfig = 0x2 being the correct GenKey permit — the single
nibble I had already declared unfit for me to close — and removes the fallback that would have
caught me being wrong. Ordering GenKey first costs nothing if the data lock turns out to be
required, because the lock can still follow; ordering the lock first is unrecoverable if the
nibble is wrong. That is the real safe-if-wrong direction, and it is the reverse of what I
wrote. I am not answering the underlying 608B questions here, and I should not: whether Sign
requires a locked data zone, and whether WriteConfig bit 1 is the GenKey permit, are datasheet
facts this package does not contain. My original decision leaned on "Microchip's reference
configurations" as corroboration, which is exactly the kind of half-remembered authority that
should not stand behind an irreversible step. Those stay open items for a named reviewer with
the datasheet in front of them. What I can settle from the files — the four bytes, the mask, the
opcode collision, its consequence, the guard defect, and the self-test blind spot — I have
settled. The overall question is still answerable, so this is not a cannot-decide-here: the
template's bytes are right, and the reviewer checklist is enumerable and now has a ninth item
that must be closed before anyone runs --write-config, not merely before the lock.

**Confidence:** judgement  |  **Blocks a build:** yes  |  **Signed off by:** The programme's named security reviewer, countersigned by the programme lead, against the ATECC608B datasheet — the template's own §6 says the manufacturer may not close any checklist item. The firmware coordinator must additionally sign the opcode table, because main.c and drivers.c are theirs (provision.py's own comments say so) and the collision is a device-side allocation decision, not a station one. Service engineering signs the SVC-EEG-013 §5.8 re-provisioning note, since that is the path on which the scrap case is live.

**What would change it.**

On the bytes: the 608B WriteConfig table showing bit 1 is not the GenKey permit, or that 0x2
also permits PrivWrite — either changes the nibble before any part is locked. On the sequence: a
datasheet or CryptoAuthLib check showing Sign does not require a locked data zone would retire
checklist item 4 entirely; one showing it does would schedule the lock after GenKey/pubkey/data-
write, not before. A datasheet statement that GenKey into slot 0 is permitted with the data zone
LOCKED under WriteConfig = 0x2 would be the only thing that could rehabilitate my original 2d
ordering, and it would still be the more fragile of the two. On the collision: nothing. It is
settled from the files in this package and needs a decision, not a measurement — pick one opcode
table and make main.c, provision.py, FW-EEG-001 §5, README_provisioning.md item 7,
ATECC608B_CONFIG_TEMPLATE.md §4 and provision_selftest.py's simulator agree. The measurement
that converts the rest from reasoning to fact is checklist item 8's one-part trial on a
sacrificial breakout, and it must now be run with the read-back gate in place: write the masked
bytes, READ THEM BACK from the config zone and diff before locking anything, then lock config,
GenKey, export, and verify one signature with verify_stream.py. If that trial is run before item
9 is closed, it proves nothing, because the write never reaches the part.

**Files this touches:** `firmware/main/main.c`, `firmware/main/drivers.c`, `firmware/main/drivers.h`, `firmware/tools/provision.py`, `firmware/tools/provision_selftest.py`, `firmware/tools/ATECC608B_CONFIG_TEMPLATE.md`, `firmware/tools/README_provisioning.md`, `docs/FW-EEG-001_RevC_firmware_build_and_provisioning.md`, `docs/TST-EEG-004_RevC_production_test_specification.md`, `docs/SVC-EEG-013_RevB_service_and_refurbishment_manual.md`, `docs/ASM-EEG-007_RevB_assembly_work_instructions.md`, `docs/AVL-EEG-017_RevB_approved_vendor_list.md`, `KNOWN_ISSUES.txt`


---

# Does not block a build


## D1-FIX02D-THRESHOLD

**Question.** FIX-02/D comparator threshold: section 2.3 says "threshold at 50 % of the commanded amplitude" and never fixes a voltage. Fixed divider or commanded threshold, and what values?

**Decision.**

Commanded threshold, built as follows. PWM. RP2040 slice on GP15, sysclk 125.0 MHz,
pwm_set_wrap(slice, 999). TOP = 999 gives a 1000-count period, f = 125.000 kHz exactly, duty =
CC/1000, and CC = 1000 is full scale. (TOP = 1000 was wrong: the RP2040 counter runs 0..TOP
inclusive, so the period is TOP+1.) Network. R203 = 10.0 kOhm from GP15 to the threshold node;
R204 = 10.0 kOhm from the node to M2 ground; C201 = 220 nF 50 V X7R 0603 across R204; node to
U201's inverting input. R205 = 10.0 kOhm from RL201 hot (left channel, the same node as the §2.1
BNC monitor) to U201's non-inverting input. Full-scale threshold = 3.300 x 10.0/20.0 = 1.6500 V,
1.650 mV per count. All three resistors are Vishay TNPW060310K0BEEA, already approved in this
package (AVL-EEG-017 row 126; JIG-EEG-009 RB1-RB16 and RP1). Zero constructed order codes: the
one distributor confirmation the original decision needed, and that the attack's own correction
also needed, is not needed at all. §2.3's three criteria re-checked. Settling: tau = (10.0k ||
10.0k) x 220 nF = 1.100 ms, 1 % settling at 4.605 tau = 5.07 ms against the 10 ms limit, 1.97x.
Ripple: pp = 3.3 x D(1-D)/(f.R203.C201) = 3.3 D(1-D)/275 = 12.0 D(1-D) mV; against 1 % of a 1650
D mV threshold this is 0.727 %(1-D), worst case 0.727 % as D goes to zero — inside 1 % at every
setting with 27 % margin, and better than either the original 0.91 % or the correction's 0.80 %.
Frequency: 125.0 kHz is 125x — 2.10 decades, not three — above T12b's 1 kHz burst (TST-EEG-004
line 676), which is still far enough that nothing aliases into the marker. Range. 0 to 1.650 V
covers 50 % of a burst up to 3.30 V pk at the 47.0 Ohm load. That bounds every case the package
permits: a headphone amplifier on the 5.0 V V5V rail of J8.14 cannot exceed about 2.5 V pk; the
ICD's fallback 10k/1k HP_L-to-HP_GND tap (divide-by-11) with HP_L at 2.4 V pk needs 1.2 V and
fits with 27 % to spare; and the package's own ~110 dB SPL full scale into the 47 Ohm ATH-M20x
(~1.5 V pk, threshold ~770 mV) fits. The document's stated 330-2970 mV range is still rejected —
it reaches none of the required thresholds. Verb. `THR MV <millivolts, 0..1650>`, replying `OK
THR mv=NNNN permille=NNN`. The same ECO must strike `THR <per mille of the rail>` at JIG-EEG-009
line 876 and `THR <per mille of the 3.300 V rail>` at line 1649, so no host tool can be written
to the old meaning. Power-on default THR MV 165, not zero, so fix_m2.c's "marker is already
high" path does not refuse every burst on a freshly booted fixture. Also state, because a
builder cannot infer them: GP15 for the PWM (free pins are 0, 1, 12, 13, 14, 15; reserve
GP12-GP14 for the §8.8 I2S transmitter and GP0/GP1 for UART); R205's far end on RL201 hot; and
that J27.3 HP_GND is bonded to M2 ground, which the single-supply comparator and the ground-
referenced threshold both require. §2.4's BOM gains four lines, not the "one resistor and one
capacitor" §2.3 estimates. 1.650 mV per count is setting granularity, not accuracy: the 3.3 V
rail tolerance and the GPIO output resistance (330 uA x ~100 Ohm = ~33 mV, ~2 % of full scale)
set accuracy, and 2 % of threshold on a 1 kHz burst is about 2 us of onset error against T12b's
1 ms sample grid. Operationally. At first article for each headphone-amplifier model, measure
the burst amplitude across RL201 with the oscilloscope at the resistor body — not "4-wire",
which is §2.1's resistance method for the 47.0 Ohm value itself — at the level T12b actually
commands, with the E-29 clamp in whatever state it is in at T12, which today is unset. Set THR
to 50 % of the measured value. Record per model and re-measure at the 6-month FIX-02
calibration. NOT closed, and deliberately left open rather than filled with a number: the
coupler-drive electrical onset for the VOICE_PRE and ROOM_PRE channels. No fitted values, no
second range.

**What the attack changed.**

Conceded, all six verified against the files: 1. The span. Confirmed at ICD-EEG-006 §2.3 (lines
~400-407): HP_TAP "must present between 0.1 and 1.1 V peak", and "If the module offers no tap,
build one inside the JMP-08 module-end assembly as a 10 kOhm / 1 kOhm divider from HP_L to
HP_GND". That is a divide-by-11, so a compliant HP_TAP does not bound the 47.0 Ohm load at all.
TST-EEG-004 T12a confirms the same: "drive each source to produce a 1.1 V peak envelope ...
channel 1 HP_TAP via J8.10, channel 2 VOICE_PRE ..., channel 3 ROOM_PRE" — 1.1 V pk is a
property of the envelope-chain input, and it applies to two channels that are not the headphone
at all. The 659 mV span was derived from a bound that does not exist. Conceded in full; this is
the half of the answer that sets R203 and R204. 2. 110 dB SPL. FW-EEG-001 line 1043 says it
explicitly of "the fitted codec and a 47 Ohm load". At the ATH-M20x's published 96 dB/mW that is
~25 mW, 1.09 Vrms, 1.54 V pk, threshold ~770 mV — already above the 659 mV I proposed. Conceded.
3. The 10 dB derating. Confirmed: TST T6 "runs after the characterisation steps; only T5a and
T30a precede it" (line 572), T28 writes "a deliberate full-scale write to the codec volume
register that bypasses the runner's own limit" (line 919), and FW-EEG-001 open item 15 (line
1372) records "The E-29 acoustic clamp is not implemented ... the codec driver is a stub". The
0.316 x 1.1 = 348 mV rescue describes a state the unit is not in at T12. Conceded, and dropped
from the procedure. 4. wrap. Conceded. TOP = 999, not 1000. 5. 125 kHz / 1 kHz = 125 = 2.10
decades, not three. Conceded as a figure; the conclusion stands. 6. The verb collision.
Confirmed verbatim at JIG lines 876 and 1649. Conceded — the unit now names itself on the wire
and both lines are edited in the same change. Also conceded from the correction's tail: the GPIO
number, R205's far end, the HP_GND bond, the non-zero power-on default, four BOM lines not two,
and "4-wire" being the wrong method word. Point 7 (ripple margin 0.91 % not 0.86 %) is correct
and I have adopted the D-to-zero worst case as the way to state it; it was never a failure, and
the new values improve it to 0.727 %. Point 8 is right that §2.3's source list is "47 Ohm load /
coupler drive --> U201" and that T12b reports per envelope channel with FIX-02/A and /B in the
fixture list — three channels, one comparator, no selector, no level for the coupler drive
anywhere. I concede the gap and refuse to fill it (below). Kept against the attack, on the
files: A. Its own correction is not the best answer and repeats the defect it names. R203 = R204
= 20.0 kOhm forces TNPW060320K0BEEA, a constructed order code needing the distributor
confirmation it criticises. 10.0 kOhm twice is TNPW060310K0BEEA, which is genuinely already in
the package (AVL row 126, JIG lines 539 and 545), gives the same 1.6500 V full scale, and has a
better ripple margin (0.727 % vs 0.800 %). Settling is 5.07 ms vs 4.61 ms — both inside 10 ms.
B. Its proposed second range fails its own criterion, on its own arithmetic. R206 = 4.99 kOhm
"from the threshold node to M2 ground" sits in parallel with its 20.0 kOhm R204: 20k || 4.99k =
3.9936k, so full scale is 3.3 x 3.9936/23.9936 = 549 mV at 0.549 mV per count, not "0-659 mV at
0.659 mV per count" — that figure treats 4.99k as the sole bottom leg. Worse, relative ripple
scales inversely with the span: 3.3(1-D)/(0.549 x 125k x 20k x 100n) = 2.40 %(1-D), i.e. 2.4x
over the 1 % criterion it re-checks its main range against. A lower range needs more R203.C, not
a smaller R204. Rejected, and the coupler half is left open instead. C. "Add it to the pin map
that tools/fixture_gen.py --check reads" is not actionable. That check (tools/fixture_gen.py
lines 1482-1513) covers FIX-01/M1 and FIX-04/M3 only, because those are the two boards with
netlists. FIX-02 has no released board data at all (§8.8: "Board data, at fixtures/pcb/FIX-01/
and fixtures/pcb/FIX-04/"), so there is nothing to compare against. GP15 goes in hal_rp2040.c
and in JIG §2.3; extending --check to FIX-02 needs a FIX-02 netlist first. D. "A resistor change
on a board already in the enclosure" overstates the recovery cost. FIX-02/D has no PCB in this
package — §2.4 is a discrete BOM in a Hammond 1590B. It is a hand-wired change, not a re-cut.
The consequence it describes is real; the cost is smaller. E. Everything the attack listed as
surviving does survive: the commanded route, R204/R205 as package parts, the TNPW0603
construction rule, C201 as an unqualified X7R setting tau only, and R205 with the negative half-
cycle clamped.

**Reasoning.**

The attack broke the range argument and nothing else structural, and the range is what sets the
two resistors. HP_TAP <= 1.1 V pk is a spec on a tap that the ICD itself permits to be a divide-
by-11, so it never bounded the 47.0 Ohm load; the package's own ~110 dB SPL figure into 47 Ohm
puts the load above 1.1 V pk independently; and the 10 dB E-29 derating I leaned on is not in
force at T12, because T6 writes constants after the characterisation steps and the clamp is not
implemented. Three independent reasons the 659 mV span is too small, any one of which is enough.
The defensible bound is not a measurement but a ceiling: a headphone amplifier fed from the 5.0
V V5V rail of J8.14 cannot put more than about 2.5 V pk across the load, so a 0-1.650 V
threshold (50 % of 3.30 V pk) covers every case the package permits, including the divide-by-11
tap case at 1.2 V, with 27 % to spare. That is the smallest span that is honestly safe, and a
span is the one thing here that should be sized to the worst permitted case rather than to a
typical one, because being short is uncommissionable and being long only costs resolution the
measurement does not need. Choosing 10.0 kOhm twice instead of 20.0 kOhm twice is not cosmetic.
It hits the same 1.6500 V, improves the ripple worst case, and removes the last constructed part
number from this decision — the package's own recurring failure mode is order codes nobody
confirmed, and this closes one instead of adding one. The coupler-drive half is where I stop.
§2.3's source list really does feed "47 Ohm load / coupler drive" into one comparator, T12b
really does report per envelope channel, and no document states the coupler drive in volts — it
is a per-coupler constant set at calibration to give 70.0 dB SPL, and no coupler has been built
or calibrated. A second range cannot be dimensioned without that number, and the attack's
attempt to dimension one produces a network that violates the ripple criterion by 2.4x. The
right answer is to say so and to measure it at first coupler calibration, not to fit a switched
resistor to a guess. The open item in §7 is scoped to FIX-02/D, which is the 47 Ohm head, so the
question as asked is answered; the coupler channels are an adjacent gap that this decision names
rather than papers over.

**Confidence:** derived  |  **Blocks a build:** no  |  **Signed off by:** The FIX-02 fixture designer jointly with the TST-EEG-004 owner — JIG-EEG-009 §2.3 and §7 name them both, because T12b's burst level is theirs to define and this threshold sets a per-unit group-delay constant that ships in the device and is subtracted from the study's latency data. Plus the schematic and safety reviewer for the J27.3 HP_GND-to-M2-ground bond, which bridges the DUT's audio ground to the fixture and host side and sits alongside the marker's existing DC path into SPARE1 (§2.3's 41.8 uA single-fault case). Plus the JIG-EEG-009 document owner for the FIXPROTO verb change at lines 876 and 1649.

**What would change it.**

A measured burst above 3.30 V pk at the 47.0 Ohm load — which would need a headphone amplifier
on more than the 5.0 V of J8.14 — pushes past the 1.650 V full scale; R204 then goes to 20.0
kOhm for a 2.200 V span and C201 to 100 nF to hold the ripple criterion. A TLV3201 datasheet
showing the fitted part's supply range does not cover 3.3 V, or an output drop at the 1.000 mA
of §2.3 that is not small against the rail, changes the marker rail and this divider with it —
that is the confirmation §2.3 already asks for. A T12b burst level fixed by TST-EEG-004's owner
materially below full scale would narrow the required range and permit a finer span. And the
first measured coupler drive level, taken when a FIX-02/A or /B coupler is first calibrated to
70.0 dB SPL, is what closes the voice and room half — until then no second range should be
fitted.

**Files this touches:** `docs/JIG-EEG-009_RevB_test_fixture_design.md`, `fixtures/firmware/src/fix_m2.c`, `fixtures/firmware/include/fixproto.h`, `fixtures/firmware/include/fixhal.h`, `fixtures/firmware/src/hal_rp2040.c`, `docs/TST-EEG-004_RevC_production_test_specification.md`, `docs/ECO-EEG-016_RevB_change_control_and_document_register.md`


## D4-FIRMWARE-TIMING

**Question.** RELAY_SETTLE_MS = 10 and the other firmware timing constants that are stated rather than measured.

**Decision.**

VALUES, all kept from the original decision except the host-contract line: 1. RELAY_SETTLE_MS =
20 ms, in fix_m1.c:34 and fix_m3.c:31. Unchanged from the decision. Verified harmless: 10 -> 20
alone leaves the suite at 154 checks, 0 failures, PASS. 2. HV_DISCHARGE_MS = 5000 ms,
fix_m3.c:38. Unchanged, not raised, not lowered. 3. SELFTEST ARM timeout = 300 s. Unchanged. 4.
TCS34725 PON-to-AEN = 5 ms (was 3 ms), fix_m1.c:472. Unchanged from the decision. 5. COL READ
stops sleeping blind, as decided, with the ambiguity resolved: clear AEN, re-enable AEN,
hal_sleep_ms(320), then poll STATUS (0x13) for AVALID with hal_sleep_ms(1) between reads; ERR
COL 10 TIMEOUT if AVALID is not set within 400 ms MEASURED FROM THE AEN RISING EDGE, i.e. 80 ms
of slack past the 320 ms wait. No extra PON warm-up is needed on the AEN toggle because PON
stays set. WHAT THE FINAL CALL CHANGES AGAINST THE ORIGINAL DECISION: 6. Section 8.2's 2 s rule
is NOT restated. The decision's "2 s since the last line received" is withdrawn. Instead JIG-
EEG-009 section 8.2 gains the sentence its parent already has: "Long operations are given 20 s,
as FW-EEG-001 section 6.2 gives CMD_TIMING_SELFTEST and CMD_ATECC_GENKEY. SELFTEST RELAYS is the
one command in this protocol that needs it: 96 readings at RELAY_SETTLE_MS plus a flushed # line
each is about 2 s against a 20 s budget. BURST blocks up to 1 s waiting for the comparator edge
and stays inside the 2 s rule." Section 8.4's SELFTEST row and the ARM reply say "long
operation, 20 s host budget". 7. The COL READ justification is rewritten. The defect is
provenance, not phase: the sensor free-runs from COL INIT, so the blind
hal_sleep_ms(TCS_INTEG_MS + 10) returns whichever 300 ms window last completed, up to ~310 ms
before the command. On section 1.7's indexed carrier (one detent per site) a COL READ issued
after moving to the next site can return a frame belonging to the previous site, with no error
and no way to tell. The phase argument is deleted: section 1.7's 72 whole periods make the ratio
start-independent for any 300 ms window, and the amber state is not codeable in this build
anyway. 8. hal_sim.c must model STATUS: set tcs[0x13] |= 0x01 when the firmware writes ENABLE
with AEN set, clear it when AEN is cleared. Load-bearing, not optional. 9. hal_sim.c:13 "9.6 s
of relay settling" becomes 1.92 s. 10. "to 50 V" is dropped from the discharge measurement. It
is written as "record the tester's specified discharge time and the measured time for the output
to fall below the touch-safe limit its own manual states", which is what section 8.7 and
fix_m3.c:33-37 already ask for. 11. Section 8.4's "two latch events per change" is qualified to
exclude the SELFTEST sweep, which does channel_open + relay_set + ONE hal_sr_write. Standing as
written: the direction of the constant, the rejection of leaving it at 10, of making it
operator-configurable, and of splitting SELFTEST into sixteen commands; and the bring-up
measurement (scope one contact, operate/release/bounce, coil driven from a TPIC6B595 drain).

**What the attack changed.**

CONCEDED (all verified against the files, not taken on trust): - Point 1, the host contract. FW-
EEG-001 RevC line 1007 reads "Long operations (CMD_TIMING_SELFTEST, CMD_ATECC_GENKEY) are given
20 s." JIG section 8.2 quoted only the first sentence and then said the rule "is FW-EEG-001
section 6.2's rule and is reused rather than reinvented". The parent already has the carve-out
and the exemplar is literally a self-test. Section 8.2's own table says Informational "# ..." is
"**never** a response", and fixproto.c:62-72 shows fx_info() emits "# %s", so all 96 RLYREAD
lines are # lines: the decision's "2 s since the last line received" would have made # lines
liveness-bearing, forked a shared rule, and let a fixture wedged in a #-emitting loop never trip
the timeout. Fully conceded, and this is the single biggest change. - Point 2, the COL READ
rationale. Section 1.7 says 300 ms is 72 whole 4.1667 ms phase periods "so the amber ratio does
not depend on where the integration window happens to start". That IS start-independence, and it
holds for any 300 ms window; the decision had it backwards. Section 1.7 also says the bicolour
phase scheme "is specified and not yet coded", so the amber state cannot be exercised at all.
Void twice over. Rationale replaced, fix kept. - Point 3, the breakage. Reproduced exactly.
HEAD: 74 + 29 + 51 = 154, PASS. Decision applied verbatim: "FAIL a read returns all four
channels" and "FAIL and the ratio in per mille", 74 checks 2 failures. Cause confirmed at
hal_sim.c:130-145 — tcs[] is 32 bytes, tcs_init_once() writes only 0x12 and 0x14-0x1B, STATUS
0x13 is never set and the firmware never writes it, so AVALID is permanently 0. I then applied
the attack's own fix and got 154 checks, 0 failures, PASS. Conceded and adopted. - Point 4, the
overhead. hal_rp2040.c:126-131 does fputs + fputc + fflush(stdout) per line, on
CMakeLists.txt:46-47 pico_enable_stdio_usb(1) / stdio_uart(0). 96 flushed lines over USB CDC on
1 ms frames is order 100 ms that the 96 x 20.2 ms estimate omits. The sweep at 20 ms is ~2.03 s,
not "inside a whisker" of 2 s — it is over it. This makes the section 8.2 change load-bearing
rather than cosmetic, and makes the attack's version of it the only one that works. - Point 5.
hal_sim.c:13 says "a self-test that costs 9.6 s of relay settling on hardware". The sweep is 16
x 6 = 96 sleeps; at 10 ms that is 0.96 s. Wrong by 10x already, 1.92 s at 20 ms. Conceded. -
Point 6(a). "within 400 ms" was genuinely ambiguous — I had to pick a reading to reproduce the
failure. Pinned to "from the AEN rising edge". - Point 6(b). Grepped the package: "50 V" appears
only as a capacitor voltage rating (AVL-EEG-017, ECO-EEG-019, ASM). Section 8.7 and
fix_m3.c:33-37 say the number to check is the tester's own discharge specification. A decision
whose premise is that stated numbers need sources had introduced an unsourced one. Conceded. -
Point 7. fix_m1.c:406-412 — the sweep does channel_open(n), relay_set(n, m), then ONE
hal_sr_write. Release of the old and operate of the new ride the same latch edge. Section 8.4's
blanket "two latch events per change" does not describe the sweep. Harmless there (fx_role_safe
first, source OFF, RP1 only) but the caveat is real and caps what the constant buys in that
loop. REJECTED, because the attack is wrong: - Point 3's accusation that "The decision names two
source files and one document line. It does not name hal_sim.c." FALSE. hal_sim.c is the THIRD
of the five entries in files_to_update, and host_test.c is the fourth. The demonstrated breakage
is real and I reproduced it; the file-list charge is not. What the decision actually failed to
do was say WHAT has to change in hal_sim.c — a smaller and different fault. Point 5 carries the
same false premise. - Point 1's parenthetical "SELFTEST RELAYS is the only one in this
protocol". Overstated. fix_m2.c:39 sets BURST_WAIT_US = 1000000ull and fix_m2.c:216-224 blocks
on it waiting for the comparator edge, so BURST can take up to 1 s to answer. It stays inside
the 2 s rule so it does not need the 20 s budget, but the sentence going into section 8.2 must
not claim SELFTEST is the only long-running command. I have reworded it. - Point 6(c)'s
replacement arithmetic. The attack is right that "500 time constants" is a hand-wave, but its
own "~100 kOhm into ~1 nF, tau ~100 us, 50,000 tau" is equally unsourced. I keep the conclusion
— delete the tau claim — not the substitute number. The package already names the right
quantity. NOT FOUND BY EITHER SIDE: the "154 checks" figure is stated in five places —
fixtures/firmware/README.md:51 and JIG-EEG-009 lines 1368, 1438, 1691 and 1805. With the
hal_sim.c STATUS fix the count stays 154, so nothing moves. But if host_test.c gains checks for
the new TIMEOUT path (it should), all five must move together or the package contradicts its own
run evidence.

**Reasoning.**

The core call survives the attack intact and I re-derived it rather than inheriting it. The
relay is an Omron G6K-2F-Y DC5 (section 1.8) driven by a TI TPIC6B595DW described in the same
row as "150 mA open-drain, clamped". A clamped coil is precisely the flyback condition datasheet
release times are not measured under, and a clamp routinely doubles or triples release, so a ~3
ms catalogue release becomes 6-9 ms in this circuit. chain_push() at fix_m1.c:117-121 writes
then sleeps, and cmd_ch at fix_m1.c:227-231 calls it twice — all-open, settle, target, settle —
so the first sleep is exactly the one that must cover release. 10 ms sits inside the fitted
part's own uncertainty; 20 ms does not. The cost is countable and nil: a CHALL is two latch
writes, 40 ms, against section 1.1's six-minute parallel T7. The cost of being too fast is a
make-before-break in a ratio leg, which is the one thing the 1000:1 divider cannot tolerate. The
datasheet is not in the package, so this stays judgement, not derivation — but the direction is
derived and the attack conceded it. Where the attack won, it won on evidence I could re-run. The
decisive one is that the decision's section 8.2 rewrite was not merely unnecessary but harmful:
it would have forked a rule the document says is reused, made "#" lines liveness-bearing against
section 8.2's own "never a response", and weakened the timeout — all to buy 60 ms of headroom
that point 4 shows does not even exist, since the flushes push the sweep past 2 s anyway. The
parent contract already grants 20 s to exactly this class of command. Importing that is strictly
better than restating anything. The COL READ case is the interesting one, because the fix is
right and the reason was wrong. Section 1.7's integer-periods construction is a start-
independence property; citing it as the thing a free-running window defeats inverts it. But the
change still earns its place on a different and stronger argument: the sensor free-runs from COL
INIT, the blind 310 ms sleep returns whichever window last completed, and with one indexed
detent per site a READ taken after moving the carrier can silently return the previous site's
frame. That is a wrong-number-with-no-error failure on the one fixture item that has to be
calibrated. Clearing AEN is also mechanically necessary, not decorative: AVALID on a free-
running part is already set, so polling alone would return a stale frame instantly. I set
needs_human_signoff true where the original decision left it null. fix_m3.c is the firmware of
the FIX-04 card that switches 500 V DC through the WH-EEG-008 H4 and H10 tests; section 8.7
calls it "the only fixture in the set that switches a voltage that can kill". Editing a timing
constant in that file is not a thing one person does quietly, even though HV_DISCHARGE_MS itself
is untouched. Section 8.2 is released Rev B text shared with FW-EEG-001, so it moves under
change control. And the COL READ redesign changes what the package's only run evidence actually
covers. blocks_a_build is false. These are shop-floor fixtures, not the product; section 8.8
already says nothing has been built, printed, fabricated or measured; and the constant has an
obvious safe default which is the one being adopted. A manufacturer can build a fixture with 20
ms compiled in and nothing about the kit's fabrication waits on this.

**Confidence:** judgement  |  **Blocks a build:** no  |  **Signed off by:** The JIG-EEG-009 owner (test engineering lead) signs the firmware constants and the section 8.2 / 8.4 text, routed as an ECO in ECO-EEG-016 because both sections are released Rev B text and section 8.2 restates a rule shared with FW-EEG-001 section 6.2. The electrical-safety reviewer countersigns the fix_m3.c edit specifically, because that file is the 500 V card's interlock firmware (section 8.7) even though HV_DISCHARGE_MS is unchanged. The FW-EEG-001 owner is notified rather than asked to sign, since the change imports their rule instead of forking it.

**What would change it.**

A scoped release time on the fitted Omron G6K-2F-Y with the coil driven from a TPIC6B595 drain
and clamped, recording operate, release and bounce: under 6 ms allows 15 ms, and two independent
measurements allow 10 ms. Anything at or above 10 ms holds 20 ms or raises it. A measured
discharge time on the fitted MIT525-class tester longer than 5 s raises HV_DISCHARGE_MS, and
that measurement must happen before the first WH-EEG-008 H4. A measured TCS34725 window longer
than 400 ms from the AEN rising edge (oscillator tolerance on 125 steps of 2.4 ms) moves the
poll bound off 400 ms. And a measured SELFTEST RELAYS wall time on real USB CDC settles the
"about 2 s" in the new section 8.2 sentence; if it exceeds ~3 s the sentence must carry the
measured figure rather than an estimate. If host_test.c gains checks for the new TIMEOUT path,
the "154" in all five places moves with it.

**Files this touches:** `fixtures/firmware/src/fix_m1.c`, `fixtures/firmware/src/fix_m3.c`, `fixtures/firmware/test/hal_sim.c`, `fixtures/firmware/test/host_test.c`, `docs/JIG-EEG-009_RevB_test_fixture_design.md`, `docs/ECO-EEG-016_RevB_change_control_and_document_register.md`, `fixtures/firmware/README.md`


## D6-FIX04-OUTLINE

**Question.** The FIX-04 scanner card outline, priced at EUR 40 in section 6.1 and never dimensioned.

**Decision.**

RATIFY THE OUTLINE, DELETE THE RELAY GRID, PROPAGATE THE PRICE, AND FIX THE ACCEPTANCE NUMBER.
1. OUTLINE — write into JIG-EEG-009 section 4.1, matching section 1.9's treatment of FIX-01:
"120.0 x 80.0 mm, two-layer FR-4 Tg >= 150 C, 1.60 mm, 1 oz copper, ENIG, green mask, white
legend both sides, IPC-6012 class 2 and IPC-A-600 class 2, minimum track and clearance 0.20 /
0.20 mm. Four M3 non-plated holes, 3.2 mm finished, at (5, 5), (115, 5), (5, 75), (115, 75), 6.0
mm keep-out. Origin bottom-left, Y up. Zones: scanner matrix x 0.0-85.0, logic and entry x
85.0-120.0, y 0.0-80.0 both." Every value is read back from the released FIX-04-Edge_Cuts.gbr
and FIX-04-NPTH.drl. Nothing is invented and nothing is re-cut. Then close the provenance loop,
or the fix is half-applied: - fixture_gen.py:119 — source="JIG-EEG-009 section 4.1" (FIX01's
pattern at :86); delete the "NOT in JIG-EEG-009" comment at :107. - Re-run `python3
tools/fixture_gen.py --pcb`; update fixtures/MANIFEST.json bytes+sha256 for
FIX-04_constraints.txt and README_fixture_pcb_data.txt. The four artwork/drill files do NOT
change and must not be listed as changing: the zone note is a constraints-file string, not
printed to F_Silkscreen (only `cap` is), and Zoning.gbr draws rectangles only. - Regenerate JIG-
EEG-009_RevB.{docx,pdf} via tools/make_docs.py / finalise_docs.py. 2. RELAY GRID — do NOT
mandate one. Not four columns of six, not four rows of six, not five of five. Replace
fixture_gen.py:122 with "24 DPDT relays, grid set at layout (constraints section 5 d),
instrument bus and common bus", and add to the constraints file as rule 5(d): "Column pitch is
land width + 3.0 mm and ROW pitch is land height + 3.0 mm: rule 5(a) binds every 500 V conductor
pair, including the NO pads of vertically adjacent relays, so the creepage is charged on BOTH
axes. The usable relay band is x 0.0-85.0 by y 10.6-80.0 (69.4 mm), not the full zone: J401,
J402, J403 and J407 sit at y = 6.0 with footprints spanning x 6.4-86.14, y 4.4-7.6, and 3.0 mm
of creepage must stand off them. The M3 keep-outs at (5, 5) and (5, 75) take both left-column
corners. At the assumed 10.0 x 7.0 mm envelope any of the candidate grids closes; six across by
four up needs 78.0 x 40.0 mm and has 7.0 mm and 29.4 mm to spare. The land the grid can carry,
at the 10:7 aspect assumed here: six columns of four, up to 11.2 x 7.8 mm; four columns of six,
up to 12.2 x 8.6 mm; five columns of five, up to 14.0 x 9.8 mm. Five columns of five carries the
largest part and is the grid to reach for if the datasheet is big; it is not fixed here. The
grid is chosen when the Omron G6K-2F-Y datasheet is opened." 3. ACCEPTANCE NUMBER — 160.8 mm2
must NOT be quoted in section 4.1 as the figure to check the datasheet against. It comes from
area_budget(), which charges no creepage. Once rule 5(a) is charged on both axes the binding
limit is grid fit, and the best grid caps the land at about 137 mm2 (14.0 x 9.8 mm). Section 4.1
states 137 mm2 / 14.0 x 9.8 mm as the acceptance limit and names 160.8 mm2 as the area-only
figure it supersedes on this board. 4. PRICE — EUR 72, and all five dependents move in the same
edit: FIX-04 materials subtotal 372 -> 404; FIX-04 fixture total 757 -> 789; "FIX-01 + FIX-02 +
FIX-03 + FIX-04" 3 095 -> 3 127; "One fixture set, materials and labour" 3 465 -> 3 497; "One
fixture set including programme-specific instruments" 5 145 -> 5 177. Basis, in the section's
own idiom: "FIX-01's five-off line is EUR 120 for a 160.0 x 100.0 mm board, EUR 0.15 per cm2 of
finished board; 120.0 x 80.0 mm at the same rate is EUR 72. A five-off ENIG order is setup-
dominated, so 72 is the floor if the board is ordered alone and FIX-01's 120 is the practical
ceiling; section 6.3 already runs both boards through one 15-day layout leg and one 10-day
fabrication leg, and ordered on that one setup the incremental cost is area-proportional, which
is why 72 and not a figure in between. EUR 40 was below the floor." 5. LOG, do not settle here:
a G6K-class signal relay's own COM-to-NO pin spacing is well under 3.0 mm, so rule 5(a) as
written cannot be met inside the relay package. Either 5(a) is a board-level rule about inter-
device conductors, or the relay is not rated for the 500 V duty. This is an operator-safety
question on the one fixture where a flashover reaches a person, and it belongs to the safety
review, not to this decision.

**What the attack changed.**

CONCEDED — the attack is right on the substance, and I verified each claim in the files rather
than taking it. - The relay rule is deleted. `grep -rn "12\.4" docs/ tools/ fixtures/` returns
HM-04 the electrode body (mech_gen.py:551, RUL-EEG-021:84, PARTS-EEG-019:240) and nothing else.
The package's only relay figure is fixture_gen.py:137 `RELAY_ENV_MM2 = 10.0 * 7.0`, flagged
ASSUMED. My 12.4 mm land was fabricated, and 10.6 mm was the short side of the maximum-carryable
envelope, not a part. Mandating a grid on that is the exact failure fixture_gen.py:131-136 and
section 8.8 spend paragraphs refusing. - "Four rows of six does not fit" was wrong. At the
package's own 10.0 x 7.0, six across is 6 x 13.0 = 78.0 mm in an 85.0 mm zone and four up is 4 x
10.0 = 40.0 mm. It fits with 7.0 mm spare. My 92.4 mm only existed because of the invented 12.4.
- My own prescription was unbuildable. I charged 3.0 mm creepage on the column pitch and nothing
on the row pitch, but rule 5(a) in FIX-04_constraints.txt:63-69 says the relay common and NO
contacts keep 3.0 mm "to every other conductor" — which is exactly what relay N's NO pad and
relay N+1's NO pad are. Charged consistently, four columns of six is 6 x 13.6 = 81.6 mm of
height in an 80.0 mm board. It fails by 1.6 mm on the board and by 12.2 mm on the usable band. -
The scanner zone's bottom strip is occupied. CONNECTORS["FIX-04"] puts J401, J402, J403 and J407
at y = 6.0, and fixture_gen.py:521 draws each footprint (x-1.6, y-1.6) to (x+(ways-1)*2.54+1.6,
y+1.6). "Room to spare" was measured against a zone that is not free. - The price change was
half an edit. Section 6.1's FIX-04 column really does sum 40+55+12+40+45+20+20+140 = 372 -> 757
-> 3 095 -> 3 465 -> 5 145, in the same section that says a BOM that quietly does not add up is
worse than one that is three euro out. Changing one cell and no totals was that failure. - The
rate argument contradicted itself. I argued setup dominance makes a small board more than area-
proportional, then priced it exactly area-proportionally. Now resolved on a real mechanism —
section 6.3 already puts both boards on one layout-and-fabrication leg, so the shared setup is
what makes 72 the figure rather than a floor. - The premise was overstated. Section 4.1 does say
"its board data is released at `fixtures/pcb/FIX-04/` on the same terms as FIX-01's", and RFQ-
EEG-001 section 10 (line 679) is one line for the whole set, not a per-PCB line. No bidder is
guessing at a board size. The defect is the asymmetry with section 1.9, which is worth fixing on
its own. - The fix would have created the contradiction it claimed to remove. Writing 120 x 80
into 4.1 while fixture_gen.py:119 still says "JIG-EEG-009 section 4.1 gives the card no outline"
leaves that sentence printed at FIX-04_constraints.txt:20, in the file a layout contractor is
handed. Editing only the .md repeats the stale-rendition defect KNOWN_ISSUES.txt:291 already
logs against TST-EEG-004 Rev C. KEPT — the outline, unchanged. 120.0 x 80.0 mm is in the
released Gerber, the four M3 positions are in the released drill file, and the section 1.9 /
section 4.1 asymmetry is a real hole worth closing. Keeping FIX-04 undimensioned in the document
while FIX-01 gets a full outline section is not defensible, and neither the attack nor I dispute
that. KEPT — the price correction and the EUR 72 figure. The attack broke my reasoning for it,
not the number. THE ATTACK'S OWN ERRORS, corrected rather than copied: - J401 spans x 6.4-37.54,
not 8.0-35.94; the attack dropped the 1.6 mm footprint margin fixture_gen.py:521 adds. J407's
footprint reaches x 86.14 and crosses into the logic zone. Occupied strip is x 6.4-86.14, so the
usable band starts at y 10.6 once 3.0 mm of creepage stands off it, giving 69.4 mm and not the
attack's "roughly 70". - Source line is FIX-04_constraints.txt:20, not 24; RELAY_ENV_MM2 is
fixture_gen.py:137, not 135; source= is :119, not :115. - The attack's five-columns-of-five is
arithmetically sound but it sized it on 15.2 x 10.6 mm, the maximum-carryable envelope, which is
itself creepage-free — at that land the cells total 5 940 mm2 and the 60 % budget no longer
closes. Five of five is in my answer as the largest-carrying grid at 14.0 x 9.8 mm, not as a
placement to adopt. - Neither of us caught the real one: 160.8 mm2 is an area-only figure and
the grid fit caps the land near 137 mm2. Quoting 160.8 in section 4.1 would have sent a layout
contractor at a part 17 % too big. - The attack lists FIX-04-Zoning.gbr and
FIX-04-F_Silkscreen.gbr as changing. They do not. Only `cap` reaches silkscreen
(fixture_gen.py:478); the zone note is a constraints-file string. I dropped both from the file
list — and MANIFEST.json, which carries per-file bytes and sha256, was missing from both lists.

**Reasoning.**

The question has two halves and they have different answers, which is why the original decision
failed as a unit. The outline half is settled and always was.
fixtures/pcb/FIX-04/FIX-04-Edge_Cuts.gbr draws 0,0 -> 120000000,80000000 in 4.6 metric and
FIX-04-NPTH.drl places T01C3.200 at the four corners. The document does not contradict this —
section 4.1 incorporates the directory by reference and section 8.8 repeats it — so ratifying
120.0 x 80.0 mm into 4.1 changes no geometry, re-cuts no model, and only removes an asymmetry:
FIX-01 gets a full section 1.9 with stack-up, holes and zones, FIX-04 gets a pointer. Closing
that is cheap and correct. The condition that made it safe to ratify is also real and
reproduces: max_env = (5760 - 1901.16)/24 = 160.8 mm2 against a 70.0 assumed envelope, 2.3x
headroom, where FIX-01 sits at 70.7 against 70.0 with 1.0 % margin. FIX-04 survives the
datasheet; FIX-01 might not. The placement half was never mine to settle and I settled it anyway
on a number that is not in the package. That is the failure. 12.4 mm is the HM-04 electrode
body, three files deep, and it is the only 12.4 the package contains. Mixing it with 10.6 — the
short side of the maximum-carryable envelope, itself derived from an assumed 10:7 aspect —
produced a rule that fails its own creepage clause in the axis I forgot to apply it to. Worse,
it displaced an existing note that was correct: at the package's own 10.0 x 7.0, six across by
four up needs 78.0 x 40.0 mm and closes comfortably. I replaced a working note with an
unbuildable mandate and called it an improvement. So the right move is to state the constraint
rather than the answer, which is what the rest of this package already does with every unopened
datasheet. Charge rule 5(a) on both axes, name the usable band the connectors actually leave,
and give the layout contractor the land each grid can carry: 11.2 x 7.8 mm at six columns of
four, 12.2 x 8.6 mm at four columns of six, 14.0 x 9.8 mm at five columns of five. That is the
whole decision surface, expressed as arithmetic anyone can re-run when the datasheet arrives,
with no invented part. Running that arithmetic surfaced the one thing neither the decision nor
the attack had: area_budget() charges no creepage, so its 160.8 mm2 overstates what this
particular board can take. Under any grid the creepage-inclusive limit lands near 137 mm2. On
the one card in the package with a 3.0 mm rule, the area budget is not the binding constraint
and section 4.1 must not present it as one — that is a number a contractor would have taken as
acceptance and been 17 % wrong on. The price stands but its argument did not. EUR 40 is
inconsistent with the package's only rate — FIX-01's EUR 120 for 5-off of 160 cm2 is EUR 0.15
per cm2 of finished board, and 96 cm2 at that rate is EUR 72 — and section 6.1 explicitly exists
to make RFQ section 10's one-off line comparable between bidders, so internal consistency is the
standard it sets for itself. What was wrong was arguing setup dominance and then pricing area-
proportionally. The resolution is in the package, not in a hedge: section 6.3 already puts
FIX-01 and FIX-04 through one 15-day layout leg and one 10-day fabrication leg, so they go out
on one setup and the incremental cost of the smaller board is area-proportional. And a corrected
cell without its five totals is the defect the section names in its own text, so the totals move
in the same edit or the edit does not happen. Last, an edit that touches only the .md is not an
edit. The source string at fixture_gen.py:119 is printed verbatim into the released constraints
file, so leaving it makes the document and the released data flatly contradict rather than
merely differ; and the .docx and .pdf are what a manufacturer is issued, which is precisely how
TST-EEG-004 Rev C shipped renditions with no T30 in them (KNOWN_ISSUES.txt:291).

**Confidence:** derived  |  **Blocks a build:** no  |  **Signed off by:** Scoped, because most of this does not need a signature. The section 4.1 outline block and the section 6.1 price and totals are the JIG-EEG-009 document owner's to apply — derived values, no geometry change, no signature needed. What needs sign-off is item 5: the programme safety review that owns RISK-EEG-011 and adopted the pollution-degree-2 clearance table must rule on whether rule 5(a)'s 3.0 mm is a board-level inter-device rule or a part-level one, because a G6K-class signal relay cannot meet 3.0 mm inside its own package and this is the fixture where a flashover reaches an operator. If the ruling is part-level, the relay selection in AVL-EEG-017 changes and the section 6.1 relay line changes with it. The rule-5(d) placement text should not be released to a layout contractor ahead of that ruling.

**What would change it.**

1. The Omron G6K-2F-Y datasheet, which is the one document that settles the grid. Its
recommended land pattern decides directly: at or under 11.2 x 7.8 mm, six columns of four closes
and nothing else need change; up to 12.2 x 8.6 mm, four columns of six; up to 14.0 x 9.8 mm,
five columns of five; above 14.0 x 9.8 mm the card grows, and unlike FIX-01 there is no
enclosure note saying where the room comes from. Opening it also replaces RELAY_ENV_MM2 = 10.0 *
7.0 and re-runs the area budget for both boards in one line. 2. The safety review's ruling on
rule 5(a). If 3.0 mm is part-level, the relay is wrong for the 500 V duty and the grid question
is moot until a replacement is chosen. If it is board-level, rule 5(d)'s both-axes pitch is
correct as written. 3. A real 5-off quotation for both boards from one fabricator, which
replaces EUR 120 and EUR 72 with measured numbers and the five totals with them. It should be
sought together with the FIX-01 outline of D2, since section 6.3 already sends both boards out
on one setup and a single quotation prices the setup once — which is the assumption EUR 72 rests
on. 4. Any change to the FIX-04 front-edge connector row. The usable band of y 10.6-80.0 is a
consequence of J401, J402, J403 and J407 sitting at y = 6.0; moving them to the logic zone or to
an end panel returns roughly 10 mm of height and makes four columns of six the largest-carrying
grid instead of five of five.

**Files this touches:** `docs/JIG-EEG-009_RevB_test_fixture_design.md`, `tools/fixture_gen.py`, `fixtures/pcb/FIX-04/FIX-04_constraints.txt`, `fixtures/pcb/FIX-04/README_fixture_pcb_data.txt`, `fixtures/MANIFEST.json`, `docs/JIG-EEG-009_RevB_test_fixture_design.docx`, `docs/JIG-EEG-009_RevB_test_fixture_design.pdf`, `KNOWN_ISSUES.txt`


## MECH-D2

**Question.** Which cable gland fills the four M12 x 1.5 entries, and what flex rating applies at the helmet end where the umbilical moves with the participant's head?

**Decision.**

TWO DIFFERENT PARTS, BOTH WRITTEN AS CRITERIA, NEITHER CLOSED ON A PART NUMBER. H-8, pod end, 2
per kit, proposed identifier POD-P1-06 (not issued): a plain compression M12 x 1.5 gland, no
bend-protection member. H-10, helmet end, 2 per kit, proposed identifier HM-13 (not issued, and
out of the HM-12..HM-19 Phase 2 reserve): the same gland with an integral bend-protection
sleeve. No type designation is written for it. The "SKINTOP BS-M12x1.5" of the original decision
is withdrawn — it was constructed from a naming rule, and a type number this package invents
must not reach a PO. BINDING CRITERIA, both ends, all from the package (HARDWARE_SCHEDULE.md §4
line 121, mech_gen.py:293-298): - clamping range covering 3.0 to 6.5 mm (WH-01 4.30 nom / 4.60
max, WH-02 4.50 nom) - panel range covering 3.50 mm (pod: 2.50 wall + 1.00 pad) and 4.40 mm
(helmet: 2.40 floor + 2.00 HM-12 plate) - locknut at most 17.00 mm across flats - sealing at
least IP54 (the pod's design target, ASM-EEG-007 §5.1). NOT IP68 — that figure appears nowhere
in this package. - cable retention at least 15 N (WH-EEG-008 H6) - body and locknut polyamide,
not brass or nickel-plated brass FLEX RATING, helmet end only: the sleeve holds the cable to a
radius of at least 27 mm — WH-02's dynamic minimum, larger than WH-01's 26 mm, binding because
one part serves both cables — through a full 90 degrees. That is 42.41 mm of arc, so the
CONTROLLED LENGTH BEYOND THE NUT FACE IS AT LEAST 45 mm, not 40. WH-EEG-008 test H7 gains a
second station at OE-1/OE-2: 50 000 cycles at +/-90 deg, no continuity change, H1 repeated
after, first article only — 13.89 h at 1 Hz. POD END, reason restated: no gland form fixes the
pod entry, because the bend there is INTERNAL. POD-P1-04 holds the jacket 9.0 mm off the wall;
by WH-EEG-008 §6's own method (R + half OD) a 90-degree turn out of the gland needs 15.15 mm for
WH-01 and 16.25 mm for WH-02. It is 6.15 and 7.25 mm short. An external spiral cannot reach that
bend, and the pod wall is the one place the foam has no room. New open item against POD-P1-04
and mech_gen.py:311-313. TIE-BREAK, stated because nothing in the model catches it: if the
approved gland's locknut exceeds 17.00 mm across flats, the criterion wins and the part is
rejected. 17.00 is the P-clip clearance limit (16.0 - 4.0 - 9.815 = 2.19 mm of gap at AF 17;
1.00 mm at AF 19.05), not something the build checks. FOAM, raised in its own right and not as a
consequence of choosing a gland: the CASE-00 Rev C POD-P1 bay is 169 x 149 mm for a 163 x 143 mm
pod — 3.0 mm per side — and any M12 gland fitted body-outboard, locknut inboard (ASM-EEG-007 §4
record field), projects far more than 3 mm from the wall it is fitted to. The bay must be re-cut
or given local reliefs at PKG-EEG-015 §2.4's trial pack. The helmet bay is unaffected: layers
2-7 give 150 mm below the layer-1 shelf against 70.79 mm of frame, so 79.21 mm is clear below
the shell floor for the gland and the 45 mm sleeve — confirm at the same trial pack, it is
tighter than it was at 40 mm.

**What the attack changed.**

CONCEDED, all six checked and all six correct. 1. Sleeve length 40 mm -> at least 45 mm.
Decisive and arithmetic: 27 * pi/2 = 42.41 mm of arc for one 90-degree bend, so a 40 mm
controlled length runs out 2.4 mm before the swing the same paragraph tests to, and the last
degrees of every one of the 50 000 cycles land on unsupported jacket. A vendor quoting a
compliant 40 mm sleeve would deliver a part that cannot pass the station it was bought for. (The
attack's provenance claim — that 40 was lifted from the "P-clip 40 mm behind its housing" at WH-
EEG-008 lines 785/959/1238 — is suggestive, not proven; the arithmetic settles it without
needing it. mech_gen.py:314-315 rules that 40 mm figure out at the POD clip, not at the helmet
entry, so that half of the attack's point is loosely aimed.) 2. The pod-end reason measured the
wrong axis, and I repeated it. mech_gen.py:311-313's 26.0 mm is the ALONG-WALL distance, which
nothing constrains; the constrained axis is the 9.0 mm perpendicular offset POD-P1-04 sets (boss
5.0 off the wall + 4.0 to the cable axis in the clip). Confirmed against WH-EEG-008 line 1315,
which is the package's own method for exactly this arithmetic. "A 13 mm static bend radius" is
deleted as the reason. The conclusion — no bend protection at the pod — survives on a different
and truer reason, and a new open item is raised instead. 3. The max-of-both rule was applied at
one end only. WH-EEG-008 §4 line 976 gives WH-02 14 mm static, not WH-01's 13, and
mech_gen.py:328/330 give both pod entries the identical +/-16.0 clip geometry. Applied now:
16.25 mm for WH-02. 4. Requirements were being read back as a datasheet. Verified: "IP68" occurs
nowhere in the package (grep across all .md/.py/.txt); the package's ask is IP54. 3.0-6.5 mm is
GLAND_CLAMP_MIN/MAX, a requirement, and mech_gen.py:288-292 says so in terms. SVC-EEG-013 line
591 names SKINTOP ST-M12x1.5 only in the sentence that DELETES it with WH-08, and PARTS-EEG-019
line 193 and WH-EEG-008 line 89 do the same. H-8 is therefore NOT closed. I went one step
further than the attack asked and withdrew the constructed BS designation as well. 5.
"_pod_holds() and _oe_holds() fail the build if it moves" is false for the 17.00 figure. Lines
370 and 1288-1290 are seat >= AF/cos30 against a 22.00 seat, which passes to AF 19.05. The
asserts that DO bind are the panel-range ones (372, 1294-1295), which is what the generated
HARDWARE_SCHEDULE §2 sentence actually claims. Rewritten as an acceptance criterion with a tie-
break. 6. HM-13 was issued as fact. PARTS-EEG-019 line 169 reserves HM-12 to HM-19 for Phase 2
and mech_gen.py:1311-1317 already flags HM-12 as a proposal needing the register owner. HM-13 is
now proposed, unengraved, bag-labelled until issued. POD-P1-06 likewise. 7. Consequential edits
were missing. HARDWARE_SCHEDULE.md is generated ("Do not edit it by hand", lines 4-6), so
splitting the part means editing mech_gen.py:1253 and :1257 and the §2 sentence they feed, or
the schedule keeps saying "H-8 and H-10 are the same part, which is deliberate". Also confirmed:
ASM-EEG-007 line 165 has one "Spanner, 17 mm" row and line 1224 one "gland: ____" field, and
AVL/BOM need two lines where HARDWARE_SCHEDULE §5 item 2 asks for one. mech_gen.py, ASM-EEG-007
and PARTS-EEG-019 are added to the file list. KEPT, and independently re-checked against the
files: - The two-part split itself. HARDWARE_SCHEDULE §4 line 121 already states it: "At the
helmet end the umbilical flexes with the participant's head, so a bend-restricting form is
preferred there and the two ends may end up different parts; that is a decision, and it has not
been taken." This ruling takes it. - Polyamide, not metal. ICD-EEG-006 §4 lines 863-866 say what
the decision says they say, and design.py:23 puts the zone split at x = 62 with J14 at x = 5.0.
- 27 mm as the binding dynamic radius; 4.40 = 2.40 + 2.00; the 22.00 seat / 19.63 across corners
/ 32.00 axis spacing chain; 70.79 mm of frame; 150 mm of helmet void; 13.89 h. - The foam
finding, which is real: bay 169 x 149 (mech_gen.py:1442, PKG-EEG-015 line 351) against
POD_OW/POD_OH 163.0 x 143.0 (:201), and _layout_holds() line 1492 only ever asserted a 3.0 mm
difference, which nothing in the build would have caught. It is separated from the gland choice,
because it was wrong before anyone chose a gland. ADDED, found while checking and in neither the
decision nor the attack: H7's existing crown station is 1000 cycles (WH-EEG-008 line 1441)
against §4's stated 50 000-cycle target for both cables. Putting a 50 000-cycle station at the
entry creates two standards inside one test. The entry station stays at 50 000 — that is the
number the sleeve is bought to make reachable — and the crown station's 1000-vs-50 000 gap is
raised as its own open item rather than left silent.

**Reasoning.**

The attack's shape is right: the split, the helmet-end bend protection, the polyamide rule and
the criteria table are all supported by the files, and four load-bearing numbers and citations
underneath them were not. The two that actually change hardware are the sleeve length and the
pod-end reasoning. 27 * pi/2 = 42.41 mm is not arguable; a 40 mm sleeve under a +/-90 degree
test is a part that fails at the one place it exists to protect, and 45 mm costs nothing at
quotation time. The pod-end error is worse than it looks, because it was hiding a real defect:
the P-clip gives the cable 9.0 mm of perpendicular room where the package's own method (WH-
EEG-008 line 1315, R + half OD) needs 15.15 and 16.25. That is a live open item against
POD-P1-04, and the original decision's phrasing would have closed it by calling it benign. The
citation errors matter for a different reason. HARDWARE_SCHEDULE §4's preamble forbids closing
these lines "by picking a part number off a distributor's site without checking the criteria
against its datasheet", and mech_gen.py:288-292 says in terms that every gland figure in this
package is a requirement and not a measurement. Writing "SKINTOP ST-M12x1.5, clamping range 3.0
to 6.5 mm, IP68" reads as a specification that has been verified. It has not: IP68 is not in the
package at all, 3.0-6.5 is the ask, and the only three places the type designation appears are
the three that delete it with WH-08. Constructing "BS-M12x1.5" from a naming rule is the same
error one level worse, so it goes. I did not concede beyond what the files support. The 17.00
across-flats limit is a genuine criterion in the released schedule, and the clip clearance
behind it is real (2.19 mm at AF 17, 1.00 mm at AF 19.05) — what was wrong was claiming the code
enforces it. The fix is a tie-break clause, not a different number. This is answerable. Every
dimension the ruling depends on is in the released model or a released document, and the four
bores already exist in POD-P1-01 and in HM-12. What is not answerable here — and must not be
invented — is the vendor's side: the locknut across flats, the sleeve's published minimum radius
and controlled length, the gland's projection from the panel face, and whether a polyamide M12 x
1.5 bend-protection variant exists in any family at all. Those are datasheet-on-file items
before the PO, which is exactly how the package's own OPEN WITH CRITERIA convention handles
them.

**Confidence:** judgement  |  **Blocks a build:** no  |  **Signed off by:** The safety reviewer together with AVL-EEG-017 procurement for the two gland lines, the polyamide rule and the datasheets — the same pairing HARDWARE_SCHEDULE §4 already requires for H-4, "since the material is part of the safety case". The PARTS-EEG-019 register owner for POD-P1-06 and for HM-13 out of the HM-12..HM-19 Phase 2 reserve. WH-EEG-008's programme engineer for the H7 second station and the 27 mm / 45 mm figures. The PKG-EEG-015 owner, through an ECO-EEG-016 number, for the CASE-00 Rev C POD-P1 bay re-cut and for the regenerated HARDWARE_SCHEDULE.

**What would change it.**

Five vendor figures the package does not have, all required on file before the PO and not after.
(1) The approved gland's locknut across flats: above 17.00 mm the criterion rejects the part;
the model would not catch it, because the seat asserts pass to 19.05 mm. (2) The sleeve's
published minimum bend radius: above 27 mm the helmet part changes. (3) The sleeve's controlled
length: below 45 mm it cannot cover the 42.41 mm arc H7 station 2 swings through. (4) The
gland's projection from the panel face, which sizes the POD-P1 foam bay re-cut and has to be
confirmed against the 79.21 mm below the helmet shell floor. (5) Distributor confirmation that a
polyamide M12 x 1.5 bend-protection variant exists at all — if none does, the helmet line falls
back to any M12 x 1.5 polyamide gland with an integral bend-protection spiral meeting the
criteria above, and if nothing on the market meets them the entry hardware itself has to be
reconsidered. Separately, if POD-P1-04 is redesigned to hold the jacket 16.25 mm off the wall
instead of 9.0 mm, the pod entry's internal-bend finding closes and the pod line becomes clean
on its own terms.

**Files this touches:** `tools/mech_gen.py`, `mech/HARDWARE_SCHEDULE.md`, `docs/AVL-EEG-017_RevB_approved_vendor_list.md`, `docs/WH-EEG-008_RevB_harness_and_cable_assembly.md`, `docs/PARTS-EEG-019_RevB_part_identifier_register.md`, `docs/ASM-EEG-007_RevB_assembly_work_instructions.md`, `docs/SVC-EEG-013_RevB_service_and_refurbishment_manual.md`, `docs/PKG-EEG-015_RevB_packing_labelling_and_shipping.md`, `docs/EEG_kit_BOM_for_bidders_RevC.xlsx`, `docs/ECO-EEG-016_RevB_change_control_and_document_register.md`, `docs/RUL-EEG-021_RevA_rulings_register.md`


## MECH-D3

**Question.** HM-01 has no cable entry. What diameter, at what position, are the two OE-1/OE-2 bores, and is adding them an ECO against the released shell?

**Decision.**

TWO BORES, Ø12.50 mm, axes parallel to +Z, at x = -16.00 (OE-1, WH-01) and x = +16.00 (OE-2,
WH-02), y = -103.01, through the occipital shell floor plate from z = -56.00 (underside) to z =
-53.60 (cavity face) — 2.40 mm of PA12. Both edges broken 0.30 x 45 deg. Tolerance: Ø12.50 +0.30
/ -0.00 AS REAMED (not as-printed). Caveat carried forward from oe_entry_plate(): no document
states which way the frame's +x points, so OE-1/OE-2 swap if the frame convention is the other
way; nothing else moves, the plate is symmetrical and the glands identical. METHOD — REVERSED
FROM THE DECISION UNDER ATTACK. The bores are NOT cut into the model. HM-01's released mesh
stays byte-identical at Rev A, and the bores remain the fixtured bench operation that ASM-
EEG-007 Rev B section 4.1 step 5 already specifies: HM-12 laid on the floor underside with 8.00
mm showing at the front edge, 8.00 mm at the rear, 27.00 mm from each plate end to the outside
of the side wall, clamped, both holes piloted through it and opened to Ø12.50 with the reamer
that the section 4.1 tooling row already buys ("Drill and reamer, Ø12.5 mm, qty 3"). HM-12 stays
the drill jig — it is not demoted to a fit gauge. ECO — NO. This is not an ECO against HM-01,
because under the reversed method no released geometry file changes and no revision letter
moves. What is raised instead is a DOCUMENTATION CORRECTION under the next free number, ECO-
EEG-030 (the register itself states this is the next free number; ECO-EEG-016 is the register,
not a change number, and it explicitly renumbered a change off 016 so that no change shares a
number with the document). Its scope: (1) ASM section 4.1 step 5 gains the tolerance, the 0.30 x
45 deg edge break, and a dimensioned first-article check on the four setting margins — today
they are set by eye against no gauge; (2) WH-EEG-008 section 7 gains the OE-1/OE-2 coordinates
and a cross-reference to ASM 4.1 step 5, closing the KNOWN_ISSUES item by reference; (3)
HARDWARE_SCHEDULE H-10 gains the bore tolerance; (4) MECH_RELEASE_STATUS.md line 15 and the
mech_gen prose that generates it are corrected — they report AVL K24 as listing HM-01 among the
quotable twelve, and K24 does the opposite; (5) PARTS-EEG-019 section 5 line 639 ("not yet
copied -- see OA-1") is corrected, the file is in mech/stl/. HM-01 stays Rev A, stays on K24's
not-quotable list, and OA-1 (no STEP, no parametric source) is untouched by this change.

**What the attack changed.**

CONCEDED — five of the attack's seven points, four of them decisive: 1. THE METHOD, entirely. I
reproduced the failure end to end rather than taking it on trust. cadquery 2.8.0 has no STL
importer (ImportTypes = BIN/BREP/DXF/STEP; importShape('STL') raises RuntimeError). trimesh
5.1.0 reports boolean.engines_available == set() — no manifold3d, no pymeshlab, no Blender. The
only remaining route is raw OCP, and it fails silently: RWStl -> 194,828 single-triangle faces
-> BRepBuilderAPI_Sewing takes 141 s and returns a COMPOUND of TWO shells. Shell 0 is a
216-face, 0.0296 cm3 fragment that is closed AND valid; shell 1 holds the real 133.5751 cm3 and
is neither closed nor valid. MakeSolid(shells[0]) therefore succeeds on a crumb, and
BRepAlgoAPI_Cut against the Ø12.5 cylinder reports done=True in 0.03 s with the volume unchanged
at 0.0296 cm3 — against an expected drop of 2 x pi x 6.25^2 x 2.40 = 588.8 mm3. A build step
written the natural way "succeeds", writes an HM-01 "Rev B" STL with no cable entry in it, and
stamps a fresh SHA-256 into MANIFEST.json. That is the exact fault the decision existed to
prevent, relocated into the toolchain. "mech_gen.py gains a step" is not implementable and I
have withdrawn it. 2. THE ECO PREMISE. "HM-01 is a released part inside AVL K24" is false. AVL-
EEG-017 Rev B K24 reads "Files not yet released, and therefore not quotable: HM-01 frame (STL
only, no STEP, OA-1)". mech/step/ confirms it — every other released solid has a STEP, HM-01 has
none. The stated reason is OA-1, which raising a revision letter does not cure, so "AVL K24's
MJF print set quotes HM-01 Rev B" could never have been an output of this ECO. The decision
trusted MECH_RELEASE_STATUS.md line 15, which is mech_gen-generated prose that the governing AVL
contradicts; that prose is now itself in scope for correction. 3. THE TOLERANCE. Ø12.50
+0.30/-0.00 as-printed contradicts the package's own MJF figure, stated three times (WH-EEG-008
lines 852 and 1271, AVL K37: "MJF holds about +/-0.30 mm on a feature this size", and "is not a
machined panel hole"). A printed bore at Ø12.25 is legal MJF, functionally fine against the
M12x1.5 major Ø12.0, and a reject to that drawing. The attack's sharpest line stands: you cannot
delete the reamer and tighten the tolerance in the same ECO. Keeping the reamer resolves it —
+0.30/-0.00 is exactly what a reamed hole holds, and the tolerance is now explicitly qualified
AS REAMED. 4. ECO-EEG-016 IS NOT A CHANGE NUMBER. It is the change-control register at Rev B,
whose own Rev A-to-B note renumbered a change from 016 to 018 "so that no change shares a number
with this document", and which twice states the next free number is ECO-EEG-030. The decision
allocated no number at all. 5. THE REASONING OVERSTATEMENT. "the bore edge is the strain-relief
anchor that reacts H6's 15 N site-end pull, so a chipped edge is a structural defect" is
contradicted by the package's own released text. ASM section 4.4 step 2: the gland's clamping
nut on the jacket "is the strain relief at this end and it is what the 15 N site-end pull of WH-
EEG-008 H6 reacts against". HARDWARE_SCHEDULE line 121 puts cable retention on the gland.
oe_entry_plate()'s own docstring says the same. At 15 N a chipped bore edge is a sealing and
cosmetic concern, not a structural one. The argument never needed it — and with the drill route
retained, the thin-skin grab risk it was deployed against is managed by the pilot-then-ream
sequence and the inside support that ASM already mandates, not by moving the operation into a
kernel that cannot perform it. 6. Also conceded, from the attack's point 6: tools/emit_extras.py
sets V1 = ../package, which does not exist in this tree (only package_v1.zip), and its copy is
guarded by `not os.path.exists(dst)`. The only HM-01 in the tree is the output path, so any
generator step would have read and written the same file and consumed its own input on first
run. KEPT — the WHERE and the WHAT, which I re-derived myself rather than accepting the
attacker's concession: Ray-probing the released mesh (194,828 tris, watertight, 133.61 cm3, bbox
-95.53..95.53 / -126.01..103.55 / -56.00..102.00, matching MANIFEST) with vertical columns at
(±16.00, -103.01), sampled around the full Ø12.50 bore circle (r=6.25) and the Ø22 seat circle
(r=11.0) at 15 deg intervals, returns exactly one hit set at every one of 48 sample points:
[-56.000, -53.600, 29.600, 32.000]. Solid, flat, 2.400 mm of floor, nothing to break into, and
83.2 mm of clear cavity above for the internal locknut. Probing the whole 62 x 30 plate
footprint at x = -31, -27, -16, 0, +16, +27, +31 and y = -118.01, -103.01, -88.01 gives
-56.000/-53.600 in every column — the underside is flat 4 mm beyond the package's own measured
grid. Ø12.50 is ENTRY_BORE_D, the identical figure POD-P1-01 already prints for the identical
M12x1.5 gland. The arithmetic checks: (-126.01 + -80.01)/2 = -103.01; 17/cos30 = 19.630 and 32 -
19.63 = 12.37 mm of spanner clearance; 32/6.00 = 5.33x the section 7 minimum group separation;
62/2 = 31 and 58 - 31 = 27.00 — which is exactly the margin ASM section 4.1 step 5 already gives
the operator. _oe_holds() passes on import. CORRECTED — where the attack itself was wrong: Its
point 4 charges that "ASM-EEG-007 Rev B ... is missing from the decision entirely" and "WH-
EEG-008 Rev B is not in the scope either". Both are false: both documents are in the decision's
files_to_update list. The attack read the decision's ECO narrative paragraph and not its file
list. The scope does have real holes — AVL-EEG-017 and MECH-EEG-020 are named in the decision's
prose but absent from its file list, and mech/HARDWARE_SCHEDULE.md is in neither — so the
substance of the complaint survives, but not the charge as made. Its point 3 is also softer than
stated. PARTS-EEG-019 section 4.3 rule 6 already records that rule 2 was broken for the Rev B
geometry — MP-01, POD-P1-01 and POD-P1-02 were resized with no ECO raised before release,
"recorded, not excused". A recorded deviation is precedented in this register, not novel. It is
moot here anyway: reversing the method means no letter moves and no same-named-file hazard
arises, so the attack's proposed rename to HM-01_RevB_frame_monocoque.stl is not needed and
would settle section 1.3 rule 2 for one file while leaving seven others inconsistent. Its
correction option (b) — add manifold3d or pymeshlab plus a post-cut watertightness/volume/ray
assertion — is technically sound and I would accept it if the model MUST carry the bores. It is
rejected here for a reason the attack did not weigh: PARTS-EEG-019 OA-1 states HM-01's "geometry
changes once the Stage 0 fit measurement is done", and OA-1 explicitly "does not block
printing". Adding a second geometry kernel to hand-patch a mesh that is already scheduled to be
replaced buys nothing the drill route does not already deliver.

**Reasoning.**

The question has three parts and they separate cleanly after the attack. WHAT AND WHERE —
settled, and settled by measurement. I did not accept the attacker's verification; I redid it.
The floor plate under (±16.00, -103.01) is 2.400 mm of solid, flat PA12 from z = -56.000 to
-53.600 with nothing above it until the roof at 29.600, at every one of 48 probe points around
both the bore and the seat circles, and flat across the entire HM-12 footprint out to x = ±31.
Ø12.50 is not a new number: it is ENTRY_BORE_D, what POD-P1-01 already prints for the same gland
at the pod end of the same umbilical, so one gland and one hole size serves all four entries. x
= ±16.00 is forced by two 17.00 mm across-flats locknuts (19.63 across corners, leaving 12.37 mm
of spanner clearance at 32.00 mm spacing) and clears WH-EEG-008 section 7's 6.00 mm
electrode/light group separation by 5.33x. y = -103.01 is the measured mid-depth of the floor,
which centres the plate with 8.00 mm of floor beyond each edge. The route is not a preference:
all three channel mouths open into the shell cavity, the wall's far side is the participant's
occiput under the HM-02B pads, and the floor is the only way in that costs the cable no bend at
the frame against WH-01's 26 mm dynamic radius. HOW — reversed, on reproduced evidence. The
decision's central move was to take the operation off the bench and into the model. Three
findings kill it. First, the capability does not exist: cadquery 2.8.0 cannot import STL and
trimesh 5.1.0 has zero boolean engines, so there is no route that does not add a dependency.
Second, and worse, the route that appears to work does not: OCP sewing splits 194,828 triangles
into two shells, the first being a 216-face 0.0296 cm3 crumb that is closed and valid, so the
obvious implementation builds a solid from it, cuts it in 0.03 s, reports done=True, and writes
a "Rev B" HM-01 with no cable entry and a fresh hash. I ran this and watched the volume not
move. Third, the generator would have consumed its own input, because emit_extras.py's V1 source
path does not exist in this tree and the only HM-01 present is the output file. A change control
argument that rests on "the cut is deterministic and hashable" cannot survive a step that hashes
the wrong geometry. Against that, the bench route is already fully released. ASM-EEG-007 Rev B
section 4.1 step 5 carries the coordinates, the diameter, HM-12 as the jig, the four setting
margins, drill-from-outside with inside support, swarf control and the re-run draw cord on all
three channels; section 4.4 steps 1 and 2 fit the plate and both glands; the tooling row buys
three reamers; the takt table budgets 15 minutes; the QC checklist has two lines for it. Nothing
had to be invented — the decision proposed to delete a working, released, correctly-scoped
operation and replace it with one that cannot be built. The two objections it raised against the
bench route both dissolve: the thin-skin grab is what pilot-then-ream with inside support exists
to prevent, and the bore edge is not the load path at all, because ASM section 4.4 step 2 puts
H6's 15 N on the gland's jacket clamp. Keeping the reamer also resolves the tolerance
contradiction rather than papering over it. +0.30/-0.00 is unattainable as-printed against the
package's own thrice-stated ±0.30 MJF figure, but it is exactly what a reamed hole holds. The
tolerance is now qualified AS REAMED so the two cannot drift apart again. ECO — the honest
answer is no, and that is a stronger answer than the one the decision gave. Under the reversed
method no released geometry file changes, so no revision letter moves, HM-01 stays Rev A, the
engraving problem of section 4.3 rule 2 never arises, and the two-files-one-name hazard the
decision itself invoked never arises either. HM-01 also stays exactly where AVL K24 has it: not
released, not quotable, pending a STEP under OA-1. What remains is a documentation correction,
which takes ECO-EEG-030 — the number the register itself names as next free — and which is
mostly about making four documents stop contradicting an operation that is already correctly
specified in a fifth. Three residual gaps I am recording rather than closing, because they are
outside this question: HM-12 has no MECH-EEG-020 sheet at all (the index runs 25 sheets and
HM-12 is not among them); HM-12's identifier is proposed, not issued, since PARTS section 1.2
reserves HM-12..HM-19 for Phase 2; and ASM's own note that the released frame gives each section
one channel where WH-EEG-008 section 7 requires two is a far larger problem than the entry bores
and is not touched by any of this.

**Confidence:** derived  |  **Blocks a build:** no  |  **Signed off by:** Mechanical owner (tools/mech_gen.py and mech/) signs the reversal of method and confirms HM-01 stays Rev A with its mesh byte-identical. ECO/document-control owner signs ECO-EEG-030 and the five document corrections, and confirms 030 is still free at issue. Print bureau QA and programme goods-in countersign the new dimensioned first-article check on the four setting margins, per PARTS-EEG-019 section 4.1. RISK-EEG-011 owner sees it because HM-01 is patient-applied and the bores sit 20.60 mm behind the wall the HM-02B occiput pads bear on. PARTS-EEG-019 register owner separately confirms or replaces the proposed HM-12 identifier, which remains unissued and unrelated to this decision.

**What would change it.**

1. THE FIRST HM-01 PRINT, MEASURED. Every floor constant has sd 0.000 over 30 section points,
but no part has ever been printed and MJF shrink is anisotropic. If the as-printed floor plate
is more than about ±0.5 mm off the modelled y span, HM-12 and both bores move together and the
constants are re-fitted to the measured part. This is now a fixturing question rather than a
model question, which is a cheaper failure. 2. THE GLAND'S ACTUAL LOCKNUT ACROSS FLATS. 17.00 mm
is assumed (GLAND_LOCKNUT_AF), not read off a datasheet — AVL K24-class gland data has not been
obtained. Above 17.00 mm the 32.00 mm axis spacing must grow, both bores move outboard, HM-12
grows with them, and OE_SEAT_D follows. 3. A WORKING MESH-BOOLEAN PLUS A PARAMETRIC HM-01. If
OA-1 closes and HM-01 gains a parametric source, the bores should be modelled in and the drill
deleted — that is the end state ASM section 4.1 step 5 already anticipates in writing ("Not
needed once a parametric HM-01 prints the bores"). Until then, adding manifold3d or pymeshlab to
hand-patch a mesh that OA-1 says will be replaced buys nothing. 4. IF THE MODEL MUST CARRY THE
BORES BEFORE OA-1 CLOSES — for a reason not yet on the table — then the attack's option (b) is
the only acceptable form: a real boolean engine, the v1 source extracted from package_v1.zip to
a distinct read-only path so the generator cannot consume its own input, and a mandatory post-
cut assertion that fails the build unless the output is watertight, the volume has dropped by
588.8 mm3 ±1%, and a vertical ray at (±16.00, -103.01) returns NO hit between z = -56.00 and
-53.60. Without that assertion the silent failure I reproduced ships. The tolerance would then
have to relax to Ø12.50 ±0.30 per the package's own MJF figure, and the Ø12.50 bore would have
to be added to FIT-01, which exists to gate a printed fit and today carries only the
9.20/9.35/9.15 family. 5. THE FRAME'S +x CONVENTION. If a document ever states it and it runs
the other way, OE-1 and OE-2 swap. Nothing else moves.

**Files this touches:** `docs/ASM-EEG-007_RevB_assembly_work_instructions.md`, `docs/ECO-EEG-016_RevB_change_control_and_document_register.md`, `docs/WH-EEG-008_RevB_harness_and_cable_assembly.md`, `docs/PARTS-EEG-019_RevB_part_identifier_register.md`, `tools/mech_gen.py`, `mech/MECH_RELEASE_STATUS.md`, `mech/HARDWARE_SCHEDULE.md`, `KNOWN_ISSUES.txt`


## MECH-D4

**Question.** Which side of the frame is "left"? The package uses the word for OE-1, the halo runs, the temple mount and the 10-20 sites and never fixes the convention.

**Decision.**

RULING. "Left" unqualified means the PARTICIPANT'S ANATOMICAL LEFT. PARTICIPANT FRAME (HM-01 and
anything worn): right-handed, origin at the frame centre, +x = participant's right, +y =
anterior, +z = superior. This is RAS. Left is -x. VALUES THAT FOLLOW, none of which move
released geometry: - OE-1 (WH-01, 12-way screened electrode cable) stays at x = -16.00, y =
-103.01, z = -56.00 + floor thickness, exactly as oe_entry_plate() released it. OE-2 (WH-02,
10-way contact-light cable) stays at +16.00. - The -x halo branch carries T7, F7, REF_L and
BIAS_EL; the +x branch carries T8 and REF_R. HM01_HALO_MOUTH (+45.41, -82.41, -11.25) is
therefore the RIGHT mouth; 55.5 mm is the near halo trunk, 77.4 mm the cross-run from OE-1 to
the right mouth, 85.1 mm the N1 trunk. - C3 and the left temple socket are at -x; C4 and T8 at
+x. EVIDENCE, in the order an inspector can check it (all three re-measured by me, not taken on
trust): 1. The released mesh decides it on its own. HM-01 carries exactly ONE feature with no
mirror partner, and all of it is at -x. A 1.2M/400k-point KD-tree mirror test leaves 6401 points
above 1 mm deviation, 6377 of them at negative x; the 24 at +x are the mirror shadow of the
channel bore. The feature: a plain cylindrical socket, bore Ø12.80 mm, ~23 mm deep, mouth at
(-61.71, +61.41, +25.71), axis (-0.630, +0.523, +0.574) i.e. outboard-forward-up, OD ≈ 14.6 mm,
standing off the front-left halo band with a Ø3.9 mm channel bore into the band beneath it. It
cannot be an electrode station: HM-04 is a 12.4 mm SQUARE body (mech_gen.py:545-551) needing a
Ø17.5 mm circle, and the axis points away from the scalp. Every one-sided frame feature the
package names anywhere is a LEFT-side feature — the left temple socket (ASM-EEG-007 §4.5) and
F7, the one 10-20 site with no contralateral partner. No right-only frame feature is named
anywhere. Therefore -x is the participant's left, checkable with a caliper on the first print.
2. HM-01's own file is right-handed and not inside-out: signed volume from its winding =
+133,605.7 mm3; mean dot(stored facet normal, right-hand-rule normal) = 1.0000 across all
194,828 facets. With -y posterior (occipital shell y = -80.01..-126.01, HM-02B pads on the
-80.01 face, the three channel mouths in it) and +z superior (floor z = -56.000 the lowest point
of the part; crown +86.71 sagittal, +86.45 coronal), a right-handed triad gives y_hat x z_hat =
x_hat = anatomical Right. Do NOT cite "the CadQuery/OCCT kernel that wrote every mesh in mech/":
it did not write this one. 3. IFU-EEG-014 §13.1 fixes the anatomical half — "Odd numbers are on
the left, even numbers on the right" — and the participant fits the helmet unaided, so no
observer's-left exists in the procedure. Do NOT cite MECH-EEG-020's "RIGHT (looking along -X)"
as support. SCOPE RULE — TWO FRAMES, NOT THREE. The word is always written with its frame. (a)
PARTICIPANT frame, above, for HM-01 and anything worn. (b) DESIGN-SOURCE frame for EEG-CAR-01
AND for POD-P1, which is dimensioned in the carrier's own coordinates (mech_gen.py:71-73 _c(),
PANEL "x from the board origin"): left = low x in the top-left-origin, Y-down view seen from the
component side. That is what "AGND_REF left of x = 62 mm" already means and what mech_gen.py:179
and :508 already mean — "Left-wall parts have x < BW/2". So POD-P1's LEFT wall is the -X SHORT
END wall carrying the three DIN 42802 openings at design x = 8.0, y = 76/88/100 and the WH-01
gland opposite J14; the RIGHT-HAND wall is the +X end wall carrying BTN_A/B/C, the jacks, the
USB-C ports and the microSD. The ±Y LONG walls are neither; the only thing on one is the WH-02
gland on the -Y wall. Shop-floor gloss, if one is wanted: "pod upright, lid up, reader facing
the LONG wall that carries the WH-02 gland — the DIN end wall is then on the reader's left."

**What the attack changed.**

CONCEDED — four things, all verified against the files. 1. The POD-P1 clause is deleted. I
confirmed the break. grep for "lid removed", "toward the reader", "as seen", "viewed from",
"looking", "facing you" across ASM-EEG-007 and SVC-EEG-013 returns nothing relevant, so the
decision's "which is what §5.1 and §5 already mean" was an invention. Worse, the gloss inverts
the answer: POD_IW/POD_IH = 158/138 (mech_gen.py:200), so the ±X walls are the SHORT end walls
and carry every panel opening (":508 panel openings, on the two short walls"; side = -1 if x <
BW/2 else 1), while the ±Y walls are the long ones. "Lid removed" is a view down +Z; putting a
panel end wall toward the reader makes the LONG walls left and right — the opposite pair from
PANEL:179, from IFU-EEG-014's "POD-P1 left end wall at y = 76, 88 and 100 mm", and from ASM-
EEG-007's "WH-01 through the left wall opposite J14" (HARNESS:328 puts that gland at x =
-POD_IW/2). An assembler following the original clause looks for three DIN sockets on a long
wall and finds one gland. Replaced with the design-source rule that already exists in the
source. 2. "Three frames" becomes two. POD-P1's PANEL table is in carrier coordinates converted
by _c(); it is EEG-CAR-01's design frame applied to the box, not a third frame. Confirmed. 3.
The kernel citation is struck. mech_gen.py:674-675 says HM-01 is "a carried-over v1 mesh with no
parametric source (PARTS-EEG-019 OA-1)"; its STL is dated 31 Aug against 2 Sep for every
generated mesh. No kernel in this package wrote it. Replaced with the file's own handedness,
which I re-measured (+133,605.7 mm3, mean dot 1.0000 — the attack's figures are exact). 4. MECH-
EEG-020 is struck as corroboration and now carries a cost. mech_drawings.py:33-35 with the
unflipped projection at :243 and :258-260 cannot make all three labels true: TOP (0,1) and RIGHT
(1,2) are consistent with cameras at +Z and +X, but FRONT (0,2) plots +X to the page's right,
which is the view from -Y. I went further than the attack and checked whether that is visible on
this part: the X-Z silhouette has exactly one one-sided patch, 248.34 mm2 at x -74.53..-50.52, z
23.60..41.55, with every other difference at or below 0.01 mm2 of triangulation noise. So sheet
3's FRONT view of HM-01 is provably mirrored on the one part where it shows. That is an ECO, and
"nothing moves / the answer confirms the released model" was too clean. REJECTED / CORRECTED —
two things the attack got wrong. 5. The socket is NOT KEYED. The attack calls it "a keyed
cylindrical socket" and concludes ASM-EEG-007 open item 21 is "FALSE as to the socket". I
sectioned the bore at seven depths: area 128.6 mm2 and Deq 12.80 mm constant from t = -1 to t =
11, radius 6.28..6.52 mm, circle-fit sd 0.079 mm, perimeter 40.3 against 40.5 for a true circle.
There is no keyway anywhere along the depth. "Keyed" was inferred from the ASM requirement, not
measured. So item 21 must be RE-SCOPED, not closed: it is wrong that the socket is "located and
dimensioned nowhere — not in the HM-01 mesh", and it is newly right that §4.5's "keyed so it
cannot be fitted rotated" is NOT met by the released frame. The attack's correction would have
closed a line that has to stay open in a different form. 6. The attack over-weights the part
identification. It hangs the mesh argument on the boss BEING the left temple socket. It does not
need to be. Fz/Cz/Pz are midline, C3/C4 and T7/T8 are pairs, and F7 is the one unpaired 10-20
site — on the left. The temple socket is on the left. No right-only frame feature is named
anywhere in the package. So whichever left-side fitting the boss is meant to be, the handedness
conclusion is the same, and it survives being wrong about the part. That makes the mesh route
stronger than either the decision or the attack stated. The attack's dismissal of MECH-EEG-020
is also slightly too strong: TOP and RIGHT are internally consistent with +X = right, so two of
three views do support the ruling; only FRONT is broken. KEPT: the ruling itself, unchanged in
every value. -x = participant's left, OE-1 at -16.00, OE-2 at +16.00, the halo branch
assignments, and the right-hand +x/+y/+z triad.

**Reasoning.**

The attack's own headline is "core answer survives, and is under-proven", and that is what the
files show. I checked every cited line and re-ran the geometry independently rather than
accepting the numbers. What held. The mesh bounds are x ±95.526, y -126.010..+103.550, z
-56.000..+102.000; the crown fits are -31.32 + 118.03 = 86.71 and -0.83 + 87.28 = 86.45; the
occipital shell runs y = -80.01 (skull-facing, the face HM-02B pads sit on) to -126.01 and the
floor at z = -56.00 is the lowest point of the part. So -y is posterior and +z superior, from
geometry, not choice. The file is right-handed and not inside-out. Given those, y_hat x z_hat =
x_hat makes +x the anatomical right. IFU-EEG-014 §13.1 line 234 supplies the anatomical half,
and WH-EEG-008's channel-fill table does put T7/F7/REF_L/BIAS_EL on the left halo and T8/REF_R
on the right. Two routes, same answer, and the answer confirms the released placement —
oe_entry_plate()'s own docstring says "No document in this package states which way the frame's
+x points, so OE-1 is put on -x here", so the ruling ratifies the released model rather than
moving it. What I added. The mirror test is decisive and neither party fully exploited it. The
frame is mirror-symmetric to 0.27 mm at the 90th percentile everywhere except one lobe, and that
lobe is entirely at -x. Because the package names left-side one-sided fittings and no right-side
one, the physical part itself states which side is left, and a fitter can confirm it with a
caliper before any document is read. That is the best kind of evidence this package can have,
and it is now the first line. What broke and why it matters. The POD-P1 clause was written to
stop the ambiguity recurring and instead reintroduced it, pointing at walls that carry no panel.
It cited two documents that say nothing about viewing. That clause had to go, and the
replacement is not invented — it is the rule already implemented in the design source and
already used by IFU-EEG-014. The drawing-set corroboration had to go too, and it takes an ECO
with it, because I confirmed the mirrored FRONT view is visible on exactly this part. Where I
would not follow the attack. It measured the socket's envelope but not its bore profile, and
called it keyed. It is not. Conceding that would have closed an open item on a patient-worn part
on the strength of a feature that is not there, which is the failure mode this review exists to
prevent. The correct outcome is that the socket's position and bore are now known and the keying
requirement is now a live, named gap against HM-01 and the unmodelled HM-07A.

**Confidence:** derived  |  **Blocks a build:** no  |  **Signed off by:** Three signatures, because the ruling crosses three boundaries. (1) The mechanical design owner for HM-01 and MECH-EEG-020, who must accept the frame-axis definition, raise the ECO on tools/mech_drawings.py and re-issue all 25 sheets. (2) The clinical/protocol owner, because the ruling binds eight 10-20 electrode names to physical sides of a participant's head on a patient-worn part — if this is wrong, every recording is mislabelled and no downstream check catches it. (3) The register owner for RUL-EEG-021 and PARTS-EEG-019, who records the ruling and rules on the re-scoped ASM-EEG-007 open item 21 and the new keying gap. No released mesh is re-cut, but a released drawing set is, and the electrode-side naming is patient-facing, so this does not go in on a generator comment.

**What would change it.**

Only evidence that the occipital shell is not at -y: a v1 HM-01 source file, an orientation
render or a form-study photograph showing the brow at -y. That would flip anterior and, with
right-handedness held, take +x with it. The mesh is symmetric about x = 0 apart from the single
-x lobe, so x cannot be settled from the geometry alone — the anterior call is load-bearing, and
it rests on the shell, the three channel mouths and the HM-02B occiput-pad naming all agreeing.
The mesh route has its own falsifier, now that it is the first line of evidence: a document or a
v1 record identifying the -x lobe at (-61.71, +61.41, +25.71) as a RIGHT-side fitting, or naming
any right-only frame feature at all. Nothing in the package does, and a caliper on the first
HM-01 print settles it in a minute — measure which side carries the Ø12.80 mm socket. That check
should be added to the first-article inspection before the ruling is relied on for a build. What
will NOT change it: the identity of the lobe. Both candidate identifications (the left temple
socket, or F7, the one unpaired 10-20 site) are left-side, so the ruling holds either way.

**Files this touches:** `docs/RUL-EEG-021_RevA_rulings_register.md`, `docs/ICD-EEG-006_RevB_interface_control_document.md`, `docs/ASM-EEG-007_RevB_assembly_work_instructions.md`, `docs/WH-EEG-008_RevB_harness_and_cable_assembly.md`, `tools/mech_gen.py`, `tools/mech_drawings.py`, `mech/drawings/MECH-EEG-020_sheet_index.csv`, `mech/drawings/MECH-EEG-020_RevA_printed_part_drawings.pdf`, `KNOWN_ISSUES.txt`


## D2-RECORD-SHA256

**Question.** TST-EEG-004 Rev C section 12 requires the SHA-256 of the per-unit record on the certificate and never says in what form or over which bytes (section 16 item 17).

**Decision.**

RULING (under ECO-EEG-016, closing TST-EEG-004 §16 item 17). 1. ENCODING — unchanged. 64
lowercase hexadecimal characters, no prefix, no separators. Schema pattern stays
`^[0-9a-f]{64}$`. Consistent with all seven 64-hex fields the record already carries
(identity.firmware_sha256, identity.tool_eeg_022_sha256, results.T0.data.netlist_file_sha256,
results.T24.data.firmware_image_sha256, results.T25.data.image_sha256_partition_a,
...partition_b, signatures.record_sha256). 2. BYTES — unchanged in substance. SHA-256 over the
delivered record file, byte for byte, with the 64 characters that are the VALUE of the JSON
member `signatures.record_sha256` — found BY PARSING the file, at their own offset — replaced in
place by 64 '0'. Length-preserving, so no offset moves. The delivered file is the signed object.
3. DELETED from the decision: the sentence "the delivered file is mandated to be canonical so
the two routes to the hash agree", the re-serialisation route, and the "either
validate_test_record.py or one line of shell" equivalence. There is now ONE definition and ONE
route. 4. ADDED, replacing the false justification with the true one: number spelling (`0.5` vs
`0.5000` vs `1.0E-7`) and string escaping (`é` vs `é`) DO NOT MATTER, because only delivered
bytes are hashed. Two records are compared by parsed value, never by re-serialisation. 5.
CANONICAL FORM — demoted from a hash-enabling mandate to a separately checked conformance rule,
verified by validate_test_record.py as five NAMED errors, never as a hash argument: (a) BOM
present; (b) any CR byte; (c) keys not sorted at some level; (d) indent not exactly two spaces;
(e) not exactly one trailing newline. A Windows station's CRLF file then fails as "not
canonical", not as a hash dispute. 6. VERIFICATION — this exact line is published, and it is
parse-based: python3 -c "import sys,json,hashlib;b=open(sys.argv[1],'rb').read();v=json.loads(b)
['signatures']['record_sha256'].encode();i=b.rfind(b'\"'+v+b'\"');print('OK' if
hashlib.sha256(b[:i+1]+b'0'*64+b[i+65:]).hexdigest()==v.decode() else 'MISMATCH')" TIOV-B-
nnnn_test.json Printed beside it: a first-match `sed 's/[0-9a-f]\{64\}/0…0/'` zeroes
identity.firmware_sha256, not record_sha256 — verified. 7. PRINT — the 4x16 grouping is DROPPED.
The hash prints unbroken on its own full-width line beneath the signature table of §13 item 8,
labelled "SHA-256 of the source record — 64 hex characters, lower case, no spaces". This removes
the collision with FW-EEG-001 Rev C §7.4 (whose spaces ARE part of the fingerprint value) and
the table-cell wrap the 114.7 mm arithmetic ignored, and it preserves the certificate template's
"filled from the record and from nowhere else" invariant with no amendment. 8. THREE PLACES: the
JSON, the certificate, and the `record_sha256` column of records/lot_summary_template.csv. All
three carry the same ungrouped 64 characters. 9. REFURBISHMENT: appending a §12 refurbishment
block changes the file, therefore changes the hash. `record_sha256` is recomputed and the
certificate REISSUED at each refurbishment — this is not a new choice, SVC-EEG-013 Rev B §8
already rules that the printed calibration record in the case lid pocket "is reissued at every
refurbishment". The superseded certificate is retained with the F1 in the device history record
(QP-EEG-010 Rev B §9.2). The "separate chained file" alternative is rejected: it contradicts
§12's "appended under the same unit serial". 10. WORKED EXAMPLE, with its value:
records/EXAMPLE_TIOV-B-0000_test.json is written today by make_records.py with `json.dump(...,
indent=2, ensure_ascii=False)` and NO sort_keys, so the delivered bytes are unsorted and do not
reproduce the recorded hash. The fix is `sort_keys=True` on that one call. The recorded hash
DOES NOT CHANGE: 4255b6444aee27a7521aaba12fa78efa588508d45e97473440190c4801b5e6ed. Verified —
once the same data is written sorted, the zero-filled delivered bytes are exactly the bytes the
validator serialises today, and the round trip closes. CONSEQUENTIAL CORRECTION, ruled here
because it is determined and not a choice: the schema's identity.key_fingerprint pattern
`^[0-9A-F]{16}$` rejects the form FW-EEG-001 §7.4 mandates and the M-03 label prints (`A1B2 C3D4
E5F6 0718`), while the schema's own description says the value is "identical to the string
printed on the label". §7.4 says the fingerprint "is defined here and nowhere else" and that
TST-EEG-004 cites it, so the schema is wrong: pattern becomes `^[0-9A-F]{4}( [0-9A-F]{4}){3}$`.
If this lands in the same regeneration it changes the example's bytes and the generator
recomputes 4255b644... accordingly.

**What the attack changed.**

CONCEDED — five of seven points, all verified against the files. (1) The load-bearing sentence
is FALSE and I withdraw it. I built the counter-example: two files both satisfying every
canonical clause (UTF-8, no BOM, LF, sorted keys, two-space indent, one trailing newline) with
identical parsed data hash differently, because the form pins nothing about number spelling or
escape style. But the attack's own correction (c) shows this strengthens the ruling rather than
wounding it: under file-bytes hashing those divergences are irrelevant. The false argument is
deleted and the honest one put in its place. (2) The two named checks disagree TODAY, exactly as
charged, with the attack's exact numbers. validate_test_record.py:156-167 `canonical_bytes()`
re-serialises with Python; validate() at :304 opens the file in TEXT mode and never sees raw
bytes; the check at :293-298 compares against the re-serialisation. On the shipped example the
validator reproduces 4255b644... while zero-filling the delivered bytes gives
035c376054eb6b5e404716e48d7d697a2eba232a1da89d773d8c35edb14be5bc. Without the validator rewrite
the ruling is unimplemented and a correct C#/LabVIEW record is rejected by the package's own
tool. Correction (a) adopted in full. (3) The zero-fill caveat guarded the wrong hazard.
Verified: the record carries 7 sha256-named fields and 7 sixty-four-hex strings (my reasoning
named 3, missing firmware_image_sha256, image_sha256_partition_a and _b); the FIRST 64-hex match
in the sorted text is identity.firmware_sha256; signatures.record_sha256 is the LAST, since
`signatures` sorts last at top level and `record_sha256` last within it. The schema has exactly
one record_sha256 with additionalProperties:false at both levels, and refurbishment items are
{date, receipt_record_reference, results} with additionalProperties:false — so the collision the
caveat guarded really cannot occur. Corrections (b) and (f) adopted; I publish the parse-based
one-liner rather than hand-waving at shell. (4) The print collision is real and both citation
slips are mine. FW-EEG-001 Rev C §7.4 (docs/FW-
EEG-001_RevC_firmware_build_and_provisioning.md:1173-1177) defines the fingerprint as 16
uppercase hex in four groups of four separated by single spaces, with the spaces INSIDE the JSON
value ("public_key_fingerprint": "A1B2 C3D4 E5F6 0718") and on the M-03 label; and the
18-uppercase-hex ATECC rule lives in the schema, not §7.4. Case is not the discriminator I
claimed once both are grouped. Grouping dropped entirely — correction (e), first option. (5) The
grouping had no implementation and broke an invariant. Certificate line 102 is a two-column
table cell; the template header at lines 6-9 says every {{...}} is filled from the record "and
from nowhere else"; line 29 already sets a 64-char firmware hash in the same table. And nothing
in the package fills the template — make_records.py:1218 writes the template only, and a
package-wide grep finds no renderer. Conceded; dropping the grouping makes the exception
unnecessary. PARTLY CONCEDED — (6) archival fragility. The hazard is real and I keep it as a
stated risk, but it does not favour a content hash. TST-EEG-004 §12 (line 1158) ships records as
one ZIP per lot, which protects the transport leg from the mail-gateway and text-mode-transfer
cases named. More important, correction (d) — which I adopt — is precisely what restores the
discrimination the attack says a file-bytes hash loses: a re-indented or CRLF-converted file
fails as a NAMED canonical error, so "reformatted" and "altered" are distinguishable after all.
CONCEDED THEN NARROWED — (7) refurbishment. The decision did leave it open and that was a gap.
But it is not a choice between two designs: SVC-EEG-013 Rev B §8 already rules the printed
calibration record "is reissued at every refurbishment". The ruling cites that; the attack's
alternative (a separate chained file) is rejected as contradicting a released document. REJECTED
— one detail of correction (a). "Regenerate EXAMPLE_TIOV-B-0000_test.json AND ITS RECORDED HASH"
is half wrong. The file must be rewritten sorted, but the hash value is unchanged at
4255b644...4801b5e6ed. I verified the round trip: the zero-filled sorted delivered bytes are
byte-identical to what canonical_bytes() serialises today, so the fix is one keyword,
`sort_keys=True`, and the certificate's printed value stays put. FOUND BY ME, in neither the
decision nor the attack — the edit list as written would be silently reverted.
tools/finalise_docs.py main() rewrites docs/RUL-EEG-021_RevA_rulings_register.md from
tools/RULINGS.md, and the register itself warns that a hand edit "is reverted, without a
warning, on the next run": a ruling filed only in the register is lost. Five of the seven files
I listed (the schema, the example, the CSV, the certificate template, README.txt) are OUTPUTS of
records/make_records.py main() — hand edits to them are overwritten. And docs/*.docx and *.pdf
are re-rendered from the .md by tools/make_docs.py, so the released TST-EEG-004 PDF keeps
carrying the proposal until that is run.

**Reasoning.**

The attack broke the justification, not the ruling — and it says so itself ("Hashing the
delivered file is a defensible ruling"). What survives scrutiny is that file-bytes hashing is
the only one of the three candidates that closes item 17's stated failure mode. Re-
serialisation, the status quo in the schema description, TST §12 and both tools, leaves float
formatting, non-ASCII escaping and key collation to whichever library a station happens to use,
so two manufacturers can follow the prose exactly and disagree — the exact defect item 17 exists
to record. RFC 8785 JCS would close it properly, but no implementation ships in this package, it
discards the indentation that makes a record diffable, and it still needs the zero-fill rule
bolted on. Hashing what is delivered removes the whole class: every party hashes the same bytes.
The attack's strongest blow — that the canonical form does not pin numbers or escapes — is true
and I verified it by construction, but it argues FOR this ruling. Those divergences only bite a
re-serialisation route. Once the delivered bytes are the definition, the canonical form has no
hash work left to do, which is why it moves from a mandate nothing enforces to five named
conformance errors the validator raises. That change also disposes of the attack's archival
objection: reformatting now surfaces as "not canonical", not as an unexplained hash mismatch.
Two things genuinely had to go. The 4x16 print grouping put a second grouped-hex convention on a
page where FW-EEG-001 §7.4's spaces are part of a value, had no implementation, and would have
made this the first exception to the certificate template's own "from the record and from
nowhere else" rule — for a benefit the arithmetic overstated, since the field is a table cell,
not a free line. And the first-match shell hint was a foot-gun: I confirmed the first 64-hex
string in a sorted record is identity.firmware_sha256. I can decide this here. Nothing turns on
a measurement that has not been taken or a model that is wrong; every claim on both sides
resolved against files I opened. It stays 'judgement' rather than 'derived' because the choice
among file-bytes, re-serialisation and JCS is settled by argument, not computed.

**Confidence:** judgement  |  **Blocks a build:** no  |  **Signed off by:** Programme lead, as a ruling under ECO-EEG-016 — TST-EEG-004 Rev C §16 item 17 names the programme as owner and states that until it is ruled "two manufacturers can both be right and disagree". The ruling must be entered in tools/RULINGS.md (the source RUL-EEG-021 is generated from; a hand edit in the register is silently reverted) and then RUL-EEG-021 and TST-EEG-004 regenerated. The manufacturer's QA signs the record and certificate against it once ruled; nobody at the manufacturer may set it. The programme counter-signs at goods-in in Brussels (§13 sign-off, RFQ-EEG-001 Rev E §9.3), and it is the programme, not the manufacturer, that recomputes the hash and reissues the certificate at each refurbishment.

**What would change it.**

An ingestion pipeline at goods-in that must re-serialise records before filing them would break
file-bytes hashing and push the decision back towards RFC 8785 JCS — that is the one change that
reverses the ruling rather than trimming it. A first-article manufacturer whose test-station
stack cannot emit sorted-key two-space JSON no longer changes the hash definition at all, only
the severity of the canonical-conformance check, which drops from error to warning; that is the
whole point of separating the two. If the key_fingerprint correction lands in the same
regeneration, the worked example's bytes change and 4255b644... changes with them — the
generator recomputes it, and the ruling's text must not quote a stale value. TST-EEG-004 §16
item 18 stands either way: the schema has never seen a real record, and the first Phase 1 record
is where a field of the wrong shape will be found.

**Files this touches:** `tools/RULINGS.md`, `docs/TST-EEG-004_RevC_production_test_specification.md`, `records/validate_test_record.py`, `records/make_records.py`, `records/TST-EEG-004_RevC_unit_test_record.schema.json`, `records/EXAMPLE_TIOV-B-0000_test.json`, `records/TST-EEG-004_RevC_calibration_certificate.md`, `records/README.txt`, `records/lot_summary_template.csv`, `docs/RUL-EEG-021_RevA_rulings_register.md`, `tools/finalise_docs.py`, `tools/make_docs.py`, `docs/TST-EEG-004_RevC_production_test_specification.docx`, `docs/TST-EEG-004_RevC_production_test_specification.pdf`, `KNOWN_ISSUES.txt`


## D3-BAY-TAG-CAP-HEIGHT

**Question.** PKG-EEG-015 section 2.3 asks for an 8 mm cap height on a 60 x 12 mm foam bay tag and no legend fits (open item 15). Decide the cap height and whether the tag grows.

**Decision.**

TWO blanks, not one, because there are two mounting surfaces with opposite scarcities. 85 x 12
mm at 4.0 mm is withdrawn; 60 x 12 mm is withdrawn; 171 x 21 mm stays rejected. (A) ART-LBL-04A,
rear-wall tag, the six shallow bays (BOOM MICROPHONE, SPARE CUPS + KEYLESS SPARES, SPARE CELL,
CONSUMABLES, EAR CLIPS + EMG LEADS, CABLES + CHARGER): blank 70 x 22 mm, side margins >= 3.0 mm,
top/bottom >= 1.6 mm, up to THREE lines, TAG_LEADING stays at the released 1.25. Uniform cap 5.0
mm. Sized to the FLAT run of the wall, opening - 2R from mech_gen.py:1439-1449: BOOM 181, SPARE
CUPS 80, SPARE CELL 77, CONSUMABLES 78, CABLES 78, EAR CLIPS 74. Binding bay EAR CLIPS at 74,
less the section 2.1 +/-1.0 mm pocket tolerance = 73, so a 70 mm blank keeps >= 1.5 mm of flat
foam each side and touches no fillet. Height costs nothing: every one of these walls is 50 mm
deep or more. Max achievable uniform cap on that blank is 5.53 mm; 5.0 is ruled to leave wrap
and print slack. (B) ART-LBL-04B, top-face tag, the three deep wells (HELMET HM-01, HEADPHONES,
POD-P1 ENCLOSURE): blank 135 x 11 mm, side margins 3.0 mm, top/bottom 1.5 mm, ONE line, uniform
cap 8.0 mm - section 2.3's own figure, MET. Measured need at 8.0 mm plus 2 x 3.0 mm margins:
HELMET HM-01 97.6, HEADPHONES 89.6, POD-P1 ENCLOSURE 128.3, all inside 135. Placement: HELMET
and HEADPHONES in the 14 mm bottom sheet-edge margin strip (11 mm tag leaves 1.5 mm of foam each
side nominal, >= 0.5 mm at the tolerance extreme); POD-P1 in the 181 x 36 mm solid patch above
its bay. Explicit keep-out: the 8 mm halo bearing shelf, the ring between the layer-1 opening
(22, 22, 181, 220) and the layers-2-to-7 opening (14, 14, 197, 236). No label goes under the
only load path in the pack. (C) Section 2.3's 8 mm is NOT withdrawn wholesale. It is met on the
three deep wells and restated as unattainable on a rear wall, on a measured reason the original
ruling never gave: at an 8 mm cap CONSUMABLES is 92.2 mm of text as ONE unbreakable word,
needing a 98.2 mm blank at 3 mm margins against a 78 mm flat wall. No line count fixes a single
word. (D) Precondition - open item 16 is ruled BEFORE this is applied to the spare-cell tag, and
it does not change the cap. Bare `SPARE CELL`, or D4's `SPARE CELL` / `EMPTY IN CIRCULATION`,
fits 70 x 22 at 5.0 mm on <= 3 lines. The full section-7 string `SPARE CELL -- DEPOT ONLY, EMPTY
IN CIRCULATION` also fits at 5.0 mm, on four lines (widest word CIRCULATION = 50.4 mm), block 4
x 5.0 + 3 x 1.25 + 2 x 1.6 = 27.0 mm, so that one tag - or all six rear-wall tags - goes to 70 x
27 mm on a 50 mm wall. The UN 3481 / PI967 control string can be kept in full at the ruled cap.
There is no longer any typographic pressure to shorten it.

**What the attack changed.**

CONCEDED, all verified in the files. 1. 85 mm is unbuildable. Bay openings are filleted
rectangles - mech_gen.py `rounded()` at :1504 draws every profile with the radii of the BAYS
table at :1439-1449, and section 2.2 states the same radii and why. Flat run = opening - 2R:
SPARE CELL 77 (not 93), SPARE CUPS 80, CONSUMABLES 78, CABLES 78, EAR CLIPS 74 short / 80 long.
The "about 4 mm each side" is minus 4 mm. Worse, the decision's own binding one-line case fails
on its own bay: EAR CLIPS + EMG LEADS is 74.79 mm of text at 4.0 mm, 80.8 mm with the ruled >=
3.0 mm margins, over BOTH of that bay's flat walls. Which wall is "rear" is nowhere defined in
the package, so even the most favourable reading leaves SPARE CELL (77), SPARE CUPS (80) and EAR
CLIPS (80) unable to take 85 mm flat. 2. 12 mm is not a Rev C sheet constraint on a rear wall.
Every shallow bay is 50 mm deep or more (section 2.2 Cut depth column). The 14 mm edge margin
binds only the HEADPHONES and HELMET top-face tags. Forcing one blank made six height-rich,
width-poor tags inherit a ceiling that belongs to three width-rich, height-poor ones. 3. 171 mm
is a tool artifact. `max_lines=2` at artwork_gen.py:1244 and the `need` computation at
:1251-1252, which only ever considers a 1-line and a half-and-half 2-line break. Freed of that,
the width price of an 8 mm cap is 98.2 mm, set by CONSUMABLES, not 171. 4. Six bays are narrower
than 171 mm, not five - POD-P1 ENCLOSURE is 169. 5. The helmet top-face geometry was loosely
stated. Layer 1 leaves a 181 x 22 mm band below the opening and 181 x 16 above, not "the 14 mm
margin and the 8 mm webs". The conclusion (do not tag it) survives, but only because 8 mm of
that band is the halo bearing shelf - a reason the ruling never gave. It is now written into the
decision as a keep-out. 6. TAG_LEADING 1.25 -> 1.2 was an unannounced change to
artwork_gen.py:1185 that made the two-line block land at exactly 12.000 mm. Reverted; the
released 1.25 stands. 7. Ordering. The width table measures the bare `SPARE CELL` (35.82 + 4 =
39.8, reproduces exactly) while the ruling text simultaneously requires a two-line spare-cell
tag from D4. On 85 x 12 at 4.0 mm the section-7 string does NOT fit at any line count: its best
two-line split needs an 89.5 mm blank, at 85 mm it can only reach 3.79 mm, and greedy `wrap()`
breaks it to three lines and a 16.8 mm block. The arithmetic closes only if D4 is applied - i.e.
a UN 3481 control string is shortened as a side effect of a typography ruling. That is the right
criticism and it reverses the order of work. KEPT, and the attack is wrong or short here. a. The
4.0 mm arithmetic was CORRECT for the blank it was computed on. I reproduced all nine widths to
0.1 mm with the package's own metric, and on 85 x 12 at 3.0/1.6 margins, <= 2 lines, the largest
uniform cap is exactly 4.00 mm, binding on SPARE CUPS + KEYLESS SPARES. The measurement was
sound; it was applied to a blank that cannot be bonded. b. The attack's 6.13 mm and 6.86 mm are
correct arithmetic on an 85 mm blank with the height freed - but 85 mm is the width the attack
itself proves unbuildable, so those describe a tag that cannot be stuck to anything either. The
achievable rear-wall figures are 4.97 mm (70 x 18, <= 2 lines, reproduces exactly) and 5.53 mm
(70 x 22, <= 3 lines; the attack says 5.55, which is CONSUMABLES' cap, not the binding one). c.
The attack undersells the top face. It offers HEADPHONES "a 7 mm cap on one line". All three
deep-well legends carry a full 8.00 mm cap on one line on a 135 x 11 mm blank inside the 14 mm
strip. Section 2.3's requirement is achievable where it matters most and should not have been
withdrawn there. d. The rejection of 171 x 21 stands and is stronger than stated - six bays, and
no rear wall has 171 mm of flat run except BOOM MICROPHONE at 181. e. Unrelated to the attack:
the ruling's ANSI Z535.4 "about five times the rule of thumb" is not sourced anywhere in package
v2.3. Do not carry that sentence into the document.

**Reasoning.**

The attack breaks the two load-bearing numbers and I checked both against the released generator
rather than taking them on trust. The fillets are real and drawn (mech_gen.py `rounded()`), so a
tag bonds to opening - 2R, and 85 mm exceeds that on the bays the decision named. The 12 mm
ceiling is real but belongs only to the three top-face tags, where the neighbouring foam is the
14 mm sheet-edge margin; on a rear wall there are 50 mm of depth and no ceiling at all. Once
those two errors are separated, the geometry stops being one problem and becomes two, with
opposite scarcities - and a single blank is the worst possible answer to that, because it hands
each family the other family's constraint. Two blanks cost one extra steel-rule die at Phase 3
and buy a 25 percent taller cap on the rear walls and section 2.3's full 8 mm on the deep wells.
I did not concede the cap arithmetic, because it reproduces exactly and the attack's replacement
figures are computed on the same 85 mm blank it had just declared unbuildable. What was wrong
was the surface it was measured against, not the metric. The most consequential correction is
the ordering one. The old ruling made a dangerous-goods content question (open item 16) depend
on a typography ruling, and D4's answer - shortening the string - only looked necessary because
of a false 12 mm ceiling. Remove the ceiling and the pressure disappears: the full `SPARE CELL
-- DEPOT ONLY, EMPTY IN CIRCULATION` fits at the ruled 5.0 mm cap on four lines and a 27 mm
blank, on a wall that is 50 mm deep. The typography now costs the DG control nothing, which is
the correct relationship between the two. Values chosen deliberately below the maximum: 5.0 mm
against an achievable 5.53, and a 70 mm blank against a 73 mm worst-case flat run, so that the
ruling does not repeat the zero-slack fault the attack correctly identified in the 12.000 mm
block.

**Confidence:** derived  |  **Blocks a build:** no  |  **Signed off by:** Programme packaging owner with QA for the two blank geometries and the caps, at the trial pack of section 9 open item 1 against a measured shell; the programme's DG-trained shipper (REG-EEG-012 Rev B section 3.7) signs the spare-cell legend under open item 16 BEFORE this cap ruling is applied to that tag. Raised as an ECO under ECO-EEG-016, changing PKG-EEG-015 sections 2.3 and 4.2 together, with QP-EEG-010 FK-04 amended to a falsifiable acceptance (a named minimum cap and no lifted edge after one pack/unpack cycle).

**What would change it.**

1. Open item 16 ruled to keep the full section-7 string: the rear-wall blank goes from 70 x 22
to 70 x 27 mm at the same 5.0 mm cap, on four lines. The cap does not move. 2. A trial pack
showing a 22 mm polyester tag will not stay bonded to cut PE at mid-depth through one
pack/unpack cycle, or that a participant cannot read a tag 25 mm down a 50 mm well - then the
rear-wall family moves back to the top face where there is no room, and the whole scheme is a
Rev D. 3. A measured shell that changes the 516 x 390 mm sheet, and therefore the 14 mm edge
margins that cap the top-face tag at 11 mm and its 8.0 mm cap. 4. A definition of which of a
bay's four walls is "the rear wall". If it is ruled to be the LONG wall of every bay, the
binding flat run rises from 74 to 77 mm and the rear-wall blank can go to about 73 mm, worth
roughly +0.2 mm of cap - not enough to change the ruling, but it should be written down rather
than left open. 5. A Rev D re-columned sheet (already contemplated for the finger reliefs of
open item 12) that widens the webs and the bays - it would move every flat run in this decision.

**Files this touches:** `docs/PKG-EEG-015_RevB_packing_labelling_and_shipping.md`, `tools/artwork_gen.py`, `docs/ECO-EEG-016_RevB_change_control_and_document_register.md`, `docs/QP-EEG-010_RevB_quality_plan.md`


## D4-SPARE-CELL-TAG

**Question.** The spare-cell bay tag is specified twice - section 4.2 makes it `SPARE CELL` (identical to the section 2.2 schedule) and section 7 makes it `SPARE CELL -- DEPOT ONLY, EMPTY IN CIRCULATION` (open item 16). Which governs?

**Decision.**

Section 2.2 governs. The tag reads `SPARE CELL` alone - one line, no sub-legend, no new blank
size, and no amendment to the section 4.2 rule. The attack is upheld and its correction adopted,
with two amendments where the correction is itself wrong or incomplete. VALUES, all recomputed
with the package's own tools/artwork_gen.text_width() against the real blank: - Blank: 60 x 12
mm, unchanged (PKG-EEG-015 section 4.2 ART-LBL-04 row). Live box 56.0 x 10.4 mm (w -
2*TAG_MARGIN, h - 2*0.8). - Legend: `SPARE CELL`, byte-identical to the section 2.2 schedule. -
Cap height as generated: 6.25 mm on ONE line. That is the LARGEST cap of the nine tags, ahead of
HEADPHONES at 5.36. It was 2.68 mm on two lines, the smallest. The strict reading of 4.2 turns
the worst tag in the kit into the best one. - Resulting cap range for the nine tags: 6.25 SPARE
CELL / 5.36 HEADPHONES / 4.89 HELMET HM-01 / 4.86 CONSUMABLES / 4.62 POD-P1 ENCLOSURE, BOOM
MICROPHONE, EAR CLIPS + EMG LEADS, CABLES + CHARGER / 4.35 SPARE CUPS + KEYLESS SPARES. - Open
item 15's proposal re-derives from about 171 x 21 mm to about 110 x 21 mm; the width driver
moves from the spare-cell tag to `EAR CLIPS + EMG LEADS` at 109.8 mm. I ran this: it recomputes
by itself. WHAT TO WRITE: 1. Section 4.2: replace the "specified twice" paragraph (lines
738-742) with a plain statement that the ART-LBL-04 legends are the section 2.2 schedule legends
verbatim with no exception, and that the spare-cell tag reads `SPARE CELL`. The rule itself is
untouched; it was never the problem. TRAP: do not write the phrase "its tag reads `...`" into
the replacement text - Doc.spare_cell_tag() regexes that phrase over the WHOLE document, so it
would reactivate the override from section 4.2. 2. Section 7 (line 976-977): keep "The SPARE
CELL bay stays in the foam and stays empty in circulation; it carries a spare only on depot-to-
depot moves handled by the programme's trained shipper" and DELETE only ", and its tag reads
`SPARE CELL -- DEPOT ONLY, EMPTY IN CIRCULATION`". Replace it with the depot control that
actually binds a shipper: the bay is filled and emptied against KPL-EEG-001 and the section 8
despatch record. 3. Section 2.3: the drift sentence stands. Delete the worked example "the
section 7 form of the spare-cell tag 320 mm" (it was arithmetically right - 319.9 mm - but it
ceases to exist). The range sentence changes at BOTH ends: "runs from 5.36 mm on `HEADPHONES`
down to 2.68 mm on the spare-cell tag" becomes "runs from 6.25 mm on `SPARE CELL` down to 4.35
mm on `SPARE CUPS + KEYLESS SPARES`". The 88 mm HEADPHONES example stays valid; `SPARE CELL`
alone needs 75.6 mm at 8 mm caps and is no longer the driver. 4. Open item 15: stays open; its
figure is restated as about 110 x 21 mm. 5. Open item 16: closed - "section 2.2 governs; section
7's tag clause withdrawn; the participant control is IFU-EEG-014 section 1". 6. Same ECO, not
later: SVC-EEG-013 line 348 drops the clause; SVC-EEG-013 section 9 item 7 (line 955, "Closed at
this issue") is restated, because it is closed on the strength of the string being withdrawn;
REG-EEG-012 (~line 360) becomes "section 2.2 governs the tag, section 7 governs the bay". 7.
Regenerate ART-LBL-04_bay_tag_spare_cell.svg, ART-LBL-04_foam_bay_tags.pdf and re-hash
README_artwork.txt (lines 31, 44, 92). If the programme later decides the prohibition must
appear on the foam, the honest form is a SECOND tag at its own size on its own section 4.2 row -
not a second line on a 60 mm blank - taken with open item 15 at the trial pack.

**What the attack changed.**

CONCEDED - the decision is fatally wrong, and I verified every number rather than taking the
attack's word. 1. UNBUILDABLE, confirmed. The blank is 60 x 12 mm, not 85. Section 4.2's ART-
LBL-04 row, section 2.3 ("60 x 12 mm"), open item 15, README_artwork.txt line 31 and the shipped
SVG (`viewBox="0 0 60.0000 12.0000"`) all agree; "85" appears nowhere as a tag dimension. The
decision's own figures refute it: at a 4.0 mm cap, text_width gives `SPARE CELL` 35.82 mm glyph
+ 2x2.0 TAG_MARGIN = 39.82, and `EMPTY IN CIRCULATION` 71.52 + 4 = 75.52. Those ARE the
decision's 39.8 and 75.5 - they are required BLANK widths, not widths "inside the 85 mm blank".
75.5 > 60; live width is 56.0 and the line is 27.7% too wide. Max cap for the decision's own
two-line layout on the real blank is 3.132 mm; it is 4.530 mm on a hypothetical 85 mm blank,
which is exactly where the 4.0 came from. 2. Height claim wrong. _fit_cap uses n*cap +
(n-1)*cap*(TAG_LEADING-1): two lines at 4.0 = 9.0 mm of type in a 10.4 mm live height, not
"exactly the 12 mm". 3. No ruled 4.0 mm cap exists. WANT_CAP = 8.0, from section 2.3 "Cap height
8 mm". No tag is set at 4.0. The uniformity the decision invoked is fabricated. 4. The rejected
option is misdescribed. artwork_gen.py:1244 calls _fit_cap(..., max_lines=2) - two lines is a
hard cap, three is unreachable. The shipped SVG says "cap height 2.68 mm on 2 line(s)" on the
same 60 x 12 blank as the other eight. "Three lines, a second tag size for one bay" is false on
both counts, and the 2.68 the decision quoted IS the two-line result. 5. The gain would have
been 0.45 mm (2.68 -> 3.13), still 28% below the next-smallest at 4.35. The decision's own
premise - that this exception makes the tag the worst in the kit - survives its own fix. 6. "The
only printed control" is false. IFU-EEG-014 Rev B lines 61 and 66, a lid-wallet item, already
carry "Empty, on every kit and every leg. Your kit has one battery and it is already inside the
box. Nothing here is missing" and "If a hollow is empty and it is not the SPARE CELL one, tell
us before you start." 7. Cross-document breakage, confirmed at the cited lines and named nowhere
in files_to_update: SVC-EEG-013 line 955 item 7 is "Closed at this issue" resting on the section
7 string, line 348 restates it in the packing procedure, REG-EEG-012 ~line 360 says "sections
2.2 and 7 govern that bay and its tag". 8. Amending 4.2 without 2.3 is forbidden in terms by
open item 15 ("Changing the tag changes section 4.2 and section 2.3 together"), and
Doc.size_mm() parses ONLY the section 4.2 size cell - so an 85 mm edit there would silently
regenerate 85 mm artwork against a 60 mm section 2.3: the exact drift the decision claimed to
defend. 9. The 17/14 mm argument is attached to the wrong bay. Section 2.3 gives deep wells
(helmet, pod, headphones) a top-face tag; SPARE CELL is shallow - section 2.2 line 354 puts it
on layers 1 to 2, 50 mm - so its tag is on a 50 mm rear wall. The 14 mm figure is a foam-bay-to-
sheet-edge PLAN margin (lines 361 and 530), not a tag-height limit. 10. "Still machine-checked
against the cut file" is false. artwork_gen parses the section 2.2 Markdown table;
mech_gen.py:1445 carries the bay schedule as its own hardcoded Python tuple; artwork_gen
contains no reference to mech_gen or to any dxf. The tag is checked against the document, not
the DXF. 11. Stale side effect confirmed: the decision's own scenario makes `EMPTY IN
CIRCULATION` at 8 mm the driver at 143.04 + 4 = 147 mm, so it left open item 15 carrying 171 mm
that it had itself invalidated. KEPT from the original decision - one thing. 'DEPOT ONLY' is an
instruction to a trained shipper working from the packing list and the despatch record. That is
a reason to route it to KPL-EEG-001 and the section 8 record, which is where item 2 above puts
it - not a reason to keep half of it on a participant-facing tag. REJECTED FROM THE ATTACK'S OWN
CORRECTION - two things, both checked: A. Its item 7 says to delete the "--" XML-comment
workaround in Art._comment() because it "exists only for this string". It does not. I grepped
the generated SVGs for the en-dash substitution and found it live in three files: ART-
LBL-02_kit_id_plate.svg ("KIT-007 in 24 pt, ... unit serial beneath"), ART-
LBL-05_carton_marking_set.svg ("FRAGILE -- RESEARCH INSTRUMENT") and the spare-cell tag.
Deleting that guard would emit SVGs that every conforming XML parser rejects for two labels
unrelated to the spare cell - the precise failure its own docstring records. KEEP the guard;
only its docstring example changes. B. Its item 3 changes only the "down to" half of section
2.3's cap range. Both halves change, because bare `SPARE CELL` at 6.25 mm becomes the largest-
set tag of the nine, displacing HEADPHONES at the top of the range. REFINEMENT: the attack
treats the code deletion as part of the ruling. It is not. Doc.spare_cell_tag() matches "its tag
reads `...`" over the whole document; delete section 7's clause and it returns None, the branch
at line 1242 goes inert, and I ran it - `SPARE CELL` regenerates at 6.25 mm on one line and the
open-item-15 proposal recomputes to (110.0, 21.0) with no code change at all. Removing the dead
code is optional tidying and must not be conflated with the ruling.

**Reasoning.**

The decision was built on a blank size that does not exist in the package. Everything downstream
of "85 x 12 mm" - the claim that both lines fit, the "4.0 mm cap like every other tag", the
"exactly 12 mm" height, the three-line/second-tag-size straw man it rejected - collapses with
it. Worse, the two numbers it cited as proof of fit (39.8 and 75.5) are the package's own
required-blank-width outputs, so the decision quoted the very numbers that refute it. On the
real 60 x 12 blank its layout sets at 3.13 mm, a 0.45 mm gain that leaves the tag still 28%
below the next-smallest and still the worst in the kit - the exact defect it was written to
cure. Once that is gone, the question is easy and the files answer it. Section 4.2's rule and
section 2.3's drift invariant both say the legend is the schedule legend; artwork_gen enforces
it by reading the schedule rather than having it typed; and the only reason ever offered for the
exception was that the second line is the sole printed control against a participant refilling
an empty lithium bay. That reason is false: IFU-EEG-014 Rev B carries a longer, plainer,
participant-facing control in the lid wallet, read before unpacking, in words that 20 characters
of 3 mm type on a foam wall cannot match. And the decision's split-by-audience premise is wrong
about geography - by section 2.3 the tag sits on a shallow-bay rear wall inside the
participant's own case, so the "shipper-only" half reaches the participant either way. Its
safety logic also inverts: it deletes the half that forbids ('DEPOT ONLY') and keeps the half
that merely describes the condition that tempts refilling. The payoff for the strict reading is
not neutral, it is positive: bare `SPARE CELL` sets at 6.25 mm, the largest cap of the nine
tags, and the still-open item 15 proposal falls from about 171 x 21 mm to about 110 x 21 mm
because the spare-cell tag stops being the width driver. I confirmed both by running the
generator with the section 7 clause removed. Where I part from the attack is on its remedy, not
its case. It would delete an XML well-formedness guard on the belief that only this string needs
it; two other labels trigger it today, and removing it would ship parser-rejected artwork for
the kit ID plate and the carton marking set. It also under-specifies the section 2.3 edit by
half a sentence. And it overstates the code work: the generator already degrades correctly the
moment the document clause goes, which matters because it means the ruling is a documentation
change with a regeneration, not a code change someone could get wrong.

**Confidence:** derived  |  **Blocks a build:** no  |  **Signed off by:** Programme, with the DG-trained shipper who signs the UN 3481 / PI967 row of PKG-EEG-015 section 7 itself - note the original decision's "named in QP-EEG-010" is wrong: QP-EEG-010 names no shipper, it carries audit row A-22 "Is the delivery free of a spare cell?". QA at the trial pack (QP-EEG-010 FK-04, legend present and legible after one pack/unpack cycle). The SVC-EEG-013 owner, because section 9 item 7 is currently marked "Closed at this issue" on the strength of the string being withdrawn and cannot be left standing. ECO under ECO-EEG-016 as ONE change covering sections 4.2, 2.3 and 7, open items 15 and 16, and the two other documents - a ruling that silently un-closes another document's closed item is not closed.

**What would change it.**

A ruling that the charged spare returns to the circulating kit: that puts every consignment
under PI966 instead of UN 3481 / PI967 section II, contradicts RFQ-EEG-001 Rev E S-09, and
changes the message entirely - it would also require re-opening REG-EEG-012 section 3.1 and PKG-
EEG-015 section 7, which that section already says in terms. Or the DG-trained shipper ruling
that the prohibition must appear on the foam and not only on KPL-EEG-001 and the despatch
record: that is a SECOND tag at its own size on its own section 4.2 row, not a second line, and
it belongs with open item 15 and D3 at the trial pack. Or a measured shell (open item 2) forcing
a foam re-layout that changes the SPARE CELL bay from shallow to a deep well, which would move
its tag to the top face and re-open the height question. Nothing about the 60 x 12 mm blank or
the 6.25 mm cap changes without one of those.

**Files this touches:** `docs/PKG-EEG-015_RevB_packing_labelling_and_shipping.md`, `docs/SVC-EEG-013_RevB_service_and_refurbishment_manual.md`, `docs/REG-EEG-012_RevB_regulatory_and_compliance_file.md`, `docs/ECO-EEG-016_RevB_change_control_and_document_register.md`, `tools/artwork_gen.py`, `graphics/labels/ART-LBL-04_bay_tag_spare_cell.svg`, `graphics/labels/ART-LBL-04_foam_bay_tags.pdf`, `graphics/labels/README_artwork.txt`


## D5-LABEL-POSITIONS

**Question.** Section 4.2 fixes each label's face and size but not where it sits on that face; DRW-LBL-PLACEMENT's positions are a proposal (open item 17). Can those positions be released, and with what values?

**Decision.**

Positions are released as an edge-dimensioned arrangement, with the tamper seal re-oriented, the
bay-tag depth moved off the foam layer joint, and two items explicitly NOT released. RELEASED,
dimensioned from the two nearest edges (a measured shell changes the numbers, not the
arrangement): - ART-LBL-01 (50 x 25), primary: POD-P1 lid outer face, centred in the flat 55 x
30 keep-out, 2.5 mm all round = 56.5 mm from the left, 59.0 mm from the bottom of the 163 x 143
lid, clear of the gasket line (4.1). Arithmetic verified. - ART-LBL-02 (80 x 40): case lid
exterior, 40 mm from the left edge, 40 mm from the lid's top edge, wholly on flat moulding. -
ART-LBL-03 (100 x 60): case base exterior, centred, wholly inside one flat moulded panel, never
bridging a foot, rib or skid. FALLBACK REWRITTEN: if the measured shell carries no 100 x 60 flat
panel, a reduced variant is drawn to the largest flat panel found — the pattern 4.2 already uses
for ART-LBL-06 ("reduced 105 x 74 where the face is too small", and `ART-
LBL-06_lithium_battery_mark_reduced.svg` already exists). The label is never applied bridging a
rib. - ART-LBL-06 (120 x 110): a 535 x 345 SIDE face, centred, 40 mm from the top — what 4.2
already says. The side face takes it at full size; no reduced variant needed. - CARTON LONG
FACE, both items in the upper band: document wallet (225 x 165) top-left, 40 mm from the left
and 40 mm from the top; ART-LBL-05 (200 x 150) top-right, 40 mm from the right and 40 mm from
the top. On the opposite long face ART-LBL-05 is centred, 40 mm from the top. 225 + 200 = 425
across a 640 mm face leaves 135 mm of slack, so they sit side by side in x and the overlap is
gone. Face dimensions are stated as EXTERNAL (about 654 x 359 in double-wall BC), not the 640 x
345 internal. - ART-LBL-07 (90 x 20, two off): applied across each hasp with its 90 mm axis
PERPENDICULAR to the lid/base split, the centre perforation ON the split, 45 mm on the lid and
45 mm on the base, centred on the latch's horizontal centreline, on flat shell and clear of the
gasket sealing face. Dimensioned from the latch, not the shell edge. - BAY TAGS (ART-LBL-04):
rear-wall tags are centred within the cut face of layer 1 and never cross a layer joint — 12.5
mm down, one number for all six shallow bays. The wall is named in cut-file terms (the +Y wall
of the bay as drawn in `mech/CASE-00_foam_layer_1.dxf`), not "rear" or "longest rear", neither
of which has a datum anywhere in the package. HELMET and HEADPHONES take the top-face tag
centred on the bay's own width in the 14 mm sheet-edge margin; POD-P1 takes the solid patch
above its bay, which is 181 x 44 (376 - 332 by the schedule's own closure), not the 181 x 36 the
document states. - The pressure-equalisation valve stays a written constraint, not a drawn keep-
out. NOT RELEASED, and named as still open: - ART-LBL-01's lid-interior duplicate stays an
explicit proposal. Section 4.1 says only "One identical label inside the case lid"; 3.2 says
only that the lid "retains" the A4 wallet and never positions it; DRW-LBL-PLACEMENT has four
views and none is the lid interior. There is no datum to dimension from and nothing for QA to
sign against. When it is fixed, it must be clear of the 15 mm convoluted lid pad of section 2.1.
- Bay-tag WIDTH is out of scope here and the positions above are height-rules only. The 12.5 mm
depth rule survives any tag up to about 21 mm tall; the width does not survive as stated.
DRAWING CONSEQUENCE: DRW-LBL-PLACEMENT view 2 is a plan of the lid exterior and cannot express a
seal that wraps the split. It needs a front elevation at the latches, and a fifth/sixth view for
the lid interior if the duplicate is ever fixed.

**What the attack changed.**

CONCEDED — all five numbered points, each verified in the files: 1. Bay-tag depth. Section 2.1
line 276 is "Seven loose-laid 25 mm layers"; the 2.2 schedule cuts BOOM MICROPHONE, SPARE CUPS,
SPARE CELL and EAR CLIPS through layers 1 to 2 at depth 50. "25 mm down on a 50 mm bay" is
exactly the layer 1/2 interface, so a 12 mm tag with permanent acrylic bonds two sheets the spec
says are not bonded, defeats SVC-EEG-013 line 392 ("replace any layer whose bay no longer
retains its item"), and shears in transit against a legibility check QP-EEG-010 FK-04 signs
(line 460). Changed to 12.5 mm, uniform, inside layer 1. 2. Tamper seal. `art_lbl_07()` line
1482 draws the perforation at x = w/2 down the 20 mm axis with the comment "the seal is cut by
the hasp: the perforation line is drawn as the die instruction", and lays the copy in two 45 mm
halves. "10 mm each side of the split" leaves that die line perpendicular to the opening motion,
doing nothing, and gives a removable adhesive only 10 mm of reach across the FC-30 quarantine
boundary. The drawing is worse than the attack said: `drw_lbl_placement()` lines 1748-1749 place
the seal at y=0.0, 90 x 20 — wholly on the lid, not straddling at all. Rotated to match the
released artwork. 3. "Faces and sizes are fixed" is false where Correction 1 turns on it. 4.2's
Size cell for ART-LBL-05 reads "printed on the carton"; the 200 x 150 is `art_lbl_05()`'s own
hardcoded `w, h = 200.0, 150.0` (line 1271), where ART-LBL-04 and ART-LBL-07 call
`doc.size_mm()`. Resizing the printed set was a live option that was never weighed. "Arithmetic,
not taste" is withdrawn; the side-by-side arrangement is kept as a judgement. 4. ART-LBL-03's
fallback contradicted its own rule — centring a 100 x 60 label on a flat area smaller than 100 x
60 bridges a rib by construction, on the face the decision itself calls the abrasion face.
Replaced with 4.2's own reduced-variant pattern. 5. ART-LBL-01's duplicate was released against
a datum the package does not carry. Demoted to proposal. Lesser, all confirmed: the 85 x 12 tag
exists nowhere in v2.3 (4.2 line 720 holds 60 x 12), and the D3 ruling that set it was itself
returned WRONG — so Correction 3 could not be dimensioned to it. Worse, D5's own justification
("85 mm fits the 93 mm SPARE CELL rear wall") is wrong for the same reason D3 was: `mech_gen.py`
lines 1439-1447 give every bay a corner radius, so the flat run is opening minus 2R — SPARE CELL
77, EAR CLIPS 74, SPARE CUPS 80, CONSUMABLES and CABLES 78. "Rear wall" has no datum: nothing in
the document orients the sheet to the hinge (grep for hinge returns nothing). 181 x 36 is 181 x
44. The 640 x 345 is internal. REJECTED — two things the attack got wrong or overreached on: A.
"The bonded area on each side of the tamper boundary falls from 45 mm to 10 mm." As area those
are identical: 45 x 20 = 900 mm2 and 90 x 10 = 900 mm2. The real defects are the dead die line
and the 10 mm peel reach on a removable adhesive. Conclusion kept, reasoning corrected. B. The
carton swap as proposed — wallet top-left, ART-LBL-05 bottom-right — is refused. ART-LBL-05
carries the ISO 780 THIS WAY UP pair, drawn as two upright arrows at `art_lbl_05()` lines
1279-1284, plus FRAGILE. Handling marks belong in the upper band of the face, not the bottom-
right corner. The attack treated the vertical band as a zero-sum choice when it is not: the two
sit side by side in x with 135 mm of slack, so BOTH go to the top. The wallet gets the abrasion
protection the attack correctly argued for, and the handling marks keep the position the
standard puts them in. Also declined as defects, kept as notes only: the UN3481-versus-counter
point (4.2 says "one side face" in terms, and the attack concedes Correction 2 is right — this
is a one-line trade to record, not an error), and the helmet 22-vs-14 mm point (the attack
concedes its own conclusion survives, since 8 mm of the 22 is the halo shelf).

**Reasoning.**

The attack's core is right and it is right for a reason worth stating: three of its five points
are not taste, they are a released artifact contradicting itself. The perforation in
`art_lbl_07()` is a die instruction to the printer; a placement that leaves it perpendicular to
the shear plane ships a seal that cannot part where it is cut. The 25 mm bay-tag depth lands on
the one plane in a seven-layer loose-laid stack where adhesive is forbidden by construction. The
ART-LBL-03 escape clause instructs the packer to do the thing the sentence before it prohibits.
Each of those is checkable and each checked out. What the attack did not break is the shape of
the answer. The 200 x 40 overlap between ART-LBL-05 and the document wallet is real, reproduced
at `drw_lbl_placement()` lines 1767-1771; section 6 pins the wallet to one long face and 4.2
pins ART-LBL-05 to two opposing long faces, so they must share; 425 mm across a 640 mm face
means they fit side by side. That resolution stands. So does edge-dimensioning, which is the
property that makes every number here survive a measured shell, and so does Correction 2, which
only restores what 4.2 already says. Where I part company with the attack is the carton vertical
band. Its abrasion argument for the wallet is sound — the pocket holding the pre-paid return
label is the item whose loss strands a kit in a participant's home, and 40 mm off the deck on a
carton that is set down and dragged twice per loan is the wrong band for it. But the fix it
proposed pays for that by putting THIS WAY UP and FRAGILE in the bottom-right corner, and those
marks exist to be read by a handler at a glance. The constraint that makes both possible is the
one the decision itself discovered: the labels are side by side in x, so the y band is free for
each independently. Putting both at 40 mm from the top costs nothing and loses neither argument.
Two things genuinely cannot be settled from what exists, and inventing values for them would be
the failure this review is for. The bay-tag width depends on a tag size that is currently in
three states at once — 60 x 12 in section 4.2 and the generator, 85 x 12 from a D3 ruling that
was itself returned WRONG, 171 x 21 in open item 15 — and it must be checked against the flat
wall (opening minus 2R, binding at 74 to 77 mm), not the opening. At 171 mm every rear-wall
position fails. So I release the depth rule and the wall identification, which are stable under
any tag size up to about 21 mm tall, and send the width back with the geometric budget attached.
And the lid-interior duplicate has no datum at all: no wallet position, no drawing view, a 15 mm
convoluted pad on the same face with no clearance called out. A position released against
nothing is exactly the failure the decision existed to remove, so it stays a proposal and says
so.

**Confidence:** judgement  |  **Blocks a build:** no  |  **Signed off by:** Programme mechanical for the tamper-seal orientation against the measured shell — it must confirm 45 mm of flat shell each side of the split beside each latch and that the seal clears the gasket sealing face, which is the IP67 requirement M-05 — and for the POD-P1 lid keep-out and the ART-LBL-01 unit-label position, which is the M-03 label on the enclosure a participant handles. Packer and QA together at the first packed kit for every other position, against a shell that has been measured (open items 2 and 17). The bay-tag width goes back to whoever closes open item 15 and re-rules D3-BAY-TAG-CAP-HEIGHT; it is not closed here. Open item 16 (the spare-cell legend) has to close before the width can, since it is the width driver.

**What would change it.**

The measured shell and the carton built to it — every number above is dimensioned from an edge
or from the latch so those measurements change numbers and not arrangement. A latch area with
less than 45 mm of flat shell each side of the split, or a gasket face that runs too close: in
that case ART-LBL-07 is re-drawn (shorter, or with the perforation moved to the long
centreline), and the placement is NOT rotated back against the die line. A moulded feature at
40/40 on the lid, or a base with no 100 x 60 flat panel. The closure of open items 15 and 16,
which sets the tag width and must be checked against opening minus 2R with the binding wall at
74 mm (EAR CLIPS + EMG LEADS) or 77 mm (SPARE CELL), not against the opening. A stated position
for the A4 wallet in the lid, which is what would let the ART-LBL-01 duplicate move from
proposal to released. An HM-01 drawing: the Phase 2 and 3 unit-label placement on the occipital
shell rear face stays undimensioned and is explicitly not decided here.

**Files this touches:** `docs/PKG-EEG-015_RevB_packing_labelling_and_shipping.md`, `tools/artwork_gen.py`, `graphics/labels/DRW-LBL-PLACEMENT_label_placement.svg`, `graphics/labels/DRW-LBL-PLACEMENT_label_placement.pdf`, `graphics/labels/README_artwork.txt`, `KNOWN_ISSUES.txt`


## D6-SPECIMEN-SERIAL

**Question.** The specimen unit label needs a serial, and every serial the scheme allocates names a unit that will exist (open item 18).

**Decision.**

TIOV-B-0000 is reserved permanently and never allocated — outcome unchanged — but on the
firmware-sentinel basis, not the block-range basis, and with three of the four operative clauses
rewritten. RULING TEXT (PKG-EEG-015 §5, replacing the "Proposed, and not yet ruled" paragraph):
TIOV-B-0000 is the pre-provisioning sentinel that `firmware/main/drivers.c` `unit_serial_into()`
writes and that the USB iSerialNumber (main.c:715/731) and the IDENTIFY reply (main.c:524) carry
until end-of-line provisioning step 6b. `firmware/tools/provision.py check_serial()` refuses it
as a --serial argument and TOOL-EEG-022 treats it as "not provisioned". It is therefore
permanently unallocatable — which is why the blocks start at 0001 — and the specimen may use it
precisely because no unit ever leaves the line bearing it. Stated plainly, and reversing what
the withdrawn wording implied: an unprovisioned unit on the bench DOES report 0000, so 0000 on a
label means "not a released unit", not "not a unit". SPECIMEN VALUES (all unchanged): unit
serial TIOV-B-0000; kit id KIT-000; hardware revision EEG-CAR-01-B; ATECC factory serial
0123456789ABCDEF01; fingerprint 9F2C 4108 BB37 1D0A; real ECC200 Data Matrix of
`TIOV-B-0000|EEG-CAR-01-B|0123456789ABCDEF01|9F2C4108BB371D0A` — I ran the encoder: 60
characters, 32x32, 0.375 mm module at 12 mm. Artwork otherwise identical to production: no
overprint, no watermark, no changed text. records/EXAMPLE_TIOV-B-0000_test.json keeps the serial
with record_type `example`. NEW CLAUSE — QUARANTINE RULE PLUS A MACHINE GATE: a unit whose T5b
iSerialNumber, whose label, or whose record reads TIOV-B-0000 is unprovisioned and is
quarantined; this is not a consistency failure and self-consistency at 0000 does not clear it.
One line in §5, one in TST-EEG-004, and — load-bearing — a PHASE_BLOCKS check in
`records/validate_test_record.py cross_checks()` under `if production:`, mirroring
provision.py:314. OVERPRINT STILL REFUSED, on the two grounds that survive measurement: appended
to the serial line, "TIOV-B-0000 SPECIMEN" is 45.73 mm at the 10 pt floor and 51.57 mm at the
2.9 mm cap actually drawn, against a 33.85 mm column, so it shrinks the serial to 1.90 mm cap =
7.4 pt and breaches §4.1's 10 pt minimum — the `serial_cap` vs `serial_cap_minimum` check
already in artwork_gen.py. A separate tenth line would fit, and the ruling concedes it: the grid
leaves 1.55 mm of the 22.2 mm field, and "SPECIMEN - NOT A UNIT" at 1.2 mm cap is 19.57 mm wide
in a 33.85 mm column. It is refused on the evidence ground alone — a specimen whose artwork
differs from production stops being evidence that the production artwork prints, adheres and
scans. STRUCK: "self-evidently not a device". Deleted, not restated. Replace with "the
specimen's ATECC serial is a visibly synthetic counting sequence". DISPOSAL CLAUSE REHOMED:
specimens printed on production substrate are counted and destroyed against the artwork-release
/ FAI record for the label, not the device history record. KIT-000: reserved in PKG §5's "Kit id
versus unit serial" paragraph, which owns kit ids, with the allocation range stated there as
KIT-001 upward. Not a row in the TIOV-B range table.

**What the attack changed.**

CONCEDED — seven of eight points, all verified in the files: 1. RATIONALE (conceded, with one
correction to the attacker). drivers.c:277 `strncpy(dst, "TIOV-B-0000", n - 1); /* until
provisioned */` confirmed; main.c:715/731/524 confirmed. The package already carries the right
reason in four places — provision.py:156 and check_serial():314, calibration_schema.py:432,
webtest/js/diagnostics.js:159 and EEG-Connectivity-Test.html:969 (`sn !== 'TIOV-B-0000'`).
Ratifying the block-range wording would have put §5 against all four. But the attack overstated:
"0000 falls outside all three allocation blocks" is TRUE — provision.py's PHASE_BLOCKS confirms
it. What is false is the inference. The existing §5 sentence "a specimen printed by accident, or
a proof left on a bench, cannot be mistaken for the label of a unit that exists" (PKG:876-878)
is wrong in exactly the direction that matters. The block fact is true but not load-bearing; the
firmware fact is. 2. MACHINE-GATE GAP — the most valuable finding, and I PROVED it rather than
accepting it. I built a `record_type: production` record at TIOV-B-0000, filename
`TIOV-B-0000_test.json`, real SHA-256, no DEFERRED steps, and ran `validate_test_record.py
--production`: **VALID, 0 errors**. cross_checks (:186-233) has no serial-range check; the
schema pattern `^TIOV-B-[0-9]{4}$` (line 37) admits 0000. Conceded and closed with the new gate.
Two caveats to the attacker's framing: the hazard needs a two-step mistake (specimen label on a
unit AND a record opened at 0000), and the historical 6b failure alone — real, minuted at
provision.py:637-643, "it never reached the device, so the USB iSerialNumber stayed at the
unprovisioned default" — would be caught by T5b. The validator hole is real and independent
regardless. 3. CITED CONTROL NOT IN THE STEP (conceded). PKG §4.1:708-710 says "at T18 the
operator scans the Data Matrix and compares it field by field". TST-EEG-004 T18 Equipment reads
"Torque driver, label printer, the kit packing list KPL-EEG-001" — no scanner, no verifier — and
the Procedure never mentions the symbol. The decision cited prose, not the operator's step. 4.
DISPOSAL CLAUSE UNBUILDABLE (conceded). `grep 15415` returns only PKG §4.1:710, §4.3:819 and
artwork_gen strings — no TST step, no QP Form 2/3 row, no owner, no sample size, no verifier in
any equipment list. QP Form 3 row FK-03 is a read-back-and-compare, not a graded verification.
The DHR is "One record per programme serial" — QP §9:602 (attack said §10; slip, content
confirmed) — so a specimen has no record to live in. 5. OVERPRINT GEOMETRY (conceded). Every
number reproduced exactly: col 33.85, 45.734 @ 2.572, 51.566 @ 2.9, grid 20.65 in 22.2, slack
1.55, shrunk cap 1.9037 = 7.4 pt. "Crowds the quiet zone" is impossible — every line is drawn
`max_width=col` and `Art.text` shrinks and logs to `a.shrunk`. But the attacker's own tenth-line
figure is wrong: "SPECIMEN - NOT A UNIT" at 1.2 mm cap is 19.57 mm (FONT) / 21.95 mm (FONT_B),
not 9.2 mm. Its conclusion survives — 19.57 < 33.85, and 1.2 mm cap plus a 0.35 mm gap is 1.55
mm, exactly the slack, so it fits with zero margin. 6. ATECC CLAIM (conceded, and sharper than
the attack put it). `0xEE` occurs in exactly ONE place in the entire package: drivers.c:303
`sn[8] = 0xEE;`, fabricated after reading only words 0 and 2 (SN[0..7]). Nothing tests the
terminal byte — my synthetic production record passed with `atecc_factory_serial:
"000000000000000000"`. Three conventions circulate: specimen `...EF01`, records example all-
zeros, webtest/tests/interop/drivers_sim.c:19 `0123B4B5C6D7E8F9EE`, which reads as a REAL device
under the proposed rule. Sharper still: the specimen serial STARTS `0123`, the genuine ATECC
prefix — so the entire discrimination hangs on the one byte the firmware invents. 7. KIT-000
(conceded). No kit-id allocation table exists. §5:896 gives only "`KIT-<nnn>` identifies the
circulating asset"; PKG:718 uses KIT-007 as an example; artwork_gen.py:968 uses KIT-000/KIT-123
as Code-128 self-test strings. Nothing refuses KIT-000. "Reserved on the same basis" had no
basis, because the basis is a firmware sentinel that kit ids do not have. 8. EXAMPLE-RECORD
DIVERGENCE (conceded as a note). Verified: atecc `000000000000000000`, fingerprint
`0000000000000000` against the label's. Deliberate, and the ruling should say so. KEPT AGAINST
THE ATTACK: - The outcome. Nothing found argues for a different serial; the firmware sentinel
makes the reservation more necessary, not less — the ruling now recognises a fact rather than
creating one. - All four specimen values and the payload. I re-derived the Data Matrix
independently: 60 chars, 32x32, 0.375 mm. The attack conceded this and it holds. - No overprint.
The attack's own analysis leaves the evidence argument standing, and it is sufficient on its
own. - The three rejected alternatives (TIOV-B-0001, out-of-format TIOV-B-SPEC, empty).
Unchallenged and correct. - Adding a row to §5 is safe: PHASE_BLOCKS is hardcoded in
provision.py:159 and nothing parses the table. ALSO FOUND, against the attacker: its cited
precedent does not exist. PKG §5:868 cites "**CN-PKG-01** in the ECO-EEG-016 register", and
`grep CN-PKG-01 docs/` returns only that one line — the register has no such entry. The attack's
housekeeping instruction "as CN-PKG-01 did for the format withdrawal" points at a dangling
reference. Pre-existing package defect, worth raising while ECO-EEG-016 is open anyway.

**Reasoning.**

The attack's verdict — "the outcome survives; the reasoning and three of the four operative
clauses do not" — is right, and I checked it rather than taking it. Every file-and-line citation
opened: drivers.c:277 and :296-303, main.c:524/715/731, provision.py:156/:314/:637-643,
calibration_schema.py:432, diagnostics.js:159, EEG-Connectivity-Test.html:969,
validate_test_record.py:186-233, the schema pattern at :37, TST-EEG-004 T5:558 and T18:758-772,
PKG §4.1:708-710, §4.3:819, §5:873-899, open item 18:1114, QP §9:602 and Form 2/3,
artwork_gen.py:90-95/:1040-1102/:1939, drivers_sim.c:19. Two things I did not take on trust. I
re-ran the label geometry inside artwork_gen and reproduced the attack's five numbers to three
decimals — and caught its sixth (the tenth-line width) as wrong by a factor of two, without that
changing its conclusion. And I constructed the exact record the attack described and ran the
validator on it: VALID, 0 errors. That turns its strongest claim from an assertion into a
demonstration, and it is the finding that most deserves to change the package. The decision
under review reached the right answer for a reason the package itself had already rejected.
provision.py is the tell: it refuses n == 0 in its own branch, with its own message, BEFORE it
tests the phase blocks. Whoever wrote it knew the block-range argument was not the reason. The
decision picked up the weaker of two rationales already circulating in the package — the block
wording lives in the records/artwork half (make_records.py:30, records/README.txt:28, TST-
EEG-004:1170, artwork_gen.py:91, both specimen SVGs), the firmware wording in the
firmware/webtest half — and would have promoted the weaker one into the governing document. That
is the opposite of one home per fact. The substantive change is that the corrected rationale
exposes a hazard the old wording concealed. Once §5 says out loud that an unprovisioned unit
reports 0000, it is no longer defensible that every control touching the serial is a consistency
check: T5b compares character for character, T18's Limit compares label to record, FK-03 reads
back and compares, A-13 samples two kits and compares. All four are satisfied by a self-
consistent 0000. The only allocation check in the package is check_serial(), which runs at the
provisioning station and never sees a record. So the ruling has to carry its own gate, and the
cheapest correct one is three lines in validate_test_record.py mirroring PHASE_BLOCKS. I would
rather ship a ruling with one machine gate than three prose ones. I struck the ATECC claim
rather than repairing it, because repairing it needs a fact this package does not contain.
drivers.c fabricates sn[8] = 0xEE after reading only SN[0..7]; there is no datasheet citation
anywhere and no test anywhere. If the 608B's fixed value is not 0xEE, every real label carries
an invented byte and the specimen's trailing 01 becomes the pattern of a real part rather than
its opposite — the discrimination inverts silently. Writing "self-evidently not a device" into a
governing document invites reliance on a check no step performs, on a byte no code reads.
Deleting the sentence costs the ruling nothing; the reservation does not depend on it. The
datasheet check is a separate task with a separate owner, and I have not invented its answer. On
the overprint I conceded the geometry and kept the refusal, because the attack itself only
demolished the weaker of the two reasons given. A tenth line fits — barely, consuming all 1.55
mm of slack — so refusing it is a policy choice about what a specimen is for, not a claim about
what the generator can draw. Stating it that way makes the ruling honest and makes it easy to
reverse if the programme later wants training-kit specimens. The rest is homing. A specimen has
no unit, so it cannot open a device history record; the count-and-destroy line belongs against
artwork release. ISO/IEC 15415 is named as the gate that releases the artwork (§4.3 says so
explicitly: "Nothing here has been printed, applied, wiped or read by a verifier") but has no
owner, aperture, sample size or verifier anywhere, so nothing can be counted at it yet. And
KIT-000 cannot be reserved "on the same basis" when there is no basis and no kit-id range at all
— it needs the range written down first, in the paragraph that owns kit ids. I am confident
enough to rule because the serial, its four values and the no-overprint outcome are all
derivable from files I read and code I executed. The two items I cannot settle here — the SN[8]
datasheet fact and the 15415 verification's owner — I have handed off explicitly rather than
filling in.

**Confidence:** derived  |  **Blocks a build:** no  |  **Signed off by:** Programme technical lead — closes PKG-EEG-015 §9 open item 18, owns the §5 rationale replacement, the quarantine line, and the KIT-001-upward kit-id range; minutes the ruling in RUL-EEG-021 §B beside the existing "Serial number" row. Manufacturer QA manager (QP-EEG-010 §3:232) — owns the ISO/IEC 15415 characteristic before anything can be counted at it: a QP Form 2 or Form 3 row or a numbered TST step, with verifier, aperture and sample size in an equipment list, plus whether graded-and-IPA-wiped samples are retained as evidence or destroyed. Also owns rehoming the count-and-destroy line to the artwork-release / FAI record. Programme technical lead approves the FAI (QP:229). Firmware owner — signs off the ATECC608B datasheet check on SN[8] and cites the datasheet revision at drivers.c:303, which today fabricates the byte. This is a security-boundary item: TIOV-B-0000 is the WebUSB persistent-authorisation identity shared by every unprovisioned unit (PKG §5:886-888), and the ruling makes that string printed and scannable. Signoff is required because this touches a security boundary (the authorisation identity and the quarantine rule), changes a released artwork descriptor string that must be re-cut, and adds a gate to a released validator.

**What would change it.**

A decision to extend a phase block down to 0000. This now requires more than a table edit: 0000
is the firmware sentinel, so the block would have to be moved only after drivers.c
`unit_serial_into()` is given a different unprovisioned default, and provision.py,
calibration_schema.py and both webtest copies changed with it. That ordering is the point of the
corrected rationale. The ATECC608B datasheet check. It no longer changes this ruling — the claim
is struck — but it changes drivers.c and what the printed ATECC serial means. If SN[8] is not
fixed at 0xEE, every label carries a fabricated byte and the package cannot detect it; if it is,
the rule can be reinstated as a real control with a T18 step behind it ("a printed ATECC factory
serial not ending EE is a specimen; quarantine"), and the webtest sim serial 0123B4B5C6D7E8F9EE
must change because it reads as a genuine device. A plan to use specimens outside first-article
verification — training kits, demonstrations, trade stands. That defeats the evidence argument,
which is the only ground the overprint refusal now stands on, and justifies a separate
overprinted variant. The geometry permits it: a tenth line at 1.2 mm cap, 19.57 mm wide in a
33.85 mm column, consuming all 1.55 mm of vertical slack. This is the likeliest reason the
ruling gets revisited. If the programme declines the validate_test_record.py gate, the ruling
reverts to three prose controls and the §5 quarantine line has to be strengthened to compensate
— I would then argue the reservation is not safely closable. Evidence that a phase block above
0999 has been allocated, which would need PKG-EEG-015 §5 and provision.py PHASE_BLOCKS changed
in that order (provision.py:322-324 states the order).

**Files this touches:** `docs/PKG-EEG-015_RevB_packing_labelling_and_shipping.md`, `docs/TST-EEG-004_RevC_production_test_specification.md`, `docs/QP-EEG-010_RevB_quality_plan.md`, `docs/RUL-EEG-021_RevA_rulings_register.md`, `docs/ECO-EEG-016_RevB_change_control_and_document_register.md`, `records/validate_test_record.py`, `records/README.txt`, `records/make_records.py`, `tools/artwork_gen.py`, `graphics/labels/ART-LBL-01_unit_label_specimen.svg`, `graphics/labels/ART-LBL-02_kit_id_plate_specimen.svg`, `graphics/labels/README_artwork.txt`, `firmware/main/drivers.c`


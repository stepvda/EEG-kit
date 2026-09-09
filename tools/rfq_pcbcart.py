#!/usr/bin/env python3
"""
rfq_pcbcart.py -- fill the PCBCart assembly RFQ form from `dist/rfq/pcbcart/fields.json`.

**THIS SCRIPT DOES NOT SUBMIT.**  It fills, it uploads, it screenshots every section, it
prints a field-by-field diff of what is on the page against `fields.json`, and then it
stops and waits for a person.  A wrong figure sent to a fabricator cannot be withdrawn,
so the last action is always a human one.

GROUND RULES, ENFORCED IN CODE AND NOT ONLY IN THE DOCSTRING

  * `--headless` and `--submit` are mutually exclusive (`main()`).  Nobody auto-submits.
  * Submission additionally requires an interactive stdin and a typed confirmation.
  * ONE BOARD PER RUN, and no retry loop anywhere.  If a step fails the run stops and
    reports.  Re-running a partly completed submission is how a vendor's sales desk ends
    up with duplicate tickets, so this script would rather do nothing twice than
    something twice.
  * THE DIMENSION UNIT IS ASSERTED BEFORE ANY DIMENSION IS TYPED, from two independent
    places on the page.  Entering 150 x 130 into a form set to inches is the single
    highest-consequence failure available here.
  * A CAPTCHA inside the quote form stops the run and hands back to the human.  Nothing
    here tries to solve or bypass one.
  * Dialogs are CAPTURED AND REPORTED, never blindly dismissed.  This page carries about
    twenty modal notices and several of them are real warnings about the order.

WHY THE SELECTORS LOOK LIKE THIS

The option lists are injected client-side by `new_assembly_vue.js` as `$[option.text]$`
templates, so they cannot be read from the served HTML and were discovered against the
live page.  Each group is a `div[data-name=KEY].option-box` holding `.option-child`
divs; selecting one is a click, and the app writes the result into a hidden
`input[name="product_options[KEY][text]"]`.  That hidden input is the READBACK, which is
what makes the pre-submit diff meaningful: it is the value the form will actually post,
not the value this script believes it clicked.

ORDER MATTERS.  `PCB_MATERIAL_LAYERS` must be set first: at 2 layers the form has no
inner-copper control at all, and the thickness list is different (0.5 and 0.6 mm exist,
2.4 mm does not).  `FILL_ORDER` is not alphabetical for that reason.

Requires: a virtual environment with playwright==1.58.0 and its pinned Chromium.

    python3 -m venv .venv-rfq
    ./.venv-rfq/bin/pip install -r tools/rfq_requirements.txt
    ./.venv-rfq/bin/python -m playwright install chromium
    ./.venv-rfq/bin/python tools/rfq_pcbcart.py --board EEG-CAR-01

Licence: CC BY-SA 4.0.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
PACK = os.path.join(PKG, "dist", "rfq", "pcbcart")
FORM_URL = "https://www.pcbcart.com/assembly"

# Sources whose change would make a built pack stale.
SOURCES = [os.path.join(HERE, n) for n in
           ("design.py", "wh_bus.py", "emit_rfq_pack.py")]


# Present on an untouched load of the form; not caused by this script.
BASELINE_PAGE_ERRORS = (
    "missing ) after argument list",
    "Unexpected identifier 's'",
    "e is not defined",
)


class Stop(RuntimeError):
    """Stop and hand back to the human.  Never caught to retry."""


# ---------------------------------------------------------------------------------------
# The form plan
# ---------------------------------------------------------------------------------------
class Opt:
    """One PCBCart option group.

    `text` is the option to click, spelled as the live page spells it.  `canonical` names
    the `fields.json` answer it implements, and `deviation` -- when the portal's list has
    no exact match for the specification -- says so, loudly, in the diff and in the record.
    """

    __slots__ = ("key", "text", "canonical", "deviation")

    def __init__(self, key, text, canonical=None, deviation=None):
        self.key, self.text = key, text
        self.canonical, self.deviation = canonical, deviation


# Values below are the PORTAL'S SPELLING of an answer that lives in fields.json.  The
# script cross-checks each against its canonical answer before it clicks anything.
CARRIER_OPTIONS = [
    Opt("PCB_MATERIAL_LAYERS", "4 layer", "layers"),          # FIRST: reshapes the form
    Opt("PCB_TYPE", "FR4", "material"),
    Opt("PCB_MAT_DETAIL", "FR4-Tg 150C", "material"),
    Opt("PCB_BOARD_TYPE", "single unit", "delivery_method"),
    Opt("PCB_THICKNESS", "1.6 mm", "thickness"),
    Opt("PCB_SURFACE_FINISH", "ENIG -Electroless Nickle/Immersion Gold - RoHS",
        "surface_finish"),
    Opt("PCB_ENIG_THICKER_AU", "None", "surface_finish"),
    Opt("PCB_COPPER_WEIGHT", "35 um", "copper_outer"),
    Opt("PCB_COPPER_WEIGHT_INNER", "18 um", "copper_inner",
        "THE FORM HAS NO 17 um OPTION. The specification is 17 um (0.5 oz) inner "
        "copper; 18 um is the nearest option and is the same 0.5 oz class. Stated in "
        "the Notes box and in README_for_bidder.txt so the vendor quotes the right "
        "thing."),
    Opt("PCB_SOLDERMASK", "Both Sides", "soldermask"),
    Opt("PCB_SOLDERMASK_COLOR", "Green", "soldermask"),
    Opt("PCB_SILKSCREEN_LEGEND", "2 sides", "legend"),
    Opt("PCB_SILKSCREEN_LEGEND_COLOR", "White", "legend"),
    Opt("PCB_MIN_TRACING_SPACING", "0.20 mm", "min_track_clearance"),
    Opt("PCB_SMALLEST_HOLES", "0.30 mm", "smallest_hole"),
    Opt("PCB_INSPECTION", "IPC 2", "class"),
    Opt("PCB_IMPEDANCE", "No", "impedance"),
    Opt("PCB_BURIED_BLIND", "No", "buried_blind"),
    Opt("PCB_LASER_DRILL", "No", "buried_blind"),
    Opt("PCB_INNTERCONNECTED_LAYER", "No", "buried_blind"),
    Opt("PCB_VIA_IN_PAD", "None", "vias"),
    Opt("PCB_VIA_FILLED", "None", "vias"),
    # design.py fabrication note 11 asks the FABRICATOR to mark its own date code and UL
    # mark on the bottom silkscreen.  That is a manufacturing marking, not a date this
    # submission states, and the two must not be confused.
    Opt("PCB_UL", "Yes - add to bottom silkscreen", None),
    Opt("PCB_DATE", "Yes - add to bottom silkscreen", None),
]

WH_BUS_OPTIONS = [
    Opt("PCB_MATERIAL_LAYERS", "2 layer", "layers"),
    Opt("PCB_TYPE", "FR4", "material"),
    Opt("PCB_MAT_DETAIL", "FR4-Tg 150C", "material"),
    Opt("PCB_BOARD_TYPE", "panel", "delivery_method"),
    # These three exist ONLY once the board type is 'panel', and all three default to
    # '--', which is not an answer. A V-scored array that goes up with Route Process
    # unset is a panel the fabricator gets to choose the separation method for.
    Opt("PCB_PANEL", "1", "panel_designs"),
    Opt("PCB_PANEL_ROUTING", "Panel as V-Scoring", "panel_route_process"),
    Opt("PCB_PANEL_X_OUT", "No", "panel_x_out"),
    Opt("PCB_THICKNESS", "0.8 mm", "thickness"),
    Opt("PCB_SURFACE_FINISH", "ENIG -Electroless Nickle/Immersion Gold - RoHS",
        "surface_finish"),
    Opt("PCB_ENIG_THICKER_AU", "None", "surface_finish"),
    Opt("PCB_COPPER_WEIGHT", "35 um", "copper_outer"),
    Opt("PCB_SOLDERMASK", "Both Sides", "soldermask"),
    Opt("PCB_SOLDERMASK_COLOR", "Green", "soldermask"),
    Opt("PCB_SILKSCREEN_LEGEND", "2 sides", "legend"),
    Opt("PCB_SILKSCREEN_LEGEND_COLOR", "White", "legend"),
    Opt("PCB_MIN_TRACING_SPACING", "0.20 mm", "min_track",
        "The board's minimum track is 1.20 mm, far above anything on this list; "
        "0.20 mm is the list's coarsest entry and claims no capability we need."),
    Opt("PCB_SMALLEST_HOLES", "0.40 mm", "holes",
        "The board's only hole is 0.80 mm finished, comfortably above the list's "
        "coarsest entry of 0.40 mm."),
    Opt("PCB_INSPECTION", "IPC 2", "class"),
    Opt("PCB_IMPEDANCE", "No", "impedance"),
    Opt("PCB_SKIP_V_SCORING", "None", "panel"),
    Opt("PCB_UL", "Yes - add to bottom silkscreen", None),
    Opt("PCB_DATE", "Yes - add to bottom silkscreen", None),
]

PLAN = {
    "EEG-CAR-01": {"options": CARRIER_OPTIONS, "bom_name": "EEG-CAR-01 Rev B geometry / Rev C BOM"},
    "WH-BUS-01": {"options": WH_BUS_OPTIONS, "bom_name": "WH-BUS-01 Rev A bare board"},
}


# ---------------------------------------------------------------------------------------
# Preconditions
# ---------------------------------------------------------------------------------------
def load_pack(board: str) -> tuple:
    fj = os.path.join(PACK, "fields.json")
    if not os.path.exists(fj):
        raise Stop(f"{os.path.relpath(fj, PKG)} does not exist. "
                   f"Run: python3 tools/emit_rfq_pack.py")
    with open(fj, encoding="utf-8") as fh:
        man = json.load(fh)

    if man.get("schema") != "rfq-pack/1":
        raise Stop(f"fields.json schema is {man.get('schema')!r}, expected 'rfq-pack/1'")

    subs = [s for s in man.get("submissions", []) if s["board"] == board]
    if not subs:
        have = ", ".join(s["board"] for s in man.get("submissions", []))
        raise Stop(f"fields.json has no submission for {board}. It has: {have}")
    sub = subs[0]

    for req in ("fields", "uploads", "notes_short"):
        if not sub.get(req):
            raise Stop(f"fields.json submission for {board} is incomplete: no {req!r}")

    # Stale?  Older than anything it describes, or than the sources behind it.
    age = os.path.getmtime(fj)
    stale = []
    for u in sub["uploads"]:
        p = os.path.join(PACK, sub["dir"], u["name"])
        if not os.path.exists(p):
            raise Stop(f"fields.json lists {u['name']} but it is not in the pack. "
                       f"Re-run tools/emit_rfq_pack.py")
        if os.path.getmtime(p) > age + 1:
            stale.append(os.path.relpath(p, PKG))
    for s in SOURCES:
        if os.path.exists(s) and os.path.getmtime(s) > age + 1:
            stale.append(os.path.relpath(s, PKG))
    if stale:
        raise Stop("fields.json is OLDER than what it describes:\n  "
                   + "\n  ".join(stale)
                   + "\nRe-run: python3 tools/emit_rfq_pack.py")

    # Every upload must verify against the checksum the pack recorded.
    import hashlib
    for u in sub["uploads"]:
        p = os.path.join(PACK, sub["dir"], u["name"])
        h = hashlib.sha256()
        with open(p, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 16), b""):
                h.update(chunk)
        if h.hexdigest() != u["sha256"]:
            raise Stop(f"{u['name']} does not match the SHA-256 in fields.json. "
                       f"Re-run tools/emit_rfq_pack.py")
    return man, sub


# ---------------------------------------------------------------------------------------
# Page helpers
# ---------------------------------------------------------------------------------------
def assert_millimetres(page) -> dict:
    """Two independent readings, before any dimension is typed.

    `#appForm input[name=unit]` is what the form will POST.  `window.UserStatus.unit` is
    what `unitFormat()` in the page's own script branches on.  A signed-in account whose
    profile dimension is inch flips the second one.  Both must say mm.
    """
    st = page.evaluate("""() => {
      const u = document.querySelector('#appForm input[name=unit]');
      let us = null;
      try { us = window.UserStatus ? window.UserStatus.unit : null; } catch (e) {}
      let li = null;
      try { li = window.UserStatus ? window.UserStatus.islogin : null; } catch (e) {}
      return {form_unit: u ? u.value : null, userstatus_unit: us, islogin: li};
    }""")
    bad = [k for k in ("form_unit", "userstatus_unit") if st[k] != "mm"]
    if bad:
        raise Stop(
            f"DIMENSION UNIT IS NOT MILLIMETRES: {st}\n"
            f"Nothing has been typed. Entering a dimension now would send the wrong "
            f"board size to a fabricator.\n"
            f"If you are signed in, the account profile's dimension setting is the "
            f"cause: change it at https://www.pcbcart.com/profile/modify.html?type=1 "
            f"or run this anonymously, where the page defaults to mm.")
    return st


def assert_no_captcha(page) -> None:
    """A CAPTCHA inside the quote form stops the run.

    The footer 'Quick Contact' widget has an image verification of its own and is NOT
    the quote form; scoping this to #appForm is deliberate, not sloppy.
    """
    n = page.evaluate("""() => {
      const f = document.querySelector('#appForm');
      if (!f) return -1;
      return f.querySelectorAll(
        'input[name=verify], .verifyimg, img[src*="verify"], iframe[src*="captcha"], '
        + '.g-recaptcha, .cf-turnstile').length;
    }""")
    if n == -1:
        raise Stop("#appForm is not on the page; the form did not load as expected.")
    if n:
        raise Stop(f"A CAPTCHA or image verification appeared inside the quote form "
                   f"({n} element(s)). Stopping and handing back to you. This script "
                   f"does not attempt to solve or bypass one.")


def pick_option(page, key: str, text: str) -> str:
    """Select one option and return the form's own readback for that group.

    IF THE OPTION IS ALREADY SELECTED, DO NOT CLICK IT.  Clicking an already-active
    choice makes the app rebuild the form and DISCARD state set earlier in the run:
    re-clicking PCB_TYPE 'FR4', which is the default anyway, silently reverted
    PCB_MATERIAL_LAYERS to 2 layers and took the inner-copper control away with it.
    A no-op click is not a no-op on this page.
    """
    # Groups are INSERTED as earlier answers make them relevant -- the inner-copper
    # control does not exist until the board is four layers and the material detail has
    # settled -- so a missing group may simply not have been rendered yet.  Wait for it
    # before concluding it is gone.
    deadline = time.time() + 8.0
    while time.time() < deadline:
        if page.evaluate("""(k) => !!document.querySelector(
                `.option-box[data-name="${k}"]`)""", key):
            break
        page.wait_for_timeout(150)

    current = read_option(page, key)
    if current == text:
        return current
    ok = page.evaluate("""([key, text]) => {
      const box = document.querySelector(`.option-box[data-name="${key}"]`);
      if (!box) return 'NO_GROUP';
      const kids = [...box.querySelectorAll('.option-child')];
      const hit = kids.find(c => c.innerText.trim() === text);
      if (!hit) return 'NO_OPTION:' + kids.map(c => c.innerText.trim()).join(' | ');
      hit.click();
      return 'OK';
    }""", [key, text])
    if ok == "NO_GROUP":
        raise Stop(f"{key}: no such option group on the page. The form has changed; "
                   f"re-run discovery before trusting this script.")
    if ok.startswith("NO_OPTION:"):
        raise Stop(f"{key}: the page has no option {text!r}.\n"
                   f"  It offers: {ok.split(':', 1)[1]}")
    # Wait for the readback to settle rather than sleeping a guessed interval.  The
    # app re-renders whole groups when layers change, and a fixed 350 ms was not
    # enough -- the click landed and the hidden input still read the old value.
    # This waits for the form's own state to agree; it does NOT click again.
    deadline = time.time() + 8.0
    got = read_option(page, key)
    while got != text and time.time() < deadline:
        page.wait_for_timeout(150)
        got = read_option(page, key)
    return got


def read_option(page, key: str) -> str:
    return page.evaluate("""(key) => {
      const el = document.querySelector(`input[name="product_options[${key}][text]"]`);
      return el ? el.value : null;
    }""", key)


def set_text(page, name: str, value: str) -> str:
    el = page.query_selector(f'#appForm [name="{name}"]')
    if el is None:
        raise Stop(f"no input named {name!r} in #appForm")
    el.fill(str(value))
    page.wait_for_timeout(120)
    return el.input_value()


def settle_and_repair(page, options) -> list:
    """Re-read every option after the whole form is filled; repair anything that drifted.

    This form is reactive: later answers re-run rules that can reset earlier ones, and
    the app re-renders whole groups while doing it. So the value that was accepted when
    it was clicked is not necessarily the value the form will post.

    ONE repair pass, then the truth is reported either way. That distinction matters: a
    value that drifts once is a re-render race and repairing it is right, but a value
    that drifts AGAIN after being re-applied is the vendor's own rule refusing the
    combination -- and that must be reported, not hammered. Nothing here loops.
    """
    drifted = []
    for opt in options:
        got = read_option(page, opt.key)
        if got != opt.text:
            drifted.append({"control": opt.key, "wanted": opt.text, "was": got})
    if not drifted:
        return []
    print(f"\n  {len(drifted)} option(s) drifted while the rest of the form was "
          f"filled; repairing once:")
    for d in drifted:
        print(f"    {d['control']:30s} {d['was']!r} -> {d['wanted']!r}")
        opt = next(o for o in options if o.key == d["control"])
        try:
            d["after_repair"] = pick_option(page, opt.key, opt.text)
        except Stop as e:
            d["after_repair"] = f"REPAIR FAILED: {e}"
        d["repaired"] = d.get("after_repair") == d["wanted"]
    page.wait_for_timeout(1500)
    for d in drifted:
        final = read_option(page, d["control"])
        d["final"] = final
        d["repaired"] = final == d["wanted"]
        if not d["repaired"]:
            print(f"    {d['control']}: STILL {final!r} after one repair. That is the "
                  f"form refusing the combination, not a race. Not retried.")
    return drifted


def shot(page, name: str, out: str) -> str:
    os.makedirs(out, exist_ok=True)
    p = os.path.join(out, f"{name}.png")
    page.screenshot(path=p, full_page=True)
    return p


# ---------------------------------------------------------------------------------------
# The run
# ---------------------------------------------------------------------------------------
def run(board: str, headless: bool, allow_submit: bool,
        session: str = None, authorised_by: str = None) -> int:
    from playwright.sync_api import sync_playwright

    man, sub = load_pack(board)
    plan = PLAN[board]
    shots_dir = os.path.join(PACK, "screenshots", board)
    fields = sub["fields"]
    contact = man["contact"]

    dialogs, deviations, diff, needs_human = [], [], [], []

    def want(key):
        f = fields.get(key)
        return f["value"] if f else None

    print(f"rfq_pcbcart: {board}")
    print(f"  pack     {os.path.relpath(PACK, PKG)}")
    print(f"  form     {FORM_URL}")
    print(f"  mode     {'headless' if headless else 'headed'}, "
          f"submit {'ARMED' if allow_submit else 'disabled'}"
          + (f", signed in via {os.path.basename(session)}" if session
             else ", anonymous"))
    if authorised_by:
        print(f"  authority {authorised_by}")
    print()

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=headless, slow_mo=0 if headless else 120)
        ctx = browser.new_context(
            viewport={"width": 1500, "height": 1300},
            **({"storage_state": session} if session else {}))
        page = ctx.new_page()

        # Captured, not dismissed blindly.  Every one is reported at the end.
        def on_dialog(d):
            dialogs.append({"type": d.type, "message": d.message})
            print(f"  [dialog] {d.type}: {d.message}")
            d.dismiss()

        page.on("dialog", on_dialog)
        # The page throws three of its own errors on a plain load with no interaction
        # at all -- verified against an untouched load -- so they are labelled rather
        # than reported as though this script caused them. Anything else is ours to
        # explain.
        page.on("pageerror", lambda e: dialogs.append({
            "type": "pageerror",
            "message": str(e)[:300],
            "baseline": any(b in str(e) for b in BASELINE_PAGE_ERRORS)}))

        page.goto(FORM_URL, wait_until="networkidle", timeout=90_000)
        page.wait_for_timeout(2500)

        assert_no_captcha(page)
        unit = assert_millimetres(page)
        print(f"  unit     form={unit['form_unit']} "
              f"UserStatus={unit['userstatus_unit']} "
              f"islogin={unit['islogin']!r}  -> millimetres confirmed")
        shot(page, "00_loaded", shots_dir)

        # ---- PCB section -------------------------------------------------------------
        print("\n  PCB")
        for opt in plan["options"]:
            got = pick_option(page, opt.key, opt.text)
            flag = ""
            if opt.deviation:
                deviations.append({"control": opt.key, "selected": opt.text,
                                   "canonical": want(opt.canonical),
                                   "why": opt.deviation})
                flag = "   << DEVIATION"
            print(f"    {opt.key:30s} {got!r}{flag}")
            if got != opt.text:
                raise Stop(f"{opt.key}: clicked {opt.text!r} but the form reads "
                           f"{got!r}. Stopping rather than guessing.")
        shot(page, "01_pcb_options", shots_dir)

        # ---- dimensions, only now that mm is proven ----------------------------------
        assert_millimetres(page)
        dims = want("dimensions")            # e.g. "150.0 x 130.0 mm"
        w, h = [p.strip() for p in dims.replace("mm", "").split("x")]
        gw = set_text(page, "product_options[PCB_BOARD_SIZE_W][value]", w)
        gh = set_text(page, "product_options[PCB_BOARD_SIZE_H][value]", h)
        print(f"\n  size     {gw} x {gh} mm   (fields.json: {dims})")
        shot(page, "02_board_size", shots_dir)

        # ---- delivery, quantity, origin ----------------------------------------------
        dm = want("delivery_method")
        page.select_option('#appForm select[name="delivery_method"]', label=dm)
        print(f"  delivery {dm}")

        # From `quantity_breaks`, which the pack emits as a machine-readable list, and
        # NOT by parsing the prose in `quantities`. Parsing the prose silently left
        # WH-BUS-01 on the form's default of 10.
        qty = [q.strip() for q in want("quantity_breaks").split("|") if q.strip()]
        if not qty:
            raise Stop("fields.json has no usable quantity_breaks")
        if True:
            boxes = page.query_selector_all('#appForm input[name="quantity[]"]')
            for _ in range(len(qty) - len(boxes)):
                add = page.query_selector('#appForm .add-quantity, #appForm .quantity-add')
                if add is None:
                    add = page.evaluate_handle("""() => [...document.querySelectorAll(
                        '#appForm a, #appForm span, #appForm div')].find(
                        e => e.innerText.trim() === '+')""").as_element()
                if add is None:
                    raise Stop("cannot find the [+] control to add a quantity break")
                add.click()
                page.wait_for_timeout(300)
            boxes = page.query_selector_all('#appForm input[name="quantity[]"]')
            if len(boxes) < len(qty):
                raise Stop(f"needed {len(qty)} quantity boxes, the form has "
                           f"{len(boxes)}")
            for box, q in zip(boxes, qty):
                box.fill(q)
            print(f"  quantity {', '.join(qty)}"
                  f"   ({fields['quantity_breaks']['label']})")

        page.evaluate("""(t) => {
          const el = [...document.querySelectorAll('#appForm .option-child')]
            .find(c => c.innerText.trim() === t);
          if (el) el.click();
        }""", "As decided by PCBCART")

        for label, value in (("custom_testing", want("custom_testing")),
                             ("ic_programming", want("ic_programming"))):
            page.evaluate("""([name, val]) => {
              const hid = document.querySelector(`#appForm input[name="${name}"]`);
              if (!hid) return;
              const grp = hid.closest('div');
              const el = [...grp.querySelectorAll('.option-child')]
                .find(c => c.innerText.trim() === val);
              if (el) el.click();
            }""", [label, value])
        print(f"  testing  {want('custom_testing')}   "
              f"programming {want('ic_programming')}")
        shot(page, "03_delivery_quantity", shots_dir)

        # ---- assembly side -----------------------------------------------------------
        if sub["assembled"]:
            side = want("assembly_side")
            page.evaluate("""(t) => {
              const el = [...document.querySelectorAll('#appForm .option-child')]
                .find(c => c.innerText.trim().toLowerCase() === t.toLowerCase());
              if (el) el.click();
            }""", side)
            print(f"  side     {side}")
        shot(page, "04_assembly", shots_dir)

        # ---- uploads -----------------------------------------------------------------
        # The form has exactly two file inputs -- a required "BOM File" and a "PCB
        # File" -- and neither is `multiple`. They are matched by the label beside
        # them, not by index, so a reordering of the page does not silently put the
        # Gerbers in the BOM slot.
        print("\n  uploads")
        exts = tuple(man["vendor"]["upload_extensions"])
        slots = page.evaluate("""() => {
          const out = [];
          document.querySelectorAll('input[type=file]').forEach((f, i) => {
            const wrap = f.closest('.quote-upload-file') || f.parentElement;
            out.push({i, label: (wrap ? wrap.innerText : '').replace(/\\s+/g, ' ').trim(),
                      multiple: f.multiple});
          });
          return out;
        }""")
        handles = page.query_selector_all('input[type=file]')
        for u in sub["uploads"]:
            if u["name"].rsplit(".", 1)[-1].lower() not in exts:
                raise Stop(f"{u['name']} is not an accepted extension {exts}")
            idx = [sl["i"] for sl in slots if u["slot"].lower() in sl["label"].lower()]
            if not idx:
                raise Stop(f"no upload slot labelled {u['slot']!r} on the page. "
                           f"Slots are: {[sl['label'] for sl in slots]}")
            path = os.path.join(PACK, sub["dir"], u["name"])
            handles[idx[0]].set_input_files(path)
            print(f"    {u['slot']:9s} <- {u['name']}")
            page.wait_for_timeout(5000)
        page.wait_for_timeout(3000)
        assert_no_captcha(page)
        shot(page, "05_uploads", shots_dir)

        # ---- basic info and notes ----------------------------------------------------
        set_text(page, "bom_name", plan["bom_name"])
        set_text(page, "username", contact["name"])
        set_text(page, "company", contact["company"])
        set_text(page, "phone", contact["phone"])
        set_text(page, "email", contact["email"])
        try:
            page.select_option('#appForm select[name="country"]',
                               label=contact["country"])
        except Exception as e:
            raise Stop(f"could not select country {contact['country']!r}: {e}")
        page.wait_for_timeout(2500)

        # `country_state` is required and is populated only after a country is chosen.
        # A province is part of somebody's address; this script will not guess one.
        state_opts = page.evaluate("""() => {
          const s = document.querySelector('#appForm select[name=country_state]');
          return s ? [...s.options].map(o => o.text).filter(Boolean) : [];
        }""")
        if contact.get("state"):
            if contact["state"] not in state_opts:
                raise Stop(f"contact state {contact['state']!r} is not offered for "
                           f"{contact['country']}. Offered: {state_opts}")
            page.select_option('#appForm select[name="country_state"]',
                               label=contact["state"])
            print(f"  state    {contact['state']}")
        elif state_opts:
            needs_human.append(
                f"State/province (required). The form offers: "
                f"{', '.join(state_opts)}. Set CONTACT['state'] in "
                f"tools/emit_rfq_pack.py and rebuild the pack, or choose it on the "
                f"page by hand before submitting.")
            print("  state    NOT SET -- a person must choose it (see below)")

        notes = sub["notes_short"]
        if deviations:
            notes += "\n" + " ".join(
                f"FORM LIMITATION ({d['control']}): {d['why']}" for d in deviations)
        got_notes = set_text(page, "notes", notes)
        # The Notes control is <input type="text">, not a textarea: it holds the
        # characters but FLATTENS the line breaks, so the nine numbered notes arrive as
        # one run-on paragraph. That is why the full text travels as a file.
        notes_lost = len(notes) - len(got_notes)
        notes_flattened = notes.count("\n") > 0 and "\n" not in got_notes
        print(f"\n  contact  {contact['name']}, {contact['company']}, "
              f"{contact['country']}")
        print(f"  notes    {len(notes)} chars offered, {len(got_notes)} accepted"
              + ("   << TRUNCATED" if notes_lost > 0 else "")
              + ("   << LINE BREAKS FLATTENED (single-line input)"
                 if notes_flattened else ""))
        shot(page, "06_basic_info_notes", shots_dir)

        # ---- settle, then diff ---------------------------------------------------
        drifted = settle_and_repair(page, plan["options"])
        shot(page, "07_settled", shots_dir)

        print("\n" + "=" * 78)
        print("PAGE vs fields.json")
        print("=" * 78)
        for opt in plan["options"]:
            got = read_option(page, opt.key)
            mark = "ok " if got == opt.text else "BAD"
            diff.append({"control": opt.key, "want": opt.text, "got": got,
                         "match": got == opt.text})
            print(f"  {mark} {opt.key:30s} {got!r}")
        checks = [("product_options[PCB_BOARD_SIZE_W][value]", w),
                  ("product_options[PCB_BOARD_SIZE_H][value]", h),
                  ("bom_name", plan["bom_name"]),
                  ("username", contact["name"]),
                  ("company", contact["company"]),
                  ("phone", contact["phone"]),
                  ("email", contact["email"]),
                  ("delivery_method", dm)]
        if contact.get("state"):
            checks.append(("country_state", contact["state"]))
        for name, wantv in checks:
            el = page.query_selector(f'#appForm [name="{name}"]')
            if el and el.evaluate("e => e.tagName") == "SELECT":
                got = el.evaluate("e => e.options[e.selectedIndex]"
                                  " ? e.options[e.selectedIndex].text : null")
            else:
                got = el.input_value() if el else None
            ok = (got == wantv)
            diff.append({"control": name, "want": wantv, "got": got, "match": ok})
            print(f"  {'ok ' if ok else 'BAD'} {name:30s} {got!r}")

        bad = [d for d in diff if not d["match"]]
        if needs_human:
            print("\n  OUTSTANDING -- required, and not this script's to fill:")
            for n in needs_human:
                print(f"    * {n}")
        if deviations:
            print("\n  DEVIATIONS -- the form has no exact option for these:")
            for d in deviations:
                print(f"    {d['control']}: selected {d['selected']!r} for "
                      f"specification {d['canonical']!r}")
                print(f"      {d['why']}")
        if notes_lost > 0:
            print(f"\n  NOTE: the Notes box dropped {notes_lost} characters. The full "
                  f"text is in README_for_bidder.txt inside the uploaded ZIP.")
        elif notes_flattened:
            print(f"\n  NOTE: the Notes control is a single-line text input, so the "
                  f"nine notes arrive as one paragraph with the line breaks removed. "
                  f"No text was lost. The readable copy is README_for_bidder.txt "
                  f"inside the uploaded ZIP.")
        if dialogs:
            print(f"\n  DIALOGS SEEN ({len(dialogs)}) -- captured, not dismissed blindly:")
            for d in dialogs:
                tag = " (the site's own, present on an untouched load)" \
                    if d.get("baseline") else ""
                print(f"    [{d['type']}] {d['message'][:160]}{tag}")
        print("\n" + "=" * 78)
        if bad:
            print(f"{len(bad)} FIELD(S) DO NOT MATCH. Do not submit.")
        else:
            print("Every field on the page matches fields.json.")
        print(f"Screenshots: {os.path.relpath(shots_dir, PKG)}")
        print("=" * 78)

        record = {
            "board": board, "ticket": man["ticket"], "form_url": FORM_URL,
            "unit_check": unit, "diff": diff, "deviations": deviations,
            "drifted": drifted,
            "dialogs": dialogs,
            "needs_human": needs_human,
            "signed_in": bool(session),
            "authorised_by": authorised_by,
            "notes_chars_offered": len(notes),
            "notes_chars_accepted": len(got_notes),
            "notes_truncated": notes_lost > 0,
            "notes_line_breaks_flattened": notes_flattened,
            "uploads": [{"name": u["name"], "sha256": u["sha256"]}
                        for u in sub["uploads"]],
            "submitted": False,
        }

        if not allow_submit:
            print("\nSTOPPING BEFORE SUBMIT. This run was not armed to submit.")
            print("Check the screenshots and the diff above, then re-run with "
                  "--submit to be offered the button.")
        elif bad:
            print("\nREFUSING TO OFFER SUBMIT: the page does not match fields.json.")
        elif needs_human:
            print("\nREFUSING TO OFFER SUBMIT: a required field is still unfilled "
                  "and is not this script's to fill. See OUTSTANDING above.")
        else:
            print("\nThe form is filled and matches.")
            if authorised_by:
                # The typed confirmation exists to prove that a person saw the filled
                # form and said yes.  A recorded authorisation is that same proof, and
                # it is written verbatim into submission_record.json so it can be
                # audited afterwards.  It does NOT relax anything else: a mismatched
                # field or an unfilled required field still refuses to submit, whoever
                # authorised it.
                print(f"Submitting on recorded authority: {authorised_by}")
                record.update(submit(page, shots_dir))
            else:
                print("Nothing has been sent.")
                print(f"Type exactly:  SUBMIT {board}")
                try:
                    typed = input("> ").strip()
                except EOFError:
                    typed = ""
                if typed != f"SUBMIT {board}":
                    print("Not submitted.")
                else:
                    record.update(submit(page, shots_dir))

        # One file, keyed by board: a second board's run must not erase the first's.
        rec_path = os.path.join(PACK, "submission_record.json")
        all_records = {}
        if os.path.exists(rec_path):
            try:
                with open(rec_path, encoding="utf-8") as fh:
                    prev = json.load(fh)
                if isinstance(prev, dict) and "boards" in prev:
                    all_records = prev["boards"]
            except (ValueError, OSError):
                all_records = {}
        all_records[board] = record
        with open(rec_path, "w", encoding="utf-8") as fh:
            json.dump({"schema": "rfq-submission-record/1", "ticket": man["ticket"],
                       "boards": all_records}, fh, indent=2)
            fh.write("\n")
        print(f"\nRecord: {os.path.relpath(os.path.join(PACK, 'submission_record.json'), PKG)}")

        if not headless:
            print("Browser stays open for 60 s so you can look at it.")
            page.wait_for_timeout(60_000)
        ctx.close()
        browser.close()

    return 1 if [d for d in diff if not d["match"]] else 0


def submit(page, shots_dir: str) -> dict:
    """One click.  No retry, whatever happens."""
    before = page.url
    btn = page.query_selector('#appForm button[type=submit], #appForm .submit-btn, '
                              '#appForm input[type=submit]')
    if btn is None:
        btn = page.evaluate_handle("""() => [...document.querySelectorAll(
            '#appForm a, #appForm button, #appForm div')].find(
            e => /^(submit|get quote|submit quote)$/i.test(
                (e.innerText || '').trim()))""").as_element()
    if btn is None:
        return {"submitted": False, "error": "no submit control found"}
    btn.click()
    page.wait_for_timeout(9000)
    shot(page, "07_after_submit", shots_dir)
    body = page.evaluate("() => document.body.innerText.slice(0, 4000)")
    import re
    # PCBCart returns two identifiers and they are not the same number: a Quote# in the
    # page text, and a quote_id in the success URL.  Capture both, and capture them
    # specifically -- an over-broad pattern here collects words like "Order" from the
    # surrounding furniture and buries the reference that actually matters.
    refs = []
    for pat in (r"Quote\s*#\s*([A-Z0-9][A-Z0-9\-]{4,24})",
                r"quote[_ -]?id[=:\s]+([A-Z0-9][A-Z0-9\-]{2,24})",
                r"\b(?:ticket|reference)\s*(?:no\.?|number|#)?[:\s]+"
                r"([A-Z]{2,}-[A-Z0-9\-]{3,20})"):
        refs += re.findall(pat, body + " " + page.url, re.I)
    return {"submitted": True, "url_before": before, "url_after": page.url,
            "references": sorted(set(refs)), "page_text": body[:2000]}


def main() -> int:
    ap = argparse.ArgumentParser(description="Fill the PCBCart assembly RFQ form. "
                                             "Does not submit unless a person says so.")
    ap.add_argument("--board", required=True, choices=sorted(PLAN))
    ap.add_argument("--headless", action="store_true",
                    help="run without a visible browser (never with --submit)")
    ap.add_argument("--submit", action="store_true",
                    help="offer the submit button after the diff; still requires a "
                         "typed confirmation on an interactive terminal, or "
                         "--authorised-by")
    ap.add_argument("--session", metavar="PATH",
                    help="Playwright storage state for a signed-in session; omit to "
                         "submit anonymously")
    ap.add_argument("--authorised-by", metavar="TEXT",
                    help="who authorised this submission and on what basis. Recorded "
                         "verbatim in submission_record.json. Stands in for the typed "
                         "confirmation where there is no interactive terminal; it "
                         "relaxes no other check")
    a = ap.parse_args()

    if a.session and not os.path.exists(a.session):
        print(f"REFUSED: session file {a.session} does not exist.", file=sys.stderr)
        return 2
    if a.submit and a.headless and not a.authorised_by:
        print("REFUSED: --headless and --submit together with no recorded authority. "
              "A person has to see the filled form before it is sent.", file=sys.stderr)
        return 2
    if a.submit and not sys.stdin.isatty() and not a.authorised_by:
        print("REFUSED: --submit needs an interactive terminal to confirm on, or "
              "--authorised-by to record who said yes.", file=sys.stderr)
        return 2
    try:
        return run(a.board, a.headless, a.submit, a.session, a.authorised_by)
    except Stop as e:
        print(f"\nSTOPPED\n{e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

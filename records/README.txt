records/ -- the machine-readable per-unit test record
=====================================================================

Owned by:   TST-EEG-004 Rev C section 12 (the record) and section 13 (the certificate)
Generated:  records/make_records.py
Licence:    CC BY-SA 4.0

TST-EEG-004 section 12 specifies one JSON file per unit, `<unit_serial>_test.json`, and says
the field counts are "fixed so a record can be validated mechanically". Until this directory
existed there was nothing to validate against, so nothing caught a missing mandatory field,
and two manufacturers reading the same prose would have emitted different key names and
different nesting for the same 70 T23 currents, 32 T10 impedances and 24 T7a gains. Neither
file could have been ingested without hand-mapping, which is the comparability failure the
document's own opening calls fatal for the study.

FILES
---------------------------------------------------------------------
  TST-EEG-004_RevC_unit_test_record.schema.json
      JSON Schema 2020-12. Every field count section 12 states is a minItems == maxItems
      pair, so a short array is a schema error and not a silent gap. `unit`, `limit` and
      `uncertainty` are `const` strings taken verbatim from each step's table in section 8,
      so a record cannot claim a limit the specification does not set.

  EXAMPLE_TIOV-B-0000_test.json
      A worked record that validates and CONTAINS NO MEASUREMENTS. Every number is the
      sentinel -9999 or 9999, every hash is sixty-four zeros, every free-text field begins
      EXAMPLE-, every step verdict is DEFERRED with a reason, `record_type` is `example`,
      and the serial TIOV-B-0000 is in none of the blocks PKG-EEG-015 section 5 allocates.
      It is a shape, not a result.

  lot_summary_template.csv
      The header row of the per-lot summary CSV that section 12 puts in the per-lot ZIP.
      The step columns are generated from the section 2 step list, so a new step appears
      here on the next run.

  TST-EEG-004_RevC_calibration_certificate.md
      The section 13 certificate template. Every placeholder is a JSON pointer into the
      record, so the certificate and the record cannot disagree.

  validate_test_record.py
      Validates a record against the schema, then applies the checks a schema cannot
      express: that a DEFERRED or NOT_APPLICABLE step carries a reason, that the T5b
      iSerial and the T6 fingerprint match the identity block, that the seven T30 frame
      integrity counters are zero when T30 passes, and that signatures.record_sha256 is
      the hash of the record. Run it with --production to reject an example record.

  make_records.py
      Writes all of the above from one specification table. It reads the step list out of
      TST-EEG-004 section 2 and REFUSES TO RUN if the document and the table disagree.
      That check is not decoration: T30 was added to the document after the record template
      was drafted, and this is the mechanism that would have caught it.

HOW TO USE
---------------------------------------------------------------------
  python3 records/validate_test_record.py records/EXAMPLE_TIOV-B-0000_test.json
  python3 records/validate_test_record.py --production TIOV-B-0001_test.json
  python3 records/make_records.py            regenerate everything

WHAT IS NOT SETTLED
---------------------------------------------------------------------
  * The record's SHA-256 is defined here, because section 12 requires the hash on the
    certificate without saying what it is taken over. It is the record serialised as UTF-8
    JSON with sorted keys, a two-space indent and a trailing newline, with
    signatures.record_sha256 itself set to sixty-four zeros. That definition is this
    directory's PROPOSAL. It is arbitrary in the way any canonicalisation is arbitrary, and
    it needs the programme's ruling before a manufacturer signs against it.
  * The eleven steps that need a host stream decoder (T7, T8, T9, T10, T12, T13, T14, T15,
    T16, T26, T27) cannot be filled today: TST-EEG-004 section 16 item 10 records that the
    decoding tool does not exist. Their `identity.stream_decoder` is null and their verdicts
    are DEFERRED with that reason. The schema does not pretend otherwise.
  * Nothing here has been run against a real record, because no unit has been built.

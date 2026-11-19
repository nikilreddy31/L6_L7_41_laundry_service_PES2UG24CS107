# L6_L7_41 - Laundry Service

## Lab 7: Fuzz Testing

### Application under test

`laundry_service.py` exposes three functions:

- `parse_order(text)` parses `garment:weight` and returns a title-cased garment and a finite, non-negative weight.
- `weight_average(weights_csv)` returns the floor average of a non-empty CSV list of non-negative integers.
- `payable_charge(text)` calculates `charge * 1.18 - discount`, with a zero floor.

Malformed input, non-text input, negative values, NaN, infinity, missing delimiters, and extra delimiters are rejected with `ValueError`. This gives callers a predictable validation error instead of incidental exceptions such as `AttributeError` or `IndexError`.

### Fuzz and property tests

`test_laundry_service.py` uses Hypothesis to feed arbitrary text and non-text objects to every public function. Inputs either produce a result satisfying its invariants or raise the documented `ValueError`. Additional generated properties verify normal order parsing, floor averaging, tax/discount arithmetic, and zero-floor behavior.

Install the test dependencies and run the complete Lab 7 suite from this directory:

```shell
python -m pip install pytest hypothesis
python -m pytest -v
```

The fuzz tests use 300 generated examples per function; valid-input properties use 150 examples each. The malformed-input examples run deterministically alongside the generated tests.

### Verified result

Command: `python -m pytest -v`

Result: **8 tests passed** (3 fuzz tests, 3 generated valid-input properties, and 2 deterministic example/validation tests). The fuzz tests each ran 300 Hypothesis examples, and each valid-input property ran 150 examples.

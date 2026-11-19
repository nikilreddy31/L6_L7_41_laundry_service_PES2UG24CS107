"""Hypothesis fuzz tests and properties for Laundry Service input functions."""

import math
import string

from hypothesis import given, settings, strategies as st

from laundry_service import parse_order, payable_charge, weight_average


FUZZ_INPUTS = st.one_of(
    st.text(max_size=100),
    st.none(),
    st.integers(),
    st.floats(allow_nan=False, allow_infinity=False),
    st.booleans(),
    st.binary(max_size=40),
    st.lists(st.text(max_size=12), max_size=5),
    st.dictionaries(st.text(max_size=8), st.integers(), max_size=4),
    st.tuples(st.text(max_size=12), st.integers()),
)
FUZZ_SETTINGS = settings(max_examples=300, deadline=None)


@FUZZ_SETTINGS
@given(FUZZ_INPUTS)
def test_parse_order_no_crash(value):
    """Arbitrary values either parse to a safe result or raise documented ValueError."""
    try:
        result = parse_order(value)
    except ValueError:
        return
    assert isinstance(result, tuple) and len(result) == 2
    garment, weight = result
    assert isinstance(garment, str) and garment
    assert math.isfinite(weight) and weight >= 0


@FUZZ_SETTINGS
@given(FUZZ_INPUTS)
def test_weight_average_no_crash(value):
    """Fuzz malformed CSV and non-text objects without leaking runtime errors."""
    try:
        result = weight_average(value)
    except ValueError:
        return
    assert isinstance(result, int) and result >= 0


@FUZZ_SETTINGS
@given(FUZZ_INPUTS)
def test_payable_charge_no_crash(value):
    """Fuzz malformed charge data and enforce a finite non-negative result."""
    try:
        result = payable_charge(value)
    except ValueError:
        return
    assert math.isfinite(result) and result >= 0


@settings(max_examples=150, deadline=None)
@given(
    st.text(
        alphabet=st.sampled_from(string.ascii_letters + " "),
        min_size=1,
        max_size=40,
    ).filter(lambda garment: garment.strip()),
    st.floats(min_value=0, max_value=1_000_000, allow_nan=False, allow_infinity=False),
)
def test_parse_order_valid_orders(garment, weight):
    assert parse_order(f" {garment} : {weight!r} ") == (garment.strip().title(), weight)


@settings(max_examples=150, deadline=None)
@given(st.lists(st.integers(min_value=0, max_value=1_000_000), min_size=1, max_size=100))
def test_weight_average_matches_floor_average(weights):
    csv = ",".join(str(weight) for weight in weights)
    assert weight_average(csv) == sum(weights) // len(weights)


@settings(max_examples=150, deadline=None)
@given(
    st.floats(min_value=0, max_value=1_000_000, allow_nan=False, allow_infinity=False),
    st.floats(min_value=0, max_value=1_000_000, allow_nan=False, allow_infinity=False),
)
def test_payable_charge_applies_tax_discount_and_zero_floor(charge, discount):
    result = payable_charge(f"{charge!r}|{discount!r}")
    expected = max(charge * 1.18 - discount, 0)
    assert math.isclose(result, expected, rel_tol=1e-12, abs_tol=1e-9)


def test_documented_examples_and_boundaries():
    assert parse_order("regular:6") == ("Regular", 6.0)
    assert weight_average("3,5,8") == 5
    assert payable_charge("300|40") == 314
    assert payable_charge("10|100") == 0


def test_malformed_inputs_raise_value_error():
    for function, values in (
        (parse_order, [None, "", "regular", ":2", "regular:", "regular:1:2", "regular:-1", "regular:nan", "regular:inf"]),
        (weight_average, [None, "", ",", "1,,2", "1,x", "-1,2"]),
        (payable_charge, [None, "", "10", "10|1|2", "|2", "2|", "nan|0", "2|-1", "1e309|0", "1.7e308|0"]),
    ):
        for value in values:
            try:
                function(value)
            except ValueError:
                continue
            raise AssertionError(f"{function.__name__} accepted malformed input {value!r}")

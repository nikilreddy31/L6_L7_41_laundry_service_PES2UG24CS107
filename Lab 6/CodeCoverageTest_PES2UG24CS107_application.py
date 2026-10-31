"""Statement coverage tests for the Laundry Service application."""

import pytest

from laundry_service import dropoff_status, extra_weight_charge, order_acceptable


@pytest.mark.parametrize(
    ("garment", "weight", "speed", "member", "expected"),
    [
        ("regular", 4, "standard", False, 0),  # Within included weight.
        ("regular", 6, "standard", False, 30),
        ("delicate", 6, "express", True, 50),  # Member allowance includes 2 kg.
        ("bedding", 9, "express", True, 50),  # Membership does not change bedding.
        ("regular", 16, "express", False, 825),  # More than 10 kg extra.
    ],
)
def test_extra_weight_charge_statement_paths(garment, weight, speed, member, expected):
    assert extra_weight_charge(garment, weight, speed, member) == expected


@pytest.mark.parametrize(
    ("weight", "items", "delicate", "expected"),
    [
        (10, 20, False, True),
        (26, 20, False, False),
        (10, 41, False, False),
        (10, 5, True, True),
        (10, 6, True, False),
    ],
)
def test_order_acceptance_statement_paths(weight, items, delicate, expected):
    assert order_acceptable(weight, items, delicate) is expected


@pytest.mark.parametrize(
    ("minutes", "bedding", "express", "expected"),
    [
        (60, False, False, "accepted"),
        (45, False, False, "late"),
        (39, False, False, "rejected"),
        (120, True, True, "accepted"),
        (101, True, True, "late"),
        (99, True, True, "rejected"),
    ],
)
def test_dropoff_status_statement_paths(minutes, bedding, express, expected):
    assert dropoff_status(minutes, bedding, express) == expected


@pytest.mark.parametrize(
    ("garment", "weight", "message"),
    [("unknown", 1, "unknown garment type"), ("regular", -0.1, "invalid weight")],
)
def test_extra_weight_validation(garment, weight, message):
    with pytest.raises(ValueError, match=message):
        extra_weight_charge(garment, weight, "standard", False)

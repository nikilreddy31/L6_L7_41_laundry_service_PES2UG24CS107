"""Branch and boundary coverage tests for the Laundry Service application."""

import pytest

from laundry_service import dropoff_status, extra_weight_charge, order_acceptable


@pytest.mark.parametrize(
    ("garment", "weight", "speed", "member", "expected"),
    [
        ("regular", 5, "standard", False, 0),  # Exactly included weight.
        ("regular", 6, "standard", False, 30),  # Standard rate.
        ("regular", 6, "express", False, 50),  # Non-standard rate.
        ("regular", 5, "standard", True, 0),  # Member allowance boundary.
        ("regular", 7, "standard", True, 0),
        ("regular", 8, "standard", True, 30),
        ("delicate", 5, "standard", True, 0),  # Member allowance applies.
        ("delicate", 6, "express", True, 50),
        ("bedding", 8, "standard", True, 0),  # Bedding is excluded from bonus.
        ("bedding", 9, "express", True, 50),
        ("regular", 15, "standard", False, 300),  # Extra exactly 10: no surcharge.
        ("regular", 16, "standard", False, 495),  # Extra greater than 10.
        ("regular", 16, "express", False, 825),  # Express surcharge path.
    ],
)
def test_charge_decisions_and_boundaries(garment, weight, speed, member, expected):
    assert extra_weight_charge(garment, weight, speed, member) == expected


@pytest.mark.parametrize(
    ("garment", "weight", "message"),
    [
        ("unknown", 1, "unknown garment type"),
        ("regular", -0.01, "invalid weight"),
    ],
)
def test_charge_rejects_invalid_inputs(garment, weight, message):
    with pytest.raises(ValueError, match=message):
        extra_weight_charge(garment, weight, "standard", False)


@pytest.mark.parametrize(
    ("weight", "items", "delicate", "expected"),
    [
        (10, 5, True, True),  # Delicate item limit accepted.
        (10, 6, True, False),  # Delicate item limit exceeded.
        (25, 40, False, True),  # Both regular limits at boundary.
        (25.01, 1, False, False),  # Weight limit exceeded.
        (10, 41, False, False),  # Item limit exceeded.
    ],
)
def test_order_acceptance_branches_and_boundaries(weight, items, delicate, expected):
    assert order_acceptable(weight, items, delicate) is expected


@pytest.mark.parametrize(
    ("minutes", "bedding", "express", "expected"),
    [
        (60, False, False, "accepted"),
        (59, False, False, "late"),
        (40, False, False, "late"),  # Exactly cutoff minus 20.
        (39, False, False, "rejected"),
        (90, True, False, "accepted"),
        (89, True, False, "late"),
        (120, False, True, "accepted"),  # Express cutoff without bedding.
        (101, False, True, "accepted"),
        (150, True, True, "accepted"),  # Bedding plus express cutoff.
        (119, True, True, "late"),
        (100, True, True, "late"),
        (99, True, True, "rejected"),
    ],
)
def test_dropoff_cutoff_branches_and_boundaries(minutes, bedding, express, expected):
    assert dropoff_status(minutes, bedding, express) == expected

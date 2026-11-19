import math


def _require_text(value, field_name):
    """Reject non-text fuzz inputs consistently instead of leaking AttributeError."""
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be text")


def _finite_nonnegative_number(value, field_name):
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError) as error:
        raise ValueError(f"{field_name} must be a finite non-negative number") from error
    if not math.isfinite(number) or number < 0:
        raise ValueError(f"{field_name} must be a finite non-negative number")
    return number


def parse_order(text):
    """Parse ``garment:weight`` and reject malformed or invalid weights."""
    _require_text(text, "order")
    parts = text.split(":")
    if len(parts) != 2:
        raise ValueError("order must contain exactly one ':' separator")

    garment, kg = (part.strip() for part in parts)
    if not garment:
        raise ValueError("garment must not be empty")
    return garment.title(), _finite_nonnegative_number(kg, "weight")

def weight_average(weights_csv):
    """Return the floor average of a non-empty CSV list of whole kg values."""
    _require_text(weights_csv, "weights")
    tokens = weights_csv.split(',')
    if any(not token.strip() for token in tokens):
        raise ValueError("weights must be a non-empty CSV list")
    try:
        values = [int(token.strip()) for token in tokens]
    except (TypeError, ValueError, OverflowError) as error:
        raise ValueError("weights must be whole numbers") from error
    if any(value < 0 for value in values):
        raise ValueError("weights must be non-negative")
    return sum(values) // len(values)

def payable_charge(text):
    """Apply 18% tax and a discount, flooring the payable amount at zero."""
    _require_text(text, "charge")
    parts = text.split('|')
    if len(parts) != 2:
        raise ValueError("charge must contain exactly one '|' separator")
    charge, discount = (
        _finite_nonnegative_number(part.strip(), name)
        for part, name in zip(parts, ("charge", "discount"))
    )
    total = charge * 1.18 - discount
    if not math.isfinite(total):
        raise ValueError("payable charge must remain finite")
    return max(total, 0)

def main():
    print("==== Running parse_order ====")
    user_input = input("Enter garment:weight in kg (e.g. regular:6): ")
    result = parse_order(user_input)
    print("Garment and Weight:", result)

    print("\n==== Running weight_average ====")
    user_input = input("Enter garment weights as CSV (e.g. 3,5,8): ")
    result = weight_average(user_input)
    print("Average Weight:", result)

    print("\n==== Running payable_charge ====")
    user_input = input("Enter charge|discount (e.g. 300|40): ")
    result = payable_charge(user_input)
    print("Payable Charge:", result)

if __name__ == "__main__":
    main()

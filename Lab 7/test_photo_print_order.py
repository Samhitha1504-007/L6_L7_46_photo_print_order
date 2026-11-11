import math
from hypothesis import given, strategies as st
from photo_print_order import parse_order, file_size_average, payable_amount


# ---------------------------------------------------------------
# Fuzz tests: random text (or None) must never crash the functions
# ---------------------------------------------------------------

@given(st.text() | st.none())
def test_parse_order_no_crash(s):
    try:
        parse_order(s)
    except Exception as e:
        assert False, f"parse_order crashed with: {e!r}"


@given(st.text() | st.none())
def test_file_size_average_no_crash(s):
    try:
        file_size_average(s)
    except Exception as e:
        assert False, f"file_size_average crashed with: {e!r}"


@given(st.text() | st.none())
def test_payable_amount_no_crash(s):
    try:
        payable_amount(s)
    except Exception as e:
        assert False, f"payable_amount crashed with: {e!r}"


# ---------------------------------------------------------------
# Fuzz tests with structured inputs that look almost valid
# ---------------------------------------------------------------

@given(st.lists(st.integers(min_value=-10, max_value=100) | st.just(""), max_size=6))
def test_file_size_average_csv_no_crash(parts):
    # CSV strings like "", "4,,8" or "-3,5"
    s = ",".join(str(p) for p in parts)
    try:
        file_size_average(s)
    except Exception as e:
        assert False, f"file_size_average crashed on {s!r}: {e!r}"


@given(st.floats(allow_nan=True, allow_infinity=True),
       st.floats(allow_nan=True, allow_infinity=True))
def test_payable_amount_float_inputs(amount, discount):
    # inputs like "nan|0", "inf|5" or "1e308|0"
    result = payable_amount(f"{amount}|{discount}")
    assert result is None or (math.isfinite(result) and result >= 0), \
        f"payable_amount returned {result!r}"


@given(st.integers(min_value=-1000, max_value=1000))
def test_parse_order_copies_not_negative(copies):
    result = parse_order(f"4x6:{copies}")
    assert result is None or result[1] >= 0, f"negative copies accepted: {result!r}"


# ---------------------------------------------------------------
# Property tests: valid input gives the correct result
# ---------------------------------------------------------------

@given(st.sampled_from(["4x6", "5x7", "8x10"]), st.integers(min_value=0, max_value=10000))
def test_parse_order_valid(size, copies):
    assert parse_order(f" {size} : {copies} ") == (size.upper(), copies)


@given(st.lists(st.integers(min_value=0, max_value=1000), min_size=1, max_size=20))
def test_file_size_average_valid(values):
    result = file_size_average(",".join(str(v) for v in values))
    assert result == sum(values) // len(values)
    assert min(values) <= result <= max(values)


@given(st.integers(min_value=0, max_value=100000), st.integers(min_value=0, max_value=100000))
def test_payable_amount_valid(amount, discount):
    expected = max(amount * 1.18 - discount, 0)
    assert math.isclose(payable_amount(f"{amount}|{discount}"), expected, abs_tol=0.01)

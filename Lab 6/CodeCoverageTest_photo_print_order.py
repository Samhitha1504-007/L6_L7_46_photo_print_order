import pytest
from photo_print_order import extra_print_charge, order_valid, dispatch_status


# ---------- extra_print_charge ----------

def test_within_included_prints():
    # 15 copies of 4x6 is within the 20 included -> no charge
    assert extra_print_charge("4x6", 15, "matte", False) == 0


def test_unknown_print_size_raises():
    with pytest.raises(ValueError, match="unknown print size"):
        extra_print_charge("6x9", 10, "matte", False)


def test_negative_copies_raises():
    with pytest.raises(ValueError, match="invalid copies"):
        extra_print_charge("4x6", -1, "matte", False)


def test_member_bonus_matte_small_extra():
    # member on 4x6: included 20 + 5 = 25, extra = 5, matte rate 4 -> 20
    assert extra_print_charge("4x6", 30, "matte", True) == 20


def test_large_extra_canvas_surcharge():
    # 5x7 non-member: included 15, extra = 85 (>50)
    # rate = 7 (non-matte) + 2 (bulk) + 5 (canvas) = 14 -> 85 * 14 = 1190
    assert extra_print_charge("5x7", 100, "canvas", False) == 1190


# ---------- order_valid ----------

def test_order_valid():
    assert order_valid(10, 100, False) is True


def test_rush_order_within_limit():
    assert order_valid(10, 30, True) is True


def test_file_too_large_rejected():
    assert order_valid(30, 10, False) is False


# ---------- dispatch_status ----------

def test_framed_domestic_on_time():
    # framed cutoff 24
    assert dispatch_status(30, True, False) == "on_time"


def test_unframed_international_on_time():
    # cutoff 12 + 24 = 36
    assert dispatch_status(40, False, True) == "on_time"


def test_unframed_domestic_tight():
    # cutoff 12, 8 >= 12 - 6
    assert dispatch_status(8, False, False) == "tight"


def test_unframed_domestic_missed():
    assert dispatch_status(1, False, False) == "missed"

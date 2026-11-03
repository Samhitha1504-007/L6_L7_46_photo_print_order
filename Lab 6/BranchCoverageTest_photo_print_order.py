import pytest
from photo_print_order import extra_print_charge, order_valid, dispatch_status


# =====================================================================
# extra_print_charge
# =====================================================================

# --- validation branches ---

def test_unknown_print_size_raises():
    with pytest.raises(ValueError, match="unknown print size"):
        extra_print_charge("6x9", 10, "matte", False)


def test_negative_copies_raises():
    with pytest.raises(ValueError, match="invalid copies"):
        extra_print_charge("4x6", -1, "matte", False)


def test_zero_copies_allowed():
    # copies < 0 is False at the boundary
    assert extra_print_charge("4x6", 0, "matte", False) == 0


# --- membership branch: (is_member and print_size != "8x10") ---

def test_member_bonus_applies_on_4x6():
    # T and T -> included 25, extra 5, matte 4 -> 20
    assert extra_print_charge("4x6", 30, "matte", True) == 20


def test_member_no_bonus_on_8x10():
    # T and F -> no bonus: included 10, extra 5, matte 4 -> 20
    assert extra_print_charge("8x10", 15, "matte", True) == 20


def test_non_member_no_bonus():
    # F -> included 20, extra 10, glossy 7 -> 70
    assert extra_print_charge("4x6", 30, "glossy", False) == 70


# --- extra <= 0 branch ---

def test_within_included_prints():
    assert extra_print_charge("4x6", 15, "matte", False) == 0


def test_exactly_included_prints():
    # extra == 0 boundary -> no charge
    assert extra_print_charge("5x7", 15, "glossy", False) == 0


def test_one_over_included():
    # extra == 1 -> charged
    assert extra_print_charge("5x7", 16, "glossy", False) == 7


# --- finish branch: matte vs other ---

def test_matte_rate():
    # 8x10 non-member: included 10, extra 10, matte 4 -> 40
    assert extra_print_charge("8x10", 20, "matte", False) == 40


def test_non_matte_rate():
    # extra 10, glossy 7 -> 70
    assert extra_print_charge("8x10", 20, "glossy", False) == 70


# --- bulk branch: extra > 50, and nested canvas branch ---

def test_extra_exactly_50_no_bulk_surcharge():
    # 4x6 non-member: included 20, extra 50 -> not > 50, rate 7 -> 350
    assert extra_print_charge("4x6", 70, "glossy", False) == 350


def test_bulk_matte_surcharge():
    # extra 51 -> rate 4 + 2 = 6 -> 306
    assert extra_print_charge("4x6", 71, "matte", False) == 306


def test_bulk_glossy_no_canvas():
    # extra > 50, finish != canvas -> rate 7 + 2 = 9; extra 80 -> 720
    assert extra_print_charge("4x6", 100, "glossy", False) == 720


def test_bulk_canvas_surcharge():
    # 5x7 non-member: extra 85, rate 7 + 2 + 5 = 14 -> 1190
    assert extra_print_charge("5x7", 100, "canvas", False) == 1190


def test_small_canvas_order_no_canvas_surcharge():
    # canvas surcharge only applies for bulk; extra 5 -> rate 7 -> 35
    assert extra_print_charge("4x6", 25, "canvas", False) == 35


# =====================================================================
# order_valid
# =====================================================================

def test_order_valid():
    assert order_valid(10, 100, False) is True


def test_rush_within_limit():
    assert order_valid(10, 30, True) is True


def test_rush_at_limit():
    assert order_valid(10, 50, True) is True


def test_rush_over_limit():
    assert order_valid(10, 51, True) is False


def test_rush_ignores_file_size():
    # rush branch returns before file size check
    assert order_valid(100, 10, True) is True


def test_file_too_large_rejected():
    assert order_valid(30, 10, False) is False


def test_file_size_at_limit_accepted():
    assert order_valid(25, 10, False) is True


def test_copies_at_limit_accepted():
    assert order_valid(10, 500, False) is True


def test_copies_over_limit_rejected():
    assert order_valid(10, 501, False) is False


# =====================================================================
# dispatch_status
# =====================================================================

def test_framed_domestic_on_time():
    # cutoff 24
    assert dispatch_status(30, True, False) == "on_time"


def test_framed_domestic_exact_cutoff():
    assert dispatch_status(24, True, False) == "on_time"


def test_framed_domestic_tight():
    # 18 <= h < 24
    assert dispatch_status(20, True, False) == "tight"


def test_framed_domestic_tight_lower_bound():
    assert dispatch_status(18, True, False) == "tight"


def test_framed_domestic_missed():
    assert dispatch_status(17, True, False) == "missed"


def test_unframed_domestic_on_time():
    # cutoff 12
    assert dispatch_status(12, False, False) == "on_time"


def test_unframed_domestic_tight():
    assert dispatch_status(8, False, False) == "tight"


def test_unframed_domestic_missed():
    assert dispatch_status(1, False, False) == "missed"


def test_unframed_international_on_time():
    # cutoff 12 + 24 = 36
    assert dispatch_status(40, False, True) == "on_time"


def test_unframed_international_tight():
    assert dispatch_status(30, False, True) == "tight"


def test_framed_international_on_time():
    # cutoff 24 + 24 = 48
    assert dispatch_status(48, True, True) == "on_time"


def test_framed_international_tight():
    assert dispatch_status(45, True, True) == "tight"


def test_framed_international_missed():
    assert dispatch_status(41, True, True) == "missed"

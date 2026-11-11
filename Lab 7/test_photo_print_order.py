from hypothesis import given, strategies as st
from photo_print_order import parse_order, file_size_average, payable_amount

@given(st.text() | st.none())
def test_parse_order_no_crash(s):

@given(st.text() | st.none())
def test_file_size_average_no_crash(s):

@given(st.text() | st.none())
def test_payable_amount_no_crash(s):

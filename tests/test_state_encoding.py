import pytest

from configuration import *

def test_decoding():
    encoded = BACKLED_MODE*16 + FRONTLED_MODE*27 + POTLED_REL_BRIGHTNESS*2 + FRONTLED_DIY4_REL_RGB*18
    decoded = decode_state(encoded)
    assert decoded.backled_mode == 16
    assert decoded.frontled_mode == 27
    assert decoded.potled_rel_brightness == 2
    assert decoded.frontled_diy4_rel_rgb == 18

def test_decoding_encoded_default():
    state = State()
    assert decode_state(encode_state(state)) == state

def test_encoding_decoded():
    assert encode_state(decode_state(0)) == 0
    assert encode_state(decode_state(1)) == 1
    assert encode_state(decode_state(15)) == 15
    assert encode_state(decode_state(15518461)) == 15518461
    assert encode_state(decode_state(5465484964161161)) == 5465484964161161 # < STATE_MAX_SIZE

def test_encoding_rollover():
    assert encode_state(decode_state(STATE_MAX_SIZE)) == STATE_MAX_SIZE
    assert encode_state(decode_state(STATE_MAX_SIZE + 1)) == 0
    assert encode_state(decode_state(STATE_MAX_SIZE + 2)) == 1

def test_rgb_encoding():
    for i in range(81):
        assert get_r(set_r(i, 0)) == 0
        assert get_r(set_r(i, 1)) == 1
        assert get_r(set_r(i, 2)) == 2
        assert get_g(set_g(i, 0)) == 0
        assert get_g(set_g(i, 1)) == 1
        assert get_g(set_g(i, 2)) == 2
        assert get_b(set_b(i, 0)) == 0
        assert get_b(set_b(i, 1)) == 1
        assert get_b(set_b(i, 2)) == 2

        assert get_r(set_g(i, 0)) == get_r(i)
        assert get_r(set_g(i, 1)) == get_r(i)
        assert get_r(set_g(i, 2)) == get_r(i)
        assert get_r(set_b(i, 0)) == get_r(i)
        assert get_r(set_b(i, 1)) == get_r(i)
        assert get_r(set_b(i, 2)) == get_r(i)
        
        assert get_g(set_r(i, 0)) == get_g(i)
        assert get_g(set_r(i, 1)) == get_g(i)
        assert get_g(set_r(i, 2)) == get_g(i)
        assert get_g(set_b(i, 0)) == get_g(i)
        assert get_g(set_b(i, 1)) == get_g(i)
        assert get_g(set_b(i, 2)) == get_g(i)

        assert get_b(set_r(i, 0)) == get_b(i)
        assert get_b(set_r(i, 1)) == get_b(i)
        assert get_b(set_r(i, 2)) == get_b(i)
        assert get_b(set_g(i, 0)) == get_b(i)
        assert get_b(set_g(i, 1)) == get_b(i)
        assert get_b(set_g(i, 2)) == get_b(i)
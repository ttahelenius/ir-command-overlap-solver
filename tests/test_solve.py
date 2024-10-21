import pytest

from main import solve_command_series
from configuration import Command

USE_CACHE = True

def test_simple():
    assert solve_command_series("backled r, frontled g, potled b", "frontled b",   USE_CACHE) == [Command.FRONT_B]
    assert solve_command_series("backled r, frontled g, potled b", "frontled r3",  USE_CACHE) == [Command.FRONT_R3]
    assert solve_command_series("backled r, frontled g, potled b", "backled off",  USE_CACHE) == [Command.BACK_OFF]
    assert solve_command_series("backled r, frontled g, potled b", "frontled off", USE_CACHE) == [Command.FRONT_ONOFF]
    assert solve_command_series("backled r, frontled g, potled b", "frontled w3",  USE_CACHE) == [Command.FRONT_W3]

def test_heuristic():
    assert solve_command_series("backled g, frontled b3, potled r4", "backled g4", USE_CACHE) == \
        [Command.BACK_G4_FRONT_GDOWN]

    assert solve_command_series("backled g, frontled b3, potled r4", "backled g3", USE_CACHE) == \
        [Command.BACK_G3_FRONT_DIY2,
         Command.FRONT_B3]

    assert solve_command_series("backled g, frontled diy6, potled r4", "backled g3", USE_CACHE) == \
        [Command.FRONT_ONOFF,
         Command.BACK_G3_FRONT_DIY2,
         Command.FRONT_ONOFF]
    
    assert solve_command_series("backled r, frontled r5, potled r", "backled w", USE_CACHE) == \
        [Command.BACK_W_FRONT_FADE7,
         Command.FRONT_R5_POT_G4,
         Command.FRONT_ONOFF,
         Command.FRONT_DIY5_POT_R,
         Command.FRONT_ONOFF]
    
    assert solve_command_series("backled g, frontled b3, potled g", "frontled r2", USE_CACHE) == \
        [Command.FRONT_R2]
    
    assert solve_command_series("backled g, frontled b3, potled g", "frontled diy2", USE_CACHE) == \
        [Command.BACK_OFF,
         Command.BACK_G3_FRONT_DIY2,
         Command.BACK_ON]
    
    assert solve_command_series("backled g, frontled b3, potled r3", "frontled g5", USE_CACHE) == \
        [Command.FRONT_G5_POT_R4,
         Command.FRONT_GUP_POT_R3]
    
    assert solve_command_series("backled r, frontled r, potled r", "frontled r5", USE_CACHE) == \
        [Command.FRONT_R5_POT_G4,
         Command.FRONT_ONOFF,
         Command.FRONT_DIY5_POT_R,
         Command.FRONT_ONOFF]
    
    assert solve_command_series("backled g, frontled b3, potled r4", "potled r5", USE_CACHE) == \
        [Command.FRONT_GDOWN_POT_R5]

    assert solve_command_series("backled g, frontled b3, potled r4", "potled g4", USE_CACHE) == \
        [Command.FRONT_R5_POT_G4,
         Command.FRONT_B3]

    assert solve_command_series("backled g, frontled b5, potled r4", "potled g", USE_CACHE) == \
        [Command.FRONT_ONOFF,
         Command.FRONT_DIY4_POT_G,
         Command.FRONT_ONOFF]
    
    assert solve_command_series("backled r, frontled r5, potled r, frontled off", "backled w", USE_CACHE) == \
        [Command.FRONT_ONOFF,
         Command.BACK_W_FRONT_FADE7,
         Command.FRONT_R5_POT_G4,
         Command.FRONT_ONOFF,
         Command.FRONT_DIY5_POT_R]
    
    assert solve_command_series("backled r, frontled r5, potled r, backled off, frontled off, potled off", "potled on", USE_CACHE) == \
        [Command.FRONT_ONOFF,
         Command.FRONT_FADE7_POT_ON,
         Command.FRONT_R5_POT_G4,
         Command.FRONT_ONOFF,
         Command.FRONT_DIY5_POT_R]
    
    assert solve_command_series("backled r, frontled jump3, potled r, frontled off", "backled w", USE_CACHE) == \
        [Command.FRONT_ONOFF,
         Command.BACK_W_FRONT_FADE7,
         Command.BACK_OFF,
         Command.BACK_R_FRONT_JUMP3,
         Command.BACK_ON,
         Command.FRONT_ONOFF]

def test_would_be_slow_without_cache_device_toggling_optimization():
    assert solve_command_series("backled g2, frontled b2, potled r4", "frontled w5", USE_CACHE) == \
        [Command.FRONT_W5_POT_FADE,
         Command.FRONT_ONOFF,
         Command.FRONT_G5_POT_R4,
         Command.FRONT_ONOFF]
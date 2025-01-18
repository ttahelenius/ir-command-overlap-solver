"""
This file features the data required to define the graph to be traversed, as
well as some convenience functions related to that.
Not exactly an elegant representation but gets the job done.
"""

import dataclasses
from enum import Enum

# E.g. brightening as an unintended side effect can be countered by dimming later
# but this only works if the brightness wasn't initially at maximum, which can not
# be known. Therefore it's often better to avoid triggering any other relative
# state than the intended one.
AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY = True

class Command(Enum):
    FRONT_ONOFF = 0
    FRONT_PLAYPAUSE = 1
    FRONT_DIM = 2
    FRONT_BRIGHTEN = 3
    FRONT_R = 4
    FRONT_G = 5
    FRONT_B = 6
    FRONT_W = 7
    FRONT_W2 = 8
    FRONT_W3 = 9
    FRONT_W4 = 10
    FRONT_W5_POT_FADE = 11
    FRONT_B2 = 12
    FRONT_B3 = 13
    FRONT_B4 = 14
    FRONT_B5_POT_B4 = 15
    FRONT_G2 = 16
    FRONT_G3 = 17
    FRONT_G4 = 18
    FRONT_G5_POT_R4 = 19
    FRONT_R2 = 20
    FRONT_R3 = 21
    FRONT_R4 = 22
    FRONT_R5_POT_G4 = 23
    FRONT_RUP_POT_G3 = 24
    FRONT_RDOWN_POT_G5 = 25
    FRONT_GUP_POT_R3 = 26
    FRONT_GDOWN_POT_R5 = 27
    FRONT_BUP_POT_B3 = 28
    FRONT_BDOWN_POT_B5 = 29
    FRONT_QUICK_POT_STROBE = 30
    FRONT_SLOW_POT_SMOOTH = 31
    FRONT_AUTO_POT_FLASH = 32
    FRONT_DIY1_POT_G2 = 33
    FRONT_DIY2_POT_R2 = 34
    FRONT_DIY3_POT_B2 = 35
    FRONT_DIY4_POT_G = 36
    FRONT_DIY5_POT_R = 37
    FRONT_DIY6_POT_B = 38
    FRONT_FLASH_POT_W = 39
    FRONT_JUMP3_POT_DOWN = 40
    FRONT_JUMP7_POT_UP = 41
    FRONT_FADE3_POT_OFF = 42
    FRONT_FADE7_POT_ON = 43
    BACK_R5_FRONT_RUP = 44
    BACK_R4_FRONT_RDOWN = 45
    BACK_G5_FRONT_GUP = 46
    BACK_G4_FRONT_GDOWN = 47
    BACK_B5_FRONT_BUP = 48
    BACK_B4_FRONT_BDOWN = 49
    BACK_SMOOTH_FRONT_QUICK = 50
    BACK_FADE_FRONT_SLOW = 51
    BACK_STROBE_FRONT_AUTO = 52
    BACK_R3_FRONT_DIY1 = 53
    BACK_G3_FRONT_DIY2 = 54
    BACK_B3_FRONT_DIY3 = 55
    BACK_R2_FRONT_DIY4 = 56
    BACK_G2_FRONT_DIY5 = 57
    BACK_B2_FRONT_DIY6 = 58
    BACK_FLASH_FRONT_FLASH = 59
    BACK_R_FRONT_JUMP3 = 60
    BACK_G_FRONT_JUMP7 = 61
    BACK_B_FRONT_FADE3 = 62
    BACK_W_FRONT_FADE7 = 63
    BACK_ON = 64
    BACK_OFF = 65
    BACK_DOWN = 66
    BACK_UP = 67


COMMANDS = {
    # [Command]                     : ([executable],         [side-effect])
    Command.FRONT_ONOFF             : ("frontled onoff",     None),
    Command.FRONT_PLAYPAUSE         : ("frontled playpause", None),
    Command.FRONT_DIM               : ("frontled dim",       None),
    Command.FRONT_BRIGHTEN          : ("frontled bright",    None),
    Command.FRONT_R                 : ("frontled r",         None),
    Command.FRONT_G                 : ("frontled g",         None),
    Command.FRONT_B                 : ("frontled b",         None),
    Command.FRONT_W                 : ("frontled w",         None),
    Command.FRONT_W2                : ("frontled w2",        None),
    Command.FRONT_W3                : ("frontled w3",        None),
    Command.FRONT_W4                : ("frontled w4",        None),
    Command.FRONT_W5_POT_FADE       : ("frontled w5",        "potled fade"),
    Command.FRONT_B2                : ("frontled b2",        None),
    Command.FRONT_B3                : ("frontled b3",        None),
    Command.FRONT_B4                : ("frontled b4",        None),
    Command.FRONT_B5_POT_B4         : ("frontled b5",        "potled b4"),
    Command.FRONT_G2                : ("frontled g2",        None),
    Command.FRONT_G3                : ("frontled g3",        None),
    Command.FRONT_G4                : ("frontled g4",        None),
    Command.FRONT_G5_POT_R4         : ("frontled g5",        "potled r4"),
    Command.FRONT_R2                : ("frontled r2",        None),
    Command.FRONT_R3                : ("frontled r3",        None),
    Command.FRONT_R4                : ("frontled r4",        None),
    Command.FRONT_R5_POT_G4         : ("frontled r5",        "potled g4"),
    Command.FRONT_RUP_POT_G3        : ("frontled rup",       "potled g3"),
    Command.FRONT_RDOWN_POT_G5      : ("frontled rdown",     "potled g5"),
    Command.FRONT_GUP_POT_R3        : ("frontled gup",       "potled r3"),
    Command.FRONT_GDOWN_POT_R5      : ("frontled gdown",     "potled r5"),
    Command.FRONT_BUP_POT_B3        : ("frontled bup",       "potled b3"),
    Command.FRONT_BDOWN_POT_B5      : ("frontled bdown",     "potled b5"),
    Command.FRONT_QUICK_POT_STROBE  : ("frontled quick",     "potled strobe"),
    Command.FRONT_SLOW_POT_SMOOTH   : ("frontled slow",      "potled smooth"),
    Command.FRONT_AUTO_POT_FLASH    : ("frontled auto",      "potled flash"),
    Command.FRONT_DIY1_POT_G2       : ("frontled diy1",      "potled g2"),
    Command.FRONT_DIY2_POT_R2       : ("frontled diy2",      "potled r2"),
    Command.FRONT_DIY3_POT_B2       : ("frontled diy3",      "potled b2"),
    Command.FRONT_DIY4_POT_G        : ("frontled diy4",      "potled g"),
    Command.FRONT_DIY5_POT_R        : ("frontled diy5",      "potled r"),
    Command.FRONT_DIY6_POT_B        : ("frontled diy6",      "potled b"),
    Command.FRONT_FLASH_POT_W       : ("frontled flash",     "potled w"),
    Command.FRONT_JUMP3_POT_DOWN    : ("frontled jump3",     "potled down"),
    Command.FRONT_JUMP7_POT_UP      : ("frontled jump7",     "potled up"),
    Command.FRONT_FADE3_POT_OFF     : ("frontled fade3",     "potled off"),
    Command.FRONT_FADE7_POT_ON      : ("frontled fade7",     "potled on"),
    Command.BACK_R5_FRONT_RUP       : ("backled r5",         "frontled rup"),
    Command.BACK_R4_FRONT_RDOWN     : ("backled r4",         "frontled rdown"),
    Command.BACK_G5_FRONT_GUP       : ("backled g5",         "frontled gup"),
    Command.BACK_G4_FRONT_GDOWN     : ("backled g4",         "frontled gdown"),
    Command.BACK_B5_FRONT_BUP       : ("backled b5",         "frontled bup"),
    Command.BACK_B4_FRONT_BDOWN     : ("backled b4",         "frontled bdown"),
    Command.BACK_SMOOTH_FRONT_QUICK : ("backled smooth",     "frontled quick"),
    Command.BACK_FADE_FRONT_SLOW    : ("backled fade",       "frontled slow"),
    Command.BACK_STROBE_FRONT_AUTO  : ("backled strobe",     "frontled auto"),
    Command.BACK_R3_FRONT_DIY1      : ("backled r3",         "frontled diy1"),
    Command.BACK_G3_FRONT_DIY2      : ("backled g3",         "frontled diy2"),
    Command.BACK_B3_FRONT_DIY3      : ("backled b3",         "frontled diy3"),
    Command.BACK_R2_FRONT_DIY4      : ("backled r2",         "frontled diy4"),
    Command.BACK_G2_FRONT_DIY5      : ("backled g2",         "frontled diy5"),
    Command.BACK_B2_FRONT_DIY6      : ("backled b2",         "frontled diy6"),
    Command.BACK_FLASH_FRONT_FLASH  : ("backled flash",      "frontled flash"),
    Command.BACK_R_FRONT_JUMP3      : ("backled r",          "frontled jump3"),
    Command.BACK_G_FRONT_JUMP7      : ("backled g",          "frontled jump7"),
    Command.BACK_B_FRONT_FADE3      : ("backled b",          "frontled fade3"),
    Command.BACK_W_FRONT_FADE7      : ("backled w",          "frontled fade7"),
    Command.BACK_ON                 : ("backled on",         None),
    Command.BACK_OFF                : ("backled off",        None),
    Command.BACK_DOWN               : ("backled dim",        None),
    Command.BACK_UP                 : ("backled bright",     None)
}

COMMAND_ALIASES = [
    "frontled on", "frontled off",
    "frontled paused", "frontled unpaused",
    "frontled dim", "frontled bright",
    "frontled w", "frontled w2", "frontled w3", "frontled w4", "frontled w5",
    "frontled b", "frontled b2", "frontled b3", "frontled b4", "frontled b5",
    "frontled g", "frontled g2", "frontled g3",  "frontled g4", "frontled g5",
    "frontled r", "frontled r2", "frontled r3", "frontled r4", "frontled r5",
    "frontled diy1", "frontled diy2", "frontled diy3",
    "frontled diy4", "frontled diy5", "frontled diy6",
    "frontled diy1 rup", "frontled diy2 rup", "frontled diy3 rup",
    "frontled diy4 rup", "frontled diy5 rup", "frontled diy6 rup",
    "frontled diy1 rdown", "frontled diy2 rdown", "frontled diy3 rdown",
    "frontled diy4 rdown", "frontled diy5 rdown", "frontled diy6 rdown",
    "frontled diy1 gup", "frontled diy2 gup", "frontled diy3 gup",
    "frontled diy4 gup", "frontled diy5 gup", "frontled diy6 gup",
    "frontled diy1 gdown", "frontled diy2 gdown", "frontled diy3 gdown",
    "frontled diy4 gdown", "frontled diy5 gdown", "frontled diy6 gdown",
    "frontled diy1 bup", "frontled diy2 bup", "frontled diy3 bup",
    "frontled diy4 bup", "frontled diy5 bup", "frontled diy6 bup",
    "frontled diy1 bdown", "frontled diy2 bdown", "frontled diy3 bdown",
    "frontled diy4 bdown", "frontled diy5 bdown", "frontled diy6 bdown",
    "frontled quick", "frontled slow",
    "frontled auto", "frontled flash",
    "frontled jump3", "frontled jump7", "frontled fade3", "frontled fade7",

    "backled on", "backled off",
    "backled dim", "backled bright",
    "backled quick", "backled slow",
    "backled r", "backled r2", "backled r3", "backled r4", "backled r5",
    "backled g", "backled g2", "backled g3", "backled g4", "backled g5",
    "backled b", "backled b2", "backled b3", "backled b4", "backled b5",
    "backled w",
    "backled flash", "backled smooth", "backled fade", "backled strobe",

    "potled on", "potled off",
    "potled dim", "potled bright",
    "potled quick", "potled slow",
    "potled r", "potled r2", "potled r3", "potled r4", "potled r5",
    "potled g", "potled g2", "potled g3", "potled g4", "potled g5",
    "potled b", "potled b2", "potled b3", "potled b4", "potled b5",
    "potled w",
    "potled flash", "potled smooth", "potled fade", "potled strobe",

    "frontled calibrate", "potled calibrate"
]

RELATIVE_STATES = [
    ("frontled slow", "frontled quick"), ("backled slow", "backled quick"), ("potled slow", "potled quick"),
    ("frontled dim", "frontled bright"), ("backled dim", "backled bright"), ("potled dim", "potled bright"),
    ("frontled diy1 rup", "frontled diy1 rdown"),
    ("frontled diy1 gup", "frontled diy1 gdown"),
    ("frontled diy1 bup", "frontled diy1 bdown"),
    ("frontled diy2 rup", "frontled diy2 rdown"),
    ("frontled diy2 gup", "frontled diy2 gdown"),
    ("frontled diy2 bup", "frontled diy2 bdown"),
    ("frontled diy3 rup", "frontled diy3 rdown"),
    ("frontled diy3 gup", "frontled diy3 gdown"),
    ("frontled diy3 bup", "frontled diy3 bdown"),
    ("frontled diy4 rup", "frontled diy4 rdown"),
    ("frontled diy4 gup", "frontled diy4 gdown"),
    ("frontled diy4 bup", "frontled diy4 bdown"),
    ("frontled diy5 rup", "frontled diy5 rdown"),
    ("frontled diy5 gup", "frontled diy5 gdown"),
    ("frontled diy5 bup", "frontled diy5 bdown"),
    ("frontled diy6 rup", "frontled diy6 rdown"),
    ("frontled diy6 gup", "frontled diy6 gdown"),
    ("frontled diy6 bup", "frontled diy6 bdown"),
]

def convert_target_state(target_state: str, initial_states: list[str]) -> str:
    if target_state == "frontled playpause":
        return "frontled unpaused" if "frontled paused" in initial_states else "frontled paused"
    
    for command in ["rup", "rdown", "gup", "gdown", "bup", "bdown"]:
        if target_state == "frontled " + command:
            if "frontled diy1" in initial_states:
                return "frontled diy1 " + command
            elif "frontled diy2" in initial_states:
                return "frontled diy2 " + command
            elif "frontled diy3" in initial_states:
                return "frontled diy3 " + command
            elif "frontled diy4" in initial_states:
                return "frontled diy4 " + command
            elif "frontled diy5" in initial_states:
                return "frontled diy5 " + command
            elif "frontled diy6" in initial_states:
                return "frontled diy6 " + command
            
    if target_state == "backled dim":
        for state in initial_states:
            if state in BACKLED_MODES and BACKLED_MODES.index(state) not in BACKLED_COLOR_MODES:
                return "backled slow"
    elif target_state == "backled bright":
        for state in initial_states:
            if state in BACKLED_MODES and BACKLED_MODES.index(state) not in BACKLED_COLOR_MODES:
                return "backled quick"
    elif target_state == "potled dim":
        for state in initial_states:
            if state in POTLED_MODES and POTLED_MODES.index(state) not in POTLED_COLOR_MODES:
                return "potled slow"
    elif target_state == "potled bright":
        for state in initial_states:
            if state in POTLED_MODES and POTLED_MODES.index(state) not in POTLED_COLOR_MODES:
                return "potled quick"
            
    return target_state

def get_commands_for_relative_state(state: str) -> list[Command]:
    match state:
        case "backled slow" | "backled dim":
            return [Command.BACK_DOWN]
        case "backled quick" | "backled bright":
            return [Command.BACK_UP]
        case "potled slow" | "potled dim":
            return [Command.FRONT_JUMP3_POT_DOWN]
        case "potled quick" | "potled bright":
            return [Command.FRONT_JUMP7_POT_UP]
        case "frontled dim":
            return [Command.FRONT_DIM]
        case "frontled bright":
            return [Command.FRONT_BRIGHTEN]
        case "frontled slow":
            return [Command.FRONT_SLOW_POT_SMOOTH, Command.BACK_FADE_FRONT_SLOW]
        case "frontled quick":
            return [Command.FRONT_QUICK_POT_STROBE, Command.BACK_SMOOTH_FRONT_QUICK]
        case "frontled diy1 rup" | "frontled diy2 rup" | "frontled diy3 rup" | "frontled diy4 rup" | "frontled diy5 rup" | "frontled diy6 rup":
            return [Command.FRONT_RUP_POT_G3, Command.BACK_R5_FRONT_RUP]
        case "frontled diy1 rdown" | "frontled diy2 rdown" | "frontled diy3 rdown" | "frontled diy4 rdown" | "frontled diy5 rdown" | "frontled diy6 rdown":
            return [Command.FRONT_RDOWN_POT_G5, Command.BACK_R4_FRONT_RDOWN]
        case "frontled diy1 gup" | "frontled diy2 gup" | "frontled diy3 gup" | "frontled diy4 gup" | "frontled diy5 gup" | "frontled diy6 gup":
            return [Command.FRONT_GUP_POT_R3, Command.BACK_G5_FRONT_GUP]
        case "frontled diy1 gdown" | "frontled diy2 gdown" | "frontled diy3 gdown" | "frontled diy4 gdown" | "frontled diy5 gdown" | "frontled diy6 gdown":
            return [Command.FRONT_GDOWN_POT_R5, Command.BACK_G4_FRONT_GDOWN]
        case "frontled diy1 bup" | "frontled diy2 bup" | "frontled diy3 bup" | "frontled diy4 bup" | "frontled diy5 bup" | "frontled diy6 bup":
            return [Command.FRONT_BUP_POT_B3, Command.BACK_B5_FRONT_BUP]
        case "frontled diy1 bdown" | "frontled diy2 bdown" | "frontled diy3 bdown" | "frontled diy4 bdown" | "frontled diy5 bdown" | "frontled diy6 bdown":
            return [Command.FRONT_BDOWN_POT_B5, Command.BACK_B4_FRONT_BDOWN]
    return []

BACKLED_MODES = [
    "backled r", "backled r2", "backled r3", "backled r4", "backled r5",
    "backled g", "backled g2", "backled g3", "backled g4", "backled g5",
    "backled b", "backled b2", "backled b3", "backled b4", "backled b5",
    "backled w",
    "backled smooth",
    "backled fade",
    "backled strobe",
    "backled flash",
]
BACKLED_COLOR_MODES = [i for i in range(16)]

def backled_get_command_for(mode: int) -> Command:
    return [
        Command.BACK_R_FRONT_JUMP3,
        Command.BACK_R2_FRONT_DIY4,
        Command.BACK_R3_FRONT_DIY1,
        Command.BACK_R4_FRONT_RDOWN,
        Command.BACK_R5_FRONT_RUP,
        Command.BACK_G_FRONT_JUMP7,
        Command.BACK_G2_FRONT_DIY5,
        Command.BACK_G3_FRONT_DIY2,
        Command.BACK_G4_FRONT_GDOWN,
        Command.BACK_G5_FRONT_GUP,
        Command.BACK_B_FRONT_FADE3,
        Command.BACK_B2_FRONT_DIY6,
        Command.BACK_B3_FRONT_DIY3,
        Command.BACK_B4_FRONT_BDOWN,
        Command.BACK_B5_FRONT_BUP,
        Command.BACK_W_FRONT_FADE7,
        Command.BACK_SMOOTH_FRONT_QUICK,
        Command.BACK_FADE_FRONT_SLOW,
        Command.BACK_STROBE_FRONT_AUTO,
        Command.BACK_FLASH_FRONT_FLASH
    ][mode]

FRONTLED_MODES = [
    "frontled r", "frontled r2", "frontled r3", "frontled r4", "frontled r5",
    "frontled g", "frontled g2", "frontled g3", "frontled g4", "frontled g5",
    "frontled b", "frontled b2", "frontled b3", "frontled b4", "frontled b5",
    "frontled w", "frontled w2", "frontled w3", "frontled w4", "frontled w5",
    "frontled diy1", "frontled diy2", "frontled diy3",
    "frontled diy4", "frontled diy5", "frontled diy6",
    "frontled auto",
    "frontled flash",
    "frontled jump3",
    "frontled jump7",
    "frontled fade3",
    "frontled fade7",
]
FRONTLED_COLOR_MODES = [i for i in range(20)]

def frontled_get_command_for(mode: int, potled_overlap: bool = True) -> Command:
    return [
        Command.FRONT_R,
        Command.FRONT_R2,
        Command.FRONT_R3,
        Command.FRONT_R4,
        Command.FRONT_R5_POT_G4,
        Command.FRONT_G,
        Command.FRONT_G2,
        Command.FRONT_G3,
        Command.FRONT_G4,
        Command.FRONT_G5_POT_R4,
        Command.FRONT_B,
        Command.FRONT_B2,
        Command.FRONT_B3,
        Command.FRONT_B4,
        Command.FRONT_B5_POT_B4,
        Command.FRONT_W,
        Command.FRONT_W2,
        Command.FRONT_W3,
        Command.FRONT_W4,
        Command.FRONT_W5_POT_FADE,
        Command.FRONT_DIY1_POT_G2    if potled_overlap else Command.BACK_R3_FRONT_DIY1,
        Command.FRONT_DIY2_POT_R2    if potled_overlap else Command.BACK_G3_FRONT_DIY2,
        Command.FRONT_DIY3_POT_B2    if potled_overlap else Command.BACK_B3_FRONT_DIY3,
        Command.FRONT_DIY4_POT_G     if potled_overlap else Command.BACK_R2_FRONT_DIY4,
        Command.FRONT_DIY5_POT_R     if potled_overlap else Command.BACK_G2_FRONT_DIY5,
        Command.FRONT_DIY6_POT_B     if potled_overlap else Command.BACK_B2_FRONT_DIY6,
        Command.FRONT_AUTO_POT_FLASH if potled_overlap else Command.BACK_STROBE_FRONT_AUTO,
        Command.FRONT_FLASH_POT_W    if potled_overlap else Command.BACK_FLASH_FRONT_FLASH,
        Command.FRONT_JUMP3_POT_DOWN if potled_overlap else Command.BACK_R_FRONT_JUMP3,
        Command.FRONT_JUMP7_POT_UP   if potled_overlap else Command.BACK_G_FRONT_JUMP7,
        Command.FRONT_FADE3_POT_OFF  if potled_overlap else Command.BACK_B_FRONT_FADE3,
        Command.FRONT_FADE7_POT_ON   if potled_overlap else Command.BACK_W_FRONT_FADE7
    ][mode]

POTLED_MODES = [
    "potled r", "potled r2", "potled r3", "potled r4", "potled r5",
    "potled g", "potled g2", "potled g3", "potled g4", "potled g5",
    "potled b", "potled b2", "potled b3", "potled b4", "potled b5",
    "potled w",
    "potled smooth",
    "potled fade",
    "potled strobe",
    "potled flash",
]
POTLED_COLOR_MODES = [i for i in range(16)]

def potled_get_command_for(mode: int) -> Command:
    return [
        Command.FRONT_DIY5_POT_R,
        Command.FRONT_DIY2_POT_R2,
        Command.FRONT_GUP_POT_R3,
        Command.FRONT_G5_POT_R4,
        Command.FRONT_GDOWN_POT_R5,
        Command.FRONT_DIY4_POT_G,
        Command.FRONT_DIY1_POT_G2,
        Command.FRONT_RUP_POT_G3,
        Command.FRONT_R5_POT_G4,
        Command.FRONT_RDOWN_POT_G5,
        Command.FRONT_DIY6_POT_B,
        Command.FRONT_DIY3_POT_B2,
        Command.FRONT_BUP_POT_B3,
        Command.FRONT_B5_POT_B4,
        Command.FRONT_BDOWN_POT_B5,
        Command.FRONT_FLASH_POT_W,
        Command.FRONT_SLOW_POT_SMOOTH,
        Command.FRONT_W5_POT_FADE,
        Command.FRONT_QUICK_POT_STROBE,
        Command.FRONT_AUTO_POT_FLASH
    ][mode]

pos = 1
pos = (BACKLED_ON              := pos) * (BACKLED_ON_LENGTH  := 2)  # on/off
pos = (FRONTLED_ON             := pos) * (FRONTLED_ON_LENGTH := 2)  # on/off
pos = (POTLED_ON               := pos) * (POTLED_ON_LENGTH   := 2)  # on/off
pos = (FRONTLED_PAUSED         := pos) * (FRONTLED_PAUSED_LENGTH := 2)  # unpaused/paused
pos = (BACKLED_MODE            := pos) * (BACKLED_MODE_LENGTH  := len(BACKLED_MODES))   # index in BACKLED_MODES
pos = (FRONTLED_MODE           := pos) * (FRONTLED_MODE_LENGTH := len(FRONTLED_MODES))  # index in FRONTLED_MODES
pos = (POTLED_MODE             := pos) * (POTLED_MODE_LENGTH   := len(POTLED_MODES))    # index in POTLED_MODES
pos = (BACKLED_REL_BRIGHTNESS  := pos) * (BACKLED_REL_BRIGHTNESS_LENGTH  := 3)  # 0, 1 or 2
pos = (FRONTLED_REL_BRIGHTNESS := pos) * (FRONTLED_REL_BRIGHTNESS_LENGTH := 3)  # 0, 1 or 2
pos = (POTLED_REL_BRIGHTNESS   := pos) * (POTLED_REL_BRIGHTNESS_LENGTH   := 3)  # 0, 1 or 2
pos = (BACKLED_REL_SPEED       := pos) * (BACKLED_REL_SPEED_LENGTH  := 3)  # 0, 1 or 2
pos = (FRONTLED_REL_SPEED      := pos) * (FRONTLED_REL_SPEED_LENGTH := 3)  # 0, 1 or 2
pos = (POTLED_REL_SPEED        := pos) * (POTLED_REL_SPEED_LENGTH   := 3)  # 0, 1 or 2
pos = (FRONTLED_DIY1_REL_RGB   := pos) * (FRONTLED_DIY1_REL_RGB_LENGTH := 27)  # 0, 1 or 2 channelwise
pos = (FRONTLED_DIY2_REL_RGB   := pos) * (FRONTLED_DIY2_REL_RGB_LENGTH := 27)  # 0, 1 or 2 channelwise
pos = (FRONTLED_DIY3_REL_RGB   := pos) * (FRONTLED_DIY3_REL_RGB_LENGTH := 27)  # 0, 1 or 2 channelwise
pos = (FRONTLED_DIY4_REL_RGB   := pos) * (FRONTLED_DIY4_REL_RGB_LENGTH := 27)  # 0, 1 or 2 channelwise
pos = (FRONTLED_DIY5_REL_RGB   := pos) * (FRONTLED_DIY5_REL_RGB_LENGTH := 27)  # 0, 1 or 2 channelwise
pos = (FRONTLED_DIY6_REL_RGB   := pos) * (FRONTLED_DIY6_REL_RGB_LENGTH := 27)  # 0, 1 or 2 channelwise
pos = (FRONTLED_CALIBRATION    := pos) * (FRONTLED_CALIBRATION_LENGTH := 6)  # 6 states of calibration
STATE_MAX_SIZE = pos - 1

# This through encode_state essentially constructs the graph vertices, for edges see perform_command
@dataclasses.dataclass
class State:
    backled_on: int = 1   # 0 = off, 1 = on
    frontled_on: int = 1  # 0 = off, 1 = on
    potled_on: int = 1    # 0 = off, 1 = on
    frontled_paused: int = 0  # 0 = unpaused, 1 = paused
    backled_mode: int = 0   # index in BACKLED_MODES
    frontled_mode: int = 0  # index in FRONTLED_MODES
    potled_mode: int = 0    # index in POTLED_MODES
    backled_rel_brightness: int = 0   # 0 = no change, 1 = increase, 2 = decrease
    frontled_rel_brightness: int = 0  # 0 = no change, 1 = increase, 2 = decrease
    potled_rel_brightness: int = 0    # 0 = no change, 1 = increase, 2 = decrease
    backled_rel_speed: int = 0   # 0 = no change, 1 = increase, 2 = decrease
    frontled_rel_speed: int = 0  # 0 = no change, 1 = increase, 2 = decrease
    potled_rel_speed: int = 0    # 0 = no change, 1 = increase, 2 = decrease
    frontled_diy1_rel_rgb: int = 0  # Channelwise 0 = no change, 1 = increase, 2 = decrease
    frontled_diy2_rel_rgb: int = 0  # Channelwise 0 = no change, 1 = increase, 2 = decrease
    frontled_diy3_rel_rgb: int = 0  # Channelwise 0 = no change, 1 = increase, 2 = decrease
    frontled_diy4_rel_rgb: int = 0  # Channelwise 0 = no change, 1 = increase, 2 = decrease
    frontled_diy5_rel_rgb: int = 0  # Channelwise 0 = no change, 1 = increase, 2 = decrease
    frontled_diy6_rel_rgb: int = 0  # Channelwise 0 = no change, 1 = increase, 2 = decrease
    frontled_calibration: int = 0  # 6 states of calibration
    potled_calibration: int = 0    # 1 = calibration requested

def encode_state(state: State) -> int:
    return BACKLED_ON * state.backled_on \
         + FRONTLED_ON * state.frontled_on \
         + POTLED_ON * state.potled_on \
         + FRONTLED_PAUSED * state.frontled_paused \
         + BACKLED_MODE * state.backled_mode \
         + FRONTLED_MODE * state.frontled_mode \
         + POTLED_MODE * state.potled_mode \
         + BACKLED_REL_BRIGHTNESS * state.backled_rel_brightness \
         + FRONTLED_REL_BRIGHTNESS * state.frontled_rel_brightness \
         + POTLED_REL_BRIGHTNESS * state.potled_rel_brightness \
         + BACKLED_REL_SPEED * state.backled_rel_speed \
         + FRONTLED_REL_SPEED * state.frontled_rel_speed \
         + POTLED_REL_SPEED * state.potled_rel_speed \
         + FRONTLED_DIY1_REL_RGB * state.frontled_diy1_rel_rgb \
         + FRONTLED_DIY2_REL_RGB * state.frontled_diy2_rel_rgb \
         + FRONTLED_DIY3_REL_RGB * state.frontled_diy3_rel_rgb \
         + FRONTLED_DIY4_REL_RGB * state.frontled_diy4_rel_rgb \
         + FRONTLED_DIY5_REL_RGB * state.frontled_diy5_rel_rgb \
         + FRONTLED_DIY6_REL_RGB * state.frontled_diy6_rel_rgb \
         + FRONTLED_CALIBRATION * state.frontled_calibration \
         
def decode_state(encoded: int) -> State:
    state = State()
    encoded, state.backled_on  = divmod(encoded, BACKLED_ON_LENGTH)
    encoded, state.frontled_on = divmod(encoded, FRONTLED_ON_LENGTH)
    encoded, state.potled_on   = divmod(encoded, POTLED_ON_LENGTH)
    encoded, state.frontled_paused = divmod(encoded, FRONTLED_PAUSED_LENGTH)
    encoded, state.backled_mode  = divmod(encoded, BACKLED_MODE_LENGTH)
    encoded, state.frontled_mode = divmod(encoded, FRONTLED_MODE_LENGTH)
    encoded, state.potled_mode   = divmod(encoded, POTLED_MODE_LENGTH)
    encoded, state.backled_rel_brightness  = divmod(encoded, BACKLED_REL_BRIGHTNESS_LENGTH)
    encoded, state.frontled_rel_brightness = divmod(encoded, FRONTLED_REL_BRIGHTNESS_LENGTH)
    encoded, state.potled_rel_brightness   = divmod(encoded, POTLED_REL_BRIGHTNESS_LENGTH)
    encoded, state.backled_rel_speed  = divmod(encoded, BACKLED_REL_SPEED_LENGTH)
    encoded, state.frontled_rel_speed = divmod(encoded, FRONTLED_REL_SPEED_LENGTH)
    encoded, state.potled_rel_speed   = divmod(encoded, POTLED_REL_SPEED_LENGTH)
    encoded, state.frontled_diy1_rel_rgb = divmod(encoded, FRONTLED_DIY1_REL_RGB_LENGTH)
    encoded, state.frontled_diy2_rel_rgb = divmod(encoded, FRONTLED_DIY2_REL_RGB_LENGTH)
    encoded, state.frontled_diy3_rel_rgb = divmod(encoded, FRONTLED_DIY3_REL_RGB_LENGTH)
    encoded, state.frontled_diy4_rel_rgb = divmod(encoded, FRONTLED_DIY4_REL_RGB_LENGTH)
    encoded, state.frontled_diy5_rel_rgb = divmod(encoded, FRONTLED_DIY5_REL_RGB_LENGTH)
    encoded, state.frontled_diy6_rel_rgb = divmod(encoded, FRONTLED_DIY6_REL_RGB_LENGTH)
    encoded, state.frontled_calibration = divmod(encoded, FRONTLED_CALIBRATION_LENGTH)
    return state

def is_state_setting_effective(state: State, setting: str) -> bool:
    match setting:
        case "backled off":
            return state.backled_on == 1
        case "backled on":
            return state.backled_on == 0
        case "frontled off":
            return state.frontled_on == 1
        case "frontled on":
            return state.frontled_on == 0
        case "potled off":
            return state.potled_on == 1
        case "potled on":
            return state.potled_on == 0
        case "frontled slow" | "frontled quick":
            return state.frontled_on == 1 and state.frontled_mode not in FRONTLED_COLOR_MODES
        case "frontled dim" | "frontled bright":
            return state.frontled_on == 1 and state.frontled_mode in FRONTLED_COLOR_MODES
        case "backled slow" | "backled quick":
            return state.backled_on == 1 and state.backled_mode not in BACKLED_COLOR_MODES
        case "backled dim" | "backled bright":
            return state.backled_on == 1 and state.backled_mode in BACKLED_COLOR_MODES
        case "potled slow" | "potled quick":
            return state.potled_on == 1 and state.potled_mode not in POTLED_COLOR_MODES
        case "potled dim" | "potled bright":
            return state.potled_on == 1 and state.potled_mode in POTLED_COLOR_MODES
        case "frontled diy1 rup" | "frontled diy1 rdown" | "frontled diy1 gup" | "frontled diy1 gdown" | "frontled diy1 bup" | "frontled diy1 bdown":
            return state.frontled_on == 1 and state.frontled_mode == 20
        case "frontled diy2 rup" | "frontled diy2 rdown" | "frontled diy2 gup" | "frontled diy2 gdown" | "frontled diy2 bup" | "frontled diy2 bdown":
            return state.frontled_on == 1 and state.frontled_mode == 21
        case "frontled diy3 rup" | "frontled diy3 rdown" | "frontled diy3 gup" | "frontled diy3 gdown" | "frontled diy3 bup" | "frontled diy3 bdown":
            return state.frontled_on == 1 and state.frontled_mode == 22
        case "frontled diy4 rup" | "frontled diy4 rdown" | "frontled diy4 gup" | "frontled diy4 gdown" | "frontled diy4 bup" | "frontled diy4 bdown":
            return state.frontled_on == 1 and state.frontled_mode == 23
        case "frontled diy5 rup" | "frontled diy5 rdown" | "frontled diy5 gup" | "frontled diy5 gdown" | "frontled diy5 bup" | "frontled diy5 bdown":
            return state.frontled_on == 1 and state.frontled_mode == 24
        case "frontled diy6 rup" | "frontled diy6 rdown" | "frontled diy6 gup" | "frontled diy6 gdown" | "frontled diy6 bup" | "frontled diy6 bdown":
            return state.frontled_on == 1 and state.frontled_mode == 25
        case "frontled calibrate":
            return state.frontled_on == 1
        case "potled calibrate":
            return state.potled_on == 1
    if setting in BACKLED_MODES:
        return state.backled_on == 1
    if setting in FRONTLED_MODES:
        return state.frontled_on == 1
    if setting in POTLED_MODES:
        return state.potled_on == 1
    return False

def read_state(initial_state: State, given_state: list[str]) -> State:
    state = dataclasses.replace(initial_state)

    if "backled off" in given_state:
        state.backled_on = 0
    if "backled on" in given_state:
        state.backled_on = 1
    if "frontled off" in given_state:
        state.frontled_on = 0
    if "frontled on" in given_state:
        state.frontled_on = 1
    if "potled off" in given_state:
        state.potled_on = 0
    if "potled on" in given_state:
        state.potled_on = 1
    if "frontled unpaused" in given_state:
        state.frontled_paused = 0
    if "frontled paused" in given_state:
        state.frontled_paused = 1

    for device_state in given_state:
        if device_state in BACKLED_MODES:
            state.backled_mode  = BACKLED_MODES.index(device_state)
        if device_state in FRONTLED_MODES:
            state.frontled_mode = FRONTLED_MODES.index(device_state)
        if device_state in POTLED_MODES:
            state.potled_mode   = POTLED_MODES.index(device_state)
    
    if "backled bright" in given_state:
        state.backled_rel_brightness = 1
    if "backled dim" in given_state:
        state.backled_rel_brightness = 2
    if "frontled bright" in given_state:
        state.frontled_rel_brightness = 1
    if "frontled dim" in given_state:
        state.frontled_rel_brightness = 2
    if "potled bright" in given_state:
        state.potled_rel_brightness = 1
    if "potled dim" in given_state:
        state.potled_rel_brightness = 2
    
    if "backled quick" in given_state:
        state.backled_rel_speed = 1
    if "backled slow" in given_state:
        state.backled_rel_speed = 2
    if "frontled quick" in given_state:
        state.frontled_rel_speed = 1
    if "frontled slow" in given_state:
        state.frontled_rel_speed = 2
    if "potled quick" in given_state:
        state.potled_rel_speed = 1
    if "potled slow" in given_state:
        state.potled_rel_speed = 2

    for i, attr in enumerate(['frontled_diy1_rel_rgb', 'frontled_diy2_rel_rgb', 'frontled_diy3_rel_rgb',
                             'frontled_diy4_rel_rgb', 'frontled_diy5_rel_rgb', 'frontled_diy6_rel_rgb']):
        if "frontled diy{} rup".format(i+1) in given_state:
            setattr(state, attr, getattr(state, attr) + 1)
        if "frontled diy{} rdown".format(i+1) in given_state:
            setattr(state, attr, getattr(state, attr) + 2)
        if "frontled diy{} gup".format(i+1) in given_state:
            setattr(state, attr, getattr(state, attr) + 3 * 1)
        if "frontled diy{} gdown".format(i+1) in given_state:
            setattr(state, attr, getattr(state, attr) + 3 * 2)
        if "frontled diy{} bup".format(i+1) in given_state:
            setattr(state, attr, getattr(state, attr) + 3*3 * 1)
        if "frontled diy{} bdown".format(i+1) in given_state:
            setattr(state, attr, getattr(state, attr) + 3*3 * 2)

    if "frontled calibrate" in given_state:
        state.frontled_calibration = 1

    if "potled calibrate" in given_state:
        state.potled_calibration = 1

    return state

def set_r(encoded, trit):
    return encoded - get_r(encoded) + trit

def get_r(encoded):
    return encoded % 3

def set_g(encoded, trit):
    return encoded - get_g(encoded)*3 + trit*3

def get_g(encoded):
    return (encoded // 3) % 3

def set_b(encoded, trit):
    return encoded - get_b(encoded)*9 + trit*9

def get_b(encoded):
    return encoded // 9

# This essentially constructs the graph edges, for vertices see State and encode_state
def perform_command(old_state: State, command: Command) -> State:
    new_state = dataclasses.replace(old_state)

    match command:
        case Command.FRONT_ONOFF:
            new_state.frontled_on = 1 - old_state.frontled_on
            new_state.frontled_paused = 0

        case Command.FRONT_PLAYPAUSE:
            if old_state.frontled_on == 1:
                new_state.frontled_paused = 1 - old_state.frontled_paused

        case Command.FRONT_DIM:
            if old_state.frontled_on == 1:
                if old_state.frontled_mode in FRONTLED_COLOR_MODES:
                    if new_state.frontled_rel_brightness == 2:
                        return old_state # this is a forbidden move
                    if new_state.frontled_rel_brightness == 0:
                        new_state.frontled_rel_brightness = 2
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_rel_brightness = 0

        case Command.FRONT_BRIGHTEN:
           if old_state.frontled_on == 1:
               if old_state.frontled_mode in FRONTLED_COLOR_MODES:
                    if new_state.frontled_rel_brightness == 1:
                        return old_state # this is a forbidden move
                    if new_state.frontled_rel_brightness == 0:
                        new_state.frontled_rel_brightness = 1
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_rel_brightness = 0

        case Command.FRONT_R:
            if old_state.frontled_on == 1:
                new_state.frontled_mode = 0

        case Command.FRONT_G:
            if old_state.frontled_on == 1:
                new_state.frontled_mode = 5

        case Command.FRONT_B:
            if old_state.frontled_on == 1:
                new_state.frontled_mode = 10

        case Command.FRONT_W:
            if old_state.frontled_on == 1:
                new_state.frontled_mode = 15

        case Command.FRONT_W2:
            if old_state.frontled_on == 1:
                new_state.frontled_mode = 16

        case Command.FRONT_W3:
            if old_state.frontled_on == 1:
                new_state.frontled_mode = 17

        case Command.FRONT_W4:
            if old_state.frontled_on == 1:
                new_state.frontled_mode = 18

        case Command.FRONT_W5_POT_FADE:
            if old_state.frontled_on == 1:
                new_state.frontled_mode = 19
            if old_state.potled_on == 1:
                new_state.potled_mode = 17

        case Command.FRONT_B2:
            if old_state.frontled_on == 1:
                new_state.frontled_mode = 11

        case Command.FRONT_B3:
            if old_state.frontled_on == 1:
                new_state.frontled_mode = 12

        case Command.FRONT_B4:
            if old_state.frontled_on == 1:
                new_state.frontled_mode = 13

        case Command.FRONT_B5_POT_B4:
            if old_state.frontled_on == 1:
                new_state.frontled_mode = 14
            if old_state.potled_on == 1:
                new_state.potled_mode = 13

        case Command.FRONT_G2:
            if old_state.frontled_on == 1:
                new_state.frontled_mode = 6

        case Command.FRONT_G3:
            if old_state.frontled_on == 1:
                new_state.frontled_mode = 7

        case Command.FRONT_G4:
            if old_state.frontled_on == 1:
                new_state.frontled_mode = 8

        case Command.FRONT_G5_POT_R4:
            if old_state.frontled_on == 1:
                new_state.frontled_mode = 9
            if old_state.potled_on == 1:
                new_state.potled_mode = 3

        case Command.FRONT_R2:
            if old_state.frontled_on == 1:
                new_state.frontled_mode = 1

        case Command.FRONT_R3:
            if old_state.frontled_on == 1:
                new_state.frontled_mode = 2

        case Command.FRONT_R4:
            if old_state.frontled_on == 1:
                new_state.frontled_mode = 3

        case Command.FRONT_R5_POT_G4:
            if old_state.frontled_on == 1:
                new_state.frontled_mode = 4
            if old_state.potled_on == 1:
                new_state.potled_mode = 8
                
        case Command.FRONT_RUP_POT_G3 | Command.BACK_R5_FRONT_RUP:
            if command == Command.FRONT_RUP_POT_G3 and old_state.potled_on == 1:
                new_state.potled_mode = 7
            if command == Command.BACK_R5_FRONT_RUP and old_state.backled_on == 1:
                new_state.backled_mode = 4

            if old_state.frontled_on == 1:
                if old_state.frontled_mode == 20:
                    if get_r(old_state.frontled_diy1_rel_rgb) == 1:
                        return old_state # this is a forbidden move
                    if get_r(old_state.frontled_diy1_rel_rgb) == 0:
                        new_state.frontled_diy1_rel_rgb = set_r(new_state.frontled_diy1_rel_rgb, 1)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy1_rel_rgb = set_r(new_state.frontled_diy1_rel_rgb, 0)
                if old_state.frontled_mode == 21:
                    if get_r(old_state.frontled_diy2_rel_rgb) == 1:
                        return old_state # this is a forbidden move
                    if get_r(old_state.frontled_diy2_rel_rgb) == 0:
                        new_state.frontled_diy2_rel_rgb = set_r(new_state.frontled_diy2_rel_rgb, 1)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy2_rel_rgb = set_r(new_state.frontled_diy2_rel_rgb, 0)
                if old_state.frontled_mode == 22:
                    if get_r(old_state.frontled_diy3_rel_rgb) == 1:
                        return old_state # this is a forbidden move
                    if get_r(old_state.frontled_diy3_rel_rgb) == 0:
                        new_state.frontled_diy3_rel_rgb = set_r(new_state.frontled_diy3_rel_rgb, 1)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy3_rel_rgb = set_r(new_state.frontled_diy3_rel_rgb, 0)
                if old_state.frontled_mode == 23:
                    if get_r(old_state.frontled_diy4_rel_rgb) == 1:
                        return old_state # this is a forbidden move
                    if get_r(old_state.frontled_diy4_rel_rgb) == 0:
                        new_state.frontled_diy4_rel_rgb = set_r(new_state.frontled_diy4_rel_rgb, 1)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy4_rel_rgb = set_r(new_state.frontled_diy4_rel_rgb, 0)
                if old_state.frontled_mode == 24:
                    if get_r(old_state.frontled_diy5_rel_rgb) == 1:
                        return old_state # this is a forbidden move
                    if get_r(old_state.frontled_diy5_rel_rgb) == 0:
                        new_state.frontled_diy5_rel_rgb = set_r(new_state.frontled_diy5_rel_rgb, 1)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy5_rel_rgb = set_r(new_state.frontled_diy5_rel_rgb, 0)
                if old_state.frontled_mode == 25:
                    if get_r(old_state.frontled_diy6_rel_rgb) == 1:
                        return old_state # this is a forbidden move
                    if get_r(old_state.frontled_diy6_rel_rgb) == 0:
                        new_state.frontled_diy6_rel_rgb = set_r(new_state.frontled_diy6_rel_rgb, 1)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy6_rel_rgb = set_r(new_state.frontled_diy6_rel_rgb, 0)

        case Command.FRONT_RDOWN_POT_G5 | Command.BACK_R4_FRONT_RDOWN:
            if command == Command.FRONT_RDOWN_POT_G5 and old_state.potled_on == 1:
                new_state.potled_mode = 9
            if command == Command.BACK_R4_FRONT_RDOWN and old_state.backled_on == 1:
                new_state.backled_mode = 3

            if old_state.frontled_on == 1:
                if old_state.frontled_mode == 20:
                    if get_r(old_state.frontled_diy1_rel_rgb) == 2:
                        return old_state # this is a forbidden move
                    if get_r(old_state.frontled_diy1_rel_rgb) == 0:
                        new_state.frontled_diy1_rel_rgb = set_r(new_state.frontled_diy1_rel_rgb, 2)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy1_rel_rgb = set_r(new_state.frontled_diy1_rel_rgb, 0)
                if old_state.frontled_mode == 21:
                    if get_r(old_state.frontled_diy2_rel_rgb) == 2:
                        return old_state # this is a forbidden move
                    if get_r(old_state.frontled_diy2_rel_rgb) == 0:
                        new_state.frontled_diy2_rel_rgb = set_r(new_state.frontled_diy2_rel_rgb, 2)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy2_rel_rgb = set_r(new_state.frontled_diy2_rel_rgb, 0)
                if old_state.frontled_mode == 22:
                    if get_r(old_state.frontled_diy3_rel_rgb) == 2:
                        return old_state # this is a forbidden move
                    if get_r(old_state.frontled_diy3_rel_rgb) == 0:
                        new_state.frontled_diy3_rel_rgb = set_r(new_state.frontled_diy3_rel_rgb, 2)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy3_rel_rgb = set_r(new_state.frontled_diy3_rel_rgb, 0)
                if old_state.frontled_mode == 23:
                    if get_r(old_state.frontled_diy4_rel_rgb) == 2:
                        return old_state # this is a forbidden move
                    if get_r(old_state.frontled_diy4_rel_rgb) == 0:
                        new_state.frontled_diy4_rel_rgb = set_r(new_state.frontled_diy4_rel_rgb, 2)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy4_rel_rgb = set_r(new_state.frontled_diy4_rel_rgb, 0)
                if old_state.frontled_mode == 24:
                    if get_r(old_state.frontled_diy5_rel_rgb) == 2:
                        return old_state # this is a forbidden move
                    if get_r(old_state.frontled_diy5_rel_rgb) == 0:
                        new_state.frontled_diy5_rel_rgb = set_r(new_state.frontled_diy5_rel_rgb, 2)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy5_rel_rgb = set_r(new_state.frontled_diy5_rel_rgb, 0)
                if old_state.frontled_mode == 25:
                    if get_r(old_state.frontled_diy6_rel_rgb) == 2:
                        return old_state # this is a forbidden move
                    if get_r(old_state.frontled_diy6_rel_rgb) == 0:
                        new_state.frontled_diy6_rel_rgb = set_r(new_state.frontled_diy6_rel_rgb, 2)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy6_rel_rgb = set_r(new_state.frontled_diy6_rel_rgb, 0)

        case Command.FRONT_GUP_POT_R3 | Command.BACK_G5_FRONT_GUP:
            if command == Command.FRONT_GUP_POT_R3 and old_state.potled_on == 1:
                new_state.potled_mode = 2
            if command == Command.BACK_G5_FRONT_GUP and old_state.backled_on == 1:
                new_state.backled_mode = 9

            if old_state.frontled_on == 1:
                if old_state.frontled_mode == 20:
                    if get_g(old_state.frontled_diy1_rel_rgb) == 1:
                        return old_state # this is a forbidden move
                    if get_g(old_state.frontled_diy1_rel_rgb) == 0:
                        new_state.frontled_diy1_rel_rgb = set_g(new_state.frontled_diy1_rel_rgb, 1)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy1_rel_rgb = set_g(new_state.frontled_diy1_rel_rgb, 0)
                if old_state.frontled_mode == 21:
                    if get_g(old_state.frontled_diy2_rel_rgb) == 1:
                        return old_state # this is a forbidden move
                    if get_g(old_state.frontled_diy2_rel_rgb) == 0:
                        new_state.frontled_diy2_rel_rgb = set_g(new_state.frontled_diy2_rel_rgb, 1)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy2_rel_rgb = set_g(new_state.frontled_diy2_rel_rgb, 0)
                if old_state.frontled_mode == 22:
                    if get_g(old_state.frontled_diy3_rel_rgb) == 1:
                        return old_state # this is a forbidden move
                    if get_g(old_state.frontled_diy3_rel_rgb) == 0:
                        new_state.frontled_diy3_rel_rgb = set_g(new_state.frontled_diy3_rel_rgb, 1)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy3_rel_rgb = set_g(new_state.frontled_diy3_rel_rgb, 0)
                if old_state.frontled_mode == 23:
                    if get_g(old_state.frontled_diy4_rel_rgb) == 1:
                        return old_state # this is a forbidden move
                    if get_g(old_state.frontled_diy4_rel_rgb) == 0:
                        new_state.frontled_diy4_rel_rgb = set_g(new_state.frontled_diy4_rel_rgb, 1)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy4_rel_rgb = set_g(new_state.frontled_diy4_rel_rgb, 0)
                if old_state.frontled_mode == 24:
                    if get_g(old_state.frontled_diy5_rel_rgb) == 1:
                        return old_state # this is a forbidden move
                    if get_g(old_state.frontled_diy5_rel_rgb) == 0:
                        new_state.frontled_diy5_rel_rgb = set_g(new_state.frontled_diy5_rel_rgb, 1)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy5_rel_rgb = set_g(new_state.frontled_diy5_rel_rgb, 0)
                if old_state.frontled_mode == 25:
                    if get_g(old_state.frontled_diy6_rel_rgb) == 1:
                        return old_state # this is a forbidden move
                    if get_g(old_state.frontled_diy6_rel_rgb) == 0:
                        new_state.frontled_diy6_rel_rgb = set_g(new_state.frontled_diy6_rel_rgb, 1)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy6_rel_rgb = set_g(new_state.frontled_diy6_rel_rgb, 0)

        case Command.FRONT_GDOWN_POT_R5 | Command.BACK_G4_FRONT_GDOWN:
            if command == Command.FRONT_GDOWN_POT_R5 and old_state.potled_on == 1:
                new_state.potled_mode = 4
            if command == Command.BACK_G4_FRONT_GDOWN and old_state.backled_on == 1:
                new_state.backled_mode = 8

            if old_state.frontled_on == 1:
                if old_state.frontled_mode == 20:
                    if get_g(old_state.frontled_diy1_rel_rgb) == 2:
                        return old_state # this is a forbidden move
                    if get_g(old_state.frontled_diy1_rel_rgb) == 0:
                        new_state.frontled_diy1_rel_rgb = set_g(new_state.frontled_diy1_rel_rgb, 2)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy1_rel_rgb = set_g(new_state.frontled_diy1_rel_rgb, 0)
                if old_state.frontled_mode == 21:
                    if get_g(old_state.frontled_diy2_rel_rgb) == 2:
                        return old_state # this is a forbidden move
                    if get_g(old_state.frontled_diy2_rel_rgb) == 0:
                        new_state.frontled_diy2_rel_rgb = set_g(new_state.frontled_diy2_rel_rgb, 2)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy2_rel_rgb = set_g(new_state.frontled_diy2_rel_rgb, 0)
                if old_state.frontled_mode == 22:
                    if get_g(old_state.frontled_diy3_rel_rgb) == 2:
                        return old_state # this is a forbidden move
                    if get_g(old_state.frontled_diy3_rel_rgb) == 0:
                        new_state.frontled_diy3_rel_rgb = set_g(new_state.frontled_diy3_rel_rgb, 2)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy3_rel_rgb = set_g(new_state.frontled_diy3_rel_rgb, 0)
                if old_state.frontled_mode == 23:
                    if get_g(old_state.frontled_diy4_rel_rgb) == 2:
                        return old_state # this is a forbidden move
                    if get_g(old_state.frontled_diy4_rel_rgb) == 0:
                        new_state.frontled_diy4_rel_rgb = set_g(new_state.frontled_diy4_rel_rgb, 2)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy4_rel_rgb = set_g(new_state.frontled_diy4_rel_rgb, 0)
                if old_state.frontled_mode == 24:
                    if get_g(old_state.frontled_diy5_rel_rgb) == 2:
                        return old_state # this is a forbidden move
                    if get_g(old_state.frontled_diy5_rel_rgb) == 0:
                        new_state.frontled_diy5_rel_rgb = set_g(new_state.frontled_diy5_rel_rgb, 2)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy5_rel_rgb = set_g(new_state.frontled_diy5_rel_rgb, 0)
                if old_state.frontled_mode == 25:
                    if get_g(old_state.frontled_diy6_rel_rgb) == 2:
                        return old_state # this is a forbidden move
                    if get_g(old_state.frontled_diy6_rel_rgb) == 0:
                        new_state.frontled_diy6_rel_rgb = set_g(new_state.frontled_diy6_rel_rgb, 2)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy6_rel_rgb = set_g(new_state.frontled_diy6_rel_rgb, 0)

        case Command.FRONT_BUP_POT_B3 | Command.BACK_B5_FRONT_BUP:
            if command == Command.FRONT_BUP_POT_B3 and old_state.potled_on == 1:
                new_state.potled_mode = 12
            if command == Command.BACK_B5_FRONT_BUP and old_state.backled_on == 1:
                new_state.backled_mode = 14

            if old_state.frontled_on == 1:
                if old_state.frontled_mode == 20:
                    if get_b(old_state.frontled_diy1_rel_rgb) == 1:
                        return old_state # this is a forbidden move
                    if get_b(old_state.frontled_diy1_rel_rgb) == 0:
                        new_state.frontled_diy1_rel_rgb = set_b(new_state.frontled_diy1_rel_rgb, 1)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy1_rel_rgb = set_b(new_state.frontled_diy1_rel_rgb, 0)
                if old_state.frontled_mode == 21:
                    if get_b(old_state.frontled_diy2_rel_rgb) == 1:
                        return old_state # this is a forbidden move
                    if get_b(old_state.frontled_diy2_rel_rgb) == 0:
                        new_state.frontled_diy2_rel_rgb = set_b(new_state.frontled_diy2_rel_rgb, 1)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy2_rel_rgb = set_b(new_state.frontled_diy2_rel_rgb, 0)
                if old_state.frontled_mode == 22:
                    if get_b(old_state.frontled_diy3_rel_rgb) == 1:
                        return old_state # this is a forbidden move
                    if get_b(old_state.frontled_diy3_rel_rgb) == 0:
                        new_state.frontled_diy3_rel_rgb = set_b(new_state.frontled_diy3_rel_rgb, 1)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy3_rel_rgb = set_b(new_state.frontled_diy3_rel_rgb, 0)
                if old_state.frontled_mode == 23:
                    if get_b(old_state.frontled_diy4_rel_rgb) == 1:
                        return old_state # this is a forbidden move
                    if get_b(old_state.frontled_diy4_rel_rgb) == 0:
                        new_state.frontled_diy4_rel_rgb = set_b(new_state.frontled_diy4_rel_rgb, 1)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy4_rel_rgb = set_b(new_state.frontled_diy4_rel_rgb, 0)
                if old_state.frontled_mode == 24:
                    if get_b(old_state.frontled_diy5_rel_rgb) == 1:
                        return old_state # this is a forbidden move
                    if get_b(old_state.frontled_diy5_rel_rgb) == 0:
                        new_state.frontled_diy5_rel_rgb = set_b(new_state.frontled_diy5_rel_rgb, 1)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy5_rel_rgb = set_b(new_state.frontled_diy5_rel_rgb, 0)
                if old_state.frontled_mode == 25:
                    if get_b(old_state.frontled_diy6_rel_rgb) == 1:
                        return old_state # this is a forbidden move
                    if get_b(old_state.frontled_diy6_rel_rgb) == 0:
                        new_state.frontled_diy6_rel_rgb = set_b(new_state.frontled_diy6_rel_rgb, 1)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy6_rel_rgb = set_b(new_state.frontled_diy6_rel_rgb, 0)

        case Command.FRONT_BDOWN_POT_B5 | Command.BACK_B4_FRONT_BDOWN:
            if command == Command.FRONT_BDOWN_POT_B5 and old_state.potled_on == 1:
                new_state.potled_mode = 14
            if command == Command.BACK_B4_FRONT_BDOWN and old_state.backled_on == 1:
                new_state.backled_mode = 13

            if old_state.frontled_on == 1:
                if old_state.frontled_mode == 20:
                    if get_b(old_state.frontled_diy1_rel_rgb) == 2:
                        return old_state # this is a forbidden move
                    if get_b(old_state.frontled_diy1_rel_rgb) == 0:
                        new_state.frontled_diy1_rel_rgb = set_b(new_state.frontled_diy1_rel_rgb, 2)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy1_rel_rgb = set_b(new_state.frontled_diy1_rel_rgb, 0)
                if old_state.frontled_mode == 21:
                    if get_b(old_state.frontled_diy2_rel_rgb) == 2:
                        return old_state # this is a forbidden move
                    if get_b(old_state.frontled_diy2_rel_rgb) == 0:
                        new_state.frontled_diy2_rel_rgb = set_b(new_state.frontled_diy2_rel_rgb, 2)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy2_rel_rgb = set_b(new_state.frontled_diy2_rel_rgb, 0)
                if old_state.frontled_mode == 22:
                    if get_b(old_state.frontled_diy3_rel_rgb) == 2:
                        return old_state # this is a forbidden move
                    if get_b(old_state.frontled_diy3_rel_rgb) == 0:
                        new_state.frontled_diy3_rel_rgb = set_b(new_state.frontled_diy3_rel_rgb, 2)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy3_rel_rgb = set_b(new_state.frontled_diy3_rel_rgb, 0)
                if old_state.frontled_mode == 23:
                    if get_b(old_state.frontled_diy4_rel_rgb) == 2:
                        return old_state # this is a forbidden move
                    if get_b(old_state.frontled_diy4_rel_rgb) == 0:
                        new_state.frontled_diy4_rel_rgb = set_b(new_state.frontled_diy4_rel_rgb, 2)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy4_rel_rgb = set_b(new_state.frontled_diy4_rel_rgb, 0)
                if old_state.frontled_mode == 24:
                    if get_b(old_state.frontled_diy5_rel_rgb) == 2:
                        return old_state # this is a forbidden move
                    if get_b(old_state.frontled_diy5_rel_rgb) == 0:
                        new_state.frontled_diy5_rel_rgb = set_b(new_state.frontled_diy5_rel_rgb, 2)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy5_rel_rgb = set_b(new_state.frontled_diy5_rel_rgb, 0)
                if old_state.frontled_mode == 25:
                    if get_b(old_state.frontled_diy6_rel_rgb) == 2:
                        return old_state # this is a forbidden move
                    if get_b(old_state.frontled_diy6_rel_rgb) == 0:
                        new_state.frontled_diy6_rel_rgb = set_b(new_state.frontled_diy6_rel_rgb, 2)
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_diy6_rel_rgb = set_b(new_state.frontled_diy6_rel_rgb, 0)

        case Command.FRONT_QUICK_POT_STROBE | Command.BACK_SMOOTH_FRONT_QUICK:
            if command == Command.FRONT_QUICK_POT_STROBE and old_state.potled_on == 1:
                new_state.potled_mode = 18
            if command == Command.BACK_SMOOTH_FRONT_QUICK and old_state.backled_on == 1:
                new_state.backled_mode = 16
            
            if old_state.frontled_on == 1:
                if old_state.frontled_mode not in FRONTLED_COLOR_MODES:
                    if old_state.frontled_rel_speed == 1:
                        return old_state # this is a forbidden move
                    if old_state.frontled_rel_speed == 0:
                        new_state.frontled_rel_speed = 1
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_rel_speed = 0

        case Command.FRONT_SLOW_POT_SMOOTH | Command.BACK_FADE_FRONT_SLOW:
            if command == Command.FRONT_SLOW_POT_SMOOTH and old_state.potled_on == 1:
                new_state.potled_mode = 16
            if command == Command.BACK_FADE_FRONT_SLOW and old_state.backled_on == 1:
                new_state.backled_mode = 17

            if old_state.frontled_on == 1:
                if old_state.frontled_mode not in FRONTLED_COLOR_MODES:
                    if old_state.frontled_rel_speed == 2:
                        return old_state # this is a forbidden move
                    if old_state.frontled_rel_speed == 0:
                        new_state.frontled_rel_speed = 2
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.frontled_rel_speed = 0

        case Command.FRONT_AUTO_POT_FLASH | Command.BACK_STROBE_FRONT_AUTO:
            if command == Command.FRONT_AUTO_POT_FLASH and old_state.potled_on == 1:
                new_state.potled_mode = 19
            if command == Command.BACK_STROBE_FRONT_AUTO and old_state.backled_on == 1:
                new_state.backled_mode = 18

            if old_state.frontled_on == 1:
                new_state.frontled_mode = 26
                new_state.frontled_paused = 0

        case Command.FRONT_DIY1_POT_G2 | Command.BACK_R3_FRONT_DIY1:
            if command == Command.FRONT_DIY1_POT_G2 and old_state.potled_on == 1:
                new_state.potled_mode = 6
            if command == Command.BACK_R3_FRONT_DIY1 and old_state.backled_on == 1:
                new_state.backled_mode = 2

            if old_state.frontled_on == 1:
                new_state.frontled_mode = 20

        case Command.FRONT_DIY2_POT_R2 | Command.BACK_G3_FRONT_DIY2:
            if command == Command.FRONT_DIY2_POT_R2 and old_state.potled_on == 1:
                new_state.potled_mode = 1
            if command == Command.BACK_G3_FRONT_DIY2 and old_state.backled_on == 1:
                new_state.backled_mode = 7

            if old_state.frontled_on == 1:
                new_state.frontled_mode = 21

        case Command.FRONT_DIY3_POT_B2 | Command.BACK_B3_FRONT_DIY3:
            if command == Command.FRONT_DIY3_POT_B2 and old_state.potled_on == 1:
                new_state.potled_mode = 11
            if command == Command.BACK_B3_FRONT_DIY3 and old_state.backled_on == 1:
                new_state.backled_mode = 12

            if old_state.frontled_on == 1:
                new_state.frontled_mode = 22

        case Command.FRONT_DIY4_POT_G | Command.BACK_R2_FRONT_DIY4:
            if command == Command.FRONT_DIY4_POT_G and old_state.potled_on == 1:
                new_state.potled_mode = 5
            if command == Command.BACK_R2_FRONT_DIY4 and old_state.backled_on == 1:
                new_state.backled_mode = 1

            if old_state.frontled_on == 1:
                new_state.frontled_mode = 23

        case Command.FRONT_DIY5_POT_R | Command.BACK_G2_FRONT_DIY5:
            if command == Command.FRONT_DIY5_POT_R and old_state.potled_on == 1:
                new_state.potled_mode = 0
            if command == Command.BACK_G2_FRONT_DIY5 and old_state.backled_on == 1:
                new_state.backled_mode = 6

            if old_state.frontled_on == 1:
                new_state.frontled_mode = 24

        case Command.FRONT_DIY6_POT_B | Command.BACK_B2_FRONT_DIY6:
            if command == Command.FRONT_DIY6_POT_B and old_state.potled_on == 1:
                new_state.potled_mode = 10
            if command == Command.BACK_B2_FRONT_DIY6 and old_state.backled_on == 1:
                new_state.backled_mode = 11

            if old_state.frontled_on == 1:
                new_state.frontled_mode = 25

        case Command.FRONT_FLASH_POT_W | Command.BACK_FLASH_FRONT_FLASH:
            if command == Command.FRONT_FLASH_POT_W and old_state.potled_on == 1:
                new_state.potled_mode = 15
            if command == Command.BACK_FLASH_FRONT_FLASH and old_state.backled_on == 1:
                new_state.backled_mode = 19
                
            if old_state.frontled_on == 1:
                new_state.frontled_mode = 27
                new_state.frontled_paused = 0

        case Command.FRONT_FADE3_POT_OFF | Command.BACK_B_FRONT_FADE3:
            if command == Command.FRONT_FADE3_POT_OFF and old_state.potled_on == 1:
                new_state.potled_on = 0
            if command == Command.BACK_B_FRONT_FADE3 and old_state.backled_on == 1:
                new_state.backled_mode = 10
            if old_state.frontled_on == 1:
                new_state.frontled_mode = 30
                new_state.frontled_paused = 0

        case Command.FRONT_FADE7_POT_ON | Command.BACK_W_FRONT_FADE7:
            if command == Command.FRONT_FADE7_POT_ON and old_state.potled_on == 0:
                new_state.potled_on = 1
            if command == Command.BACK_W_FRONT_FADE7 and old_state.backled_on == 1:
                new_state.backled_mode = 15
            if old_state.frontled_on == 1:
                new_state.frontled_mode = 31
                new_state.frontled_paused = 0
            else:
                new_state.frontled_calibration = (old_state.frontled_calibration + 1) % FRONTLED_CALIBRATION_LENGTH

        case Command.FRONT_JUMP3_POT_DOWN:
            if old_state.frontled_on == 1:
                new_state.frontled_mode = 28
                new_state.frontled_paused = 0
            if old_state.potled_on == 1:
                if old_state.potled_mode in POTLED_COLOR_MODES:
                    if old_state.potled_rel_brightness == 2:
                        return old_state # this is a forbidden move
                    if old_state.potled_rel_brightness == 0:
                        new_state.potled_rel_brightness = 2
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.potled_rel_brightness = 0
                else:
                    if old_state.potled_rel_speed == 2:
                        return old_state # this is a forbidden move
                    if old_state.potled_rel_speed == 0:
                        new_state.potled_rel_speed = 2
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.potled_rel_speed = 0

        case Command.FRONT_JUMP7_POT_UP:
            if old_state.frontled_on == 1:
                new_state.frontled_mode = 29
                new_state.frontled_paused = 0
            if old_state.potled_on == 1:
                if old_state.potled_mode in POTLED_COLOR_MODES:
                    if old_state.potled_rel_brightness == 1:
                        return old_state # this is a forbidden move
                    if old_state.potled_rel_brightness == 0:
                        new_state.potled_rel_brightness = 1
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.potled_rel_brightness = 0
                else:
                    if old_state.potled_rel_speed == 1:
                        return old_state # this is a forbidden move
                    if old_state.potled_rel_speed == 0:
                        new_state.potled_rel_speed = 1
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.potled_rel_speed = 0

        case Command.BACK_R_FRONT_JUMP3:
            if old_state.backled_on == 1:
                new_state.backled_mode = 0
            if old_state.frontled_on == 1:
                new_state.frontled_mode = 28
                new_state.frontled_paused = 0

        case Command.BACK_G_FRONT_JUMP7:
            if old_state.backled_on == 1:
                new_state.backled_mode = 5
            if old_state.frontled_on == 1:
                new_state.frontled_mode = 29
                new_state.frontled_paused = 0

        case Command.BACK_ON:
            new_state.backled_on = 1

        case Command.BACK_OFF:
            new_state.backled_on = 0

        case Command.BACK_DOWN:
            if old_state.backled_on == 1:
                if old_state.backled_mode in BACKLED_COLOR_MODES:
                    if old_state.backled_rel_brightness == 2:
                        return old_state # this is a forbidden move
                    if old_state.backled_rel_brightness == 0:
                        new_state.backled_rel_brightness = 2
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.backled_rel_brightness = 0
                else:
                    if old_state.backled_rel_speed == 2:
                        return old_state # this is a forbidden move
                    if old_state.backled_rel_speed == 0:
                        new_state.backled_rel_speed = 2
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.backled_rel_speed = 0

        case Command.BACK_UP:
            if old_state.backled_on == 1:
                if old_state.backled_mode in BACKLED_COLOR_MODES:
                    if old_state.backled_rel_brightness == 1:
                        return old_state # this is a forbidden move
                    elif old_state.backled_rel_brightness == 0:
                        new_state.backled_rel_brightness = 1
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.backled_rel_brightness = 0
                else:
                    if old_state.backled_rel_speed == 1:
                        return old_state # this is a forbidden move
                    if old_state.backled_rel_speed == 0:
                        new_state.backled_rel_speed = 1
                    else:
                        if AVOID_CHANGING_RELATIVE_STATE_NEEDLESSLY:
                            return old_state # this is a forbidden move
                        new_state.backled_rel_speed = 0
            
    return new_state
"""
Validation for the given state definitions for caching nonsensical requests
early.
"""

from configuration import *

def is_valid_state(candidate_states: list[str]) -> bool:
    for device_state in candidate_states:
        if not device_state in COMMAND_ALIASES:
            return False
    return True

def all_modes_defined(initial_state: list[str]) -> bool:
    backled_mode_definitions = 0
    frontled_mode_definitions = 0
    potled_mode_definitions = 0
    for state in initial_state:
        if state in BACKLED_MODES:
            backled_mode_definitions += 1
        if state in FRONTLED_MODES:
            frontled_mode_definitions += 1
        if state in POTLED_MODES:
            potled_mode_definitions += 1
    return backled_mode_definitions >= 1 and frontled_mode_definitions >= 1 and potled_mode_definitions >= 1

def no_duplicate_mode_definitions(given_state: list[str]) -> bool:
    backled_mode_definitions = 0
    frontled_mode_definitions = 0
    potled_mode_definitions = 0
    for state in given_state:
        if state in BACKLED_MODES:
            backled_mode_definitions += 1
        if state in FRONTLED_MODES:
            frontled_mode_definitions += 1
        if state in POTLED_MODES:
            potled_mode_definitions += 1
    return backled_mode_definitions <= 1 and frontled_mode_definitions <= 1 and potled_mode_definitions <= 1

def absolute_state(state: list[str]) -> bool:
    for opposites in RELATIVE_STATES:
        if opposites[0] in state or opposites[1] in state:
            return False
    return True

def no_opposites_in_relative_states(state: list[str]) -> bool:
    for opposites in RELATIVE_STATES:
        if opposites[0] in state and opposites[1] in state:
            return False
    return True
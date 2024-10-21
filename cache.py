"""
Tests every relevant scenario for initial and desired states for each led
device. The solutions that take more than 200ms to compute will be appended to
cache.bin. Such cached solutions can be requested via get_cached.
The script also, luckily, confirms that no state combination is mathematically
impossible to solve.

Note: The cache supports only one target state at a time. Combinations can be
      solved for by appending cached results for one target state at a time or
      by forgoing the cache completely.

More important note: Running this script will take several hours, probably
                     days. However, without the cache some solutions can take
                     seconds to compute. Moreover reading from the cache is
                     very fast, to the extent that there was no practical
                     reason to implement prereading it to memory for O(1)
                     access. In other words, caching guarantees that this
                     solver is practical for use between button presses.
"""

import solver
from configuration import is_state_setting_effective, get_commands_for_relative_state
from configuration import Command, State, COMMANDS, BACKLED_MODES, FRONTLED_MODES, POTLED_MODES, RELATIVE_STATES
import pathlib

# Binary file to store the cached solutions:
CACHE_FILE = pathlib.Path(__file__).parent.absolute().as_posix() + "/cache.bin"
# Only cache solutions that took longer than this to find:
CACHE_SLOWER_THAN_MS = 200
# check if an adjacent state with a device on/off has been cached and works as a solution for this state too:
DEVICE_TOGGLING_OPTIMIZATION = True

TARGET_STATES = BACKLED_MODES + FRONTLED_MODES + POTLED_MODES \
                 + [st1 for st1, _ in RELATIVE_STATES] + [st2 for _, st2 in RELATIVE_STATES] \
                 + ["backled off", "backled on", "frontled off", "frontled on", "potled off", "potled on"]

def get_cached(initial_states: list[str], target_state: str) -> list[Command]:
    if target_state in ["frontled paused", "frontled unpaused", "frontled calibrate", "potled calibrate"]: # Exception to what's cached
        return None
    
    decoded_initial_state = solver.read_state(State(), initial_states)
    decoded_desired_state = solver.read_state(decoded_initial_state, [target_state])

    return get_cached_internal(decoded_initial_state, decoded_desired_state, target_state)

def get_cached_internal(decoded_initial_state: State, decoded_desired_state: State, target_state: str):
    import dataclasses

    if DEVICE_TOGGLING_OPTIMIZATION:
        if decoded_initial_state.backled_on == 1 and target_state not in ["backled off", "backled on"]:
            new_initial_state = dataclasses.replace(decoded_initial_state)
            new_initial_state.backled_on = 0
            new_desired_state = dataclasses.replace(decoded_desired_state)
            new_desired_state.backled_on = 0
            candidate = get_cached_internal(new_initial_state, new_desired_state, target_state)
            if solver.is_solution(candidate, decoded_initial_state, decoded_desired_state):
                return candidate
            
        if decoded_initial_state.frontled_on == 1 and target_state not in ["frontled off", "frontled on"]:
            new_initial_state = dataclasses.replace(decoded_initial_state)
            new_initial_state.frontled_on = 0
            new_desired_state = dataclasses.replace(decoded_desired_state)
            new_desired_state.frontled_on = 0
            candidate = get_cached_internal(new_initial_state, new_desired_state, target_state)
            if solver.is_solution(candidate, decoded_initial_state, decoded_desired_state):
                return candidate
            
        if decoded_initial_state.potled_on == 1 and target_state not in ["potled off", "potled on"]:
            new_initial_state = dataclasses.replace(decoded_initial_state)
            new_initial_state.potled_on = 0
            new_desired_state = dataclasses.replace(decoded_desired_state)
            new_desired_state.potled_on = 0
            candidate = get_cached_internal(new_initial_state, new_desired_state, target_state)
            if solver.is_solution(candidate, decoded_initial_state, decoded_desired_state):
                return candidate
    
    return get_cached_internal0(decoded_initial_state, target_state)

def get_cached_internal0(decoded_initial_state: State, target_state: str):
    i = encode_state_combination(decoded_initial_state, target_state)
    with open(CACHE_FILE, "rb") as f:
        while (data := f.read(8)): # 8 byte chucks: state combination 4 bytes, its solution 4 bytes
            index = int.from_bytes(data[:4], byteorder='big')
            if index == i:
                return decode_solution(int.from_bytes(data[4:], byteorder='big'))
            if index > i:
                return None
    return None

def encode_state_combination(decoded_initial_state: State, target_state: str) -> int:
    backled_mode_i = decoded_initial_state.backled_mode
    frontled_mode_i = decoded_initial_state.frontled_mode
    potled_mode_i = decoded_initial_state.potled_mode
    target_i = TARGET_STATES.index(target_state)
    backled_status_i = decoded_initial_state.backled_on
    frontled_status_i = decoded_initial_state.frontled_on
    potled_status_i = decoded_initial_state.potled_on

    index = 0
    index = backled_mode_i    + index * len(BACKLED_MODES)
    index = frontled_mode_i   + index * len(FRONTLED_MODES)
    index = potled_mode_i     + index * len(POTLED_MODES)
    index = target_i          + index * len(TARGET_STATES)
    index = backled_status_i  + index * 2
    index = frontled_status_i + index * 2
    index = potled_status_i   + index * 2

    return index

def encode_solution(solution: list[Command]) -> int:
    # reversed because the last steps in the longest known solutions are small in value making the encoded solution fit 4 bytes:
    reversed = solution[::-1]
    return sum([(reversed[i].value+1)*((len(COMMANDS)+1)**i) for i in range(len(solution))])

def decode_solution(encoded: int) -> list[Command]:
    solution = []
    while encoded > 0:
        encoded, mod = divmod(encoded, len(COMMANDS)+1)
        if mod > 0:
            solution.append(Command(mod-1))
    # reversed; see above.
    return solution[::-1]


if __name__ == "__main__":
    import time

    i = 0 # all state combinations enumerated (Note: frontled pause state excluded; should always be [Command.FRONT_PLAYPAUSE])
    starting_index = 0

    cached_amount = 0

    for backled_mode in BACKLED_MODES:
        for frontled_mode in FRONTLED_MODES:
            lines = []
            for potled_mode in POTLED_MODES:
                start = time.time()
                for target_state in TARGET_STATES:
                    if target_state in [backled_mode, frontled_mode, potled_mode]:
                        i += 8
                        continue
                    solutions = set({tuple([o]) for o in get_commands_for_relative_state(target_state)})

                    for backled_status in ["backled off", "backled on"]:
                        for frontled_status in ["frontled off", "frontled on"]:
                            for potled_status in ["potled off", "potled on"]:
                                i += 1
                                if i <= starting_index:
                                    continue
                                initial_states = [backled_mode, frontled_mode, potled_mode, backled_status, frontled_status, potled_status]
                                decoded_initial_state = solver.read_state(State(), initial_states)
                                if not is_state_setting_effective(decoded_initial_state, target_state):
                                    continue
                                decoded_desired_state = solver.read_state(decoded_initial_state, [target_state])

                                solution = None

                                for candidate in solutions:
                                    if solver.is_solution(candidate, decoded_initial_state, decoded_desired_state):
                                        solution = candidate
                                        break

                                if solution == None:
                                    st = time.time()
                                    solution = solver.solve_internal(decoded_initial_state, decoded_desired_state)
                                    if time.time() - st > CACHE_SLOWER_THAN_MS/1000:
                                        cached_amount += 1
                                        lines.append((i-1, encode_solution(solution)))
                                assert solution != [], "Empty solution for {}, {}, {}, {}, {}, {} -> {}".format(backled_mode, frontled_mode, potled_mode, backled_status, frontled_status, potled_status, target_state)
                                assert solution != None, "No solution for {}, {}, {}, {}, {}, {} -> {}".format(backled_mode, frontled_mode, potled_mode, backled_status, frontled_status, potled_status, target_state)
                                solutions.add(tuple(solution))
                end = time.time()
                print("All states handled for {}, {}, {} in {} s  (i = {}; to be cached so far: {})".format(backled_mode, frontled_mode, potled_mode, end - start, i, cached_amount))

            with open(CACHE_FILE, "ab") as f:
                for index, encoded in lines:
                    f.write(index.to_bytes(4, byteorder='big') + encoded.to_bytes(4, byteorder='big'))
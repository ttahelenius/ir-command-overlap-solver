"""
The solver implements a breadth-first search to obtain an optimal solution.
However, this gets exponentially slower by each step really fast. Several good
enough known solutions will be attempted as heuristic to arrive quickly to
some solution, after which a better one is solved for. This eliminates most of
the slowest cases.

Note: a more optimal solution is only attempted up the length 3. This is
      because anything more could take hours to compute. This is a reasonable
      trade-off, as it matters quite little whether to use a solution of
      length 4 or 6 (the longest heuristic). Optionally one can lower this
      value to 0 and simply accept the heuristic although it may not be the
      most optimal.

      These solution can and should be cached (see use_cache parameter and
      cache.py). This will reduce the expected time to however many solutions
      one wishes to cache (the threshold is all slower than 200ms by default).
"""

from configuration import *
import cache

MAX_STEPS_TO_CHECK = 3

def solve(initial_state: list[str], desired_state: list[str], use_cache: bool = False) -> list[Command] | None:
    if use_cache and len(desired_state) == 1:
        cached_solution = cache.get_cached(initial_state, desired_state[0])
        if cached_solution is not None:
            return cached_solution

    decoded_initial_state = read_state(State(), initial_state)
    decoded_desired_state = read_state(decoded_initial_state, desired_state)

    special_solution = handle_special_case(decoded_initial_state, decoded_desired_state)
    if special_solution is not None:
        return special_solution
    
    if len(desired_state) == 1 and not is_state_setting_effective(decoded_initial_state, desired_state[0]):
        return []

    return solve_internal(decoded_initial_state, decoded_desired_state)

def solve_internal(decoded_initial_state: State, decoded_desired_state: State) -> list[Command] | None:
    state = encode_state(decoded_initial_state)
    endstate = encode_state(decoded_desired_state)

    if state == endstate:
        return []
    
    heuristic_solution = solve_with_heuristic(decoded_initial_state, decoded_desired_state)

    limit = MAX_STEPS_TO_CHECK
    if heuristic_solution is not None:
        # The heuristic works, still going after a more optimal solution.
        # Note: not checking beyond MAX_STEPS_TO_CHECK so taking a rather
        #       insignificant risk of missing a very slightly better solution
        #       that could take literal days to find.
        limit = min(len(heuristic_solution) - 1, MAX_STEPS_TO_CHECK)
    
    solution = bfs(decoded_initial_state, decoded_desired_state, limit)
    
    if solution is not None:
        assert is_solution(solution, decoded_initial_state, decoded_desired_state)
        return solution

    if heuristic_solution is not None:
        return heuristic_solution

    return None

# breadth-first search
def bfs(initial_state: State, desired_state: State, limit: int) -> list[Command] | None:
    from collections import deque
    if limit == 0:
        return None
    state = encode_state(initial_state)
    endstate = encode_state(desired_state)
    visited = set()
    q: deque[tuple[int, int]] = deque()
    q.append((state, 0))
    commands = COMMANDS.keys()
    while len(q) > 0:
        state, encoded_commandseries = q.popleft()
        decoded_commandseries = decode_commandseries(encoded_commandseries)
        visited.add(state)
        decoded_state = decode_state(state)
        for command in commands:
            next_state = encode_state(perform_command(decoded_state, command))
            if next_state in visited:
                continue
            next_commandseries_encoded = encode_commandseries(decoded_commandseries, command.value)
            if next_state == endstate:
                return to_commands(decode_commandseries(next_commandseries_encoded))
            if len(decoded_commandseries) == limit - 1:
                continue
            q.append((next_state, next_commandseries_encoded))
    return None

def to_commands(intlist: list[int]) -> list[Command]:
    return [Command(c) for c in intlist]

# Attempts several heuristics to speed up the solve
def solve_with_heuristic(state: State, endstate: State) -> list[Command] | None:

    if state.backled_on == 1 and endstate.backled_on == 0:
        attempt = [Command.BACK_OFF]
        if is_solution(attempt, state, endstate):
            return attempt
    if state.backled_on == 0 and endstate.backled_on == 1:
        attempt = [Command.BACK_ON]
        if is_solution(attempt, state, endstate):
            return attempt
    if state.frontled_on != endstate.frontled_on:
        attempt = [Command.FRONT_ONOFF]
        if is_solution(attempt, state, endstate):
            return attempt
    if state.potled_on == 1 and endstate.potled_on == 0:
        attempt = [Command.FRONT_FADE3_POT_OFF]
        if is_solution(attempt, state, endstate):
            return attempt
    if state.potled_on == 0 and endstate.potled_on == 1:
        attempt = [Command.FRONT_FADE7_POT_ON]
        if is_solution(attempt, state, endstate):
            return attempt

    if state.backled_on == 1 and endstate.backled_on == 1 \
            and state.backled_mode != endstate.backled_mode:
        attempt = [backled_get_command_for(endstate.backled_mode)]
        if is_solution(attempt, state, endstate):
            return attempt
        
    if state.frontled_on == 1 and endstate.frontled_on == 1 \
            and state.frontled_mode != endstate.frontled_mode:
        attempt = [frontled_get_command_for(endstate.frontled_mode, potled_overlap=False)]
        if is_solution(attempt, state, endstate):
            return attempt
        attempt = [frontled_get_command_for(endstate.frontled_mode, potled_overlap=True)]
        if is_solution(attempt, state, endstate):
            return attempt
        
    if state.potled_on == 1 and endstate.potled_on == 1 \
            and state.potled_mode != endstate.potled_mode:
        attempt = [potled_get_command_for(endstate.potled_mode)]
        if is_solution(attempt, state, endstate):
            return attempt

    if state.backled_on == 1 and endstate.backled_on == 1 \
            and state.frontled_on == 1 and endstate.frontled_on == 1 \
            and state.backled_mode != endstate.backled_mode:
        attempt = [backled_get_command_for(endstate.backled_mode),
                   frontled_get_command_for(endstate.frontled_mode)]
        if is_solution(attempt, state, endstate):
            return attempt
        
    if state.frontled_on == 1 and endstate.frontled_on == 1 \
            and state.potled_on == 1 and endstate.potled_on == 1 \
            and state.potled_mode != endstate.potled_mode:
        attempt = [potled_get_command_for(endstate.potled_mode),
                   frontled_get_command_for(endstate.frontled_mode, potled_overlap=False)]
        if is_solution(attempt, state, endstate):
            return attempt
        
    if state.frontled_on == 1 and endstate.frontled_on == 1 \
            and state.potled_on == 1 and endstate.potled_on == 1 \
            and state.frontled_mode != endstate.frontled_mode:
        attempt = [frontled_get_command_for(endstate.frontled_mode, potled_overlap=True),
                   potled_get_command_for(endstate.potled_mode)]
        if is_solution(attempt, state, endstate):
            return attempt
        
    if state.backled_on == 1 and endstate.backled_on == 1 \
            and state.frontled_on == 1 and endstate.frontled_on == 1 \
            and state.frontled_mode != endstate.frontled_mode:
        attempt = [Command.BACK_OFF,
                   frontled_get_command_for(endstate.frontled_mode, potled_overlap=False),
                   Command.BACK_ON]
        if is_solution(attempt, state, endstate):
            return attempt
        
    if state.frontled_on == 1 and endstate.frontled_on == 1 \
            and state.potled_on == 1 and endstate.potled_on == 1 \
            and state.potled_mode != endstate.potled_mode:
        attempt = [Command.FRONT_ONOFF,
                   potled_get_command_for(endstate.potled_mode),
                   Command.FRONT_ONOFF]
        if is_solution(attempt, state, endstate):
            return attempt
        
    if state.backled_on == 1 and endstate.backled_on == 1 \
            and state.frontled_on == 1 and endstate.frontled_on == 1 \
            and state.backled_mode != endstate.backled_mode:
        attempt = [Command.FRONT_ONOFF,
                   backled_get_command_for(endstate.backled_mode),
                   Command.FRONT_ONOFF]
        if is_solution(attempt, state, endstate):
            return attempt

    if state.frontled_on == 1 and endstate.frontled_on == 1 \
            and state.potled_on == 1 and endstate.potled_on == 1 \
            and state.frontled_mode != endstate.frontled_mode:
        attempt = [frontled_get_command_for(endstate.frontled_mode, potled_overlap=True),
                   Command.FRONT_ONOFF,
                   potled_get_command_for(endstate.potled_mode),
                   Command.FRONT_ONOFF]
        if is_solution(attempt, state, endstate):
            return attempt
        
    if state.backled_on == 1 and endstate.backled_on == 1 \
            and state.frontled_on == 1 and endstate.frontled_on == 1 \
            and state.potled_on == 1 and endstate.potled_on == 1 \
            and state.backled_mode != endstate.backled_mode:
        attempt = [backled_get_command_for(endstate.backled_mode),
                   frontled_get_command_for(endstate.frontled_mode, potled_overlap=True),
                   potled_get_command_for(endstate.potled_mode)]
        if is_solution(attempt, state, endstate):
            return attempt

        attempt = [backled_get_command_for(endstate.backled_mode),
                   frontled_get_command_for(endstate.frontled_mode, potled_overlap=True),
                   Command.FRONT_ONOFF,
                   potled_get_command_for(endstate.potled_mode),
                   Command.FRONT_ONOFF]
        if is_solution(attempt, state, endstate):
            return attempt
            
    if state.frontled_on == 0 and endstate.frontled_on == 0:
        if state.backled_mode != endstate.backled_mode:
            attempt = [Command.FRONT_ONOFF,
                       backled_get_command_for(endstate.backled_mode),
                       frontled_get_command_for(endstate.frontled_mode, potled_overlap=True),
                       Command.FRONT_ONOFF]
            if is_solution(attempt, state, endstate):
                return attempt
            
    if state.potled_on == 0 and endstate.potled_on == 1:
        if state.frontled_on == 1 and endstate.frontled_on == 1:
            attempt = [Command.FRONT_FADE7_POT_ON,
                       frontled_get_command_for(endstate.frontled_mode, potled_overlap=False)]
            if is_solution(attempt, state, endstate):
                return attempt
            
            attempt = [Command.FRONT_FADE7_POT_ON,
                       frontled_get_command_for(endstate.frontled_mode, potled_overlap=True),
                       potled_get_command_for(endstate.potled_mode)]
            if is_solution(attempt, state, endstate):
                return attempt

            attempt = [Command.FRONT_FADE7_POT_ON,
                       Command.BACK_OFF,
                       frontled_get_command_for(endstate.frontled_mode, potled_overlap=False),
                       Command.BACK_ON]
            if is_solution(attempt, state, endstate):
                return attempt
            
            attempt = [Command.FRONT_FADE7_POT_ON,
                       frontled_get_command_for(endstate.frontled_mode, potled_overlap=True),
                       Command.FRONT_ONOFF,
                       potled_get_command_for(endstate.potled_mode),
                       Command.FRONT_ONOFF]
            if is_solution(attempt, state, endstate):
                return attempt
            
        if state.frontled_on == 0 and endstate.frontled_on == 0:
            attempt = [Command.FRONT_ONOFF,
                       Command.FRONT_FADE7_POT_ON,
                       frontled_get_command_for(endstate.frontled_mode, potled_overlap=False),
                       Command.FRONT_ONOFF]
            if is_solution(attempt, state, endstate):
                return attempt
            
            attempt = [Command.FRONT_ONOFF,
                       Command.FRONT_FADE7_POT_ON,
                       frontled_get_command_for(endstate.frontled_mode, potled_overlap=True),
                       Command.FRONT_ONOFF,
                       potled_get_command_for(endstate.potled_mode)]
            if is_solution(attempt, state, endstate):
                return attempt
            
            attempt = [Command.FRONT_ONOFF,
                       Command.FRONT_FADE7_POT_ON,
                       Command.BACK_OFF,
                       frontled_get_command_for(endstate.frontled_mode, potled_overlap=False),
                       Command.FRONT_ONOFF,
                       Command.BACK_ON]
            if is_solution(attempt, state, endstate):
                return attempt
            
    if endstate.backled_mode == 15:
        if state.frontled_on == 0 and endstate.frontled_on == 0:
            attempt = [Command.FRONT_ONOFF,
                       Command.BACK_W_FRONT_FADE7,
                       frontled_get_command_for(endstate.frontled_mode, potled_overlap=True),
                       Command.FRONT_ONOFF,
                       potled_get_command_for(endstate.potled_mode)]
            if is_solution(attempt, state, endstate):
                return attempt
            
            attempt = [Command.FRONT_ONOFF,
                       Command.BACK_W_FRONT_FADE7,
                       Command.BACK_OFF,
                       frontled_get_command_for(endstate.frontled_mode, potled_overlap=False),
                       Command.BACK_ON,
                       Command.FRONT_ONOFF]
            if is_solution(attempt, state, endstate):
                return attempt
            
        if state.frontled_on == 1 and endstate.frontled_on == 1:
            attempt = [Command.BACK_W_FRONT_FADE7,
                       Command.BACK_OFF,
                       frontled_get_command_for(endstate.frontled_mode, potled_overlap=False),
                       Command.BACK_ON]
            if is_solution(attempt, state, endstate):
                return attempt

    return None

def handle_special_case(state: State, endstate: State) -> list[Command] | None:
    # This particular calibration requires an absurd amount of RED-commands and
    # as such it's not encoded in the graph and has to be handled semi-manually.
    if endstate.potled_calibration == 1:
        calibration_phase = [Command.FRONT_DIY5_POT_R,
                             Command.FRONT_DIY5_POT_R,
                             Command.FRONT_DIY5_POT_R,
                             Command.FRONT_DIY5_POT_R,
                             Command.FRONT_DIY5_POT_R,
                             Command.FRONT_DIY5_POT_R,
                             Command.FRONT_DIY5_POT_R,
                             Command.FRONT_DIY5_POT_R,
                             Command.FRONT_DIY5_POT_R,
                             Command.FRONT_DIY5_POT_R,
                             Command.FRONT_DIY5_POT_R,
                             Command.FRONT_DIY5_POT_R,
                             Command.FRONT_DIY5_POT_R,
                             Command.FRONT_DIY5_POT_R,
                             Command.FRONT_DIY5_POT_R,
                             Command.FRONT_DIY5_POT_R,
                             Command.FRONT_DIY5_POT_R] # Yes, really this many.
        next_state = perform_command(state, Command.FRONT_DIY5_POT_R)
        # Attempt to return back to previous state
        steps_to_return = solve_internal(next_state, state)
        if steps_to_return is not None:
            return calibration_phase + steps_to_return
        return calibration_phase # No can do.
    
    return None

def is_solution(solution: list[Command] | None, state: State, endstate: State) -> bool:
    if solution is None:
        return False
    state = dataclasses.replace(state)
    for step in solution:
        new_state = perform_command(state, step)
        if new_state == state:
            return False
        state = new_state
    return state == endstate

def encode_commandseries(commandseries: list[int], command: int) -> int:
    encoded = 0
    power = 1
    for i in range(len(commandseries)):
        encoded += (commandseries[i] + 1) * power
        power *= len(COMMANDS) + 1
    return encoded + (command + 1) * power

def decode_commandseries(commandseries_encoded: int) -> list[int]:
    commandseries = []
    encoded = commandseries_encoded
    while encoded > 0:
        encoded, mod = divmod(encoded, len(COMMANDS)+1)
        commandseries.append(mod-1)
    return commandseries
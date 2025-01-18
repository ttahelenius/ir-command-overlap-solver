"""
Attempts to find an optimal (in length) series of commands to yield the
desired end state from the given initial state while avoiding and/or
counteracting the side-effects caused by command overlap.
Takes two positional arguments: initial and desired state, formatted like
"frontled off, backled g4" etc.
Outputs the optimal series of commands.

Note: the devices are assumed to be on and unpaused unless specified
      otherwise.

Also note: The solver can be slow for unfortunate cases (see solver.py). Use
           the cache (--use-cache) if possible.

Additional optional arguments:
--machine-readable: Only output the solution as commands line by line
--use-cache:        Seeks solutions stored in cache.bin (see cache.py)
--avoid-overwhelm:  In output suggest delays that may prevent device overwhelm
                    from unexpected amount of consecutive commands. This is
                    expressed as *Delay*.
--await-repeats:    In output suggest when to await for repeated input for the
                    same command. For example one should be able to mash the
                    brightening button without being interrupted by the
                    subsequent commands in the series. However the only part
                    this script implements is to suggest *Await repeats*
                    appropriately.
"""

import configuration

class Invalid_parameters(Exception):
    pass

def read_input(arg1: str, arg2: str) -> tuple[list[str], list[str]]:
    return separate(arg1), separate(arg2)

def separate(str: str) -> list[str]:
    return [x.strip() for x in str.split(',')]

def solve_command_series(given_initial_state: str, given_desired_state: str, use_cache: bool = False) -> list[configuration.Command] | None:
    import validation as verify
    import solver

    initial_state, desired_state = read_input(given_initial_state, given_desired_state)

    if not verify.is_valid_state(initial_state):
        raise Invalid_parameters("Invalid initial state")
    if not verify.is_valid_state(desired_state):
        raise Invalid_parameters("Invalid desired end state")
    if not verify.all_modes_defined(initial_state):
        raise Invalid_parameters("Define all modes")
    if not verify.no_duplicate_mode_definitions(initial_state) or not verify.no_duplicate_mode_definitions(desired_state):
        raise Invalid_parameters("No duplicate modes allowed!")
    if not verify.absolute_state(initial_state):
        raise Invalid_parameters("Relative state not allowed as initial")
    if not verify.no_opposites_in_relative_states(desired_state):
        raise Invalid_parameters("Simultaneous opposite states not allowed")

    return solver.solve(initial_state, desired_state, use_cache)

AWAIT_REPEATS = "*Await repeats*"
DELAY = "*Delay*"

if __name__ == "__main__":
    import sys

    positional = 0
    machine_readable_output = False
    use_cache = False
    mark_delays_for_avoiding_overwhelm = False
    mark_opportunity_for_awaiting_repeat_inputs = False
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "--machine-readable":
            machine_readable_output = True
        elif sys.argv[i] == "--use-cache":
            use_cache = True
        elif sys.argv[i] == "--avoid-overwhelm":
            mark_delays_for_avoiding_overwhelm = True
        elif sys.argv[i] == "--await-repeats":
            mark_opportunity_for_awaiting_repeat_inputs = True
        else:
            if positional == 0:
                initial_state = sys.argv[i]
            elif positional == 1:
                desired_state = sys.argv[i]
            positional += 1

    if positional != 2:
        print("Arguments: (initial state) (desired state) [--machine-readable] [--use-cache] [--avoid-overwhelm] [--await-repeats]")
        sys.exit(1)

    desired_state = configuration.convert_target_state(desired_state, separate(initial_state))

    try:
        commandseries = solve_command_series(initial_state, desired_state, use_cache)
    except Invalid_parameters as e:
        print(str(e))
        sys.exit(1)

    if commandseries is None:
        if not machine_readable_output:
            print("Not a single solution found!")
        sys.exit(0)

    if not machine_readable_output:
        print("Solution found!")
        print("Execute the following commands in order:")

    backled_toggled = False
    frontled_toggled = False
    potled_toggled = False
    just_awaited_repeats = False

    for command in commandseries:
        executable, side_effect = configuration.COMMANDS[command]

        if mark_delays_for_avoiding_overwhelm:
            effects = [executable] + ([side_effect] if side_effect is not None else [])
            add_delay = False
            if any(s.startswith("backled ") for s in effects):
                if backled_toggled and not just_awaited_repeats:
                    add_delay = True
                backled_toggled = True
            if any(s.startswith("frontled ") for s in effects):
                if frontled_toggled and not just_awaited_repeats:
                    add_delay = True
                frontled_toggled = True
            if any(s.startswith("potled ") for s in effects):
                if potled_toggled and not just_awaited_repeats:
                    add_delay = True
                potled_toggled = True
            if add_delay:
                print(DELAY)

        just_awaited_repeats = False

        if machine_readable_output or side_effect == None:
            print(executable)
        else:
            print("{} (side-effect: {})".format(executable, side_effect))

        if mark_opportunity_for_awaiting_repeat_inputs:
            if configuration.Command(command) in configuration.get_commands_for_relative_state(desired_state):
                print(AWAIT_REPEATS)
                just_awaited_repeats = True

    if mark_delays_for_avoiding_overwhelm:
        if backled_toggled or frontled_toggled or potled_toggled:
            print(DELAY)
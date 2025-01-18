# **Infrared Command Overlap Solver**

A command resolver for my particular combination of three remote-controlled LED devices. It's essentially a Python script that returns a series of infrared commands that will produce the desired outcome for all these devices while counter-acting the side-effects of command overlap.

This script is directly usable in a virtual set of remote controls implemented here: https://github.com/ttahelenius/virtual-led-remote.

## **The problem**

At the time of writing I have three remote-controlled LED devices in close proximity and their remote controls happen to be configured to respond to very similar set of commands. The effect of this is that I could press a specific color button on one controller and another unrelated device switches mode.


Manually one could turn off device 2, press a button for device 1 and turn on device 2 again to solve this for two devices, and often this is an option. However it turns out that some commands affect the on/off state, or worse reconfigure the entire device if a specific command is sent while it's off.
As a result there are some mode/command combinations that require a very specific and non-trivial combination of maneuvers to counteract all the side-effects.

## **The solution**

Mathematically this can be represented as a directed graph: the sets of device states (color modes, on/off states etc.) form vertices connected by directed edges denoting the commands.
Therefore the problem becomes finding an optimal (least steps) path from the original state to the desired state. A fast enough solution is obtained through a breadth-first search aided by heuristics and caching. Luckily it turns out that every state combination is attainable in this particular case.

## **Installation**

```bash
git clone https://github.com/ttahelenius/ir-command-overlap-solver.git
```

Note: Python 3.9+ required.

## **Usage**

The three LED devices denoted as backled, frontled and potled[^1] can take various color modes such as r, g, b, r2, g2, b2 etc. denoting different shades of red, green and blue. They can also be on, off, paused etc. or in some other more dynamic modes. These should be used to denote the initial and desired states.

In its most basic form one could run:
```bash
Python main.py (initial state) (desired state)
```
For example
```bash
Python main.py "backled b5, frontled g2, potled r2" "backled b5, frontled g, potled r4, backled off"
```

Refer to the code comments in main.py etc. for more information.

[^1]: As in LED strips on the back and front of my desk and spotlights in the pot for my palm tree.

## **Adaptability**

Unfortunately this solution is for an extremely specific circumstance. Even if you'd have three other devices with the exact same options for modes and commands, the command overlap would probably vary wildly from the one encoded here and would require a lot of work to rewrite the logic.

# rioctrl- a modular hardware for riocore

rioctrl is modular open source CNC controller hardware for [riocore](https://github.com/multigcs/riocore/).

It consists of a main FPGA controller board which has 6 slots for various input/output modules.

At this time, the following modules have been designed:

* [rioctrl-controller](rioctrl-controller/README.md): Lattice ECP5 based controller board
* [rioctrl-stepdir4](rioctrl-stepdir4/README.md): 4 axis step/dir output interface
* [rioctrl-quadenc4](rioctrl-quadenc4/README.md): 4 axis quadrature encoder (ABZ) input
* [rioctrl-shifio](rioctrl-shiftio/README.md): 16 digital inputs, 16 digital outputs (PNP)
* breakouts/lichuan-lc10: breakout board that allows connecting Lichuan LC10 series servo to stepdir4 and quadenc4 module (via off-the-shelf RJ45 cables)
* breakouts/rj45-screw-terminals: breakout board from RJ45 cable to screw terminals
* breakouts/ditron-dc11-encoder: breakout board from RJ45 cable to Ditron DC11 glass scale optical encoder (DB9)

# Current state of the hardware design

The following hardware has been built and tested to be working:

* rioctrl-controller v1.0: minor rework was needed (remove a diode, rotate Y1 by 90 degrees). Fixed in v1.1.
* rioctrl-stepdir4 v1.0: electrically working, mechanically a connector was offset by 4 mm, fixed in v1.1.
* rioctrl-shiftio: working as designed.
* breakouts/rj45-screw-terminals: working as designed.

# Pretty images

### rioctrl-controller
![rioctrl-controller](rioctrl-controller/outputs/rioctrl-controller-v1.1/board.png)

### rioctrl-stepdir4
![rioctrl-stepdir4](rioctrl-stepdir4/outputs/rioctrl-stepdir4-v1.0/board.png)

### rioctrl-quadenc4
![rioctrl-quadenc4](rioctrl-quadenc4/outputs/rioctrl-quadenc4-v1.0/board.png)

### rioctrl-shiftio
![rioctrl-shiftio](rioctrl-shiftio/outputs/rioctrl-shiftio-v1.0/board.png)

### breakouts/lichuan-lc10
![breakouts/lichuan-lc10](breakouts/lichuan-lc10/outputs/lichuan-lc10-v1.0/board.png)

### breakouts/rj45-screw-terminals
![breakouts/rj45-screw-terminals](breakouts/rj45-screw-terminals/outputs/rj45-screw-terminals-v1.0/board.png)

## build.py

There is a `build.py` script that publishes outputs to each module `outputs` directory. It uses `<module>/version` file to
determine the current version, which should be updated accordingly.

For 3D renders of the boards, kicad-nightly package is needed, as the currently stable kicad version does not have board rendering functionality available from command line.
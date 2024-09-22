# rioctrl-stepdir4
![rioctrl-stepdir4](outputs/rioctrl-stepdir4-v1.0/board.png)

This module provides 4 axis of step/dir/enable signals.
* Step/dir signals are differential 5V.
* Enable signal is at the same voltage as controller's DC input.

The connectors are RJ45 (intended use is either with motor-drive specific breakout board or a generic screw-terminal type breakout board).

RJ45 green LED is wired to enable signal.

## Pinout (when using breakouts/rioctrl-rj45-breakout):

| Pin | Signal |
|-----|--------|
| 1   | Step + |
| 2   | Step - |
| 3   | Dir -  |
| 4   | Enable |
| 5   | GND    |
| 6   | Dir -  |
| 7   | GND    |
| 8   | GND    |

# Changelog

## v1.1
* Fixed slot's pin-header position (was offset by 4 mm)
* Rename silkscreen labels from axis 1..4 to join 0..3 to match riocore/LinuxCNC convention
 
## v1.0
Initial released version.

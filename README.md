rioctrl- a modular hardware for riocore

This project contains several PCBs in the same project:
* rioctrl-controller: main FPGA controller board + backplane
* rioctrl-stepdir: 3 axis step/dir output interface
* rioctrl-quadenc: 3 axis quadrature encoder input
* rioctrl-directin: 10 fast inputs (directly connected to FPGA)
* rioctrl-shifio: 12 in, 12 out, slow-ish IO (via shift register)
* rioctrl-shiftin: 24 slow-ish inputs (via shift register)
* rioctrl-shiftout: 24 slow-ish outputs (via shift register)

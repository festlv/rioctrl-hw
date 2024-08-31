#!/usr/bin/env python
#generates riocore slot description from netlist

from sexp_parser import *
import re
import logging
import json
regex = r"FPGA\/S([ABCDEF])(\d+)"


if __name__ == "__main__":
    with (open("outputs/rioctrl-controller-v1.0/netlist-rioctrl-controller.net", "r") as f):
        # this code is very dirty, it relies on kicad netlist exporter not changing the order of expressions
        expressions = parseSexp(f.read())
        nets = expressions[-1]
        assert(nets[1] == "nets")

        slot_letters = "ABCDEF"
        slots = {}
        for ch in slot_letters:
            slots[ch] = {}

        for net in nets:
            if type(net) is not list:
                continue
            netname = net[3][-1]

            matches = re.findall(regex, netname)
            if matches:
                slot, num = matches[0]
                pin = None
                for node in net:
                    if type(node) is list:
                        if node[2][2] == '"U9"':
                            pin = node[3][2].strip('"')
                assert(pin)
                logging.debug(f"slot: {slot}, {num}={pin}")
                slots[slot][num] = pin

    # prepare a list of dictionaries
    json_slots = []
    for slot, pins in slots.items():
        jobj = {
            "name": f"Slot{slot}",
            "comment": f"Slot{slot}",
            "pins": {}}
        for pin_num, fpga_pin in pins.items():
            jobj["pins"][f"P{pin_num}"] = fpga_pin
        json_slots.append(jobj)
    print(json.dumps(json_slots, indent=4))

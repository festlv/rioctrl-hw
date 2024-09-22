#!/usr/bin/env python
import logging
import sys
from pathlib import Path
import subprocess

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("build")

class BuildException(Exception):
    pass

boards = ["rioctrl-controller", "rioctrl-quadenc4", "rioctrl-stepdir4", "rioctrl-shiftio",
          "breakouts/rj45-screw-terminals", "breakouts/lichuan-lc10", "breakouts/ditron-dc11-encoder"]

def run_cmd(command:str, args: list):
    cmd = [command] + args
    ret = subprocess.run(cmd, capture_output=True)
    log.debug(f"Executing {cmd}...")
    log.debug(ret.stdout.decode("utf-8"))
    if ret.returncode != 0:
        log.info(ret.stdout.decode("utf-8"))
        log.error(ret.stderr.decode("utf-8"))
        raise BuildException(f"{command} failed")


def run_kicad_cli(args: list):
    return run_cmd("kicad-cli", args)

def run_kicad_nightly_cli(args: list):
    return run_cmd("kicad-cli-nightly", args)


def run_kikit(args: list):
    return run_cmd("kikit", args)

def run_ibom(args: list):
    return run_cmd("generate_interactive_bom", args)



def build_project(project: str) -> int:
    log.info(f"Building {project}")
    projname = project
    if "/" in projname:
        projname = projname.split("/")[-1]

    projpath = Path(project)
    if not projpath.exists():
        raise BuildException(f"Directory for {project} does not exist")
    verpath = projpath / "version"
    if not verpath.exists():
        raise BuildException(f"{verpath} does not exist")

    version = open(verpath.absolute()).read().strip()
    log.info(f"Version: {version}")

    reloutpath = Path("outputs") / f"{projname}-v{version}"
    outpath = projpath / reloutpath
    log.info(f"Outputs path: {outpath}")
    outpath.mkdir(exist_ok=True, parents=True)

    pcbpath = projpath / f"{projname}.kicad_pcb"
    schpath = projpath / f"{projname}.kicad_sch"

    # perform ERC
    run_kicad_cli(["sch", "erc", "--exit-code-violations", "-o", outpath / "sch-erc.rpt",
                   "-D", f"VERSION={version}", schpath])
    # perform DRC
    run_kicad_cli(["pcb", "drc", "--schematic-parity", "--exit-code-violations", "-o", outpath / "pcb-drc.rpt",
                   "-D", f"VERSION={version}", pcbpath])
    # plot schematic
    run_kicad_cli(["sch", "export", "pdf", "-o", outpath / f"schematic-{projname}.pdf",
                   "-D", f"VERSION={version}", schpath])

    # netlist for semi-automated riocore slot descriptions
    netlist_fname = outpath / f"netlist-{projname}.net"
    run_kicad_cli(["sch", "export", "netlist", "-o", netlist_fname, schpath])

    # export STEP of the model
    run_kicad_cli(["pcb", "export", "step", "--subst-models", "--no-dnp", "-o", outpath / f"{projname}.step",
                   "-D", f"VERSION={version}", pcbpath])

    # export BOM
    run_kicad_cli(["sch", "export", "bom", "-o", outpath / f"bom-{projname}.csv",
                   "--fields", "Reference,Value,Footprint,Manufacturer,MPN,${QUANTITY},${DNP},LCSC#",
                   "--labels", "Refs,Value,Footprint,Manufacturer,MPN,Qty,DNP,LCSC#",
                   "--group-by", "Value,Footprint",
                   schpath])
    # kikit jlcpcb gerbers&drills
    run_kikit(["fab", "jlcpcb", "--field", "LCSC#", "--nametemplate", projname + "-{}", "--no-drc", "--missingWarn", pcbpath, outpath / "jlcpcb"])

    # 3d render (needs nightly build of kicad with this functionality)
    run_kicad_nightly_cli(["pcb", "render", "--zoom", "0.8", "-o", outpath / "board.png", "-D",
                           f"VERSION={version}", pcbpath])

    # generate ibom
    run_ibom(["--dest-dir", reloutpath, "--extra-fields", "LCSC#", "--netlist-file", netlist_fname,
              "--no-browser", pcbpath])

    return 0


if __name__ == "__main__":
    ret = -1
    if len(sys.argv) > 1:
        ret = build_project(sys.argv[1])
    else:
        for proj in boards:
            ret = build_project(proj)
            if ret != 0:
                break

    sys.exit(ret)


#!/usr/bin/env python
# encoding:utf8

"""
    DragonPy - Dragon 32 emulator in Python
    =======================================

    Based on:
        ApplePy - an Apple ][ emulator in Python:
        James Tauber / http://jtauber.com/ / https://github.com/jtauber/applepy
        originally written 2001, updated 2011
        origin source code licensed under MIT License

    :copyleft: 2013-2014 by the DragonPy team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from dragonpy.utils.logging_utils import log
from dragonpy.Dragon32.periphery_dragon import Dragon32PeripheryTkinter

class CoCoPeripheryTkinter(Dragon32PeripheryTkinter):
    """
    Some documentation links:
    
    http://www.cs.unc.edu/~yakowenk/coco/text/history.html
    http://sourceforge.net/p/toolshed/code/ci/default/tree/cocoroms/bas.asm
    http://www.lomont.org/Software/Misc/CoCo/Lomont_CoCoHardware_2.pdf
    """
    def __init__(self, cfg):
        super(CoCoPeripheryTkinter, self).__init__(cfg)
#         self.read_byte_func_map.update({
#             0xc000: self.no_dos_rom,
#         })
        self.read_word_func_map.update({
            0xfffc: self.read_NMI,
        })
        self.write_word_func_map.update({
            0xfffc: self.write_word_info,
            0xfffe: self.write_word_info,
        })
        
    def read_NMI(self, cpu_cycles, op_address, address):
        log.critical("%04x| TODO: read NMI" % op_address)
        return 0x0000
        
    def write_word_info(self, cpu_cycles, op_address, address, value):
        log.critical("%04x| write word $%04x to $%04x ?!?!" % (
            op_address, value, address
        ))
        
    def reset_vector(self, cpu_cycles, op_address, address):
#         ea = 0x8C1B
        ea = 0xA027
#         ea = 0xC000
        log.info("%04x| %04x        [RESET]" % (address, ea))
        return ea # FIXME: RESET interrupt service routine ???


def test_run_direct():
    import sys, os, subprocess
    cmd_args = [
        sys.executable,
#         "/usr/bin/pypy",
        os.path.join("..", "CoCo_test.py"),
    ]
    print "Startup CLI with: %s" % " ".join(cmd_args[1:])
    subprocess.Popen(cmd_args, cwd="..").wait()


if __name__ == "__main__":
    test_run_direct()
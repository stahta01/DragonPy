# coding: utf-8

"""
    CoCo config
    ================

    :created: 2014 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2014 by the DragonPy team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

import logging
import os

from dragonlib.api import CoCoAPI
from dragonlib.utils.logging_utils import log
from dragonpy.CoCo.mem_info import get_coco_meminfo
from dragonpy.Dragon32.config import Dragon32Cfg
from dragonpy.Dragon32.keyboard_map import get_coco_keymatrix_pia_result
from dragonpy.components.rom import ROMFile
from dragonpy.core.configs import COCO


class CoCoCfg(Dragon32Cfg):
    CONFIG_NAME = COCO
    MACHINE_NAME = "CoCo"

    # How does the keyboard polling routine starts with?
    PIA0B_KEYBOARD_START = 0xfe

    RAM_START = 0x0000

    # 1KB RAM is not runnable and raise a error
    # 2-8 KB - BASIC Interpreter will be initialized. But every
    #          statement will end with a OM ERROR (Out of Memory)
    # 16 KB - Is usable

#     RAM_END = 0x03FF # 1KB
#     RAM_END = 0x07FF # 2KB # BASIC will always raise a OM ERROR!
#     RAM_END = 0x0FFF # 4KB # BASIC will always raise a OM ERROR!
#     RAM_END = 0x1FFF # 8KB # BASIC will always raise a OM ERROR!
#     RAM_END = 0x3FFF # 16KB # usable
    RAM_END = 0x7FFF # 32KB

    ROM_START = 0x8000
    ROM_END = 0xFFFF

    """
    EXTENDED COLOR BASIC

    $a000-$bfff - 'bas13.rom'    - size: $1fff (dez.: 8191) Bytes
    $8000-$9fff - 'extbas11.rom' - size: $1fff (dez.: 8191) Bytes
    """
    ROM_START = 0x8000
    DEFAULT_ROMS = (
        ROMFile(address=0x8000, max_size=0x4000,
            filepath=os.path.join(os.path.abspath(os.path.dirname(__file__)),
                "extbas11.rom"
            )
        ),
        ROMFile(address=0xA000, max_size=0x4000,
            filepath=os.path.join(os.path.abspath(os.path.dirname(__file__)),
                "bas13.rom"
            )
        ),
    )

    def __init__(self, cmd_args):
        self.ROM_SIZE = (self.ROM_END - self.ROM_START) + 1
        self.RAM_SIZE = (self.RAM_END - self.RAM_START) + 1
        super(CoCoCfg, self).__init__(cmd_args)

        self.machine_api = CoCoAPI()

        if self.verbosity <= logging.ERROR:
            self.mem_info = get_coco_meminfo()

        self.periphery_class = None# Dragon32Periphery

        self.memory_byte_middlewares = {
            # (start_addr, end_addr): (read_func, write_func)
#             (0x0152, 0x0159): (None, self.keyboard_matrix_state),
            (0x0115, 0x0119): (self.rnd_seed_read, self.rnd_seed_write)
        }

    def rnd_seed_read(self, cycles, last_op_address, address, byte):
        log.critical("%04x| read $%02x RND() seed from: $%04x", last_op_address, byte, address)
        return byte

    def rnd_seed_write(self, cycles, last_op_address, address, byte):
        log.critical("%04x| write $%02x RND() seed to: $%04x", last_op_address, byte, address)
        return byte

    def get_initial_RAM(self):
        """
        init the Dragon RAM
        See: http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=5&t=4444
        """
        mem_FF = [0xff for _ in xrange(4)]
        mem_00 = [0x00 for _ in xrange(4)]

        mem = []
        for _ in xrange(self.RAM_SIZE / 8):
            mem += mem_FF
            mem += mem_00

        return mem

    def pia_keymatrix_result(self, char_or_code, pia0b):
        return get_coco_keymatrix_pia_result(char_or_code, pia0b, auto_shift=True)


config = CoCoCfg


def test_run():
    import sys, os, subprocess
    cmd_args = [
        sys.executable,
        os.path.join("..", "CoCo_test.py"),
    ]
    print "Startup CLI with: %s" % " ".join(cmd_args[1:])
    subprocess.Popen(cmd_args, cwd="..").wait()

if __name__ == "__main__":
    test_run()

# -*- coding: utf-8 -*-
# video helpers

import re
import os
import time
from datetime import datetime
from subprocess import Popen, PIPE
import glob
import shutil

def run_shell_command(command, error_text, print_command=True, ignore_errors=False):
    """Execute external command"""

    p1 = Popen(
        command,
        stdout=PIPE,
        stderr=PIPE,
        shell=True,
        env={"PATH": "/usr/local/bin:/usr/bin:/bin"},
        universal_newlines=True,
    )
    output, err = p1.communicate()
    if print_command:
        print(("Command: %s" % command))
    if "avconv" or "ffmpeg" in command:
        pass  # avconv almost everytime return non zero
        # I should add custom error parser for avconv
        print(output, err)
    else:
        if err or "error" in output.lower() or "failed" in output.lower():
            if not ignore_errors:
                print(output, err)
            return False
    if output:
        return output
    else:
        return err


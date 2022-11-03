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


def get_video_info(video_path):
    """Extract some basic information from video file

    Return dict {'duration':duration, 'size':size}, where
    duration is movie lenght in seconds
    and size is a list of width and height (like [320, 240])"""

    command = "avconv -i %s 2>&1" % (video_path)
    output = run_shell_command(command, "Get video info", ignore_errors=True)
    if "Invalid data" in output:
        print("Possibly broken file")
        return False
    duration_re = re.compile(r"Duration: (\d{2}):(\d{2}):(\d{2})")
    # print "output [%s]:::::\n" % output
    duration_list = duration_re.findall(output)[0]
    duration = (
        int(duration_list[0]) * 60 * 60
        + int(duration_list[1]) * 60
        + int(duration_list[2])
    )
    size_re = re.compile(r", (\d{2,4})x(\d{2,4})")
    size = size_re.findall(output)[0]
    return {"duration": duration, "size": size}



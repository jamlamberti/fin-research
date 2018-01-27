"""A simple set of utilities"""

import os
import errno


def make_dir(direc):
    """
    Ensure a given directory exists
    """
    try:
        os.makedirs(direc)
    except OSError as err:
        if err.errno != errno.EEXIST:
            raise

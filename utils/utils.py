import sys
import os

def resource_path(relative_path):
    """
    Returns correct path whether running as script or as PyInstaller exe.
    """
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

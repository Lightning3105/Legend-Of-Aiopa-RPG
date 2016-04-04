#!/usr/bin/env python3

import sys
try:
    from cx_Freeze import setup, Executable
except ImportError:
    import urllib.request
    urllib.request.urlretrieve("http://socket-lightning3105.rhcloud.com/dl-cx_freeze", "cx_Freeze.zip")
    from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
includefiles = ["Resources/", "Saves/", "extraDLLs/libogg.dll", "extraDLLs/libvorbis.dll", "extraDlls/libvorbisfile.dll"]
packages = ["Multiplayer"]
build_exe_options = {'include_files':includefiles, 'packages':packages}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

target = Executable(
           # what to build
           script = "runGame.py",
           initScript = None,
           base = "Win32GUI",
           targetName = "LOARPG.exe",
           compress = True,
           copyDependentFiles = True,
           appendScriptToExe = False,
           appendScriptToLibrary = False,
           icon = "Resources/Images/Icon.ico"
  )



setup(  name = "Aiopa RPG",
        version = "0.1",
        description = "The Legend Of Aiopa 2D RPG.",
        author = "James",
        options = {"build_exe": build_exe_options},
        executables = [target])

# Elex 2 modding scripts

Contains bunch of scripts I created to speed up development of Elex 2 mods. Most of the scripts require elex2resman.exe.

Scripts:

* elex2_pak2doc.py - unpacks all \*.pak files from Elex 2 directory and converts those that are supported by elex2resman

## Before you start

1. Install Python 3.11 or higher
2. Edit config.json to configure scripts:
    * elex2resman_path - global path to where elex2resman is (including \*.exe name, with `/` instead of '\')
    * debug_level - set how much debug information should be written to console (0 will disable debug information,
      2 will print all debug information)
    * overwrite - decides if scripts should try to overwrite files previously created by them
    * max_threads - defines maximum number of threads that can be used by the script for simultaneous job

For more details about config.json check util/config.py

## Usage

### elex2_pak2doc.py

Drag Elex 2 folder and drop it on elex2_pak2.py. Inside that folder there will be new directory `unpacked` with all
content unpacked from \*.pak files, some of it converted to files that can be edited with commonly used programs (for
example \*doc files can be edited with any text editor).

Alternatively you can call program with command line. Pass Elex 2 installation directory as first argument, directory
where you want to `unpacked` folder with results of unpacking and conversion.

Example:

```cmd
python C:\modding\Elex_2\scripts\elex2_pak2doc.py "C:\Program Files (x86)\Steam\steamapps\common\ELEX2" "C:\modding\Elex_2"
```

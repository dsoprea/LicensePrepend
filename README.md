Introduction
------------

This is a tool that makes sure every matching file has a license-stub at the 
top, and works like a reasonable developer would expect it to.


Features
--------

- Only change files that don't already have the stub (idempotency).
- The license template can have replaceable tokens (e.g. "YEAR" is defined by 
  default).
- The license can be inserted after the last occurence of a line containing a 
  configurable list of strings (e.g. #!/bin/sh, <?php).
- The modified files are printed to *stdout*. These can be used to feed your VC
  (*git*, *svn*, etc..) and autocommit the changes.
- Changed files can be filtered by extension.
- Recursion can be turned off.
- Files and directories can be ignored by name (e.g. '<ins>&nbsp;&nbsp;</ins>init<ins>&nbsp;&nbsp;</ins>.py', '.svn').
- By default, it operates on the current directory.
- There is a full test-suite.


Installation
------------

```
sudo pip install plicense
```


Usage
-----

This is the minimum command-line:

```
plicense <license file-path>
```

This will recursively process every file in the current directory.

Because your projects will often include files that will be excluded (like 
__init__.py for Python projects, or .git/.svn/etc.. for version-control), 
or extensionless files that will be included, you will often need to do at 
least a couple of passes. 

For example, in order for me to install the license stubs in my 
[beantool](https://github.com/dsoprea/BeanTool) project, I needed to execute 
the following steps. You can use the table below as a reference for the 
command-line options.

1. Process my scripts/ directory. The files in this directory don't have
   extensions. However, I can't run *plicense* over the whole tree, or I'll be
   including *virtualenv* and *git* files, which should be ignored.

   ```
   beantool$ plicense -p scripts -r author "Dustin Oprea" LICENSE_STUB 
   scripts/bt
   (1)/(1) directories scanned.
   (1)/(1) files scanned.
   (1)/(1) of the found files needed the stub.
   ```

   The top portion of the script now looks like:

   ```python
   #!/usr/bin/env python2.7

   # beantool: Beanstalk console client.
   # Copyright (C) 2014  Dustin Oprea
   # 
   # This program is free software; you can redistribute it and/or
   # modify it under the terms of the GNU General Public License
   # as published by the Free Software Foundation; either version 2
   # of the License, or (at your option) any later version.


   import sys
   sys.path.insert(0, '..')

   import argparse
   ```
2. Process the Python files in the rest of the tree.

   ```
   beantool$ plicense -p beantool -e py -r author "Dustin Oprea" -f __init__.py LICENSE_STUB 
   beantool/job_terminal.py
   beantool/handlers/handler_base.py
   beantool/handlers/job.py
   beantool/handlers/server.py
   beantool/handlers/tube.py
   (2)/(2) directories scanned.
   (5)/(7) files scanned.
   (5)/(5) of the found files needed the stub.
   ```

   If you run it again, you'll see that nothing is done:

   ```
   beantool$ plicense -p beantool -e py -r author "Dustin Oprea" -f __init__.py LICENSE_STUB 
   (2)/(2) directories scanned.
   (5)/(7) files scanned.
   (0)/(5) of the found files needed the stub.
   ```


Interesting Command-Line Options
--------------------------------

A complete description of the command-line arguments can be found by using 
"-h".

| Parameter                    | Value            | Default  | Description                                                                        | Allow Multiple |
| ---------------------------- | ---------------- | -------- | ---------------------------------------------------------------------------------- |:--------------:|
| -e, --extension              | <ext>            |          | Filter by extension                                                                |                |
| -i, --indicator              | <string>         | opyright | What to look for at the top of the file if a stub is already present               |                |
| -l, --max-lines              | <n>              | 10       | The number of lines at the top of the sourcecode to check for the indicator        |                |
| -a, --insert-after           | <string>         | #!/      | If this exists at the top of the file, insert the license after rather than before | X              |
| -m, --insert-after-max-lines | <n>              | 10       | The number of lines at the top to check for insert-after strings                   |                |
| -r, --replace                | <key> <value>    |          | Do a string-replacement into the license text (will be prefixed with '$')          | X              |
| -p, --path                   | <path>           | <cwd>    | Path to use (defaults to current)                                                  |                |
| -c, --no-recursion           |                  |          | Don't print the files being updated                                                |                |
| -f, --ignore-file            | <filename>       |          | Don't process this file                                                            | X              |
| -g, --ignore-directory       | <directory name> |          | Don't process this directory                                                       | X              |

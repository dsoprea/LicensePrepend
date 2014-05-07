Introduction
------------

This is a tool that makes sure every matching file has a license-stub at the 
top, and works like a reasonable developer would expect it to.


Features
--------

- Only change files that don't already have the stub.
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
------------

This is the minimum command-line:

```
plicense <license file-path>
```

This will recursively process every file in the current directory.


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

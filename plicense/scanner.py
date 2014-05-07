import sys
import os
import os.path
import logging
import pprint

_logger = logging.getLogger(__name__)


class Scanner(object):
    def __init__(self, path, indicator, line_check_quantity, is_recursive, 
                 ignore_files, ignore_directories, is_no_stats, 
                 extension=None):

        if os.path.isdir(path) is False:
            raise ValueError("Path is not a directory.")

        self.__path = path
        self.__indicator = indicator
        self.__line_check_quantity = line_check_quantity
        self.__is_recursive = is_recursive
        self.__ignore_files = ignore_files
        self.__ignore_directories = ignore_directories
        self.__is_no_stats = is_no_stats
        self.__extension = '.' + extension.lower() \
                            if extension is not None \
                            else None

    def __dump(d):
        raw = d.encode('ASCII')
        import sys
        buf = "DUMP> "
        for c in raw:
            buf += " %s(%02X)" % (chr(c), c)

        buf += "\n"
        return buf

    def scan(self):
        _logger.debug("Scanning. Ignore directories:\n%s", self.__ignore_directories)

        dirs = 0
        files = 0
        excluded_dirs = 0
        excluded_files = 0
        havestub = 0
        for (root, child_dirs, child_files) in os.walk(self.__path):
            _logger.debug("Scanning path: %s", root)

            if self.__is_recursive is False and dirs > 0:
                break

            dirs += 1

            path_name = os.path.basename(root)
            ignored = False
            for ignored_path in self.__ignore_directories:
                if path_name.startswith(ignored_path) is False:
                    continue

                excluded_dirs += 1
                _logger.debug("Path is excluded: [%s] => [%s]", 
                              root, path_name)

                ignored = True
                break

            if ignored is True:
                continue

            for filename in child_files:
                if self.__extension is not None and \
                    os.path.splitext(filename)[1].lower() != self.__extension or \
                   filename in self.__ignore_files:
                    excluded_files += 1
                    _logger.debug("File is excluded: [%s]", filename)

                    continue
                else:
                    files += 1

                filepath = os.path.join(root, filename)
                _logger.debug("Scanning: [%s]", filepath)

                buffered = []
                with open(filepath) as f:
                    i = 0
                    found = False
                    for row in f:
                        buffered.append(row)

                        if i >= self.__line_check_quantity:
                            break

                        if self.__indicator in row:
                            found = True
                            _logger.debug("Found license indicator on line "
                                          "(%d)." % (i))

                            break
                        else:
                            _logger.debug("DID NOT find license indicator "
                                          "[%s] on line (%d): [%s]" % 
                                          (self.__indicator, i, row))

                        i += 1

                    if found is True:
                        havestub += 1
                        _logger.debug("File already has the stub on line "
                                      "(%d)." % (i))

                        continue

                    _logger.debug("File needs stub. Reading remaining lines.")

                    while True:
                        row = f.readline()
                        if row == '':
                            break

                        buffered.append(row)

                    yield (filepath, buffered)

        if self.__is_no_stats is False:
            sys.stderr.write("(%d)/(%d) directories scanned.\n" % (dirs, dirs + excluded_dirs))
            sys.stderr.write("(%d)/(%d) files scanned.\n" % (files, files + excluded_files))
            sys.stderr.write("(%d)/(%d) of the found files already had the stub.\n" % (havestub, files))

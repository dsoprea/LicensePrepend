import sys
import os
import os.path


class Scanner(object):
    def __init__(self, path, indicator, line_check_quantity, is_recursive, 
                 ignore_files, ignore_directories, extension=None):
        self.__path = path
        self.__indicator = indicator
        self.__line_check_quantity = line_check_quantity
        self.__is_recursive = is_recursive
        self.__ignore_files = ignore_files
        self.__ignore_directories = ignore_directories
        self.__extension = '.' + extension.lower() \
                            if extension is not None \
                            else None

    def scan(self):
        dirs = 0
        files = 0
        excluded_dirs = 0
        excluded_files = 0
        havestub = 0
        for (root, child_dirs, child_files) in os.walk(self.__path):
            if self.__is_recursive is False and dirs > 0:
                break

            dirs += 1

            if os.path.basename(root) in self.__ignore_directories:
                excluded_dirs += 1
                continue

            for filename in child_files:
                if self.__extension is not None and \
                    os.path.splitext(filename)[1].lower() != self.__extension or \
                   filename in self.__ignore_files:
                    excluded_files += 1
                    continue
                else:
                    files += 1

                filepath = os.path.join(root, filename)

                buffered = []
                with open(filepath) as f:
                    i = 0
                    found = False
                    for row in f:
                        if i > self.__line_check_quantity:
                            break

                        if self.__indicator in row:
                            found = True
                            break

                        buffered.append(row)
                        i += 1

                    if found is True:
                        havestub += 1
                        continue

                    while True:
                        row = f.readline()
                        if row == '':
                            break

                        buffered.append(row)

                    yield (filepath, buffered)

        sys.stderr.write("(%d)/(%d) directories scanned.\n" % (dirs, dirs + excluded_dirs))
        sys.stderr.write("(%d)/(%d) files scanned.\n" % (files, files + excluded_files))
        sys.stderr.write("(%d)/(%d) of the found files already had the stub.\n" % (havestub, files))

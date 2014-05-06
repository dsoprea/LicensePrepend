import logging

_logger = logging.getLogger(__name__)


class Injector(object):
    def __init__(self, license_lines, insert_after=[], insert_after_max_lines=10):
        (self.__license_lines, self.__nl) = license_lines

        self.__insert_after = insert_after
        self.__insert_after_max_lines = insert_after_max_lines

        _logger.debug("Injector initialized with a license of (%d) lines.", 
                      len(self.__license_lines))

    def __get_insert_index(self, lines):
        insert_at = 0

        i = 0
        for line in lines:
            if any([(candidate in line) for candidate in self.__insert_after]) is True:
                insert_at = i + 1
                _logger.debug("Inserting, at least, after line (%d).", insert_at)

            if i >= self.__insert_after_max_lines:
                break

            i += 1

        return insert_at

    def prepend(self, lines):
        insert_index = self.__get_insert_index(lines)
        lines[insert_index:insert_index] = ([self.__nl] if insert_index > 0 else []) + self.__license_lines

        print(''.join(lines))

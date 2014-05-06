import os.path
import subprocess
import tempfile
import shutil
import string
import datetime

import unittest

_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'pl')

_LICENSE = \
"""# I am a license
# Copyright $YEAR
"""

_REPLACED_LICENSE = string.Template(_LICENSE).substitute({ 
                            'YEAR': datetime.datetime.now().strftime('%Y') 
                        })

class _TestCaseBase(unittest.TestCase):
    def setUp(self):
        self.path = tempfile.mkdtemp()

        license_res = tempfile.NamedTemporaryFile()
        license_res.write(_LICENSE)
        license_res.flush()

        self.license_res = license_res

    def tearDown(self):
        self.license_res.close()
        shutil.rmtree(self.path)

    def run_cmd(self, options):
        cmd = [_SCRIPT_PATH, self.license_res.name, '--path', self.path, '--no-stats'] + options
        
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        r = p.wait()
        output = p.stdout.read()

        if r != 0:
            print(output)
            raise ValueError("The command returned failure.")

        return output

class TestGeneral(_TestCaseBase):
    def test_license_add(self):
        source_filepath = os.path.join(self.path, 'sourcecode')
        with open(source_filepath, 'w') as f:
            pass

        raw_output = self.run_cmd([])

        output = raw_output.rstrip()
        self.assertEqual(source_filepath, output)

        with open(source_filepath) as f:
            modified_source = f.read()
            self.assertEqual(_REPLACED_LICENSE + "\n", modified_source)

    def test_license_already_added(self):
        source_filepath = os.path.join(self.path, 'sourcecode')
        with open(source_filepath, 'w') as f:
            pass

        raw_output = self.run_cmd([])
        raw_output = self.run_cmd([])

        output = raw_output.rstrip()
        self.assertEqual('', output)

        with open(source_filepath) as f:
            modified_source = f.read()
            self.assertEqual(_REPLACED_LICENSE + "\n", modified_source)
#
#    def test_extension_option(self):
#        raise NotImplementedError()
#
#    def test_no_changes_option(self):
#        raise NotImplementedError()
#
#    def test_quiet_option(self):
#        raise NotImplementedError()
#
#    def test_indicator_option(self):
#        raise NotImplementedError()
#
#    def test_max_lines_option(self):
#        raise NotImplementedError()
#
#    def test_insert_after_option(self):
#        raise NotImplementedError()
#
#    def test_insert_after_max_lines_option(self):
#        raise NotImplementedError()
#
#    def test_replace_option(self):
#        raise NotImplementedError()
#
#    def test_no_recursion_option(self):
#        raise NotImplementedError()
#
#    def test_ignore_files_option(self):
#        raise NotImplementedError()
#
#    def test_ignore_directories_option(self):
#        raise NotImplementedError()

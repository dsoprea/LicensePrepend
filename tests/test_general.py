import os.path
import subprocess
import tempfile
import shutil
import string
import datetime
import logging

import unittest

_SCRIPT_PATH = os.path.join(
                os.path.dirname(__file__), 
                '..', 
                'scripts', 
                'plicense')

_LICENSE = \
"""# I am a license
# Copyright $YEAR
"""

def _get_license(**kwargs):
    replacements = dict([(k.upper(), v) for (k, v) in kwargs.items()])
    return string.Template(_LICENSE).substitute(replacements)

_YEAR = datetime.datetime.now().strftime('%Y')
_REPLACED_LICENSE = _get_license(year=_YEAR)
_logger = logging.getLogger(__name__)


class _TestCaseBase(unittest.TestCase):
    def setUp(self):
        self.path = tempfile.mkdtemp()
        self.write_license(_LICENSE)

    def tearDown(self):
        self.license_res.close()
        shutil.rmtree(self.path)

    def run_cmd(self, options, success_code=0):
        cmd = [_SCRIPT_PATH, 
               self.license_res.name, 
               '--path', self.path, 
               '--no-stats'] + \
              options
        
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        r = p.wait()
        output = p.stdout.read()

        if success_code is not None and r != success_code:
            print(output)
            raise ValueError("The command returned failure.")

        return output

    def run_cmd_return_all(self, options, success_code=0):
        cmd = [_SCRIPT_PATH, 
               self.license_res.name, 
               '--path', self.path, 
               '--no-stats'] + \
              options
        
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        r = p.wait()
        output = p.stdout.read()
        err = p.stderr.read()

        if success_code is not None and r != success_code:
            print(output)
            print(err)
            raise ValueError("The command returned failure.")

        return (output, err)

    def write_license(self, content):
        self.license_res = tempfile.NamedTemporaryFile()
        self.license_res.write(content)
        self.license_res.flush()

    def dump(self, d):
        return "DUMP> " + (' '.join([x.encode('hex') for x in d])) + "\n"


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

    def test_extension_option__hit(self):
        source_filepath = os.path.join(self.path, 'sourcecode.py')
        with open(source_filepath, 'w') as f:
            pass

        raw_output = self.run_cmd(['--extension', 'py'])

        output = raw_output.rstrip()
        self.assertEqual(source_filepath, output)

    def test_extension_option__miss(self):
        source_filepath = os.path.join(self.path, 'sourcecode')
        with open(source_filepath, 'w') as f:
            pass

        raw_output = self.run_cmd(['--extension', 'py'])
        self.assertEqual('', raw_output)

    def test_no_changes_option(self):
        source_filepath = os.path.join(self.path, 'sourcecode')
        with open(source_filepath, 'w') as f:
            pass

        raw_output = self.run_cmd(['--no-changes'])

        output = raw_output.rstrip()
        self.assertEqual(source_filepath, output)

        with open(source_filepath) as f:
            self.assertEqual('', f.read())

    def test_quiet_option(self):
        source_filepath = os.path.join(self.path, 'sourcecode')
        with open(source_filepath, 'w') as f:
            pass

        raw_output = self.run_cmd(['--quiet'])
        self.assertEqual('', raw_output)

    def test_indicator_option(self):
        source_filepath = os.path.join(self.path, 'sourcecode')
        with open(source_filepath, 'w') as f:
            f.write('#Already here\n')

        raw_output = self.run_cmd(['--indicator', 'Already here'])
        self.assertEqual('', raw_output)

    def test_max_lines_option__hit(self):
        source_filepath = os.path.join(self.path, 'sourcecode')
        with open(source_filepath, 'w') as f:
            f.write('\n')
            f.write('#Already here\n')

        raw_output = self.run_cmd([
            '--indicator', 
            'Already here', 
            '--max-lines', 
            '2'])

        self.assertEqual('', raw_output)

    def test_max_lines_option__miss(self):
        source_filepath = os.path.join(self.path, 'sourcecode')
        with open(source_filepath, 'w') as f:
            f.write('\n')
            f.write('#Already here\n')

        raw_output = self.run_cmd([
            '--indicator', 
            'Already here', 
            '--max-lines', 
            '1'])

        output = raw_output.rstrip()
        self.assertEqual(source_filepath, output)

    def test_insert_after_option(self):
        source_filepath = os.path.join(self.path, 'sourcecode')
        source_content = "\n#Insert after\n"
        with open(source_filepath, 'w') as f:
            f.write(source_content)

        raw_output = self.run_cmd(['--insert-after', 'Insert after'])
        output = raw_output.rstrip()
        self.assertEqual(source_filepath, output)

        with open(source_filepath) as f:
            modified_source = f.read()

        self.assertEqual(source_content + "\n" + _REPLACED_LICENSE + "\n", 
                         modified_source)

    def test_insert_after_max_lines_option__hit(self):
        source_filepath = os.path.join(self.path, 'sourcecode')
        with open(source_filepath, 'w') as f:
            f.write('\n')
            f.write('#Marker\n')

        raw_output = self.run_cmd([
            '--insert-after', 
            'Marker', 
            '--insert-after-max-lines', 
            '2'])

        output = raw_output.rstrip()
        self.assertEqual(source_filepath, output)

        with open(source_filepath) as f:
            modified_source = f.read()

        self.assertEqual("\n#Marker\n\n" + _REPLACED_LICENSE + "\n", 
                         modified_source)

    def test_insert_after_max_lines_option__miss(self):
        source_filepath = os.path.join(self.path, 'sourcecode')
        source_content = '\n#Marker\n'
        with open(source_filepath, 'w') as f:
            f.write(source_content)

        raw_output = self.run_cmd([
            '--insert-after', 
            'Marker', 
            '--insert-after-max-lines', 
            '0'])

        output = raw_output.rstrip()
        self.assertEqual(source_filepath, output)

        with open(source_filepath) as f:
            modified_source = f.read()

        self.assertEqual(_REPLACED_LICENSE + "\n" + source_content, 
                         modified_source)

    def test_replace_option__hit(self):
        LICENSE_TEMPLATE = _LICENSE + "$TEST_REPLACE\n"
        self.write_license(LICENSE_TEMPLATE)

        source_filepath = os.path.join(self.path, 'sourcecode')
        with open(source_filepath, 'w') as f:
            pass

        raw_output = self.run_cmd(['--replace', 'test_replace', '1234'])

        output = raw_output.rstrip()
        self.assertEqual(source_filepath, output)

        with open(source_filepath) as f:
            modified_source = f.read()

        _LICENSE_TEMP = string.Template(LICENSE_TEMPLATE).substitute(
                            YEAR=_YEAR, TEST_REPLACE='1234')

        self.assertEqual(_LICENSE_TEMP + "\n", modified_source)

    def test_replace_option__miss(self):
        LICENSE_TEMPLATE = _LICENSE + "$TEST_REPLACE\n"
        self.write_license(LICENSE_TEMPLATE)

        source_filepath = os.path.join(self.path, 'sourcecode')
        with open(source_filepath, 'w') as f:
            pass

        (output, err) = self.run_cmd_return_all([], success_code=None)
        self.assertTrue("KeyError: 'TEST_REPLACE'" in err)

    def test_no_recursion_option(self):
        inside_path = os.path.join(self.path, 'inside')
        os.mkdir(inside_path)

        source_filepath = os.path.join(self.path, 'sourcecode')
        with open(source_filepath, 'w') as f:
            pass

        source_filepath2 = os.path.join(self.path, 'inside', 'sourcecode2')
        with open(source_filepath2, 'w') as f:
            pass

        raw_output = self.run_cmd(['--no-recursion'])

        output = raw_output.rstrip()
        self.assertEqual(source_filepath, output)

    def test_ignore_files_option(self):
        filename = 'sourcecode'

        source_filepath = os.path.join(self.path, filename)
        with open(source_filepath, 'w') as f:
            pass

        raw_output = self.run_cmd(['--ignore-file', filename])

        output = raw_output.rstrip()
        self.assertEqual('', output)

    def test_ignore_directories_option(self):
        name = 'xyz'
        inner_path = os.path.join(self.path, name)
        os.mkdir(inner_path)

        source_filepath = os.path.join(inner_path, 'sourcecode')
        with open(source_filepath, 'w') as f:
            pass

        raw_output = self.run_cmd(['--ignore-directory', name])

        output = raw_output.rstrip()
        self.assertEqual('', output)

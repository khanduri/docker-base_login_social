import os
import os.path
import unittest

import pep8

# ignore stuff in virtualenvs or version control directories
ignore_patterns = ('virenv', 'migrations', 'node_module')


def ignore(dir):
    for pattern in ignore_patterns:
        if pattern in dir:
            return True
    return False


class TestPep8(unittest.TestCase):

    def test_pep8(self):
        style = pep8.StyleGuide(
            parse_argv=False,
            max_line_length=float("inf"),
        )

        errors = 0
        path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        for root, _, files in os.walk(path):
            if ignore(root):
                continue
            python_files = [os.path.join(root, f) for f in files if f.endswith('.py')]
            errors += style.check_files(python_files).total_errors

        self.assertEqual(errors, 0, 'PEP8 style errors: %d' % errors)

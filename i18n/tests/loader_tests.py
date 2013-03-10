import unittest
import os
import os.path

from i18n import resource_loader
from i18n.resource_loader import I18nFileLoadError
from i18n.config import json_available, yaml_available

RESOURCE_FOLDER = os.path.dirname(__file__) + os.sep + 'resources'


class TestFileLoader(unittest.TestCase):
    def setUp(self):
        resource_loader.loaders = {}

    def test_load_unavailable_extension(self):
        with self.assertRaisesRegexp(I18nFileLoadError, "no loader .*"):
            resource_loader.load_resource("foo.bar", "baz")

    def test_register_wrong_loader(self):
        class WrongLoader(object):
            pass
        with self.assertRaises(ValueError):
            resource_loader.register_loader(WrongLoader, [])

    def test_register_python_loader(self):
        resource_loader.init_python_loader()
        with self.assertRaisesRegexp(I18nFileLoadError, "error loading file .*"):
            resource_loader.load_resource("foo.py", "bar")

    @unittest.skipUnless(yaml_available, "yaml library not available")
    def test_register_yaml_loader(self):
        resource_loader.init_yaml_loader()
        with self.assertRaisesRegexp(I18nFileLoadError, "error loading file .*"):
            resource_loader.load_resource("foo.yml", "bar")

    @unittest.skipUnless(json_available, "json library not available")
    def test_load_wrong_json_file(self):
        resource_loader.init_yaml_loader()
        pass


suite = unittest.TestLoader().loadTestsFromTestCase(TestFileLoader)
unittest.TextTestRunner(verbosity=2).run(suite)
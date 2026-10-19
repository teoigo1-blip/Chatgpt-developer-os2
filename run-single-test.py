#!/usr/bin/env python3
"""Run unittest classes, plain test functions and legacy import assertions."""
import importlib.util
import inspect
from pathlib import Path
import sys
import unittest

path = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location(path.stem, path)
module = importlib.util.module_from_spec(spec)
sys.modules[path.stem] = module
spec.loader.exec_module(module)  # Legacy modules perform assertions on import.
suite = unittest.defaultTestLoader.loadTestsFromModule(module)
for name, value in vars(module).items():
    if name.startswith('test_') and inspect.isfunction(value) and value.__module__ == module.__name__:
        suite.addTest(unittest.FunctionTestCase(value))
if suite.countTestCases() == 0:
    suite.addTest(unittest.FunctionTestCase(lambda: None, description='Legacy module import assertions completed'))
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)

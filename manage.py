#!/usr/bin/env python
import os
from app import create_app
from flask.ext.script import Manager, Shell, Server

__author__ = 'Manuel Escriche'

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


def make_shell_context():
    return dict(app=app)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("runserver", Server(host="127.0.0.1", port=5000))


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def itest():
    import unittest
    tests = unittest.TestLoader().discover('tests', pattern='test_06.py')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run(default_command='runserver')

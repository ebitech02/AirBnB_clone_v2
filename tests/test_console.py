#!/usr/bin/python3
"""test cases for the console.py"""

import unittest
from unittest.mock import patch
from io import StringIO
import pep8
import os
import json
import console
from console import HBNBCommand
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage

class TestConsole(unittest.TestCase):
    """this will test the console"""

    @classmethod
    def setUpClass(cls):
        """setup for the test"""
        cls.consol = HBNBCommand()

    @classmethod
    def tearDownClass(cls):
        """will tear down at the end of the test"""
        del cls.consol

    def tearDown(self):
        """remove the temporary file.json created as a result"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_console(self):
        """Pep8 console.py"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(["console.py"])
        self.assertEqual(p.total_errors, 0, 'fix Pep8')

    def test_docstrings_in_console(self):
        """checking for doctsrtings"""
        self.assertIsNotNone(HBNBCommand.__doc__)
        self.assertIsNotNone(HBNBCommand.__do_quit.__doc)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)
        self.assertIsNotNone(HBNBCommand.do_show.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.do_all.__doc__)
        self.assertIsNotNone(HBNBCommand.do_update.__doc__)
        self.assertIsNotNone(HBNBCommand.help_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.help_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.help_create.__doc__)
        self.assertIsNotNone(HBNBCommand.help_show.__doc__)
        self.assertIsNotNone(HBNBCommand.help_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.help_all.__doc__)
        self.assertIsNotNone(HBNBCommand.help_update.__doc__)

    def test_emptyline(self)
    """Test empty line input"""
    with patch('sys.stdout', new=StringIO()) as f:
        self.console.onecmd("\n")
        self.assertEqual('', f.getvalue())

    def test_quit(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("quit")
            self.assertEqual('', f.getvalue())

    def test_EOF(self):
        """Test EOF command input"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("EOF")
            self.assertEqual('\n', f.getvalue())

    def test_create(self):
        """Test create command input"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create")
            self.assertEqual("** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create NonExistentClass")
            self.assertEqual("** class does not exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create user email="test@test.com" password="1234"')
            user_id = f.getvalue().strip()
            self.assertTrue(len(user_id) > 0)

    def test_show(self):
        """Test show command input"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show")
            self.assertEqual("** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show NonExistentClass")
            self.assertEqual("** class does not exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show User")
            self.assertEqual("** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show User NonExistentID")
            self.assertEqual("** no instance found **\n", f.getvalue())

    def test_destroy(self):
        """Test update command input"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update")
            self.assertEqual("** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update NonExistentClass")
            self.assertEqual("** class does not exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update User")
            self.assertEqual("** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update User NonExistentId")
            self.assertEqual("** no instance found **\n", f.getvalue())

    def test_alternate_commands(self):
        """test alternate command inputs"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("NonExistentClass.all()")
            self.assertEqual("** class does not exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("User.count()")
            self.assertEqual("0\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("NonExistentClass.count()")
            self.assertEqual("** class does not exist ** \n", f.getvalue())

    def test_update_with_args(self):
        """test with update command input"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create User email="test@test.com" password="1234"')
            user_id = f.getvalue().strip()
            self.assertTrue(len(user_id) > 0)
            self.console.onecmd(f'update User {user_id} email "updated@test.com"')
            self.console.onecmd(f'show User {user_id}')
            output = f.getvalue()
            self.assertIn('updated@test.com', output)

    def test_update_with_kwargs(self):
        """test update command with kwargs"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create User email="test@test.com" password="1234"')
            user_id = f.getvalue().strip()
            self.assertTrue(len(user_id) > 0)
            self.console.onecmd(f'update User {user_id} email="updated@test.com"')
            self.console.onecmd(f'show User {user_id}')
            output = f.getvalue()
            self.assertIn('updated@test.com', output)
if __name__ == "__main__":
    unittest.main()

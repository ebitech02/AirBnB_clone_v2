import unittest
from io import StringIO
import sys
from console import HBNBCommand
from models import storage
from models.state import State
from models.place import Place

class TestConsole(unittest.TestCase):
    def setUp(self):
        """Redirect stdout to capture printed output"""
        self.console = HBNBCommand()
        self.output = StringIO()
        sys.stdout = self.output

    def tearDown(self):
        """Reset stdout"""
        sys.stdout = sys.__stdout__

    def test_create_with_parameters(self):
        """Test create command with parameters"""
        self.console.onecmd('create State name="California"')
        output = self.output.getvalue().strip()
        self.assertTrue(len(output) > 0)
        obj = storage.all()["State." + output]
        self.assertEqual(obj.name, "California")

        self.output.seek(0)
        self.output.truncate(0)
        self.console.onecmd('create State name="Arizona"')
        output = self.output.getvalue().strip()
        self.assertTrue(len(output) > 0)
        obj = storage.all()["State." + output]
        self.assertEqual(obj.name, "Arizona")

    def test_create_place_with_parameters(self):
        """Test create command for Place with parameters"""
        self.console.onecmd('create Place city_id="0001" user_id="0001" name="My_little_house" number_rooms=4 number_bathrooms=2 max_guest=10 price_by_night=300 latitude=37.773972 longitude=-122.431297')
        output = self.output.getvalue().strip()
        self.assertTrue(len(output) > 0)
        obj = storage.all()["Place." + output]
        self.assertEqual(obj.city_id, "0001")
        self.assertEqual(obj.user_id, "0001")
        self.assertEqual(obj.name, "My little house")
        self.assertEqual(obj.number_rooms, 4)
        self.assertEqual(obj.number_bathrooms, 2)
        self.assertEqual(obj.max_guest, 10)
        self.assertEqual(obj.price_by_night, 300)
        self.assertEqual(obj.latitude, 37.773972)
        self.assertEqual(obj.longitude, -122.431297)

    def test_show(self):
        """Test show command"""
        self.console.onecmd('create State name="California"')
        state_id = self.output.getvalue().strip()
        self.output.seek(0)
        self.output.truncate(0)
        self.console.onecmd('show State ' + state_id)
        output = self.output.getvalue().strip()
        self.assertIn('California', output)

    def test_all(self):
        """Test all command"""
        self.console.onecmd('create State name="California"')
        self.console.onecmd('create State name="Arizona"')
        self.output.seek(0)
        self.output.truncate(0)
        self.console.onecmd('all State')
        output = self.output.getvalue().strip()
        self.assertIn('California', output)
        self.assertIn('Arizona', output)

    def test_destroy(self):
        """Test destroy command"""
        self.console.onecmd('create State name="California"')
        state_id = self.output.getvalue().strip()
        self.output.seek(0)
        self.output.truncate(0)
        self.console.onecmd('destroy State ' + state_id)
        self.output.seek(0)
        self.output.truncate(0)
        self.console.onecmd('show State ' + state_id)
        output = self.output.getvalue().strip()
        self.assertEqual(output, "** no instance found **")

    def test_update(self):
        """Test update command"""
        self.console.onecmd('create State name="California"')
        state_id = self.output.getvalue().strip()
        self.output.seek(0)
        self.output.truncate(0)
        self.console.onecmd('update State ' + state_id + ' name "New California"')
        self.output.seek(0)
        self.output.truncate(0)
        self.console.onecmd('show State ' + state_id)
        output = self.output.getvalue().strip()
        self.assertIn('New California', output)

if __name__ == '__main__':
    unittest.main()


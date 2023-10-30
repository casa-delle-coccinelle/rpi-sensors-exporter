import unittest

from unittest.mock import Mock, patch, mock_open
from schema import SchemaError
from os import environ

from config_loader import (
    parse_args,
    logs_setup,
    validate,
    unique_item_check,
    ads_check_device,
    gpio_pins_check,
    gpio_names_check,
    ads_inputs_check,
    ads_names_check,
    ads_dev_check,
    gpio_dev_check,
    data_check,
    load
)


class TestConfigLoader(unittest.TestCase):
    """ Tests for the config loader module """

    def setUp(self):
        print()

    def test_unique_item_check(self):
        """ Test if unique_item_check raises the correct error """
        with self.assertRaises(ValueError):
            unique_item_check(
                ['a', 'b', 'c', 'a'],
                'Test {}',
                'Test {}',
            )

        with self.assertRaises(ValueError):
            unique_item_check(
                ['a'],
                'Test {}',
                'Test {}',
                un_constraint=0
            )

        mock_notify = Mock()
        unique_item_check(
            ['a', 'b', 'c'],
            'Test1 {}',
            'Test2 {}',
            ok_messenger=mock_notify,
        )
        mock_notify.assert_called_with('Test2 c')

    def test_logs_setup(self):
        """ Test if logs_setup works """

        with (
            patch("config_loader.parse_args") as mock_args,
            patch("config_loader.logging") as mock_logging,
        ):
            mock_args.return_value = Mock(verbose=True, debug=False)
            mocked_logger = Mock()
            mock_logging.getLogger.return_value = mocked_logger
            mock_logging.INFO = 'INFO'
            mock_logging.DEBUG = 'DEBUG'
            logs_setup()
            mocked_logger.setLevel.assert_called_with(mock_logging.INFO)

        with (
            patch("config_loader.parse_args") as mock_args,
            patch("config_loader.logging") as mock_logging,
        ):
            mock_args.return_value = Mock(verbose=False, debug=True)
            mocked_logger = Mock()
            mock_logging.getLogger.return_value = mocked_logger
            mock_logging.INFO = 'INFO'
            mock_logging.DEBUG = 'DEBUG'
            logs_setup()
            mocked_logger.setLevel.assert_called_with(mock_logging.DEBUG)

        with (
            patch("config_loader.parse_args") as mock_args,
            patch("config_loader.logging") as mock_logging,
        ):
            mock_args.return_value = Mock(verbose=True, debug=True)
            mocked_logger = Mock()
            mock_logging.getLogger.return_value = mocked_logger
            mock_logging.INFO = 'INFO'
            mock_logging.DEBUG = 'DEBUG'
            logs_setup()
            mocked_logger.setLevel.assert_called_with(mock_logging.DEBUG)

    def test_parse_args(self):
        """ Test if parse_args works """

        with patch("config_loader.argparse") as mock_argparse:
            mock_argparse.ArgumentParser.return_value.parse_args.return_value = Mock(
                verbose=True, debug=False
            )
            args = parse_args()
            self.assertTrue(args.verbose)
            self.assertFalse(args.debug)

        with patch("config_loader.argparse") as mock_argparse:
            mock_argparse.ArgumentParser.return_value.parse_args.return_value = Mock(
                verbose=False, debug=True
            )
            args = parse_args()
            self.assertFalse(args.verbose)
            self.assertTrue(args.debug)

        with patch("config_loader.argparse") as mock_argparse:
            mock_argparse.ArgumentParser.return_value.parse_args.return_value = Mock(
                verbose=True, debug=True
            )
            args = parse_args()
            self.assertTrue(args.verbose)
            self.assertTrue(args.debug)

    def test_validate(self):
        """ Test if validate works """
        validate({'gpio_devices': [{'name': 'test', 'type': 'test', 'pin': 1}]})

        with self.assertRaises(SchemaError):
            validate({'gpio_devices': [{'name': 'test', 'pin': 1}]})

        with self.assertRaises(SchemaError):
            validate({'gpio_devices': [{'type': 'test', 'pin': 1}]})

        with self.assertRaises(SchemaError):
            validate({'gpio_devices': [{'type': 'test', 'pin': 'aabb'}]})

        with self.assertRaises(SchemaError):
            validate({'gpio_devices': [{'type': 'test', 'pin': 32}]})

        validate({'ads_devices': [{'name': 'test', 'type': 'test', 'analog_in': 2}]})
        with self.assertRaises(SchemaError):
            validate({'ads_devices': [{'name': 'test', 'type': 'test', 'analog_in': 4}]})

        with self.assertRaises(SchemaError):
            validate({'ads_devices': [{'name': 'test', 'type': 'test'}]})

        with self.assertRaises(SchemaError):
            validate({'ads_devices': [{'name': 'test', 'analog_in': 1}]})

        with self.assertRaises(SchemaError):
            validate({'ads_devices': [{'type': 'test', 'analog_in': 1}]})

        validate({'gpio_devices': [{'name': 'test', 'type': 'test', 'pin': 1}], 'ads_devices': [{'name': 'test', 'type': 'test', 'analog_in': 1, 'min_value': 1, 'max_value': 1}]})

    def test_ads_check_device(self):
        """ Test if ads_check_device works """

        ads_check_device({'name': 'test', 'type': 'test', 'analog_in': 2, 'min_value': 1, 'max_value': 2})

        with self.assertRaises(ValueError):
            ads_check_device("not_a_device")

        with self.assertRaises(ValueError):
            ads_check_device({'name': 'test', 'min_value': 2, 'max_value': 1})

    def test_gpio_pins_check(self):
        """ Tests if test_gpio_pins_check works as expected """
        gpio_pins_check([0, 1, 2, 3])
        gpio_pins_check([0, 2, 3])
        with self.assertRaises(ValueError):
            gpio_pins_check([1, 1, 2, 3])

    def test_gpio_names_check(self):
        """ Tests if gpio_names_check works as expected """
        gpio_names_check(['a', 'b', 'c'])
        with self.assertRaises(ValueError):
            gpio_names_check(['a', 'b', 'c', 'a'])

    def test_ads_inputs_check(self):
        """ Tests if gpio_names_check works as expected """
        ads_inputs_check([1, 2, 3])
        with self.assertRaises(ValueError):
            ads_inputs_check([1, 2, 3, 1])

    def test_ads_names_check(self):
        """ Tests if gpio_names_check works as expected """
        ads_names_check(['a', 'b', 'c'])
        with self.assertRaises(ValueError):
            ads_names_check(['a', 'b', 'c', 'a'])

    def test_ads_dev_check(self):
        """ Tests test_ads_dev_check """
        ads_dev_check({})
        ads_dev_check({
            'ads_devices': [
                {'name': 'test1', 'type': 'test', 'analog_in': 1, 'min_value': 1, 'max_value': 2},
                {'name': 'test2', 'type': 'test', 'analog_in': 2, 'min_value': 1, 'max_value': 2},
                {'name': 'test3', 'type': 'test', 'analog_in': 3},
            ]
        })
        with self.assertRaises(ValueError):
            ads_dev_check({
                'ads_devices': [
                    {'name': 'test', 'type': 'test', 'analog_in': 1, 'min_value': 1, 'max_value': 2},
                    {'name': 'test', 'type': 'test', 'analog_in': 2, 'min_value': 1, 'max_value': 2},
                ]
            })
        with self.assertRaises(ValueError):
            ads_dev_check({
                'ads_devices': [
                    {'name': 'test1', 'type': 'test', 'analog_in': 1, 'min_value': 1, 'max_value': 2},
                    {'name': 'test2', 'type': 'test', 'analog_in': 1, 'min_value': 1, 'max_value': 2},
                ]
            })
        with self.assertRaises(ValueError):
            ads_dev_check({
                'ads_devices': [
                    {'name': 'test1', 'type': 'test', 'analog_in': 1, 'min_value': 2, 'max_value': 2},
                    {'name': 'test2', 'type': 'test', 'analog_in': 2, 'min_value': 1, 'max_value': 2},
                ]
            })

    def test_gpio_dev_check(self):
        """ Tests test_gpio_dev_check """
        gpio_dev_check({})
        gpio_dev_check({
            'gpio_devices': [
                {'name': 'test1', 'type': 'test', 'pin': 1},
                {'name': 'test2', 'type': 'test', 'pin': 2},
                {'name': 'test3', 'type': 'test', 'pin': 3},
            ]
        })
        with self.assertRaises(ValueError):
            gpio_dev_check({
                'gpio_devices': [
                    {'name': 'test', 'type': 'test', 'pin': 1},
                    {'name': 'test', 'type': 'test', 'pin': 2},
                ]
            })
        with self.assertRaises(ValueError):
            gpio_dev_check({
                'gpio_devices': [
                    {'name': 'test1', 'type': 'test', 'pin': 1},
                    {'name': 'test2', 'type': 'test', 'pin': 1},
                ]
            })
        with self.assertRaises(ValueError):
            gpio_dev_check({'gpio_devices': [{'type': 'test', 'pin': 1}]})
        with self.assertRaises(ValueError):
            gpio_dev_check({'gpio_devices': [{'name': 'test1', 'type': 'test'}]})

    def test_load(self):
        """ Tests load function """
        with (
            patch("config_loader.parse_args") as mock_args,
        ):
            mock_args.return_value = Mock(config_file=None, port=None)
            port, config = load()
            self.assertEqual(port, 0)
            self.assertEqual(config, {})


if __name__ == '__main__':
    unittest.main(verbosity=2)

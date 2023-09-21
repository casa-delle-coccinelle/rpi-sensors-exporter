import unittest
import logging

from unittest.mock import Mock, patch

from config_loader import (
    parse_args,
    logs_setup,
    validate,
    unique_item_check,
    gpio_names_check,
    gpio_pins_check,
    gpio_dev_check,
    ads_names_check,
    ads_check_device,
    ads_check_device,
    ads_dev_check,
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


if __name__ == '__main__':
    unittest.main(verbosity=2)

from __future__ import print_function
import logging
import unittest
from mock import patch
import profilehooks
import sys
import time


class testProfilehooksTimeitLogger(unittest.TestCase):

    def sample_fn(self, delay_time, delay=False):
        if delay:
            time.sleep(delay_time)
        return delay

    def test_timecall_with_logger(self):
        if sys.version_info < (2, 7):
            print('Test does not support python 2.6')
            return
        logger_name = 'logtest'
        logger = logging.getLogger(logger_name)
        with patch.object(logger, 'log') as mock_logger:
            sample_fn = profilehooks.timecall(
                self.sample_fn, log_name=logger_name, log_level=logging.INFO
            )
            sample_fn(.1)
            mock_logger.assert_called_once()
            self.assertEqual(mock_logger.call_args[0][0], logging.INFO)
            self.assertIn('sample_fn(0.1)', mock_logger.call_args[0][1])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()

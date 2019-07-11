import unittest
import pytest
from utils import logger as log


class TestUtils(unittest.TestCase):
    def test_logger(self):
        logger = log.get_logger(__file__)
        assert len(logger.handlers) == 2
        logger2 = log.get_logger(__file__)
        assert logger == logger2
        logger.handlers = list()
        logger = log.get_logger(__file__, "simple")
        assert len(logger.handlers) == 2
        logger.handlers = list()
        with pytest.raises(ValueError):
            assert log.get_logger(__file__, "wrong_formatter")
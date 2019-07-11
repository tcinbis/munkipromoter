import unittest
import pytest
from utils import logger as log
from utils.config import conf, JiraLane, Catalog, JiraAutopromote, JiraEnum


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

    def test_set_and_get_config(self):
        assert conf.__getattr__("JIRA_LABELS_FIELD") == "labels"
        conf.__setattr__("JIRA_LABELS_FIELD", "label")
        assert conf.__getattr__("JIRA_LABELS_FIELD") == "label"

    def test_jira_lane(self):
        assert JiraLane.TO_DEVELOPMENT.is_promotion_lane
        assert JiraLane.TO_TESTING.is_promotion_lane
        assert JiraLane.TO_PRODUCTION.is_promotion_lane
        assert not JiraLane.DEVELOPMENT.is_promotion_lane
        assert not JiraLane.TESTING.is_promotion_lane
        assert not JiraLane.PRODUCTION.is_promotion_lane

    def test_catalog(self):
        assert Catalog.jira_lane_to_catalog(JiraLane.DEVELOPMENT) == Catalog.DEVELOPMENT
        assert Catalog.jira_lane_to_catalog(JiraLane.TO_DEVELOPMENT) == Catalog.DEVELOPMENT

        assert Catalog.DEVELOPMENT.next_catalog == Catalog.TESTING
        assert Catalog.TESTING.next_catalog == Catalog.PRODUCTION
        assert Catalog.PRODUCTION.next_catalog == Catalog.PRODUCTION

        assert Catalog.DEVELOPMENT.transition_id == "all to development"

    def test_autopromote(self):
        assert JiraAutopromote.PROMOTE
        assert not JiraAutopromote.NOPROMOTE

    def test_jira_enum(self):
        assert JiraLane.DEVELOPMENT.to_jira_rest_dict() == {'id': JiraLane.DEVELOPMENT.value}

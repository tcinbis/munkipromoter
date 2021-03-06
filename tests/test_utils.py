#  Gmacht mit ❤️ in Basel
#
#  Copyright (c) 2019 University of Basel
#  Last modified 16/07/2019, 12:55.
#
#  Developed by Tom Cinbis and Tim Königl on 16/07/2019, 13:04

import pytest

from src.utils import logger as log
from src.utils.config import JiraLane, Catalog, JiraAutopromote


class TestUtils:
    def test_logger(self):
        """Tests the logger instantiation"""
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

    def test_set_and_get_config(self, config):
        """Tests the setting and getting of config fields"""
        assert config.JIRA_LABELS_FIELD == "labels"
        config.JIRA_LABELS_FIELD = "label"
        assert config.JIRA_LABELS_FIELD == "label"

    def test_jira_lane(self):
        """Tests the jira lane enum"""
        assert JiraLane.TO_DEVELOPMENT.is_promotion_lane
        assert JiraLane.TO_TESTING.is_promotion_lane
        assert JiraLane.TO_PRODUCTION.is_promotion_lane
        assert not JiraLane.DEVELOPMENT.is_promotion_lane
        assert not JiraLane.TESTING.is_promotion_lane
        assert not JiraLane.PRODUCTION.is_promotion_lane

    def test_catalog(self):
        """Tests the jira catalog enum"""
        assert (
            Catalog.jira_lane_to_catalog(JiraLane.DEVELOPMENT)
            == Catalog.DEVELOPMENT
        )
        assert (
            Catalog.jira_lane_to_catalog(JiraLane.DEVELOPMENT)
            == Catalog.DEVELOPMENT
        )
        assert (
            Catalog.jira_lane_to_catalog(JiraLane.TO_DEVELOPMENT)
            == Catalog.DEVELOPMENT
        )

        assert Catalog.DEVELOPMENT.next_catalog == Catalog.TESTING
        assert Catalog.TESTING.next_catalog == Catalog.PRODUCTION
        assert Catalog.PRODUCTION.next_catalog == Catalog.PRODUCTION

        assert Catalog.DEVELOPMENT.transition_id == "all to development"

    def test_autopromote(self):
        """Tests the jira autopromote enum"""
        assert JiraAutopromote.PROMOTE
        assert not JiraAutopromote.NOPROMOTE

    def test_jira_enum(self):
        """Tests the jira enum"""
        assert JiraLane.DEVELOPMENT.to_jira_rest_dict() == {
            "id": JiraLane.DEVELOPMENT.value
        }

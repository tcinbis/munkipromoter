#  Gmacht mit ❤️ in Basel
#
#  Copyright (c) 2019 University of Basel
#  Last modified 16/07/2019, 12:55.
#
#  Developed by Tom Cinbis and Tim Königl on 16/07/2019, 13:04
from copy import deepcopy
from datetime import datetime, timedelta
from unittest.mock import Mock

from utils.config import JiraLane, Catalog, Present, JiraAutopromote, PackageState


class TestPromotion:
    def test_promotion_date(self, config, set_up_promoter):

        set_up_promoter._date_promotions = Mock()
        set_up_promoter._lane_promotions = Mock()

        config.DEFAULT_PROMOTION_DAY = (datetime.today() + timedelta(days=1)).strftime(
            "%A"
        )
        set_up_promoter.promote()

        assert (
            set_up_promoter._date_promotions.call_count == 0
            and set_up_promoter._lane_promotions.call_count == 1
        )

        set_up_promoter._lane_promotions.reset_mock()
        set_up_promoter._date_promotions.reset_mock()

        config.DEFAULT_PROMOTION_DAY = datetime.today().strftime("%A")
        set_up_promoter.promote()

        assert (
            set_up_promoter._date_promotions.call_count == 1
            and set_up_promoter._lane_promotions.call_count == 1
        )

    def test_same_package(self, set_up_promoter):
        orig_jira = set_up_promoter.jira_pkgs_dict
        orig_munki = set_up_promoter.munki_pkgs_dict
        set_up_promoter.promote()
        assert (
            set_up_promoter.jira_pkgs_dict == orig_jira
            and set_up_promoter.munki_pkgs_dict == orig_munki
        )

    def test_promotion_lane(self, set_up_promoter):
        setattr(
            set_up_promoter.jira_pkgs_dict["Firefox ESR EN60.8.0"],
            "jira_lane",
            JiraLane.TO_TESTING,
        )
        set_up_promoter.promote()
        assert set_up_promoter.jira_pkgs_dict == set_up_promoter.munki_pkgs_dict

    def test_catalog_lane_mismatch(self, set_up_promoter):
        orig_jira_package = deepcopy(
            set_up_promoter.jira_pkgs_dict["Firefox ESR EN60.8.0"]
        )
        setattr(
            set_up_promoter.jira_pkgs_dict["Firefox ESR EN60.8.0"],
            "catalog",
            Catalog.DEVELOPMENT,
        )
        set_up_promoter.promote()
        assert set_up_promoter.jira_pkgs_dict[
            "Firefox ESR EN60.8.0"
        ].catalog == Catalog.jira_lane_to_catalog(orig_jira_package.jira_lane)

    def test_no_munki_package(self, set_up_promoter):
        set_up_promoter.munki_pkgs_dict = dict()
        set_up_promoter.promote()
        assert (
            set_up_promoter.jira_pkgs_dict["Firefox ESR EN60.8.0"].present
            == Present.MISSING
        )

    def test_different_packages(self, set_up_promoter):
        setattr(
            set_up_promoter.munki_pkgs_dict["Firefox ESR EN60.8.0"],
            "catalog",
            Catalog.DEVELOPMENT,
        )
        set_up_promoter.promote()
        assert (
            set_up_promoter.munki_pkgs_dict["Firefox ESR EN60.8.0"]
            == set_up_promoter.jira_pkgs_dict["Firefox ESR EN60.8.0"]
        )

    def test_different_packages_not_compared_keys(self, set_up_promoter):
        setattr(
            set_up_promoter.munki_pkgs_dict["Firefox ESR EN60.8.0"],
            "autopromote",
            JiraAutopromote.NOPROMOTE,
        )
        set_up_promoter.promote()
        assert (
            not set_up_promoter.munki_pkgs_dict["Firefox ESR EN60.8.0"].state
            == PackageState.UPDATE
        )

    def test_no_autopromote(self, config, set_up_promoter):
        config.DEFAULT_PROMOTION_DAY = datetime.today().strftime("%A")
        jira_package = set_up_promoter.jira_pkgs_dict["Firefox ESR EN60.8.0"]
        jira_package.promote_date = (
            datetime.today() - timedelta(days=8)
        )
        jira_package.is_autopromote = JiraAutopromote.NOPROMOTE
        set_up_promoter.promote()
        assert jira_package.catalog == Catalog.TESTING

    def test_autopromote(self, config, set_up_promoter):
        config.DEFAULT_PROMOTION_DAY = datetime.today().strftime("%A")
        jira_package = set_up_promoter.jira_pkgs_dict["Firefox ESR EN60.8.0"]
        jira_package.promote_date = (
            datetime.today() - timedelta(days=8)
        )
        jira_package.is_autopromote = JiraAutopromote.PROMOTE
        set_up_promoter.promote()
        assert jira_package.catalog == Catalog.PRODUCTION



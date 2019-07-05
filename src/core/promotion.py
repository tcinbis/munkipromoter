from datetime import datetime
from typing import Dict

from core.base_classes import Package
from utils import logger as log
from utils.config import Catalog, PackageState, JiraLane, Present
from utils.config import conf

logger = log.get_logger(__file__)


class Promoter:
    def __init__(self, munki_packages: Dict, jira_packages: Dict):
        self.munki_pkgs_dict = munki_packages
        self.jira_pkgs_dict = jira_packages

    def promote(self):
        if (
            not datetime.now().strftime("%A")
            == conf.DEFAULT_PROMOTION_DAY
        ):
            logger.warning(
                f"Will not promote packages, as it's not {conf.DEFAULT_PROMOTION_DAY}"
            )
        else:
            self._date_promotions()

        self._lane_promotions()

    def _lane_promotions(self):
        for jira_pkg in self.jira_pkgs_dict.values():
            if jira_pkg.jira_lane.is_promotion_lane:
                # Pkg is in a promotion lane
                jira_pkg.catalog = Catalog.str_to_catalog(
                    jira_pkg.jira_lane.name.replace("TO_", "")
                )

                logger.debug(
                    f"Package {jira_pkg} in promotion lane. Promoting to {jira_pkg.catalog}"
                )

                jira_pkg.state = PackageState.UPDATE
                jira_pkg.promote_date = datetime.now()
                jira_pkg.jira_lane = JiraLane.catalog_to_lane(jira_pkg.catalog)
            elif jira_pkg.jira_lane != JiraLane.catalog_to_lane(jira_pkg.catalog):
                logger.debug(
                    f"Catalog and JiraLane Missmatch for package {jira_pkg}. Resetting catalog."
                )
                jira_pkg.catalog = Catalog.jira_lane_to_catalog(jira_pkg.jira_lane)
                jira_pkg.state = PackageState.UPDATE

            munki_package = self.munki_pkgs_dict.get(jira_pkg.key)
            if munki_package:
                for key, value in jira_pkg.__dict__.items():
                    if key not in Package.ignored_compare_keys():
                        if munki_package != jira_pkg:
                            # Not all values of the existing jira ticket and the local version match. Therefore update.
                            logger.debug(
                                f"Updating munki pkg {munki_package} values as {key} do not match: {munki_package.__dict__.get(key)} != {value}"
                            )
                            munki_package.state = PackageState.UPDATE
                            setattr(munki_package, key, value)
                            return
            else:
                jira_pkg.present = Present.MISSING

            # TODO: Maybe set UPDATE state?
            self.jira_pkgs_dict.update({jira_pkg.key: jira_pkg})

    def _date_promotions(self):
        # Start to check for promotion as it is the correct weekday
        for jira_pkg in self.jira_pkgs_dict.values():
            if (
                datetime.now() - jira_pkg.promote_date
            ).days > conf.DEFAULT_PROMOTION_INTERVAL:
                # number of days in catalog exceeds limit
                if jira_pkg.is_autopromote:
                    # only promote if autopromote is enabled
                    new_catalog = jira_pkg.catalog.next_catalog

                    if jira_pkg.catalog != new_catalog:
                        logger.debug(f"Date promotion for {jira_pkg} to {new_catalog}.")
                        jira_pkg.state = PackageState.UPDATE
                        jira_pkg.catalog = new_catalog
                        jira_pkg.jira_lane = JiraLane.catalog_to_lane(jira_pkg.catalog)
                        jira_pkg.promote_date = datetime.now()
                        self.jira_pkgs_dict.update({jira_pkg.key: jira_pkg})
                else:
                    logger.debug(
                        f"Ignoring {jira_pkg}, because autopromote is not set."
                    )

#  Gmacht mit ❤️ in Basel
#
#  Copyright (c) 2019 University of Basel
#  Last modified 16/07/2019, 12:55.
#
#  Developed by Tom Cinbis and Tim Königl on 16/07/2019, 13:03

from datetime import datetime
from typing import Dict

from core.base_classes import Package
from utils import logger as log
from utils.config import Catalog, PackageState, JiraLane, Present
from utils.config import conf

logger = log.get_logger(__file__)


class Promoter:
    """
    The main class for the promotion logic of the program.
    The munki and jira packages will be compared and the munki packages will be
    updated according to the state of the jira packages. Additionally automatic
    catalog transitions are realised if the right criteria are fulfilled.
    """

    def __init__(self, munki_packages: Dict, jira_packages: Dict):
        """
        Initializes a promoter object which contains the munki and the jira packages.

        :param munki_packages: `Dict` the munki packages
        :param jira_packages: `Dict` the jira packages
        """
        self.munki_pkgs_dict = munki_packages
        self.jira_pkgs_dict = jira_packages

    def promote(self):
        """
        The starting point of the promotion. If the day of execution is the same
        as the configured promotion date the :func:`_date_promotions` are conducted.
        Afterwards always the :func:`_lane_promotions` are performed.
        """
        if not datetime.now().strftime("%A") == conf.DEFAULT_PROMOTION_DAY:
            logger.warning(
                f"Will not promote packages, as it's not {conf.DEFAULT_PROMOTION_DAY}"
            )
        else:
            self._date_promotions()

        self._lane_promotions()

    def _lane_promotions(self):
        """
        If a jira package is in a promotion lane (TO_*CATALOG*), it is moved to
        the appropriate catalog (*CATALOG*).
        Additionally the respective munki package is searched and updated
        according to the jira package. If the munki package does not exist in
        the munki_repository it is marked as missing in jira.
        """
        for jira_pkg in self.jira_pkgs_dict.values():
            if jira_pkg.jira_lane.is_promotion_lane:
                # Pkg is in a promotion lane
                jira_pkg.catalog = Catalog.str_to_catalog(
                    jira_pkg.jira_lane.name.replace("TO_", "")
                )

                logger.debug(
                    f"Package {jira_pkg} in promotion lane. Promoting to "
                    f"{jira_pkg.catalog}"
                )

                jira_pkg.state = PackageState.UPDATE
                jira_pkg.promote_date = datetime.now()
                jira_pkg.jira_lane = JiraLane.catalog_to_lane(jira_pkg.catalog)
            elif jira_pkg.jira_lane != JiraLane.catalog_to_lane(
                jira_pkg.catalog
            ):
                logger.debug(
                    f"Catalog and JiraLane Missmatch for package {jira_pkg}. "
                    f"Resetting catalog."
                )
                jira_pkg.catalog = Catalog.jira_lane_to_catalog(
                    jira_pkg.jira_lane
                )
                jira_pkg.state = PackageState.UPDATE

            munki_package = self.munki_pkgs_dict.get(jira_pkg.key)
            if munki_package and munki_package != jira_pkg:
                for key, value in jira_pkg.__dict__.items():
                    if key not in Package.ignored_compare_keys():
                        if munki_package.__dict__.get(key) != value:
                            # Not all values of the existing jira ticket and the
                            # local version match. Therefore update.
                            logger.debug(
                                f"Updating munki pkg {munki_package} values as"
                                f" {key} do not match: "
                                f"{munki_package.__dict__.get(key)} != {value}"
                            )
                            munki_package.state = PackageState.UPDATE
                            setattr(munki_package, key, value)
            else:
                jira_pkg.present = Present.MISSING

            self.jira_pkgs_dict.update({jira_pkg.key: jira_pkg})

    def _date_promotions(self):
        """
        If a package is tagged as autopromote and is longer than one week in its
        catalog it is moved to the next catalog. The jira package is updated.
        """
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
                        logger.debug(
                            f"Date promotion for {jira_pkg} to {new_catalog}."
                        )
                        jira_pkg.state = PackageState.UPDATE
                        jira_pkg.catalog = new_catalog
                        jira_pkg.jira_lane = JiraLane.catalog_to_lane(
                            jira_pkg.catalog
                        )
                        jira_pkg.promote_date = datetime.now()
                        self.jira_pkgs_dict.update({jira_pkg.key: jira_pkg})
                else:
                    logger.debug(
                        f"Ignoring {jira_pkg}, because autopromote is not set."
                    )

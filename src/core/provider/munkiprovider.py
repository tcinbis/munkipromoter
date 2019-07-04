from __future__ import annotations

import copy
import os
import plistlib
import subprocess
from datetime import datetime, timedelta
from uuid import uuid4

from core.base_classes import Provider, Package
from utils import logger as l
from utils.config import (
    PackageState,
    JiraLane,
    Catalog,
    Present,
    JiraAutopromote,
    REPO_PATH,
    CATALOGS_PATH,
    PKGS_INFO_PATH,
    DEBUG_PKGS_INFO_SAVE_PATH,
    MAKECATALOGS,
    DEFAULT_PROMOTION_INTERVAL,
)
from utils.exceptions import (
    MunkiItemInMultipleCatalogs,
)

logger = l.get_logger(__file__)


class MunkiRepoProvider(Provider):
    def __init__(self, name, dry_run=False):
        super().__init__(name, dry_run)
        self._pkg_info_files = dict(dict())

    def connect(self):
        """
        The munki repository needs to be mounted when trying to connect.
        """
        if os.path.ismount(REPO_PATH):
            logger.debug(f"Repo at {REPO_PATH} mounted.")
            return True
        else:
            logger.critical(f"Repo mount point {REPO_PATH} not mounted.")
            return False

    def _load_packages(self):
        for filename in os.listdir(CATALOGS_PATH):
            if not (filename.startswith(".") or filename == "all"):
                # Ignore hidden files
                munki_packages = plistlib.load(
                    open(os.path.join(CATALOGS_PATH, filename), "rb")
                )

                for item in munki_packages:
                    try:
                        if "promotion_date" in item:
                            promotion_date = item.get("promote_date")
                        else:
                            promotion_date = datetime.now() + timedelta(
                                days=DEFAULT_PROMOTION_INTERVAL
                            )

                        if len(item.get("catalogs")) > 1:
                            raise MunkiItemInMultipleCatalogs(item)
                        else:
                            item_catalog = Catalog.str_to_catalog(
                                item.get("catalogs")[0]
                            )
                        # TODO: Check if promotion promote_date in pkginfo plist
                        p = Package(
                            name=item.get("name"),
                            version=item.get("version"),
                            catalog=item_catalog,
                            promote_date=promotion_date,
                            is_autopromote=JiraAutopromote.PROMOTE,
                            is_present=Present.PRESENT,
                            provider=MunkiRepoProvider,
                            jira_id=None,
                            jira_lane=JiraLane.catalog_to_lane(item_catalog),
                            state=PackageState.DEFAULT,
                            munki_uuid=uuid4(),
                        )

                        self._packages_dict.update({p.key: p})
                    except MunkiItemInMultipleCatalogs as e:
                        logger.error(e)

    def _load_pkg_infos(self):
        for dirpath, dirnames, filenames in os.walk(PKGS_INFO_PATH):
            for file in filenames:
                if file.startswith("."):
                    continue

                pkg_info_path = os.path.join(dirpath, file)
                pkg_info = plistlib.load(open(pkg_info_path, "rb"))

                # at index 0 we store the actual plist and at index 1 the path to that plist file is stored.
                d = {pkg_info.get("version"): (pkg_info, pkg_info_path)}

                if self._pkg_info_files.get(pkg_info.get("name")):
                    # pkg info files with this name already stored -> update
                    self._pkg_info_files.get(pkg_info.get("name")).update(d)
                else:
                    # no pkg info files with this name already stored -> add
                    self._pkg_info_files.update({pkg_info.get("name"): d})

    def load(self):
        self._load_packages()
        self._load_pkg_infos()
        self.is_loaded = True

    def update(self, package: Package):
        # make a deep copy of the package to prevent changes in other instances
        package_copy = copy.deepcopy(package)

        if package.key not in self._packages_dict:
            # The package is not present in the Munki repo therefore it must be missing locally
            # also update the referenced package such that jira will be informed
            package.state = PackageState.UPDATE
            package.is_present = Present.MISSING
            # the package is new for the munki repo
            package_copy.state = PackageState.NEW

            self._packages_dict.update({package_copy.key: package_copy})
            return

        p = self._packages_dict.get(package_copy.key)

        for key, value in package_copy.__dict__.items():
            if (
                key is not "promote_date"
                and key is not "jira_id"
                and key is not "munki_uuid"
                and key is not "provider"
            ):
                if p.__dict__.get(key) != value:
                    # Not all values of the existing jira ticket and the local version match. Therefore update.
                    package_copy.state = PackageState.UPDATE
                    self._packages_dict.update({package_copy.key: package_copy})
                    return
        logger.debug(f"Munki update called for {package}, but no changes detected.")

    def commit(self) -> bool:
        if not self._dry_run:
            for package in self._packages_dict.values():
                if package.state == PackageState.UPDATE:
                    pkg_info, pkg_info_path = self._pkg_info_files.get(
                        package.name
                    ).get(str(package.version))

                    if pkg_info:
                        # Plist already exists in Repo so we can continue to update it.
                        pkg_info.update({"catalogs": [package.catalog.name.lower()]})

                        f = open(
                            os.path.join(
                                DEBUG_PKGS_INFO_SAVE_PATH,
                                os.path.basename(pkg_info_path),
                            )
                            if DEBUG_PKGS_INFO_SAVE_PATH
                            else pkg_info_path,
                            "wb",
                        )
                        plistlib.dump(pkg_info, f)
                        logger.debug(f"Wrote pkg info file at {f.name}")
                        f.close()
                    else:
                        # Plist does not exist in Repo, and we can not create a new one.
                        package.state = PackageState.MISSING
                        logger.debug(
                            f"{package} is missing in {self.name} {self.__class__.__name__}"
                        )
                        continue
                elif package.state == PackageState.NEW:
                    logger.debug(
                        f"Pkg info for {package} not written, because package state is {package.state}"
                    )

            MunkiRepoProvider.make_catalogs()
            return True
        return False

    @staticmethod
    def make_catalogs():
        """
        Run makecatalogs and check whether the return code is 0.
        """
        cmd = ["python2", MAKECATALOGS, REPO_PATH]
        logger.info("Running makecatalogs.")
        subprocess.run(cmd, check=True)
        logger.info("Makecatalogs completed.")

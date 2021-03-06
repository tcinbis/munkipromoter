#  Gmacht mit ❤️ in Basel
#
#  Copyright (c) 2019 University of Basel
#  Last modified 16/07/2019, 12:55.
#
#  Developed by Tom Cinbis and Tim Königl on 16/07/2019, 13:03

from __future__ import annotations

import copy
import os
import plistlib
import subprocess
from datetime import datetime, timedelta
from uuid import uuid4

from src.core.base_classes import Provider, Package
from src.utils import logger as log
from src.utils.config import (
    PackageState,
    JiraLane,
    Catalog,
    Present,
    JiraAutopromote,
)
from src.utils.config import conf
from src.utils.exceptions import MunkiItemInMultipleCatalogs, MunkiRepoNotFound

logger = log.get_logger(__file__)


class MunkiRepoProvider(Provider):
    """
    Connects to a specific munki repository and represents the state of the
    munki packages by showing them as `Package`
    """

    def __init__(self, name: str, dry_run: bool = conf.DRY_RUN):
        """
        Initializes a `MunkiRepoProvider` object with a given name.

        :param name: `str` Name of the provider
        :param dry_run: `bool` If true, none of the changes will be committed in
        `commit`
        """
        super().__init__(name, dry_run)
        self._pkg_info_files = dict(dict())

    def connect(self):
        """
        Checks if the munki repository is mounted on the executing device.

        :raise: :class:`utils.exceptions.MunkiRepoNotFound` if we can not
        connect to the given munki repository
        :return: True if the repository is mounted
        """

        if os.path.ismount(conf.REPO_PATH) or os.path.exists(conf.REPO_PATH):
            logger.debug(f"Repo {conf.REPO_PATH} mounted or exists.")
            return True
        else:
            logger.critical(
                f"Repo {conf.REPO_PATH} not mounted or does not exist."
            )
            raise MunkiRepoNotFound(conf.REPO_PATH)

    def _load_packages(self):
        """
        Loads all available munki packages as a `Dict` of `Package` by
        converting the information of all plists from the munki repository.
        Each key for which there is no information in the plist is set to the
        default value.
        """
        logger.debug(f"Loading packages from repo: {conf.REPO_PATH}")
        # clear internal packages dict, before loading for the first time OR
        # again
        self._packages_dict.clear()
        for filename in os.listdir(conf.CATALOGS_PATH):
            if not (filename.startswith(".") or filename == "all"):
                # Ignore hidden files
                munki_packages = plistlib.load(
                    open(os.path.join(conf.CATALOGS_PATH, filename), "rb")
                )

                for item in munki_packages:
                    try:
                        # If we find something like this in our pkginfo we will
                        # use the provided information instead
                        # Otherwise fallback to default values.
                        # <key>munkipromote</key>
                        # 	<dict>
                        # 		<key>promotiondate</key>
                        # 		<string>2019-07-16</string>
                        # 		<key>autopromote</key>
                        # 		<true/>
                        # 	</dict>

                        promote_info = item.get("munkipromote")
                        if promote_info and "promotiondate" in promote_info:
                            promotion_date = datetime.strptime(
                                promote_info.get("promotiondate"), "%Y-%m-%d"
                            )
                        else:
                            promotion_date = datetime.now() + timedelta(
                                days=conf.DEFAULT_PROMOTION_INTERVAL
                            )

                        if promote_info and "autopromote" in promote_info:
                            if promote_info.get("autopromote"):
                                autopromote = JiraAutopromote.PROMOTE
                            else:
                                autopromote = JiraAutopromote.NOPROMOTE
                        else:
                            autopromote = JiraAutopromote.PROMOTE

                        if len(item.get("catalogs")) > 1:
                            raise MunkiItemInMultipleCatalogs(item)
                        else:
                            item_catalog = Catalog.str_to_catalog(
                                item.get("catalogs")[0]
                            )

                        p = Package(
                            name=item.get("name"),
                            version=item.get("version"),
                            catalog=item_catalog,
                            promote_date=promotion_date,
                            is_autopromote=autopromote,
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
        """
        Saves all the pkg info in form of the plists in the `MunkiRepoProvider`.
        """
        for dirpath, _dirnames, filenames in os.walk(conf.PKGS_INFO_PATH):
            for file in filenames:
                if file.startswith("."):
                    continue

                pkg_info_path = os.path.join(dirpath, file)
                pkg_info = plistlib.load(open(pkg_info_path, "rb"))

                # at index 0 we store the actual plist and at index 1 the path
                # to that plist file is stored.
                d = {pkg_info.get("version"): (pkg_info, pkg_info_path)}

                if self._pkg_info_files.get(pkg_info.get("name")):
                    # pkg info files with this name already stored -> update
                    self._pkg_info_files.get(pkg_info.get("name")).update(d)
                else:
                    # no pkg info files with this name already stored -> add
                    self._pkg_info_files.update({pkg_info.get("name"): d})

    def load(self):
        """
        Starts the loading of the packages and the pkg info by calling
        :func:`_load_pkg_infos` and
        :func:`_load_packages` if they are not yet loaded and if the connection
        to the munki repository
        exists.
        """
        if self.is_loaded or self.connect():
            self._load_packages()
            self._load_pkg_infos()
            self.is_loaded = True

    def update(self, package: Package):
        """
        Searches for a package in munki and updates it according to the package
        given in the argument.
        If no munki package exists matching the given package it is labeled as
        missing.

        :param package: `Package` object to be updated in the munki repo
        """
        # make a deep copy of the package to prevent changes in other instances
        package_copy = copy.deepcopy(package)

        if package.key not in self._packages_dict:
            # The package is not present in the Munki repo therefore it must be
            # missing locally also update the referenced package such that jira
            # will be informed
            package.state = PackageState.UPDATE
            package.is_present = Present.MISSING
            # the package is new for the munki repo
            package_copy.state = PackageState.NEW

            self._packages_dict.update({package_copy.key: package_copy})
            return

        p = self._packages_dict.get(package_copy.key)

        for key, value in package_copy.__dict__.items():
            if (
                key != "promote_date"
                and key != "jira_id"
                and key != "munki_uuid"
                and key != "provider"
            ):
                if p.__dict__.get(key) != value:
                    # Not all values of the existing jira ticket and the local
                    # version match. Therefore update.
                    package_copy.state = PackageState.UPDATE
                    self._packages_dict.update({package_copy.key: package_copy})
                    return
        logger.debug(
            f"Munki update called for {package}, but no changes detected."
        )

    def commit(self) -> bool:
        """
        Checks if the program runs as a dry run and if this is not the case, all
        previously made changes are added to the munki repository.

        :return: `bool` True if the run was not a dry run and changes were
        committed.
        """
        if not self._dry_run:
            for package in self._packages_dict.values():
                if package.state == PackageState.UPDATE:
                    pkg_info, pkg_info_path = self._pkg_info_files.get(
                        package.name
                    ).get(str(package.version))

                    if pkg_info:
                        # Plist already exists in Repo so we can continue to
                        # update it.
                        pkg_info.update(
                            {"catalogs": [package.catalog.name.lower()]}
                        )

                        f = open(
                            os.path.join(
                                conf.DEBUG_PKGS_INFO_SAVE_PATH,
                                os.path.basename(pkg_info_path),
                            )
                            if conf.DEBUG_PKGS_INFO_SAVE_PATH
                            else pkg_info_path,
                            "wb",
                        )
                        plistlib.dump(pkg_info, f)
                        logger.debug(f"Wrote pkg info file at {f.name}")
                        f.close()
                    else:
                        # Plist does not exist in Repo, and we can not create a
                        # new one.
                        package.state = PackageState.MISSING
                        logger.debug(
                            f"{package} is missing in {self.name}"
                            f"{self.__class__.__name__}"
                        )
                        continue
                elif package.state == PackageState.NEW:
                    logger.debug(
                        f"Pkg info for {package} not written, because package "
                        f"state is {package.state}"
                    )

            MunkiRepoProvider.make_catalogs()
            return True
        return False

    @staticmethod
    def make_catalogs():
        """
        Run makecatalogs and check whether the return code is 0.
        """
        cmd = [
            "python2",
            conf.MAKECATALOGS,
            conf.MAKECATALOGS_PARAMS,
            conf.REPO_PATH,
        ]
        logger.info("Running makecatalogs.")
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            logger.error(
                f"Running makecatalogs failed with code {e.returncode}. "
                f"{str(e)}"
            )
        logger.info("Makecatalogs completed.")

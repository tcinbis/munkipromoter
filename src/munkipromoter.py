#!/usr/local/bin/python3

#  Gmacht mit ❤️ in Basel
#
#  Copyright (c) 2019 University of Basel
#  Last modified 16/07/2019, 12:55.
#
#  Developed by Tom Cinbis and Tim Königl on 16/07/2019, 13:04

import argparse
import logging
import os

from core.promotion import Promoter
from core.provider.jiraprovider import JiraBoardProvider
from core.provider.munkiprovider import MunkiRepoProvider
from utils import logger as log
from utils.config import conf, MunkiPromoterTestConfig
from utils.exceptions import ImproperlyConfigured


class MunkiPromoter:
    """
    This class is the wrapper for the setup and the starting point of the
    promotion logic.
    """

    def __init__(self):
        """
        Initializes a MunkiPromoter with a jira and a munki provider.
        Additionally :func:`setup` is called.
        """
        self.setup()
        self._j = JiraBoardProvider("jira")
        self._m = MunkiRepoProvider("munki")

    def setup(self):
        """
        Parses all input arguments and sets the respective config values.
        """
        args = self._setup_argparser().parse_args()
        args.LOG_LEVEL_CLI = 50 - (
            (10 * args.LOG_LEVEL_CLI) if args.LOG_LEVEL_CLI > 0 else 0
        )

        if args.LOG_LEVEL_CLI > logging.__dict__.get(conf.LOG_LEVEL):
            args.LOG_LEVEL_CLI = logging.__dict__.get(conf.LOG_LEVEL)

        print(
            f"Setting log level to {logging.getLevelName(args.LOG_LEVEL_CLI)}"
        )

        for (flag, value) in vars(args).items():
            # passing the config values from the commandline interface to our
            # config class.
            conf.__setattr__(flag, value)

        self.check_config()

        # sentry_sdk.init("https://YOUR-SENTRY-PROJECT-CONFIG0@sentry.io/HERE")

    @staticmethod
    def check_config():
        """Checks if the default values are changed in the config and if some
        important requirements are satisfied"""
        logger = log.get_logger(__file__)

        correct_config = True

        if (
            "INSERT" in conf.JIRA_URL
            or "INSERT" in conf.JIRA_USER
            or "INSERT" in conf.JIRA_PASSWORD
        ):
            correct_config = False
            logger.critical(
                "Some of your Jira information is not yet configured, "
                "please change."
            )

        if not os.path.ismount(conf.REPO_PATH):
            correct_config = False
            logger.critical(
                "Your munki repository is not mounted, please mount."
            )

        if not os.path.exists(conf.MAKECATALOGS):
            correct_config = False
            logger.critical("Your make catalogs path is wrong, please correct.")

        config_file_path = os.path.join(conf.LOG_DIR, conf.LOG_FILENAME)
        if not os.path.exists(config_file_path):
            correct_config = False
            logger.critical(
                f"The config file {config_file_path} does not exists, please "
                f"create it."
            )

        if conf.DRY_RUN:
            logger.warning(
                "The program is executed in dry run mode, no changes will be "
                "commited."
            )

        if not correct_config and not isinstance(conf, MunkiPromoterTestConfig):
            # if we are testing we do not want to supply a complete
            # configuration therefore we only raise the exception when running
            # in non testing mode.
            raise ImproperlyConfigured()

    @staticmethod
    def _setup_argparser():
        """
        Initializes a argument parser that takes 6 optional arguments.

        :return: :func:`argparse.ArgumentParser` with the given arguments.
        """
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-m",
            "--munki-repo",
            type=str,
            dest="REPO_PATH",
            default=conf.REPO_PATH,
        )
        parser.add_argument(
            "-v", "--verbose", action="count", dest="LOG_LEVEL_CLI", default=0
        )
        parser.add_argument(
            "-n",
            "--dry-run",
            action="store_true",
            dest="DRY_RUN",
            default=conf.DRY_RUN,
        )
        parser.add_argument(
            "-j",
            "--jira-server",
            type=str,
            dest="JIRA_URL",
            default=conf.JIRA_URL,
        )
        parser.add_argument(
            "-u", "--user", type=str, dest="JIRA_USER", default=conf.JIRA_USER
        )
        parser.add_argument(
            "-p",
            "--password",
            type=str,
            dest="JIRA_PASSWORD",
            default=conf.JIRA_PASSWORD,
        )
        return parser

    def run(self):
        """
        The logic of the munki promoter. First jira gets updated from munki,
        meaning new issues are created if no one exists for a munki pkg.
        Next, the `Promoter` is initialized and does perform the promotion.
        In the end the changes will be added to jira and munki if it is not a
        dry run.
        """
        self._j.update_jira_from_repo(self._m.get())

        promoter = Promoter(self._m.get(), self._j.get())
        promoter.promote()

        self._j.commit()
        self._m.commit()


if __name__ == "__main__":
    MunkiPromoter().run()

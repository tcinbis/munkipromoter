#!/usr/local/bin/python3

#  Gmacht mit ❤️ in Basel
#
#  Copyright (c) 2019 University of Basel
#  Last modified 16/07/2019, 12:55.
#
#  Developed by Tom Cinbis and Tim Königl on 16/07/2019, 13:04

import argparse
import logging

from core.promotion import Promoter
from core.provider.jiraprovider import JiraBoardProvider
from core.provider.munkiprovider import MunkiRepoProvider
from utils.config import conf


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
        args.LOG_LEVEL = 70 - (10 * args.LOG_LEVEL) if args.LOG_LEVEL > 0 else 0

        print(f"Setting log level to {logging.getLevelName(args.LOG_LEVEL)}")

        for (flag, value) in vars(args).items():
            # passing the config values from the commandline interface to our
            # config class.
            conf.__setattr__(flag, value)

        # sentry_sdk.init("https://YOUR-SENTRY-PROJECT-CONFIG0@sentry.io/HERE")

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
            "-v", "--verbose", action="count", dest="LOG_LEVEL", default=1
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

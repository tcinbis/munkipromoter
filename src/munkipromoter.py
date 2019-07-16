#!/usr/local/bin/python3

#  Gmacht mit ❤️ in Basel
#
#  Copyright (c) 2019 University of Basel
#  Last modified 16/07/2019, 12:55.
#
#  Developed by Tom Cinbis and Tim Königl on 16/07/2019, 13:04

import argparse
import logging

from utils.config import conf


class MunkiPromoter:
    def __init__(self):
        self.setup()

    def setup(self):
        args = self._setup_argparser().parse_args()
        args.LOG_LEVEL = 70 - (10 * args.LOG_LEVEL) if args.LOG_LEVEL > 0 else 0

        print(f"Setting log level to {logging.getLevelName(args.LOG_LEVEL)}")

        for flag, value in vars(args).items():
            # passing the config values from the commandline interface to our config class.
            conf.__setattr__(flag, value)

        # sentry_sdk.init("https://***REMOVED***@sentry.io/***REMOVED***")

    def _setup_argparser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-m", "--munki-repo", type=str, dest="REPO_PATH", default=conf.REPO_PATH
        )
        parser.add_argument(
            "-v", "--verbose", action="count", dest="LOG_LEVEL", default=1
        )
        parser.add_argument(
            "-d", "--dry-run", action='store_true', dest="DRY_RUN", default=conf.DRY_RUN
        )
        return parser

    def run(self):
        from core.promotion import Promoter
        from core.provider.jiraprovider import JiraBoardProvider
        from core.provider.munkiprovider import MunkiRepoProvider

        __j = JiraBoardProvider("test1")
        __m = MunkiRepoProvider("test1")

        __j.update_jira_from_repo(__m.get())

        promoter = Promoter(__m.get(), __j.get())
        promoter.promote()

        __j.commit()
        __m.commit()


if __name__ == "__main__":
    MunkiPromoter().run()

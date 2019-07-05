import argparse
import logging

from utils.config import conf


def setup():
    args = _setup_argparser().parse_args()
    args.LOG_LEVEL = 70 - (10 * args.LOG_LEVEL) if args.LOG_LEVEL > 0 else 0

    print(f"Setting log level to {logging.getLevelName(args.LOG_LEVEL)}")

    for flag, value in vars(args).items():
        # passing the config values from the commandline interface to our config class.
        conf.__setattr__(flag, value)

    # sentry_sdk.init("https://***REMOVED***@sentry.io/***REMOVED***")


def _setup_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--munki-repo", type=str, dest="REPO_PATH")
    parser.add_argument("-v", "--verbose", action="count", dest="LOG_LEVEL", default=1)
    return parser


def run():
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
    setup()
    run()

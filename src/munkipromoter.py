import argparse

from core.promotion import Promoter
from core.provider.jiraprovider import JiraBoardProvider
from core.provider.munkiprovider import MunkiRepoProvider
from utils.config import conf


def setup_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--munki-repo", type=str, dest="REPO_PATH")
    return parser


if __name__ == "__main__":

    args = setup_argparser().parse_args()

    for flag, value in vars(args).items():
        # passing the config values from the commandline interface to our config class.
        conf.__setattr__(flag, value)

    # sentry_sdk.init("https://***REMOVED***@sentry.io/***REMOVED***")

    __j = JiraBoardProvider("test1")
    __m = MunkiRepoProvider("test1")

    __j.update_jira_from_repo(__m.get())

    promoter = Promoter(__m.get(), __j.get())
    promoter.promote()

    __j.commit()
    __m.commit()

#  Gmacht mit ❤️ in Basel
#
#  Copyright (c) 2019 University of Basel
#  Last modified 16/07/2019, 13:03.
#
#  Developed by Tom Cinbis and Tim Königl on 16/07/2019, 13:04
import sys

from munkipromoter import MunkiPromoter


class TestMunkiPromoter:
    def test_start(self):
        # removing arguments added by pytest which are otherwise interpreted by our argparser
        sys.argv = sys.argv[:1]
        MunkiPromoter().run()

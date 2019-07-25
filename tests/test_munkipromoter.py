#  Gmacht mit ❤️ in Basel
#
#  Copyright (c) 2019 University of Basel
#  Last modified 16/07/2019, 13:03.
#
#  Developed by Tom Cinbis and Tim Königl on 16/07/2019, 13:04
import sys
from unittest.mock import Mock

from munkipromoter import MunkiPromoter


class TestMunkiPromoter:
    def test_start(self, set_up_promoter):
        # removing arguments added by pytest which are otherwise interpreted by
        # our argparser
        sys.argv = sys.argv[:1]
        munki_promoter = MunkiPromoter()
        munki_promoter._j = Mock()
        munki_promoter._m = Mock()

        munki_promoter._j.get.return_value = dict()
        munki_promoter._m.get.return_value = dict()

        munki_promoter._j.commit.return_value = True
        munki_promoter._m.commit.return_value = True

        munki_promoter.run()

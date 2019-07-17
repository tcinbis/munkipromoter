#  Gmacht mit ❤️ in Basel
#
#  Copyright (c) 2019 University of Basel
#  Last modified 16/07/2019, 12:55.
#
#  Developed by Tom Cinbis and Tim Königl on 16/07/2019, 13:04
from datetime import datetime, timedelta
from unittest.mock import Mock


class TestPromotion:
    def test_promotion_date(self, config, set_up_promoter):

        set_up_promoter._date_promotions = Mock()
        set_up_promoter._lane_promotions = Mock()

        config.DEFAULT_PROMOTION_DAY = (datetime.today() + timedelta(days=1)).strftime(
            "%A"
        )
        set_up_promoter.promote()

        assert (
            set_up_promoter._date_promotions.call_count == 0
            and set_up_promoter._lane_promotions.call_count == 1
        )

        set_up_promoter._lane_promotions.reset_mock()
        set_up_promoter._date_promotions.reset_mock()

        config.DEFAULT_PROMOTION_DAY = datetime.today().strftime("%A")
        set_up_promoter.promote()

        assert (
            set_up_promoter._date_promotions.call_count == 1
            and set_up_promoter._lane_promotions.call_count == 1
        )

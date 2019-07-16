from datetime import datetime
from unittest.mock import Mock


class TestPromotion:
    def test_promotion_date(self, config, set_up_promoter):
        promoter = Mock()
        promoter.promote.side_effect = set_up_promoter.promote

        promoter.promote()
        assert (
                promoter._date_promotions.call_count == 1
                and promoter._lane_promotions().call_count == 1
        )

        config.DEFAULT_PROMOTION_DAY = datetime.now().strftime("%A")
        assert (
                promoter._date_promotions.call_count == 0
                and promoter._lane_promotions().call_count == 1
        )

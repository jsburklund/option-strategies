from yahoo_fin import stock_info, options
from datetime import date, datetime, timedelta
import numpy as np

DAYS_IN_FUTURE = 45
TICKER = "AAPL"
OPTION_STRATEGY = "iron_scondor"


class AnalyzeOptions:
    def __init__(self) -> None:

        # Initialize dates
        self.date_today = []
        self.desired_option_date = []
        self.nearest_date_to_target = []

        self._compute_dates()

    def _compute_dates(self) -> None:

        # Get the current date
        self.date_today = datetime.today().strftime("%Y-%m-%d")

        # Convert to string
        self.date_today = datetime.strptime(self.date_today, "%Y-%m-%d")

        # Add desired number of days in the future
        self.desired_option_date = self.date_today + timedelta(days=DAYS_IN_FUTURE)

        # Compute strike nearest to set target
        self._get_nearest_date()

    def _get_fridays(self):
        future_strikes = self.date_today  # January 1st
        future_strikes += timedelta(days=4 - future_strikes.weekday())  # First Sunday

        cnt = 0
        cnt_max = np.ceil(DAYS_IN_FUTURE / 7) + 2
        while cnt <= cnt_max:
            yield future_strikes
            future_strikes += timedelta(days=7)

            cnt += 1

        return future_strikes

    def _get_nearest_date(self) -> None:
        future_strikes = self._get_fridays()
        self.nearest_date_to_target = min(future_strikes, key=lambda x: abs(x - self.desired_option_date))


analyze_options = AnalyzeOptions()
print(analyze_options.nearest_date_to_target)

# todo:
# 1. Extract call and put options
# 2. Get IV and calculate 95% probability trade (start with iron condor)

from logging import getLogger

from .utils import MultiProcCalculator, ActivityJournalCalculatorMixin, DataFrameCalculatorMixin
from ...data import Statistics
from ...data.elevation import smooth_elevation
from ...data.frame import present
from ...names import Names, Titles, Units
from ...sql import StatisticJournalFloat

log = getLogger(__name__)


class ElevationCalculator(ActivityJournalCalculatorMixin, DataFrameCalculatorMixin, MultiProcCalculator):

    def __init__(self, *args, smooth=3, **kargs):
        self.smooth = smooth
        super().__init__(*args, **kargs)

    def _read_dataframe(self, s, ajournal):
        from ..owners import SegmentReader
        try:
            return Statistics(s, activity_journal=ajournal, with_timespan=True). \
                by_name(SegmentReader, Names.DISTANCE, Names.RAW_ELEVATION, Names.ELEVATION, Names.ALTITUDE).df
        except Exception as e:
            log.warning(f'Failed to generate statistics for elevation: {e}')
            raise

    def _calculate_stats(self, s, ajournal, df):
        if not present(df, Names.ELEVATION):
            if present(df, Names.RAW_ELEVATION):
                df = smooth_elevation(df, smooth=self.smooth)
            elif present(df, Names.ALTITUDE):
                log.warning(f'Using {Names.ALTITUDE} as {Names.ELEVATION}')
                df[Names.ELEVATION] = df[Names.ALTITUDE]
            return df
        else:
            return None

    def _copy_results(self, s, ajournal, loader, df):
        for time, row in df.iterrows():
            if Names.ELEVATION in row:
                loader.add(Titles.ELEVATION, Units.M, None, ajournal, row[Names.ELEVATION],
                           time, StatisticJournalFloat,
                           description='An estimate of elevation (may come from various sources).')
            if Names.GRADE in row:
                loader.add(Titles.GRADE, Units.PC, None, ajournal, row[Names.GRADE],
                           time, StatisticJournalFloat,
                           description='The gradient of the smoothed SRTM1 elevation.')
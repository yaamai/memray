import argparse

from ..reporters.table import TableReporter
from .common import HighWatermarkCommand


class TableCommand(HighWatermarkCommand):
    """Generate an HTML table with all records in the peak memory usage"""

    def __init__(self) -> None:
        super().__init__(
            reporter_factory=TableReporter.from_snapshot,
            reporter_name="table",
        )

    def prepare_parser(self, parser: argparse.ArgumentParser) -> None:
        super().prepare_parser(parser)
        parser.add_argument(
            "--use-local-js",
            action="store_true",
            dest="use_local",
            default=False,
            help="Use locally bundled JavaScript libraries instead of CDN links",
        )

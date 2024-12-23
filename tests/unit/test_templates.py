import pytest

from memray import AllocatorType
from memray.reporters.templates import get_report_title, render_report
from memray.reporters.flamegraph import FlameGraphReporter
from tests.utils import MockAllocationRecord


@pytest.mark.parametrize(
    ["kind", "show_memory_leaks", "inverted", "expected"],
    [
        ("flamegraph", False, False, "flamegraph report"),
        ("flamegraph", True, False, "flamegraph report (memory leaks)"),
        ("table", False, False, "table report"),
        ("table", True, False, "table report (memory leaks)"),
        ("flamegraph", False, True, "inverted flamegraph report"),
        ("flamegraph", True, True, "inverted flamegraph report (memory leaks)"),
    ],
)
def test_title_for_regular_report(kind, show_memory_leaks, inverted, expected):
    assert (
        get_report_title(
            kind=kind, show_memory_leaks=show_memory_leaks, inverted=inverted
        )
        == expected
    )


def test_local_js_injection():
        peak_allocations = [
            MockAllocationRecord(
                tid=1,
                address=0x1000000,
                size=1024,
                allocator=AllocatorType.MALLOC,
                stack_id=1,
                n_allocations=1,
                _stack=[
                    ("me", "fun.py", 12),
                    ("parent", "fun.py", 8),
                    ("grandparent", "fun.py", 4),
                ],
            ),
        ]

        reporter = FlameGraphReporter.from_snapshot(
            peak_allocations, memory_records=[], native_traces=False
        )

        html_code = render_report(
            kind="flamegraph",
            data=reporter.data,
            show_memory_leaks=False,
            inverted=False,
            use_local=True,
        )

        assert ('<script src=' not in html_code)
        

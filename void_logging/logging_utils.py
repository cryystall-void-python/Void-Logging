import math
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

REWARDS_HEADER = "Rewards"
METRICS_HEADER = "Metrics"
PLAYERS_METRICS_HEADER = "Players"
STATE_METRICS_HEADER = "State"

class AvgTracker:
    def __init__(self):
        self._value = 0
        self._count = 0

    def __iadd__(self, other):
        self._value += other
        self._count += 1

        return self

    def get_avg(self):
        if self._count == 0:
            return math.nan
        return self._value / self._count


def nest_dict(flat_dict, total_first=True):
    nested = {}
    for flat_key, value in flat_dict.items():
        parts = flat_key.split("/")
        current = nested
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            elif not isinstance(current[part], dict):
                old_val = current[part]
                current[part] = {}
                if total_first:
                    current[part]["Total"] = old_val
                else:
                    current[part] = {**current[part], "Total": old_val}
            current = current[part]
        last = parts[-1]
        if last in current and isinstance(current[last], dict):
            if total_first:
                # Move 'Total' to first if exists, else insert
                if "Total" not in current[last]:
                    current[last] = {"Total": value, **current[last]}
                else:
                    current[last]["Total"] = value
            else:
                current[last]["Total"] = value
        elif last in current and not isinstance(current[last], dict):
            old_val = current[last]
            current[last] = {}
            if total_first:
                current[last]["Total"] = old_val
                current[last]["Total"] = value
            else:
                current[last] = {**current[last], "Total": value}
        else:
            current[last] = value
    return nested

console = Console()

def _build_table(data, title=None):
    """Build a compact table for one section of metrics."""
    table = Table(title=title, expand=False, box=None, show_header=False)
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta", justify="right", no_wrap=True)

    for k, v in data.items():
        val = f"{v:.6f}" if isinstance(v, float) else str(v)
        table.add_row(k, val)

    return table


def print_metrics(data):
    """Print all sections as stacked panels."""
    panels = []
    for section, values in data.items():
        panels.append(Panel(_build_table(values, title=None), title=section, expand=False))
    console.print(*panels, sep="\n")
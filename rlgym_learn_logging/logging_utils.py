"""Utilities methods and values for various uses in the package"""

import math

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

REWARDS_HEADER = "Rewards"
METRICS_HEADER = "Metrics"
PLAYERS_METRICS_HEADER = "Players"
STATE_METRICS_HEADER = "State"


class AvgTracker:
    """A class to track the average of a value"""

    def __init__(self):
        self._value = 0
        self._count = 0

    def __iadd__(self, other):
        self._value += other
        self._count += 1

        return self

    def get_avg(self):
        """Gets the average from the value tracked"""
        if self._count == 0:
            return math.nan
        return self._value / self._count


def nest_dict(flat_dict):
    """
    Nest a flat dictionary based on '/' separator.
    Handles both flat dicts and dicts with agent/team keys.
    Prioritizes sub-metrics over top-level values.
    """

    def process_flat_dict(flat):
        nested = {}

        # First pass: collect all keys and identify which have children
        keys_with_children = set()
        for key in flat.keys():
            if "/" in key:
                parent = key.split("/")[0]
                keys_with_children.add(parent)

        # Second pass: build the nested structure
        for key, value in flat.items():
            if "/" in key:
                parts = key.split("/")
                current = nested

                # Navigate/create nested structure
                for part in parts[:-1]:
                    if part not in current:
                        current[part] = {}
                    current = current[part]

                # Set the final value
                current[parts[-1]] = value
            else:
                # Only add top-level keys if they don't have children
                if key not in keys_with_children:
                    nested[key] = value

        return nested

    # Check if this is a nested dict with agent/team keys
    if flat_dict and all(isinstance(v, dict) for v in flat_dict.values()):
        # Process each agent/team separately
        result = {}
        for agent_key, agent_dict in flat_dict.items():
            result[agent_key] = process_flat_dict(agent_dict)
        return result
        # Process as a single flat dict
    return process_flat_dict(flat_dict)


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
        panels.append(
            Panel(_build_table(values, title=None), title=section, expand=False)
        )
    console.print(*panels, sep="\n")

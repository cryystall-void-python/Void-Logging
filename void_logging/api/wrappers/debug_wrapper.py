import copy
from typing import List, Dict, Any

from rlgym.api import AgentID, StateType

from ..rewards import Logged, Log
from ..wrappers import LoggedWrapper
from ...logging_utils import nest_dict


from rich.tree import Tree
from rich import print as rprint


def nested_dict_tree(data, *, title="Root") -> Tree:
    """
    Pretty-print a nested dictionary (unknown depth) using rich.
    - Simple dicts like {"Weight": 0.0} become: "Weight = 0.0"
    - Lists print as "Item N: value" when simple
    """

    def is_simple_dict(d):
        return isinstance(d, dict) and all(
            not isinstance(v, (dict, list)) for v in d.values()
        )

    def add_branch(tree, element):
        if isinstance(element, dict):
            for key, value in element.items():
                # Case: simple leaf dict → print in one line
                if is_simple_dict(value):
                    for subkey, subval in value.items():
                        tree.add(f"[bold]{key}[/]: {subkey} = {repr(subval)}")
                    continue

                # Otherwise → nested structure
                branch = tree.add(f"[bold]{key}[/]")
                add_branch(branch, value)

        elif isinstance(element, list):
            for idx, item in enumerate(element):
                if isinstance(item, (dict, list)):
                    branch = tree.add(f"[italic]Item {idx}[/]")
                    add_branch(branch, item)
                else:
                    tree.add(f"[italic]Item {idx}:[/] {repr(item)}")

        else:
            tree.add(repr(element))

    root = Tree(f"[bold magenta]{title}[/]")
    add_branch(root, data)
    return root


class DebugWrapper(LoggedWrapper):
    """
    A wrapper to print the components of a reward
    """

    def get_rewards(
        self,
        agents: List[AgentID],
        state: StateType,
        is_terminated: Dict[AgentID, bool],
        is_truncated: Dict[AgentID, bool],
        shared_info: Dict[str, Any],
    ) -> Dict[AgentID, Logged]:
        rewards = super().get_rewards(
            agents, state, is_terminated, is_truncated, shared_info
        )
        _debug_rewards = {
            agent: copy.deepcopy(reward) for agent, reward in rewards.items()
        }

        for agent in agents:
            _debug_rewards[agent] += Log(
                value=rewards[agent].get_value(), metric="Total"
            )

        rprint(
            nested_dict_tree(
                nest_dict(
                    {agent: rw.get_logs() for agent, rw in _debug_rewards.items()}
                ),
                title=self.name,
            )
        )

        return rewards

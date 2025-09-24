import warnings

from rlgym.api import AgentID
from rlgym.rocket_league.api.game_state import GameState

from .._internal.logged_float import LoggedFloat, Log

class LoggedRewardManager:
    def __init__(self):
        self.floats: dict[AgentID, LoggedFloat] = {}
        self.current_player: AgentID = None
        self.is_ready = False

    def init(self, state: GameState[AgentID]):
        self.floats = {}

        for _id in state.cars.keys():
            self.floats.setdefault(_id, LoggedFloat())
        self.is_ready = True

    def get_reward_value(self) -> float:
        if self.current_player not in self.floats.keys():
            return 0
        return self.floats[self.current_player].value

    def __iadd__(self, other):
        if not isinstance(other, Log):
            warnings.warn(f"Operation with type {type(other)} unsupported")

        self.floats[self.current_player] += other
        return self

    def __isub__(self, other):
        if not isinstance(other, Log):
            warnings.warn(f"Operation with type {type(other)} unsupported")

        self.floats[self.current_player] -= other
        return self

    def __imul__(self, other):
        if not isinstance(other, Log):
            warnings.warn(f"Operation with type {type(other)} unsupported")

        self.floats[self.current_player] *= other
        return self

    def __itruediv__(self, other):
        if not isinstance(other, Log):
            warnings.warn(f"Operation with type {type(other)} unsupported")

        self.floats[self.current_player] /= other
        return self

    def __float__(self):
        return float(self.get_reward_value())

    def __int__(self):
        return int(float(self))

    def get_current_player_logging(self) -> LoggedFloat:
        return self.floats[self.current_player]

    def add_to_total(self, value: float | int):
        self.get_current_player_logging().logs["_total"] += value

    def get_total(self) -> float:
        return self.get_current_player_logging().logs["_total"].value

    def get_value(self, metric: str):
        return self.get_current_player_logging().get_log_value(log_name=metric)

    def get_value_for_player(self, agent_id: AgentID, metric: str):
        return self.floats[agent_id].get_log_value(metric)

    def get_all_metrics_for_player(self, agent_id: AgentID) -> set[str]:
        return set(self.floats[agent_id].metrics)

    def get_all_metrics(self) -> set[str]:
        metrics = set()

        for _id, value in self.floats.items():
            for s in value.metrics:
                metrics.add(s)

        metrics.add("_total")

        return metrics

    def reset(self):
        self.get_current_player_logging().reset()

    def set_current_player(self, agent_id: AgentID):
        self.current_player = agent_id
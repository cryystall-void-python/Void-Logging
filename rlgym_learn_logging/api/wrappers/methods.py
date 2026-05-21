from rlgym.api import AgentID, StateType

from rlgym_learn_logging.api.rewards.logged_reward import LoggedReward
from rlgym_learn_logging.api.wrappers.chain_wrapper import ChainWrapper


def chain(reward: LoggedReward[AgentID, StateType]) -> ChainWrapper[AgentID, StateType]:
    """Creates a ChainWrapper out of a logged reward

    :param reward: A logged reward
    :type reward: LoggedReward[AgentID, StateType]
    :return: A chain wrapper using the logged reward
    :rtype: ChainWrapper[AgentID, StateType]
    """
    return ChainWrapper(reward)


def combine(
    *rewards: LoggedReward[AgentID, StateType],
) -> ChainWrapper[AgentID, StateType]:
    """Creates a chain wrapper out of multiple rewards

    :return: A chain wrapper using all the rewards
    :rtype: ChainWrapper[AgentID, StateType]
    """
    return ChainWrapper.combine(*rewards)

import logging
from typing import List, Optional

from basic_game.action import Action
from basic_game.state import State


action_queue: List[Action] = []


def dispatch(action: Action) -> None:
    """Adds an action to the queue.

    This does not update the state immediately, but queues the actions for when
    the state is ready to be updated.
    """
    global action_queue
    logging.debug(f"dispatch: {action}")
    action_queue = [*action_queue, action]


def get_action(state: State) -> Optional[Action]:
    global action_queue
    logging.debug(f"`get_action`: action queue: {action_queue}")
    if len(action_queue) > 0:
        action = action_queue[0]
        action_queue = action_queue[1:]
        return action
    else:
        return None

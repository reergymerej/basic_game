import logging
from typing import List

from basic_game.action import Action


action_queue: List[Action] = []


def dispatch(action: Action) -> None:
    """Adds an action to the queue.

    This does not update the state immediately, but queues the actions for when
    the state is ready to be updated.
    """
    global action_queue
    logging.debug(f"dispatch: {action}")
    action_queue = [*action_queue, action]

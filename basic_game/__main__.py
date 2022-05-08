import argparse
import enum
import json
import logging
import os
import sys
import time
from copy import deepcopy
from pathlib import Path
from signal import SIGINT, signal
from time import sleep
from typing import List, Optional, Union

LOG_LEVEL = os.environ.get("LOG_LEVEL", "WARNING").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(levelname)s\t%(asctime)s %(message)s",
)


def parse_args(args) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--state",
        type=Path,
        help="start with state from saved .json",
    )
    return parser.parse_args()


@enum.unique
class Prompt(enum.Enum):
    END_GAME = "Would you like to end the game?"


class State:
    game_over: bool = False
    turn: int = 0
    user_prompt: Optional[Prompt] = Prompt.END_GAME
    user_input: Optional[str] = None

    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self) -> str:
        user_fields = [
            "game_over",
            "turn",
            # "user_input",
            # "user_prompt",
        ]
        lines = [f"{field}: {getattr(self, field)}" for field in user_fields]
        return "\n".join(lines)

    def __repr__(self) -> str:
        return json.dumps(self.__dict__)


@enum.unique
class ActionType(enum.Enum):
    END_GAME = enum.auto()
    PROMPT_USER = enum.auto()
    SET_USER_INPUT = enum.auto()
    TICK = enum.auto()


class Action:
    type: ActionType
    data: Union[None, str, Prompt]

    def __init__(
        self,
        type: ActionType,
        data: Union[None, str] = None,
    ) -> None:
        self.type = type
        self.data = data

    def __repr__(self) -> str:
        return json.dumps(self.__dict__, default=str)


def update_state(state: State, action: Action) -> State:
    next_state = deepcopy(state)
    logging.info(f"action: {action.type}, {action.data}")

    action_type = action.type
    if action_type == ActionType.END_GAME:
        next_state.game_over = True
    elif action_type == ActionType.TICK:
        next_state.turn = next_state.turn + 1
    elif action_type == ActionType.PROMPT_USER:
        if type(action.data) == Prompt:
            next_state.user_prompt = action.data
        else:
            raise TypeError("user prompt is not a Prompt")
    elif action_type == ActionType.SET_USER_INPUT:
        next_state.user_prompt = None
        next_state.user_input = str(action.data)
        logging.debug(
            "setting user response\n"
            f"\tQ: {state.user_prompt}\n"
            f'\tA: "{action.data}"'
        )
        if state.user_prompt == Prompt.END_GAME:
            next_state.game_over = True
            next_state.user_input = None
    else:
        raise NotImplementedError(f'unhandled action_type: "{action_type}"')

    return next_state


def load_state(state_file_path: Path) -> State:
    try:
        with open(state_file_path, "r") as file_pointer:
            state_dict = json.load(file_pointer)
            logging.debug(f"loaded state {state_dict}")
            return State(**state_dict)
    except FileNotFoundError:
        logging.info("no state file found, using default")
        return State()


def save_state(
    state_file_path: Path,
    state: State,
) -> None:
    with open(state_file_path, "w") as file_pointer:
        state_dict = state.__dict__
        logging.debug(f"saving state: {state_dict}")
        json.dump(state.__dict__, file_pointer)
    return None


action_queue: List[Action] = []


def dispatch(action: Action) -> None:
    """Adds an action to the queue.

    This does not update the state immediately, but queues the actions for when
    the state is ready to be updated.
    """
    global action_queue
    action_queue = [*action_queue, action]


def present(state: State) -> None:
    print(f"\n{'-' * 60}")
    print(state)
    print(f"\n{'-' * 60}")
    if state.user_prompt:
        user_value = input(state.user_prompt.value)
        logging.debug(f'user input: "{user_value}"')
        dispatch(
            Action(
                ActionType.SET_USER_INPUT,
                user_value,
            )
        )
    return None


def get_action(state: State) -> Action:
    global action_queue
    logging.debug(f"action queue: {action_queue}")
    if len(action_queue) > 0:
        action = action_queue[0]
        action_queue = action_queue[:1]
        return action
    else:
        return Action(ActionType.END_GAME)


def game_loop(state_file_path: Path) -> None:
    while True:
        state = load_state(state_file_path)
        present(state)
        if state.game_over:
            break
        action = get_action(state)
        next_state = update_state(state, action)
        save_state(state_file_path, next_state)


def main():
    args = parse_args(sys.argv[1:])
    logging.debug(f"using args: {args}")
    initial_state: State = State()
    if args.state:
        logging.info(f"starting from stored state {args.state}")
        initial_state = load_state(args.state)
    state_file_path = Path(f".state{time.time()}.json")
    save_state(state_file_path, initial_state)
    logging.info(f"using state {state_file_path}")

    def sigint_handler(signum, frame):
        logging.info(f"state file: {state_file_path}")
        exit(1)

    signal(SIGINT, sigint_handler)

    game_loop(state_file_path)


if __name__ == "__main__":
    main()

import argparse
import json
import logging
import os
import sys
import time
from copy import deepcopy
from pathlib import Path
from signal import SIGINT, signal
from typing import List, Optional
from basic_game.action import Action
from basic_game.enums import ActionType, Prompt
from basic_game.present import present

from basic_game.state import State

LOG_LEVEL = os.environ.get("LOG_LEVEL", "WARNING").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(levelname)s\t%(asctime)s %(filename)s@%(funcName)s %(message)s",
)


def parse_args(args) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--state",
        type=Path,
        help="start with state from saved .json",
    )
    return parser.parse_args()


def update_state(state: State, action: Action) -> State:
    next_state = deepcopy(state)
    logging.info(f'action: {action.type}, "{action.data}"')

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
            next_state.user_input = None
            if next_state.user_input == "y":
                next_state.game_over = True
    else:
        raise NotImplementedError(f'unhandled action_type: "{action_type}"')

    return next_state


def load_state(state_file_path: Path) -> State:
    try:
        with open(state_file_path, "r") as file_pointer:
            state_dict = json.load(file_pointer)
            logging.debug(
                "Checking loaded state to see if it "
                "matches current state version schema version."
            )
            loaded_state_version = state_dict["state_version"]
            current_state_version = State.state_version
            logging.debug(
                f"loaded version: {loaded_state_version}, "
                f"current version: {current_state_version}"
            )
            if current_state_version != loaded_state_version:
                logging.error("The loaded state version is incompatible.")
                raise ValueError("The loaded state version is incompatible.")
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
        state_dict["state_version"] = state.state_version
        logging.debug(f"saving state: {state_dict}")
        json.dump(state.__dict__, file_pointer)
    return None


action_queue: List[Action] = []


def get_action(state: State) -> Optional[Action]:
    global action_queue
    logging.debug(f"`get_action`: action queue: {action_queue}")
    if len(action_queue) > 0:
        action = action_queue[0]
        action_queue = action_queue[1:]
        return action
    else:
        return None


def game_loop(state_file_path: Path) -> None:
    while True:
        state = load_state(state_file_path)
        present(state)
        action = get_action(state)
        if action is None:
            break
        else:
            next_state = update_state(state, action)
            save_state(state_file_path, next_state)


def main():
    args = parse_args(sys.argv[1:])
    logging.debug(f"using args: {args}")
    initial_state: State = State(
        **{
            "game_over": False,
            "turn": 0,
            "user_prompt": None,
            "user_input": None,
        }
    )
    if args.state:
        logging.info(f"starting from stored state {args.state}")
        initial_state = load_state(args.state)
        # If there are queued actions, they will not be included here.
        # TODO: figure out a way to rehydrate queued actions.
        logging.warning("queued actions are not rehydrated")
        # TODO: convert enums from state from value to key
    state_file_path = Path(f".state{time.time()}.json")
    save_state(state_file_path, initial_state)
    logging.info(f"using state {state_file_path}")

    def sigint_handler(signum, frame):
        logging.info(f"state file: {state_file_path}")
        exit(1)

    signal(SIGINT, sigint_handler)

    game_loop(state_file_path)
    logging.info(f"using state {state_file_path}")


if __name__ == "__main__":
    main()

import argparse
import enum
import json
import logging
import os
import sys
import time
from copy import deepcopy
from pathlib import Path
from time import sleep

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


class State:
    game_over: bool
    turn: int

    def __init__(self, **kwargs) -> None:
        self.game_over = False
        self.turn = 0
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self) -> str:
        fields = [
            "game_over",
            "turn",
        ]
        lines = [f"{field}: {getattr(self, field)}" for field in fields]
        return "\n".join(lines)

    def __repr__(self) -> str:
        return json.dumps(self.__dict__)


@enum.unique
class InputType(enum.Enum):
    END_GAME = enum.auto()
    TICK = enum.auto()


class Input:
    input_type: InputType

    def __init__(self, input_type: InputType) -> None:
        self.input_type = input_type


def update_state(state: State, input: Input) -> State:
    next_state = deepcopy(state)
    logging.info(f"input: {input.input_type}")

    if input.input_type == InputType.END_GAME:
        next_state.game_over = True
    elif input.input_type == InputType.TICK:
        next_state.turn = next_state.turn + 1

    return next_state


def present(state: State) -> None:
    print(state)
    return None


def get_input(state: State) -> Input:
    if state.turn == 3:
        return Input(InputType.END_GAME)
    else:
        sleep(1)
    return Input(InputType.TICK)


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


def game_loop(state_file_path: Path) -> None:
    while True:
        state = load_state(state_file_path)
        present(state)
        if state.game_over:
            break
        input = get_input(state)
        next_state = update_state(state, input)
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
    game_loop(state_file_path)


if __name__ == "__main__":
    main()

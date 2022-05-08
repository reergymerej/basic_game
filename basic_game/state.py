import json
import logging
from pathlib import Path
from typing import Final, Optional

from basic_game.enums import Prompt


class State:
    state_version: Final[int] = 1
    game_over: bool
    turn: int
    user_prompt: Optional[Prompt]
    user_input: Optional[str]

    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            # if enum, use reverse lookup
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

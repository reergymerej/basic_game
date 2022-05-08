from copy import deepcopy
import enum
import logging
from time import sleep


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
    logging.debug(f"state: {state}")

    if input.input_type == InputType.END_GAME:
        next_state.game_over = True
    elif input.input_type == InputType.TICK:
        next_state.turn = next_state.turn + 1

    logging.debug(f"next_state: {next_state}")
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


saved_state = State()


def load_state() -> State:
    return saved_state


def save_state(state: State) -> None:
    global saved_state
    saved_state = state
    return None


def game_loop() -> None:
    while True:
        state = load_state()
        present(state)
        if state.game_over:
            break
        input = get_input(state)
        next_state = update_state(state, input)
        save_state(next_state)


game_loop()

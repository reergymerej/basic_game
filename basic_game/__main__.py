from copy import deepcopy
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


class Input:
    pass


def update_state(state: State, input: Input) -> State:
    next_state = deepcopy(state)
    next_state.turn = next_state.turn + 1
    return next_state


def present(state: State) -> None:
    print(state)
    return None


def get_input() -> Input:
    sleep(1)
    return Input()


saved_state = State()


def load_state() -> State:
    return saved_state


def save_state(state: State) -> None:
    global saved_state
    saved_state = state
    return None


def game_loop() -> None:
    state = load_state()
    while True:
        state = load_state()
        present(state)
        input = get_input()
        next_state = update_state(state, input)
        save_state(next_state)


game_loop()


    
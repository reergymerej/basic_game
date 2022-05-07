class State:
    game_over: bool

    def __init__(self) -> None:
        self.game_over = False

    def __str__(self) -> str:
        return f"game_over: {self.game_over}"


class Input:
    pass


def update_state(state: State, input: Input) -> State:
    return State()


def present(state: State) -> None:
    print(state)
    return None


def get_input() -> Input:
    return Input()


def load_state() -> State:
    return State()


def save_state(state: State) -> None:
    return None


def game_loop() -> None:
    state = load_state()
    input = get_input()
    next_state = update_state(state, input)
    save_state(next_state)
    present(next_state)


game_loop()

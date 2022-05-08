import logging
from basic_game.action import Action
from basic_game.dispatch import dispatch
from basic_game.enums import ActionType
from basic_game.state import State


def present(state: State) -> None:
    print(f"\n{'-' * 60}")
    print(state)
    print(f"\n{'-' * 60}")
    if state.user_prompt:
        user_value = input(f"{state.user_prompt.value}\n> ")
        logging.debug(f'user input: "{user_value}"')
        dispatch(
            Action(
                ActionType.SET_USER_INPUT,
                user_value,
            )
        )
    return None

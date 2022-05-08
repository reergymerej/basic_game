from copy import deepcopy
import logging
from basic_game.action import Action
from basic_game.enums import ActionType, Prompt
from basic_game.state import State


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

import json
from typing import Union
from basic_game.enums import ActionType, Prompt


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

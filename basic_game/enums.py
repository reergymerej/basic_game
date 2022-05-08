import enum


@enum.unique
class Prompt(enum.Enum):
    END_GAME = "Would you like to end the game?"


@enum.unique
class ActionType(enum.Enum):
    END_GAME = enum.auto()
    PROMPT_USER = enum.auto()
    SET_USER_INPUT = enum.auto()
    TICK = enum.auto()

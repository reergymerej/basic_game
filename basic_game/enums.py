import argparse
import enum
import json
import logging
import os
import sys
import time
from copy import deepcopy
from pathlib import Path
from signal import SIGINT, signal
from typing import Final, List, Optional, Union


@enum.unique
class Prompt(enum.Enum):
    END_GAME = "Would you like to end the game?"


@enum.unique
class ActionType(enum.Enum):
    END_GAME = enum.auto()
    PROMPT_USER = enum.auto()
    SET_USER_INPUT = enum.auto()
    TICK = enum.auto()

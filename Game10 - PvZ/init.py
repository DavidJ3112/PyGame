import pygame_gui
import os, sys
import pygame
import json
import time
from typing import (
    Any,
    Optional,
    Union,
    Callable,
    Iterable,
    Generator,
    TypeVar,
    Protocol,
    Literal,
)

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))

if parent_dir not in sys.path:
    sys.path.append(parent_dir)
if current_dir not in sys.path:
    sys.path.append(current_dir)

from general_scripts.init import *
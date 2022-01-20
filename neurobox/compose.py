"""Class for composing transforms into pipelines
"""

import functools
from typing import Any, Callable, Dict, List, Tuple
import copy
import pandas as pd


class Pipeline:
    def __init__(self, steps: List[Tuple[Callable, Dict[str, Any]]]):
        self.steps = steps

    def append_step(self, step: Tuple[Callable, Dict[str, Any]]):
        self.steps.append(step)

    def insert_step(self, index: int, step: Tuple[Callable, Dict[str, Any]]):
        self.steps.insert(index, step)

    def edit_step_param(self, index: int, param_name: str, param_value: Any):
        self.steps[index][1][param_name] = param_value

    def transform(self, df):
        funcs = [functools.partial(f, **kwargs) for f, kwargs in self.steps]
        func = functools.reduce(lambda f, g: lambda x: g(f(x)), funcs)
        return func(df)

    def clone(self):
        return copy.deepcopy(self)


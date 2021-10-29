"""Class for composing transforms into pipelines
"""

import functools
from typing import Callable, Dict, List, Tuple
import copy

class Pipeline:
    def __init__(self, steps: List[Tuple[Callable, Dict]]):
        self.steps = steps

    def append_step(self, step:Tuple[Callable, Dict]):
        self.steps.append(step)
    
    def inset_step(self, index: int, step: Tuple[Callable, Dict]):
        self.steps.insert(index, step)

    def transform(self, df):
        funcs = [functools.partial(f, **kwargs) for f, kwargs in self.steps]
        func = functools.reduce(lambda f, g: lambda x: g(f(x)), funcs)
        return func(df)
    
    def clone(self):
        return copy.deepcopy(self)
    



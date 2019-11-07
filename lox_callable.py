import time

from abc import ABC

from environment import Environment


class LoxCallable(ABC):
    def call(self, interpreter, args):
        raise NotImplementedError()

    def arity(self):
        raise NotImplementedError()

class _Clock(LoxCallable):
    def call(self, interpreter, args):
        return time.time()

    def arity(self):
        return 0

    def to_string(self):
        return "<native fn>"

class LoxFunction(LoxCallable):
    def __init__(self, declaration, closure):
        self.declaration = declaration
        self.closure = closure

    def arity(self):
        return len(self.declaration.params)

    def call(self, interpreter, args):
        env = Environment(self.closure)
        for param, arg in zip([p.lexeme for p in self.declaration.params], args):
            env.define(param, arg)

        interpreter.execute_block(self.declaration.body, env)

    def __repr__(self):
        return f"<fn {self.declaration.name.lexeme} >"

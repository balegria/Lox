class Environment():
    values = {}

    def __init__(self, enclosing=None):
        self.enclosing = enclosing

    def define(self, name, value):
        self.values[name] = value

    def get(self, name):
        if name.lexeme in self.values:
            return self.values[name.lexeme]

        if self.enclosing is not None:
            return self.enclosing.get(name)

        raise RuntimeError(name, "Undefined variable '{}'.".format(name.lexeme))

    def assign(self, name, value):
        """
        Key difference between assign and define is that assign cannot
        create a new _new_ variable.
        """
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return

        raise RuntimeError(name, "Undefined variable '{}'.".format(name.lexeme))
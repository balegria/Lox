class LoxRuntimeError(RuntimeError):
    def __init__(self, token, message):
        self.token = token
        super(LoxRuntimeError, self).__init__(message=message)
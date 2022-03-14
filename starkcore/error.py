

class StarkError(Exception):

    pass


class Error(StarkError):

    def __init__(self, code, message):
        super(Exception, self).__init__("{code}: {message}".format(code=code, message=message))
        self.code = code
        self.message = message


class InputErrors(StarkError):

    def __init__(self, content):
        self.errors = [Error(code=error["code"], message=error["message"]) for error in content]
        super(Exception, self).__init__(str(content))


class InternalServerError(StarkError):

    def __init__(self, message="Houston, we have a problem."):
        super(Exception, self).__init__(message)


class UnknownError(StarkError):

    def __init__(self, message):
        super(Exception, self).__init__("Unknown exception encountered: {}".format(message))


class InvalidSignatureError(StarkError):

    pass

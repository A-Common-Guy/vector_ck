#! usr/bin/env python3

class Error(Exception):
    pass
class RevoluteError(Error):
    pass
class OperationError(Error):
    pass
class ParameterError(Error):
    pass
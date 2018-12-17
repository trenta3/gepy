class InitializationError(Exception):
    """
    Error class that renders errors at initialization.
    """
    pass


class EvaluationError(Exception):
    """
    Error class for errors at gene / chromosome evaluation.
    """
    pass


class SelectionError(Exception):
    """
    Error class for errors in the selection phase.
    """
    pass


class ImplementationError(Exception):
    """
    Error class for errors in the implementation.
    """
    pass

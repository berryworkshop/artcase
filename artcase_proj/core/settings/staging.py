from .prod import *

DEBUG = True

try:
    from .local import *
except ImportError:
    pass

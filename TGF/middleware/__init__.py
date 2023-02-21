from .sessionControl import sessionControl
from .test import testMiddleware

def setup(dp):
    dp.middleware.setup( sessionControl() )
    #dp.middleware.setup( testMiddleware() )


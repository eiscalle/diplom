from settings import *

DEBUG = True

MIDDLEWARE_CLASSES += ('app.middleware.XhrSharing',)

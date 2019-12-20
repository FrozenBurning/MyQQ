import sys
sys.path.append('../')

from test.testchatroom import *

# Install hook so we we can import modules from source when frozen.
# from flexx.util import freeze
# freeze.install()
# freeze.copy_module("flexx",app_dir="./")
# freeze.copy_module("test.testchatroom",app_dir="./")

a = flx.App(ChatRoom)
a.serve()
# m = a.launch('firefox')  # for use during development
flx.start()
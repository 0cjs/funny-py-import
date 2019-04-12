import  sys
from    importlib import import_module

#   We are already bound to this when we start.
assert sys.modules['fakeone']

#   We have not yet set attribute module_one, so it doesn't exist
#   in our module. After setting it, it does exist as expected
#   in our module when accessed via `sys.modules`.
assert not getattr(sys.modules['fakeone'], 'module_one', None)
module_one = import_module('one')
assert module_one.one == 1              # We loaded the correct module
assert module_one == sys.modules['fakeone'].module_one

#   Replace ourselves in `sys.modules` with the module we just loaded.
#   The binding in the caller who executed `import fakeone` will be
#   done after we exit this script, and so their `fakeone` will
#   actually be bound to `module_one`.
sys.modules['fakeone'] = module_one

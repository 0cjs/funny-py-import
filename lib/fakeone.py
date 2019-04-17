import  sys
from    importlib import import_module

#   This is how we tell we're really _this_ module.
fakeone_attr = 'attr set in fakeone'

#   Unique sentinel value for getattr() etc.
ABSENT = object()

#   We are already placed in sys.modules when we start, and believe it's
#   really us because the attribute we set above is present and correct.
assert sys.modules['fakeone']
assert sys.modules['fakeone'].fakeone_attr == 'attr set in fakeone'

#   Import the module that will replace us.
#
#   We also test a bit further that we're really what's currently in
#   sys.modules: attr module_one isn't bound in the sys.modules
#   binding before we do the import and after it is.
assert ABSENT is getattr(sys.modules['fakeone'], 'module_one', ABSENT)
module_one = import_module('one')
assert module_one.one == 1              # We loaded the correct module
assert module_one == sys.modules['fakeone'].module_one

#   Replace ourself in `sys.modules` with the module we just loaded.
#   The binding in the caller who executed `import fakeone` will be
#   done after we exit this script, and so their `fakeone` will
#   actually be bound to `module_one`.
sys.modules['fakeone'] = module_one

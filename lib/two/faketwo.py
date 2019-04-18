' two/faketwo.py: When loaded, replaces two.faketwo with two.replacement '

import  sys
from    importlib import import_module

#   After replacement, nobody should see we set this because they're not us!
faketwo_version = 'attr set in two/faketwo.py'

#   Unique object to serve as sentinel.
ABSENT = object()

#   When we run here, the completed `two` is present, but the and
#   in-progress `two.faketwo` is noet yet set in `two`. This is different
#   from how it works with top-level modules, where it is set first.
assert sys.modules['two']
assert ABSENT is getattr(sys.modules['two'], 'faketwo', ABSENT)

mod_replacement = import_module('two.replacement')
#   We loaded the correct module and sys.modules['two'] has been updated.
assert mod_replacement.two_replacement == 22
assert sys.modules['two'].replacement.two_replacement == 22

#   We ourselves are still not yet loaded.
assert ABSENT is getattr(sys.modules['two'], 'faketwo', ABSENT)

#   Insert replacement module into sys.modules.
#   This works, just as it does for higher-level modules.
sys.modules['two.faketwo'] = mod_replacement

#   In parent module, set attribute for child module.
#   This appears not to work?
setattr(sys.modules['two'], 'faketwo', mod_replacement)

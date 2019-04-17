import sys

def test_fakeone_local_import():
    ABSENT = object()     # Unique sentinel value for getattr() etc.

    #   Fake is not loaded, nor bound at the top level of this module.
    assert ABSENT is sys.modules.get('fakeone', ABSENT)
    assert ABSENT is globals().get('fakeone', ABSENT)

    #   After load, it's bound locally but not globally
    import fakeone
    assert ABSENT is globals().get('fakeone', ABSENT)
    assert fakeone

    #   Attributes set in fakeone.py are not bound in the module we got.
    assert ABSENT is getattr(fakeone, 'fakeone_attr', ABSENT)

    #   But we did get attributes bound in one.py.
    assert 1 == fakeone.one
    assert 'This is one.py.' == fakeone.__doc__

    #   And, just for sanity, we check that they're there in the
    #   sys.modules binding created by fakeone's import of one.
    assert 1 == sys.modules['one'].one
    assert 'This is one.py.' == sys.modules['one'].__doc__

    #   In other words, our binding of `fakeone` created with the
    #   `import fakeone` statement above appears to have been bound to
    #   the value `sys.modules['fakeone']` _after_ fakeone.py set that.

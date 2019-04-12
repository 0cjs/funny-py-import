import sys

def test_fakeone_local_import():
    #   Fake is not loaded, nor bound at the top level of this module.
    assert not sys.modules.get('fakeone')
    assert not globals().get('fakeone')

    #   After load, it's bound locally but not globally
    import fakeone
    assert not globals().get('fakeone')
    assert fakeone

    #   Our binding of "fakeone" does have the `module_one`
    #   attribute set in fakeone.py.
    assert not getattr(fakeone, 'module_one', None)

    #   And it does have the `one` attribute set in one.py.
    assert 1 == fakeone.one

    #   In other words, our binding of `fakeone` created with the
    #   `import fakeone` statement above appears to have been bound to
    #   the value `sys.modules['fakeone']` _after_ fakeone.py set that.

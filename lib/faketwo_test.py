import sys

def test_faketwo_local_import():
    ' This tests multi-level bindings. '

    ABSENT = object()   # Unique sentinel value for getattr etc.

    #   `two` module is not loaded, nor bound at the top level of this module.
    assert ABSENT is sys.modules.get('two', ABSENT)
    assert ABSENT is sys.modules.get('two.faketwo', ABSENT)
    assert ABSENT is globals().get('two', ABSENT)

    import two.faketwo

    #   After load, it's bound locally but not globally
    assert ABSENT is globals().get('two', ABSENT)
    assert two
    assert two.faketwo

    #   The replacement module was still indeed loaded into the
    #   location determined by its name.
    doc_replacement = ' This replaces the real two. '
    assert doc_replacement == two.replacement.__doc__
    assert 22 == two.replacement.two_replacement

    #   Sadly, though faketwo set a binding for the replacement module
    #   (rather than itself) on `two.faketwo`, this was overwritten when
    #   its setup code exited.
    doc_original \
        = ' two/faketwo.py: When loaded, replaces both two and two.faketwo '
    assert doc_original == two.faketwo.__doc__
    assert 'attr set in two/faketwo.py' == two.faketwo.faketwo_version
    #   And it definitely does not have anything from replacement.
    assert ABSENT is getattr(two.faketwo, 'two_replacement', ABSENT)

    #   Modules were entered into sys.modules.
    sysmod_two = sys.modules.get('two', ABSENT)
    assert ABSENT is not sysmod_two
    sysmod_two_faketwo = sys.modules.get('two.faketwo', ABSENT)
    assert ABSENT is not sysmod_two_faketwo
    #   But, as above, contain binding to faketwo rather than the replacement
    assert doc_original == sysmod_two_faketwo.__doc__
    assert ABSENT is getattr(sysmod_two_faketwo, 'two_replacement', ABSENT)

    #   In other words, our binding of `fakeone` created with the
    #   `import fakeone` statement above appears to have been bound to
    #   the value `sys.modules['fakeone']` _after_ fakeone.py set that.

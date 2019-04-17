import builtins

original_import = builtins.__import__

def test_takeover():
    ''' Test takeover of syntatic `import` statement, i.e., make
        `import` call our own function.

        This is strongly discouraged `by the documentation
        <https://docs.python.org/3/library/functions.html#__import__>`_.
    '''
    testobj = (42,)
    def import_replacement(*args):
        #   Stdout shown only on failure in pytest.
        argtypes = ', '.join(map(lambda x: type(x).__name__, args[1:]))
        print('import_replacement(' + repr(args[0]) + ', ' + argtypes + ')')
        return testobj

    assert builtins.__import__ is original_import
    builtins.__import__ = import_replacement
    import taken_over_17361
    builtins.__import__ = original_import
    assert testobj is taken_over_17361

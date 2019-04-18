Python Import Experimentation/Abuse
===================================

This repo demonstrates that, in CPython 3.4 through 3.7, a top-level
module can replace itself with a completely different module during
the import process.

> XXX This discusses only "top level" modules (e.g., 'foo' but not
> 'foo.bar'). Expand for lower-level modules.

This is because `import foo` in the tested versions of Python appears
to do the following:
1. Bind `sys.modules['foo']` to a new module object.
2. Execute the code from the `.py` file in the context of the module
   object bound above.
3. In the module that excuted `import foo` bind `foo` to the _current
   value_ of `sys.modules['foo']`, regardless of whether that is the
   actual module object that it had originally created and put in
   `sys.modules['foo']`.

Thus, if the code executed during step 2 replaces `sys.modules['foo']`
with a different module, that new module will be the one the importer
gets (and of course any subsequent importers).

Any code in other modules that runs during step 2 and does `import
foo` before `sys.modules['foo']` is replaced will get the old version.
(Also see "Mutually Recursive Module Imports" below.) This means that
it's possible that some parts of the system will have the old module
and some the new.

This is different from the situation with [`importlib.reload()`],
which keeps the old module and merely recompiles and reruns the module
toplevel code within the context of that module.


Mutually Recursive Module Imports
---------------------------------

This is well described in a quote in [so 744403] taken from a
`comp.lang.python` discussion:

> 'import' and 'from xxx import yyy' are executable statements. They
> execute when the running program reaches that line.
>
> If a module is not in sys.modules, then an import creates the new
> module entry in sys.modules and then executes the code in the
> module. It does not return control to the calling module until the
> execution has completed.
>
> If a module does exist in sys.modules then an import simply returns
> that module whether or not it has completed executing. That is the
> reason why cyclic imports may return modules which appear to be
> partly empty.
>
> Finally, the executing script runs in a module named __main__,
> importing the script under its own name will create a new module
> unrelated to __main__.



<!-------------------------------------------------------------------->
[`importlib.reload()`]: https://docs.python.org/3/library/importlib.html#importlib.reload
[so 744403]: https://stackoverflow.com/a/744403/107294

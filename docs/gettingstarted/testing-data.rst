The tests usually require having some data on which one can test the code.
Especially the integration tests, which can sometimes require quite a complex
database state with a lot of interconnected objects.

Django provides the so called fixtures, which can be used as a solution for
this. But these turn out to be rather impractical. They are basically Django
models serialized to JSON (or even XML) and as such are quite difficult to
maintain and update, as that either means editing the JSON by hand or creating
the desired state in an empty database and serializing it.

A much better approach is to simply generate the testing data directly from
Python using the ORM. This is now being generally recognized as the appropriate
means for creating testing data and already there are some libraries dedicated
to make this easier, such as [#]_. But it's quite easy to get by even with raw
Python/Django.

.. [#] https://github.com/dnerdy/factory_boy

The testing-data factories can also be used to bootstrap the application in a
local development mode, so one can quickly get it running with some actual
content without having to create it by hand in the administration interface.

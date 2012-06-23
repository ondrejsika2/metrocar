To be able to write tests, one must think about the code actually being
*testable* already when writing it. A great benefit, apart from *being
testable*, of such code, is that it almost always is simply *better* also in all
other aspects, like readability or maintainability.

Good testability of code is mostly conditioned by having it split into small
logical chunks (functions or methods) that each have a single responsibility,
aren't tightly coupled with other parts and do not have a lot of side-effects.
Having the code split to these *units* of functionality makes it possible to
write the so called *unit tests*.

Having the code covered with unit tests allows for having a lot less of the so
called *integration tests*, which are harder to write and maintain. There only
needs to be a few of those to verify that the small parts are correctly
connected together, but there is no need to test all the possible code-paths
through the application.

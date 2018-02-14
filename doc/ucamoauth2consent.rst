The |project| Project
======================================

The |project| ``ucamoauth2consent`` project contains top-level configuration and URL routes for
the entire web application.

Settings
--------

The |project| ``ucamoauth2consent`` project ships a number of settings files.

.. _settings:

Generic settings
````````````````

.. automodule:: ucamoauth2consent.settings
    :members:

.. _settings_testsuite:

Test-suite specific settings
````````````````````````````

.. automodule:: ucamoauth2consent.settings.tox
    :members:

.. _settings_developer:

Developer specific settings
```````````````````````````

.. automodule:: ucamoauth2consent.settings.developer
    :members:

Custom test suite runner
------------------------

The :any:`test suite settings <settings_testsuite>` overrides the
``TEST_RUNNER`` setting to point to
:py:class:`~ucamoauth2consent.test.runner.BufferedTextTestRunner`. This runner captures
output to stdout and stderr and only reports the output if a test fails. This
helps make our tests a little less noisy.

.. autoclass:: ucamoauth2consent.test.runner.BufferedDiscoverRunner

.. autoclass:: ucamoauth2consent.test.runner.BufferedTextTestRunner

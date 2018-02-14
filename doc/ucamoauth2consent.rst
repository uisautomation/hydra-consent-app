The |project| Project
======================================

The |project| ``project_name`` project contains top-level configuration and URL routes for
the entire web application.

Settings
--------

The |project| ``project_name`` project ships a number of settings files.

.. _settings:

Generic settings
````````````````

.. automodule:: project_name.settings
    :members:

.. _settings_testsuite:

Test-suite specific settings
````````````````````````````

.. automodule:: project_name.settings.tox
    :members:

.. _settings_developer:

Developer specific settings
```````````````````````````

.. automodule:: project_name.settings.developer
    :members:

Custom test suite runner
------------------------

The :any:`test suite settings <settings_testsuite>` overrides the
``TEST_RUNNER`` setting to point to
:py:class:`~project_name.test.runner.BufferedTextTestRunner`. This runner captures
output to stdout and stderr and only reports the output if a test fails. This
helps make our tests a little less noisy.

.. autoclass:: project_name.test.runner.BufferedDiscoverRunner

.. autoclass:: project_name.test.runner.BufferedTextTestRunner

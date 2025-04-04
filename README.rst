========================
using-parameters-instead
========================


Most of the time, DE is done using group as a covariate, but individual specimen differences account for more of the variation than the conditions may theselves often. So the fix would be:
- fit to each folder
- test the differences in the covariate between each group.

Issues:
- Assumes that all folders have the same dispersion (alpha), which may not be the worst assumption in the world.


Features
--------

* TODO


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

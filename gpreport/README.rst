========
GPReport
========


.. image:: https://img.shields.io/pypi/v/gpreport.svg
        :target: https://pypi.python.org/pypi/gpreport

.. image:: https://img.shields.io/travis/Vladykart/gpreport.svg
        :target: https://travis-ci.com/Vladykart/gpreport

.. image:: https://readthedocs.org/projects/gpreport/badge/?version=latest
        :target: https://gpreport.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




add later


* Free software: MIT license
* Documentation: https://gpreport.readthedocs.io.


Features
--------

Stable release
--------------

To install GPReport, run this command in your terminal:

.. code-block:: console

    $ pip install gpreport

This is the preferred method to install GPReport, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for GPReport can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/Vladykart/gpreport

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/Vladykart/gpreport/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/Vladykart/gpreport
.. _tarball: https://github.com/Vladykart/gpreport/tarball/master

=====
Usage
=====

To use GPReport in a project::

    from gpreport import gpreport as gp

    # To get rdn datasets:
    rdn = gp.get_rdn_dataframes(
                login = 'LOGIN',
                password = 'PASSWORD',
                station_id = ''STATION_ID,
                date_from = 'dd.mm.yyyy',
                num_days = int
                )

    # To get vdr datasets:
    vdr = gp.get_vdr_dataframes(
                login = 'LOGIN',
                password = 'PASSWORD',
                station_id = ''STATION_ID,
                date_from = 'dd.mm.yyyy',
                num_days = int
                )

This methods returns a list of dictionary::

    [{'dataframe': pandas.DataFrame,
      'date': str,
      'station_id': str}]


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

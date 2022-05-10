Installing DataJoint for Python
===============================

Here we will cover installing the DataJoint library for Python and configuring it to connect to a database server. 
If you don't have a database server configured yet, be sure to checkout :doc:`get-database`!

System requirements
-------------------
DataJoint for Python requires **Python 3.4 or above** to function properly. To check whether you have the 
right Python version, run the following in the terminal/command prompt:

.. code-block:: bash

    $ python3 -V

If the above command runs without an error and the version is at least `3.4` (e.g.`3.6.0`),
then you are good to go!

.. _installing-dj-python:

Installing the DataJoint Package
--------------------------------

The entire source code for DataJoint Python is made available at `datajoint/datajoint-python <https://github.com/datajoint/datajoint-python>`_ 
GitHub repository. Although you certainly can install DataJoint directly from the source, it will be much 
easier to use `pip` - Python's package manager. The latest stable DataJoint releases are made available as
a package at `PyPI <https://pypi.python.org/pypi/datajoint/>`_. With this you can install DataJoint for Python
by just running the following in the terminal:

.. code-block:: bash

    $ pip3 install datajoint


and that's it! This should trigger the installation of the latest DataJoint and all of its dependencies. 
Depending on how your Python environment is configured, you may want to install within a 
`virtual environment <https://virtualenv.pypa.io/en/latest/user_guide.html>`_, installing for the user. Optionally:

.. code-block:: bash

    $ pip install virtualenv
    $ virtualenv venv/ && source venv/bin/activate
    $ (venv) pip3 install datajoint
    $ # Later:
    $ deactivate # to exit from venv

Verify that the package was properly installed by starting a Python 3 console, and try importing the 
`datajoint` package:

.. code-block:: bash

    $ python3
    
.. code-block:: python

  >>> import datajoint as dj

Make sure you have the DataJoint package installed successfully before moving on.

Upgrading DataJoint
^^^^^^^^^^^^^^^^^^^
If you already have an older version of DataJoint package installed on your system and you wish to upgrade to the latest version, 
you can run ``pip install datajoint`` again but this time passing in the ``--upgrade`` option. That is:

.. code-block:: bash

  $ pip3 install --upgrade datajoint

.. _configure-python-dj:

Configuring DataJoint
---------------------

Now you have DataJoint installed, let's configure the library to connect to the database server. 
Whichever option you have selected from :doc:`get-database`, you will need three pieces of information to connect
to the database server: the database address, and your username and password.

.. note::
  If you have signed up for the tutorial database at `DataJoint.io <https://datajoint.io>`_ you should have received
  an email with instructions on how to connect to the database, including the host address, username, and your
  temporary password.

.. note::
  If you have followed the :doc:`local-database` tutorial to setup a local database in Docker, your host address
  will be ``127.0.0.1``, username ``root`` and password ``tutorial``.

.. note::
  If you have a non-local database server setup for your lab/institution that you would like to connect to,
  simply use the host address, username and password for the target database server. These information are typically 
  provided by your database administrator.


Start an interactive Python 3 console and type in the following commands:

.. code-block:: python

  >>> import datajoint as dj
  >>> dj.config['database.host'] = 'HOST_ADDRESS'
  >>> dj.config['database.user'] = 'USER_NAME'
  >>> dj.config['database.password'] = 'PASSWORD'

Here, we are using the ``dj.config`` object to update configurations for DataJoint. Namely, we are specifing 
the address of the database (``database.host``), and the user name (``database.user``) and password 
(``database.password``). Be sure to replace ``'HOST_ADDRESS'``, ``'USER_NAME'``, and ``'PASSWORD'`` with the actual
values for your database connection! Note that these values have to be provided as strings.


Now that we have updated the connection configuration, let's check the connection status by calling `dj.conn()`:

.. code-block:: python

  >>> dj.conn()
  Connecting root@localhost:3306
  DataJoint connection (connected) root@localhost:3306

If you get a message that looks like this, then congratulations! You have just successfully accessed the database server using DataJoint!

.. note::
  The exact message will look different depending on what database server you are
  connected to.

Changing password
^^^^^^^^^^^^^^^^^

Once connected, you can easily change your password using ``dj.set_password()``

.. code-block:: python

  >>> dj.set_password()
  New Password: (enter your new password)
  Confirm Password: (enter your new password again)
  Password updated.

and that's it!

.. note::
  If you have signed up to and are connected to the tutorial database on 
  `Accounts.DataJoint.io <https://accounts.datajoint.io/login>`_, it is strongly recommeded that you 
  change your password from the temporary password that was sent to you in 
  the email!

What's next?
------------

If everything went well, you now have a fully functional developement environment for DataJoint with Python,
connected to a database server. You can now move onto :doc:`/beginner/building-first-pipeline/index`
to start learning how to use DataJoint to design and build data pipelines, or explore any other tutorials in this site to learn specific features of DataJoint.

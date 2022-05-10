Installing DataJoint for MATLAB
===============================

Here we will cover installing DataJoint library for MATLAB and configuring it to connect to a database server.
If you don't have a database server configured yet, be sure to checkout :doc:`get-database` first!

System requirements
-------------------
DataJoint for MATLAB requires **MATLAB R2015b** or later to function properly. Verify that you have the right MATLAB version before proceeding with the tutorial.

.. _installing-dj-matlab:

Installing the DataJoint Toolbox
--------------------------------

The entire source code for DataJoint MATLAB is made available at `datajoint/datajoint-matlab <https://github.com/datajoint/datajoint-matlab>`_ GitHub repository. Although you can certainly download and use DataJoint directly from the source code, DataJoint is available as a custom toolbox that you can download from `MATLAB File Exchange <https://www.mathworks.com/matlabcentral/fileexchange/63218-datajoint>`_. Follow these simple instructions to install DataJoint toolbox:

1. Navigate to `DataJoint toolbox <https://www.mathworks.com/matlabcentral/fileexchange/63218-datajoint>`_ on MATLAB File Exchange.
2. Click on ``Download`` button and select ``Toolbox`` to start downloading the toolbox.
3. Once the download completes, click on the downloaded ``DataJoint.mltbx``. This will launch MATLAB automatically and bring up a pop up dialog showing details about the toolbox.
4. Clock on ``Install`` button and follow the instructions on the screen to install the DataJoint toolbox.

And that's it! To verify that the toolbox was properly installed, run the following command in MATLAB:

.. code-block:: matlab

  >> dj.version

If that prints out the DataJoint version without an error, you are good to go!

Upgrading DataJoint
^^^^^^^^^^^^^^^^^^^
If you already have an older version of DataJoint toolbox installed on your system and you wish to upgrade to the latest version, 
you can simply follow the same exact installation steps as above to download and install the latest available version of the DataJoint for MATLAB
toolbox.

.. _configure-matlab-dj:

Configuring DataJoint
---------------------

Now that you have DataJoint installed, let's configure the library to connect to the database server. 
Whichever option you have selected from :doc:`get-database`, you will need three pieces of information to connect
to the database server: the database address, username and password.

.. note::
  If you have signed up for a tutorial database at `Accounts.DataJoint.io <https://accounts.datajoint.io/login>`_ you should have received
  an email with instructions on how to connect to the database, including the host address, username, and your
  temporary password.

.. note::
  If you have followed the :doc:`local-database` tutorial to setup a local database in Docker, your host address
  will be ``127.0.0.1``, with username ``root`` and password ``tutorial``.

.. note::
  If you have a non-local database server setup for your lab/institution that you would like to connect to,
  simply use the host address, username and password for the target database server. These information are typically 
  provided by your database administrator.

Start MATLAB and type in the following commands:

.. code-block:: matlab

  >> setenv('DJ_HOST', 'HOST_ADDRESS')
  >> setenv('DJ_USER', 'USER_NAME')
  >> setenv('DJ_PASS', 'PASSWORD')

This sets the environmental variables with ``setenv`` that configure the DataJoint connection: The address of the database (`DJ_HOST`), the user name (`DJ_USER`), and the 
password (`DJ_PASS`). Be sure to replace ``'HOST_ADDRESS'``, ``'USER_NAME'``, and ``'PASSWORD'`` with the actual
values for your database connection! Note that these values have to be provided as character array in quotes ``' '`` 


Now that we have updated the connection configuration, let's check the connection status by calling `dj.conn()`:

.. code-block:: matlab

  >> dj.conn()

When you call it for the very first time after the installation, the above command will trigger the downloading of a few extra libraries needed for DataJoint and thus may take some time. If everything works, you should get a prompt like the following:

.. code-block:: matlab

  >> dj.conn()

   0:  127.0.0.1 via TCP/IP             Server version 5.7.17

   connection_id() 
   +---------------+
   10              


   ans = 

   Connection with properties:

               host: '127.0.0.1'
               user: 'root'
          initQuery: ''
      inTransaction: 0
             connId: 0
           packages: [0×1 containers.Map]
        foreignKeys: [0×0 struct]
        isConnected: 1

If you get a message that looks like above, then congratulations! You have just successfully accessed the database server using DataJoint!

.. note::
  The exact message will look different depending on what database server you are
  connected to.

Changing password
^^^^^^^^^^^^^^^^^

Once connected, you can easily change your password using ``dj.setPassword``

.. code-block:: matlab

  >> dj.setPassword('your-new-password')
  done

and that's it!

.. note::
  If you have signed up to and are connected to the tutorial database on 
  `DataJoint.io <https://datajoint.io>`_, it is strongly recommeded that you 
  change your password from the temporary password that was sent to you in 
  the email!

What's next?
------------

If everything went well, you now have a fully functional developement environment for DataJoint,
with a database server. You can now move onto :doc:`/beginner/building-first-pipeline/index`
to start learning how to use DataJoint to design and build data pipelines, or explore any other tutorials in this site to learn specific features of DataJoint.


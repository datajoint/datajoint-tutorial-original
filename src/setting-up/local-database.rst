Setting Up a Local Database Server
==================================

Here we are going to install and setup a database server to run locally on your machine.
A local database server works perfectly well for the tutorials and is a 
very convenient way to explore and learn DataJoint. Assuming your storage and computational resources are sufficient, a local database server can also work
well for your personal project using DataJoint data pipelines. 

Setting up database using Docker
--------------------------------

DataJoint currently works with MySQL compatible database servers including `MySQL`_ and `MariaDB`_.
While you can directly install either one of these database servers on your machine and configure it
manually for use with DataJoint, we are going to install and use `Docker`_ instead to download and run a
MySQL database server that is already fully configured for use with DataJoint out of the box. Not familiar with Docker? No worries!
We'll cover just enough basics to get you up and running with a fresh, fully configured MySQL database
running on Docker, whether you are on Mac, Windows, or Linux!

.. _MySQL: https://www.mysql.com
.. _MariaDB: https://www.mariadb.org
.. _Docker: https://www.docker.com

Why Docker?
-----------
Docker in essence allows you to package a computer program (in this case a database server) along with all
the file systems and code libraries it needs into what's known as a **container**. Once packaged 
into a container, the container can be distributed to any machine with Docker and the packaged program can be run without having to go through otherwise a potentially cumbersome
installation and setup process. Although the process of installing and setting up a database server from scratch is quite
well documented and not too tough, Docker allows you to get a fully functional database server
up and running in just a few commands. 

Installing Docker
-----------------
Here we briefly cover how to install and setup Docker on your operating system.

.. note::
    For more thorough and detailed instructions, please refer to 
    `Docker documentation <https://docs.docker.com/engine/installation/>`_

Getting Docker for Mac
^^^^^^^^^^^^^^^^^^^^^^
Download and install `Docker for Mac <https://www.docker.com/docker-mac>`_ from Docker's website. Click on 
**Download from Docker Store** button, and then click on **Get Docker** in the next screen. This will
download `Docker.dmg`, which you can open to install Docker for Mac on your machine. 

Once installed, navigate to `Applications` folder and then start Docker by double clicking on the
`Docker.app` icon. You should notice that Docker whale icon on your top menu bar.

To verify that everything is working, open up a terminal (`Applications`>`Utilities`>`Terminal.app`) and type the following:

.. code-block:: bash

    $ docker run --rm hello-world

This should cause a greeting message to be printed to your screen:

.. code-block:: bash

    $ docker run --rm hello-world
    Hello from Docker!
    This message shows that your installation appears to be working correctly.

    To generate this message, Docker took the following steps:
     1. The Docker client contacted the Docker daemon.
     2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
     3. The Docker daemon created a new container from that image which runs the
        executable that produces the output you are currently reading.
     4. The Docker daemon streamed that output to the Docker client, which sent it
        to your terminal.
    ...(message truncated)

If you got this response back, congratulations! You now have a functional Docker environment and are ready to proceed!

Getting Docker for Windows
^^^^^^^^^^^^^^^^^^^^^^^^^^

You can install Docker for Windows with Docker ToolBox via <https://www.docker.com/products/docker-toolbox>`_.

Once you have downloaded and run the installer and it has finished installation, you can click on the `Docker QuickStart Terminal`, which will initialize Docker on your system and then bring up a Docker shell. 
In the shell, you can type:

.. code-block:: bash

  $ docker run --rm hello-world

This should cause a greeting message to be printed to your screen:

.. code-block:: bash

  $ docker run --rm hello-world
  ...(message truncated)
  Hello from Docker!
  This message shows that your installation appears to be working correctly.

  To generate this message, Docker took the following steps:
   1. The Docker client contacted the Docker daemon.
   2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
   3. The Docker daemon created a new container from that image which runs the
      executable that produces the output you are currently reading.
   4. The Docker daemon streamed that output to the Docker client, which sent it
      to your terminal.
  ...(message truncated)

If you got the response back, congratulations! You now have a functional Docker environment and are ready to proceed!

Getting Docker for Linux
^^^^^^^^^^^^^^^^^^^^^^^^
To get Docker for Linux, navigate to the `install Docker <https://docs.docker.com/engine/installation/#supported-platforms>`_ and follow links and instructions for your specific distributions.

.. note::

  The installation instruction will depend on your Linux distribution (i.e. Ubuntu, CentOS, Fedora, etc). Be sure to follow the installation instructions for **Docker CE(Community Edition)**. 

In some tutorials we will use `Docker Compose <https://docs.docker.com/compose/>`_ to streamline the Docker container launching process. The Docker CE for Linux does **not** come with Docker Compose by default, so please follow `the installation instructions <https://docs.docker.com/compose/install/>`_ to install Docker Compose on your machine.

To verify that everything is working, open up a terminal/command prompt and type in the following command:

.. code-block:: bash

    $ docker run --rm hello-world

You may need to prefix the above command with `sudo` depending on your installation configuration.

This should cause the greeting message to be printed to your screen:

.. code-block:: bash

    $ docker run --rm hello-world
    ...(message truncated)
    Hello from Docker!
    This message shows that your installation appears to be working correctly.

    To generate this message, Docker took the following steps:
     1. The Docker client contacted the Docker daemon.
     2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
     3. The Docker daemon created a new container from that image which runs the
        executable that produces the output you are currently reading.
     4. The Docker daemon streamed that output to the Docker client, which sent it
        to your terminal.
    ...(message truncated)

Launching a database server
---------------------------

.. warning::
  The database server launched here is only intended for use with tutorials, and any data in the database may
  be lost when you reboot your machine. For setting up a production-ready database server with Docker,
  refer to `our Docker image page <https://github.com/datajoint/mysql-docker>`_ We will cover this topic in more detail in an upcoming tutorial.

Now that you have Docker installed, setting up a database server is a breeze! We will download and run a Docker image with MySQL database pre-configured to work with DataJoint. Open up a terminal/shell prompt, and type in the following command:

.. code-block:: bash 

    $ docker run -p 3306:3306 -e MYSQL_ROOT_PASSWORD=tutorial datajoint/mysql

The above command tells Docker to:

* Download a container image called `datajoint/mysql`. This is the container with pre-installed and configured MySQL database with appropriate settings for use with DataJoint
* Open up the port `3306` (default MySQL server port) on your computer so that your database server can accept connections.
* Set the password for the `root` database user to be `tutorial`. You will use this username/password combination when connecting to the database from DataJoint later.

.. note::
    To learn more about Docker commands, please refer to the `official documentation <https://docs.docker.com/engine/reference/commandline/run/>`_.

And that's it! You now should have a fully configured MySQL database server running locally on your machine!

What's next?
------------
Congratulations! You now should have a database server running on your machine, waiting for you to start creating your own data pipeline! In the next section, we will install and set up a DataJoint library and connect to your database. Pick the language of your choice:

* :doc:`datajoint-python`
* :doc:`datajoint-matlab`



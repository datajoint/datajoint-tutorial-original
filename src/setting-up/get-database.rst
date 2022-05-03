Getting connected to a database
===============================

In this section we will explore various options on how we can get connected to a database server
for use throughout the tutorial and beyond. We will review three major options, from the easiest (and 
most recommended) to the more involved but highly customizable.

Connect to `DataJoint.io <https://accounts.datajoint.io>`_ (Recommended)
------------------------------------------------------------------------

If you want to get started trying out DataJoint as quickly as possible with minimal setup, sign up for a free 
`DataJoint account <https://accounts.datajoint.io/login>`_ to gain access to the free tutorial database server in addition 
to ready-to-play interactive Python playground environment based on Jupyter. 


Follow these simple instructions to sign up for DataJoint.io account with the access to the tutorial database.

Signing up to DataJoint.io account
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Visit https://datajoint.io and click on the Sign Up button. 
2. Follow the instructions to complete the signup. You will receive an email as part of the signup process.
3. Make note of your DataJoint.io username and password. This will be the username and password for the tutorial database.

And that's it! 

.. warning:: 
   The tutorial database is provided for learning purpose only and may be periodically cleared to maintain availability
   for all DataJoint learners. Please **DO NOT** store any important data or information in the database!
   If you're ready to move on to a persistent database server, refer to the section below_ for setting up your own database server 
   or seek for-charge hosting services offered by, for example, `DataJoint NEURO <https://datajointneuro.io>`_.


.. note::
  When you create a new schema, your schema must start with ``username_`` substituting in your DataJoint.io username. For
  an example, if you sign up with username ``johndoe``, your schema name must start with ``johndoe_`` for you to have
  full control over tables defined in the schema. More details on this will be covered in the next section.

If you are interested in general database hosting service to host entire data pipelines for yourself, your lab, or large 
multi-lab collaborations, visit https://datajointneuro.io for more information.

.. _below:

Setting up a local database server (Intermediate)
-------------------------------------------------

Alternatively you can install and set up a database server to run on your local machine. This offers a very
portable solution, but it requires some additional steps to deploy the server. If you
decide to go this route, we strongly recommend you use `Docker <https://www.docker.com>`_ to download
and launch a pre-configured database server we have provided as a Docker image.

You can find a step-by-step instructions on setting up a local database server using Docker in our 
:doc:`local-database` tutorial!


.. toctree::
   :maxdepth: 2
   :hidden:
   :includehidden:

   local-database

Setting up a database server on another machine (Advanced)
----------------------------------------------------------

Finally, you might want to set up a database server on dedicated server hardware. 
Properly setting up and maintaing a database server can require significant IT expertise and
infrastructure, depending on the desired scale. If you are interested in pursuing this option, you can find useful
configuration information at `our MySQL Docker image project <https://github.com/datajoint/mysql-docker>`_.

What's next?
------------
Once you have decided on your database server option and acquired access credentials, you are ready to move onto
setting up DataJoint library in Python or MATLAB! Pick your favorite language for
step-by-step instruction on installing and setting up DataJoint library.

* :doc:`datajoint-python`
* :doc:`datajoint-matlab`


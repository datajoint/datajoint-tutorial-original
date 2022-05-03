Saving your data pipeline
=========================

Before we progress any further on the tutorial, let's discuss how you can save your hard work. In particular,
we will cover what it means to save your data pipeline in this section.

Where is my data pipeline stored?
---------------------------------

When you create tables in DataJoint, there are actually two things getting created: the table Python classes
(e.g. ``Mouse`` class) and the actual table in the database. As you saw in the :doc:`previous section <first-table>`,
you define a class to define and access a table in the database. Let's take a look at the example of the
``Mouse`` class again.

.. code-block:: python

  @schema
  class Mouse(dj.Manual):
        definition = """
        mouse_id: int                  # unique mouse id
        ---
        dob: date                      # mouse date of birth
        sex: enum('M', 'F', 'U')    # sex of mouse - Male, Female, or Unknown/Unclassified
        """

When you defined the class for the first time ever, DataJoint created a table with the corresponding name ``mouse``
in the database server. You then access this table by using an instance of this table class:

.. code-block:: python
  
  mouse = Mouse()

If in the future, you wanted to access the same table again, you would still need to 
define the class and use it's instance to manipulate the table in the database server.

Therefore, you data pipeline consists of two parts. One is the actual tables in the database server you created
using DataJoint. These tables (and schemas) persists across sessions, and all the data you inserted are stored
in the database server. Another part is the code you wrote to define and manipulate the tables - the schemas and
classes!

So, in order for you or anyone else to access the content of the table in the database server, not only do they
need access to the database server (and the right permissions) but also the code for the schema and classes
that defines what tables exist. In other words, for you to be able to access your ``Mouse`` table later, you
will need access to the ``Mouse`` class you defined!

Saving your table code
----------------------

This means that you want to be able to save the code for your class so you can load it later to access the table.
If you are running this tutorial in an interactive session (e.g. Python or IPython console) and typing all the
code interactively, then the class definition will be lost the moment you exit out of the console! Although you
can just rewrite the table class definition again the next time you start a console, this can be very cumbersome
especially when you start having multiple tables you defined.

A better solution is to place all your table class definitions into a ``.py`` file and import the table definitions
from that file at the beginning of each Python console. Let's take a quick look at what that process could look
like.

Defining your table module
^^^^^^^^^^^^^^^^^^^^^^^^^^

Each ``.py`` file you create is actually called a module, and can be imported using the familar ``import ...`` syntax.
Pick a convenient location in your file system, and create a file called ``tutorial_tables.py``, and place the code
from :doc:`first-table` in there, including schema and class definition. Your file content should look something
like the following:

.. code-block:: python
  
  import datajoint as dj

  schema = dj.schema('tutorial', locals())       # this might differ depending on how you setup

  @schema
  class Mouse(dj.Manual):
        definition = """
        mouse_id: int                  # unique mouse id
        ---
        dob: date                      # mouse date of birth
        sex: enum('M', 'F', 'U')    # sex of mouse - Male, Female, or Unknown/Unclassified
        """

Once completed, start a new Python console session **in the directory that contains the ``tutorial_tables.py``** file,
and run the following:

.. code-block:: python

  >>> import datajoint as dj
  >>> dj.config['database.host'] = ...      # specify your database address
  >>> dj.config['database.user'] = ...      # specify your username
  >>> dj.config['database.password'] = ...  # specify your password
  >>> from tutorial_tables import *

This will make the content of your Python file available for use in the interactive session. As you define more tables,
go ahead and add them to the ``tutorial_tables.py``, and you can simply import all table definitions at the beginning
of a new interactive session. 


What's next?
------------
Now you have a way to store your work, we'll go right back to working with our table.
In the :doc:`next section <querying-data>`, we will look at how to query and fetch data from your table!

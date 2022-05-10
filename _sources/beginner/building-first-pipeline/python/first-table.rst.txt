Defining your first table
=========================

Every pipeline is composed of one or more **tables**. Each table represents a specific set of data. 
In the simplest situation, a table can contain data entered either manually by a human or automatically 
by some other piece of software. These ``Manual`` tables are similar to a spreadsheet in Excel, 
for example. A table always belongs to a **schema** which helps to organize tables into groups. 
By placing related tables into one **schema** you can keep your data pipeline well structured.

.. note::

  This tutorial assumes that you already have a database server that you can connect to and that you have 
  installed DataJoint for Python. If either of these is not true, be sure to checkout our 
  :doc:`Getting Started Tutorial </setting-up/introduction>` first before proceeding with this tutorial!


Creating a schema
-----------------

Let's get started by importing DataJoint and creating a new schema to define tables in. 
Open up an interactive Python console and import ``datajoint``:

.. code-block:: python

  import datajoint as dj

Set up your connection to the database server.

.. code-block:: python

  dj.config['database.host'] = 'HOST_ADDRESS'
  dj.config['database.user'] = 'USER_NAME'
  dj.config['database.password'] = 'PASSWORD'


.. note::
  If you need a review on how to connect to the database from DataJoint, checkout :ref:`configure-python-dj`.


Let's create our first schema called ``tutorial``!


.. code-block:: python

  schema = dj.schema('tutorial', locals())

.. note::
  If you are connected to the tutorial database hosted by `DataJoint.io <https://datajoint.io>`_, 
  you will have to prefix all schema name with ``username_`` substituting in the username for the connection. 
  For example, if your username is ``johndoe``, then you would want to run the following command instead:

  .. code-block:: python
    
    schema = dj.schema('johndoe_tutorial', locals())

And that's it! We have just created a schema in the database, and now we can now begin creating tables inside of this schema.

.. note::
  Passing in ``locals()`` allows ``schema`` object to have access to all tables that you define in the local
  name space (e.g. interative session). This allows tables to refer to each other simply by their name. 


Defining the Mouse table class
------------------------------

Now we will use the ``schema`` object to create a new table. In our hypothetical example, everything starts with a particular mouse. So let's create a table to enter and track all the mice we will work with:

.. code-block:: python

  @schema
  class Mouse(dj.Manual):
        definition = """
        # mouse
        mouse_id: int                  # unique mouse id
        ---
        dob: date                      # mouse date of birth
        sex: enum('M', 'F', 'U')    # sex of mouse - Male, Female, or Unknown/Unclassified
        """

and it turns out that this is enough to define a table! There is actually a lot going on here, so let's walk through
this code step by step.

Table classes
^^^^^^^^^^^^^
In DataJoint, tables are defined and accessed via **classes** inheriting from one of the table superclasses
provided by DataJoint. Since we will be entering data about new mice manually, we want to create a table
called ``Mouse`` as a manual table. You do so by defining a class called ``Mouse`` and inheriting from 
``dj.Manual`` super-class.

Table definition
^^^^^^^^^^^^^^^^
In addition to specifying the type or "tier" of the table (e.g. ``dj.Manual``), you need to define the
columns or **attributes** of the table. You do this by setting the ``definition`` to a string with
DataJoint data definition language. Let's take a closer look a the definition string here.


Table comment
+++++++++++++

.. code-block:: python
   :emphasize-lines: 2

   definition = """
   # mouse
   mouse_id: int                  # unique mouse id
   ---
   dob: date                      # mouse date of birth
   sex: enum('M', 'F', 'U')    # sex of mouse - Male, Female, or Unknown/Unclassified
   """

The very first line of the definition starts with a comment that describes what this table is about. Although
this is optional, leaving a meaningful comment here can be really helpful when you start defining
increasingly complex tables.

Attribute (column) definition
+++++++++++++++++++++++++++++

.. code-block:: python
   :emphasize-lines: 3

   definition = """
   # mouse
   mouse_id: int                  # unique mouse id
   ---
   dob: date                      # mouse date of birth
   sex: enum('M', 'F', 'U')    # sex of mouse - Male, Female, or Unknown/Unclassified
   """

In the definition string, you define the table's attributes (or columns) one at a time, each in
a separate line. The attribute definition takes the following format:

.. code-block:: python

  attribute_name :  data_type     # comment

As you probably can guess, the ``attribute_name`` is the name of the attribute. Separated by ``:``, you then
specify the **data type** of the attribute. This determines what kind of data can go into that attribute. 

For ``mouse_id``, we have chosen type ``int`` which can hold integers between -2147483648 and 2147483647, with
the exact range depending on your database server. Since we don't expect to have that many mice, ``int`` is
a safe choice for holding the numerical ID for the mouse. 

.. note::
  In the table definition above, we have used ``date`` data type to hold dates in the form ``YYYY-MM-DD`` (e.g. 2017-01-31)
  and ``enum`` data type to have predefined values the attribute can chose from. ``enum('M', 'F', 'U')`` states that
  ``sex`` attribute can take on the value of either ``'M'``, ``'F'``, or ``'U'``.

At the end of the definition, you can give a comment describing what this attribute stores. Although this is optional, it is strongly recommended that
you add a brief comment to help remind everyone (including yourself!) what that field is about. A good combination
of a well thought-out attribute name and a good comment can help make your table very readable.

Primary vs non-primary key attributes
+++++++++++++++++++++++++++++++++++++

.. code-block:: python
   :emphasize-lines: 4

   definition = """
   # mouse
   mouse_id: int                  # unique mouse id
   ---
   dob: date                      # mouse date of birth
   sex: enum('M', 'F', 'U')    # sex of mouse - Male, Female, or Unknown/Unclassified
   """

The ``---`` separator separates two types of attributes in the table. Above the line are your **primary-key
attributes**. These attributes are used to **uniquely identify** entries in the table. Within a table, the
combination of the primary-key attributes values **must be unique**. In this case, we only have one attribute
in the primary key (``mouse_id``) and thus every entry in the table must have a distinct ``mouse_id``,
corresponding to actual mouse.

Below the ``---`` separator are **non-primary-key attributes**. As you would guess, these are attributes
that are **not** used to identify the mouse. Typically, these attributes hold values that describe the entry
(in this case a mouse) identified by the primary-key (``mouse_id``).

Defining a table in a schema
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Going back to the class ``Mouse`` definition, 

.. code-block:: python
  :emphasize-lines: 1

  @schema
  class Mouse(dj.Manual):
        definition = """
        mouse_id: int                  # unique mouse id
        ---
        dob: date                      # mouse date of birth
        sex: enum('M', 'F', 'U')    # sex of mouse - Male, Female, or Unknown/Unclassified
        """

Notice that we **decorate** the class ``Mouse`` with the ``schema`` object we created earlier. This decoration
tells DataJoint to create the table specified by the class (``Mouse``) inside the schema pointed to by the
``schema`` object (``tutorial``).


Creating the table in the data pipeline
---------------------------------------

What you might have not realized is that, when you defined the class above, you have actually created the
corresponding table in the database server! To access the table and manipulate this table, you create an
instance of the table class:

.. code-block:: python

  mouse = Mouse()

You can now use this instance (``mouse``) to look into the table in the databasee:

.. code-block:: python

  >>> mouse
  *mouse_id    dob     sex
  +----------+ +-----+ +--------+

 (0 tuples)

You should get a display of the table's contents, verifying that you indeed have defined a table in
the pipeline.

.. note::
  If this is not the fist time going through this section of the tutorial, chances are you already have
  the table ``Mouse`` defined in the schema ``tutorial``. This is completely fine! If you define the
  class ``Mouse`` and instantiate it, the ``mouse`` instance will point to the same table you defined
  the first time you went through this tutorial.

What if I make a mistake?
-------------------------
As you work through this tutorial, you might occasionally create a table with some errors.
Most commonly, you might create a table before you are completely done with the table ``definition``.
Although there are ways to update the table definition, it is usually best to simply delete or **drop**
the table with error and redefine the table after correcting your mistakes.

For example, you might have made a spelling error in your definition:

.. code-block:: python

  @schema
  class Mouse(dj.Manual):
        definition = """
        mose_id: int                   # unique mouse id
        ---
        dob: date                      # mouse date of birth
        sx: enum('M', 'F', 'U')    # sex of mouse - Male, Female, or Unknown/Unclassified
        """

Notice that both ``mouse_id`` and ``sex`` attributes are spelled incorrectly! If you don't notice the
error before you execute the class definition statment, then your table will be defined in the data 
pipeline containing these mistakes:

.. code-block:: python

  >>> mouse = Mouse()
  >>> mouse    # view the table
  *mose_id    dob     sx
  +---------+ +-----+ +------+

   (0 tuples)

Unfortunately, changing the table definition (the ``definition`` property) of the class after the table
has been created in the data pipeline does **not** change the definition of the already-existing table.

The best way to deal with this error, especially this early in the design process, is to drop the table
alltogether. You can do so as follows:

.. code-block:: python
  
  >>> mouse.drop()
  `tutorial`.`mouse` (0 tuples)
  Proceed? [yes, No]: 

Notice that the ``drop`` method prompts you to confirm the deletion, typing anything other than ``yes`` will
either result in a reprompt or cancellation. Type in ``yes`` at the prompt to confirm the drop:

.. code-block:: python
  
  >>> mouse.drop()
  `tutorial`.`mouse` (0 tuples)
  Proceed? [yes, No]: yes
  Tables dropped. Restart kernel.

Now the table is dropped, you can fix errors in your class ``definition`` and recreate the table.

.. note::
  As the prompt for the ``drop`` method suggests, you might want to restart your Python kernel after dropping
  tables. This can be important when rendering diagrams to show table connections.

What's next?
------------
Congratulations again! You have successfully created your first table in your data pipeline. 
In the :doc:`next section <inserting-data>`, we will give the table some substance by inserting data into it!

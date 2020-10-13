Defining your first table
=========================

Every pipeline is composed of one or more **tables**. Each table represents a specific set of data. In the simplest situation, a table can contain data entered either manually by a human or automatically by some other piece of software. These ``Manual`` tables are similar to a spreadsheet in Excel, for example. A table always belongs to a **schema** which helps to organize tables into groups. By placing related
tables into one **schema** you can keep your data pipeline well structured.

.. note::

  This tutorial assumes that you already have a database server that you can connect to and that you have installed DataJoint
  for Matlab. If either of this is not true, be sure to checkout our :doc:`Getting Started Tutorial </setting-up/introduction>`
  first before proceeding with this tutorial!


Creating a schema
-----------------

Let's get started by importing DataJoint and creating a new schema to define tables in. Start MATLAB and connect to your database.

.. note::
  If you need a review on how to connect to the database from DataJoint, checkout :ref:`configure-matlab-dj`.


Let's create our first schema called ``tutorial``! Type ``dj.createSchema`` and enter ``tutorial_db`` when prompted for the database name.


.. code-block:: matlab

  dj.createSchema
  Enter database name >> tutorial

Then a GUI window will appear to prompt you for the package folder. Navigate to your desired directory and enter ``+tutorial`` to create a new package folder.

.. note::
  If you are connected to the tutorial database hosted by `DataJoint.io <https://datajoint.io>`_, you will have to prefix 
  the the schema name with your username followed by underscore: ``username_``. For example, if your username is 
  ``johndoe``, then you would do the following:

.. code-block:: matlab

  dj.createSchema
  Enter database name >> johndoe_tutorial


And that's it! We have just created a schema in the database, and now we can now begin creating tables inside of this schema.

Defining the Mouse table class
------------------------------

Now we will create a new table. In our hypothetical example, everything starts with a particular mouse. 
So let's create a table to enter and track all the mice we will work with. Open a new script called
``Mouse.m`` inside your newly crated ``+tutorial`` package and copy the following into the file:

.. code-block:: matlab

  %{
  # mouse
  mouse_id: int                  # unique mouse id
  ---
  dob: date                      # mouse date of birth
  sex: enum('M', 'F', 'U')       # sex of mouse - Male, Female, or Unknown/Unclassified
  %}

  classdef Mouse < dj.Manual
  end

and it turns out that this is enough to define a table! There is actually a lot going on here, so let's walk through
this code step by step.

Table classes
^^^^^^^^^^^^^
In DataJoint, tables are defined and accessed via **classes** inheriting from one of the table superclasses
provided by DataJoint. Since we will be entering data about new mice manually, we want to create a table
called "Mouse" as a manual table. You do so by defining a class called ``Mouse`` and inheriting from 
``dj.Manual`` super-class.

Table definition
^^^^^^^^^^^^^^^^
In addition to specifying the type or "tier" of the table (e.g. ``dj.Manual``), you need to define the
columns or **attributes** of the table. You define these in the header comment of the class using the
DataJoint data definition language. Let's take a closer look a the definition string here.


Table comment
+++++++++++++

.. code-block:: matlab
  :emphasize-lines: 2

  %{
  # mouse
  mouse_id: int                  # unique mouse id
  ---
  dob: date                      # mouse date of birth
  sex: enum('M', 'F', 'U')       # sex of mouse - Male, Female, or Unknown/Unclassified
  %}

The very first line of the definition starts with a ``# comment`` that describes what this table is about. Although
this is optional, leaving a meaningful comment here can be really helpful when you start defining
increasingly complex tables.

Attribute (column) definition
+++++++++++++++++++++++++++++

.. code-block:: matlab
  :emphasize-lines: 3

  %{
  # mouse
  mouse_id: int                  # unique mouse id
  ---
  dob: date                      # mouse date of birth
  sex: enum('M', 'F', 'U')       # sex of mouse - Male, Female, or Unknown/Unclassified
  %}

In the definition string, you define the table's attributes (or columns) one at a time, each in
a separate line. The attribute definition takes the following format:

.. code-block:: matlab

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

.. code-block:: matlab
  :emphasize-lines: 4

  %{
  # mouse
  mouse_id: int                  # unique mouse id
  ---
  dob: date                      # mouse date of birth
  sex: enum('M', 'F', 'U')       # sex of mouse - Male, Female, or Unknown/Unclassified
  %}

The ``---`` separator separates two types of attributes in the table. Above the line are your **primary-key
attributes**. These attributes are used to **uniquely identify** entries in the table. Within a table, the
combination of the primary-key attributes values **must be unique**. In this case, we only have one attribute
in the primary key (``mouse_id``) and thus every entry in the table must have a distinct ``mouse_id``,
corresponding to an actual mouse.

Below the ``---`` separator are **non-primary-key attributes**. As you would guess, these are attributes
that are **not** used to identify the mouse. Typically, these attributes hold values that describe the entry
(in this case a mouse) identified by the primary-key (``mouse_id``).

Defining a table in a schema
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Save your new class as ``Mouse.m`` in the ``+tutorial`` package folder. You may notice that there is a new function ``getSchema`` in that folder that was created by ``dj.createSchema``. This function returns the schema object that links the Matlab package ``+tutorial`` with the ``tutorial_db`` schema in the database. 

Creating the table in the data pipeline
---------------------------------------

Calling the ``Mouse`` class for the first time creates the corresponding table in the database server.
DataJoint displays the SQL code used to create the table.

.. code-block:: matlab

   >> tutorial.Mouse

   ans = 

   <SQL>
   CREATE TABLE `tutorial`.`mouse` (
   `mouse_id` int                   NOT NULL COMMENT "unique    
   mouse id",
   `dob` date                       NOT NULL COMMENT "mouse date      
   of birth",
   sex` enum('M', 'F', 'U') NOT NULL COMMENT "sex of  mouse -    
   Male, Female, or Unknown/Unclassified",
   PRIMARY KEY (`mouse_id`)
   ) ENGINE = InnoDB, COMMENT "mouse"
   </SQL>

You can also see a preview of the table contents in the database by typing ``tutorial.Mouse``:

.. code-block:: matlab

  >> tutorial.Mouse

  Object tutorial.Mouse

  :: mouse ::

  0 tuples (0.00769 s)

Of course at this point there are no entries in the mouse table.

.. note::
  If this is not the first time going through this section of the tutorial, chances are you already have
  the table ``Mouse`` defined in the schema ``tutorial``. This is completely fine! The table is only created the first time you instantiate the class.

What if I make a mistake?
-------------------------
As you work through this tutorial, you might occasionally create a table with some errors.
Most commonly, you might create a table before you are completely done with the table ``definition``.
Although there are ways to update the table definition, it is usually best to simply delete or **drop**
the table with error and redefine the table after correcting your mistakes.

For example, you might have made a spelling error in your definition:

.. code-block:: matlab

   %{
   # mouse
   mose_id: int                  # unique mouse id
   ---
   dob: date                     # mouse date of birth
   sx: enum('M', 'F', 'U')       # sex of mouse - Male, Female, or  Unknown/Unclassified
   %}

   classdef Mouse < dj.Manual
   end


Notice that both ``mouse_id`` and ``sex`` attributes are spelled incorrectly! If you don't notice the
error before you instantiated your table class:

.. code-block:: matlab
  
  tutorial.Mouse   % instantiating table with errors in definition

Then your table will be defined in the data pipeline containing these mistakes. 
Unfortunately, changing the table definition (the ``definition`` property) of the class after the table
has been created in the data pipeline does **not** change the definition of the already-existing table.

The best way to deal with this error, especially this early in the design process, is to drop the table
alltogether. You can do so as follows:

.. code-block:: matlab
  
  >>drop(tutorial.Mouse)
  ABOUT TO DROP TABLES: 
  `tutorial`.`mouse` (manual,    0 tuples)
  Proceed? (y/N)  y
  Dropped table `tutorial`.`mouse`

Now the table is dropped, you can fix errors in your class ``definition`` and recreate the table.

Where is my data pipeline stored?
---------------------------------

When you create tables in DataJoint, there are actually two things getting created: the table Matlab classes
(e.g. ``Mouse`` class) and the actual table in the database. As you saw above,
you define a class in Matlab to define and access a table in the database. 

Therefore, your data pipeline consists of two parts. One is the actual tables in the database server you created
using DataJoint. These tables (and schemas) persists across sessions, and all the data you inserted are stored
in the database server. Another part is the code you wrote to define and manipulate the tables - the schemas and
classes!

So, in order for you or anyone else to access the content of the table in the database server, not only do they
need access to the database server (and the right permissions) but also the code for the schema and classes
that defines what tables exist. For one schema, these are all stored in the same Matlab package folder 
(in this case, ``+tutorial``).

What's next?
------------
Congratulations again! You have successfully created your first table in your data pipeline. 
In the :doc:`next section <inserting-data>`, we will give the table some substance by inserting data into it!

Populating the table
====================

A table with no content is really not too useful, so let's **populate** the ``Mouse`` table by inserting some data
manually. Let's explore a few different ways to insert data into the table, first one entry at a time,
and then multiple entries at once.

Inserting one entry at a time
-----------------------------

Let's first explore how you can enter new data, one row at a time.

Inserting a tuple/list
^^^^^^^^^^^^^^^^^^^^^^

You can insert a single entry (a single row in the table) as a Python *tuple* or *list*, with values in the order
of the attributes in the table:

.. code-block:: python

  mouse.insert1( (0, '2017-03-01', 'M') )

Here we used the table's ``insert1`` method to insert a new mouse with ``mouse_id`` of ``0``, ``dob``
(date of birth) of ``2017-03-01`` and ``sex`` ``M`` (male).

Verify the new entry by checking the table's content again:

.. code-block:: python

  >>> mouse
  *mouse_id    dob            sex
  +----------+ +------------+ +--------+
  0            2017-03-01     M
   (1 tuples)

Inserting a dictionary
^^^^^^^^^^^^^^^^^^^^^^

Alternatively you can first define a dictionary with attribute names as keys and fill in the values.

.. code-block:: python
  
  data = {
    'mouse_id': 100,
    'dob': '2017-05-12',
    'sex': 'F'
  }

and then insert this dictionary into the table:

.. code-block:: python

  mouse.insert1(data)

Resulting in a new entry:

.. code-block:: python

  >>> mouse
  *mouse_id    dob            sex
  +----------+ +------------+ +--------+
  0            2017-03-01     M
  100          2017-05-12     F
   (2 tuples)

Inserting multiple entries at a time
------------------------------------

You can insert multiple entries at a time by passing in a list of tuples or list of dictionaries into the
table's ``insert`` method (instead of the ``insert1`` method). Let's prepare a few more entries
and insert them all together.

.. code-block:: python

  data = [
    (1, '2016-11-19', 'M'),
    (2, '2016-11-20', 'U'),
    (5, '2016-12-25', 'F')
  ]

  # now insert all at once
  mouse.insert(data)

Verify the insert:

.. code-block:: python

  >>> mouse
  *mouse_id    dob            sex
  +----------+ +------------+ +--------+
  0            2017-03-01     M
  1            2016-11-19     M
  2            2016-11-20     U
  5            2016-12-25     F
  100          2017-05-12     F
   (5 tuples)

You can also do the same with a list of dictionaries:

.. code-block:: python

  data = [
    {'mouse_id': 10, 'dob': '2017-01-01', 'sex': 'F'},
    {'mouse_id': 11, 'dob': '2017-01-03', 'sex': 'F'},
  ]
  
  # insert them all
  mouse.insert(data)

This results in:

.. code-block:: python

  >>> mouse
  *mouse_id    dob            sex
  +----------+ +------------+ +--------+
  0            2017-03-01     M
  1            2016-11-19     M
  2            2016-11-20     U
  5            2016-12-25     F
  10           2017-01-01     F
  11           2017-01-03     F
  100          2017-05-12     F
   (7 tuples)

.. _python-duplicate-entry:

Data integrity
--------------
One of the key features of DataJoint is data integrity - a series of checks and restrictions to make sure that
our data remains consistent through its life in the data pipeline. 

Data integrity in DataJoint starts at data
entry. What does this mean? Well **data duplication** is prevented by checking and rejecting entries with already existing primary
key values. You can see this check in action by trying to insert a new entry with ``mouse_id`` that already exists
in the table.

.. code-block:: python

  >>> mouse.insert1((0, '2015-03-03', 'U'))  # mouse with ---------------------------------------------------------------------------
  IntegrityError                            Traceback (most recent call last)
  <ipython-input-44-ce3dd3a7f75c> in <module>()
  ----> 1 mouse.insert1((0, '2015-03-03', 'U'))
  ...output truncated...
  IntegrityError: (1062, "Duplicate entry '0' for key 'PRIMARY'")

As you can see, trying to make a duplicate entry results in an ``IntegrityError``. As you step through the tutorial,
you will see more examples of how DataJoint ensures data integrity at every step of the way (but without
requiring much effort from your side).

What's next?
------------
Now that you have successfully entered some data into your first table, the data pipeline has some data to work
with. In the up-coming section, we will look at how to query and fetch data from your table!
But before we do that, let's take a loot at how to save your work in the 
:doc:`next section <save-tables>`. This way, you can take a break and then later pick up this tutorial
right where you left off without fear of losing your work!

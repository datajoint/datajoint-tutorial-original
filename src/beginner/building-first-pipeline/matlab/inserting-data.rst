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

You can insert a single entry (a single row in the table) as a Matlab *cell array*, with values in the order
of the attributes in the table. Numeric fields must have numberic values, character or date fields should be character arrays enclosed in single quotes:

.. code-block:: matlab

  insert(tutorial.Mouse, {0, '2017-03-01', 'M'} )

Here we used the ``insert`` method to insert a new mouse with ``mouse_id`` of ``0``, ``dob``
(date of birth) of ``2017-03-01`` and ``sex`` ``M`` (male).

Verify the new entry by checking the table's content again:

.. code-block:: matlab

  :: mouse class ::

    MOUSE_ID       dob        gender
    ________    __________    ______

    0           2017-03-01    M     

   1 tuples (0.375 s)

Inserting a structure
^^^^^^^^^^^^^^^^^^^^^

Alternatively you can first define a structure with attribute names as keys and fill in the values.

.. code-block:: matlab
  
  data = struct(...
    'mouse_id', 100,...
    'dob', '2017-05-12',...
    'sex', 'F')

and then insert this dictionary into the table:

.. code-block:: matlab

  insert(tutorial.Mouse,data)

Resulting in a new entry:

.. code-block:: matlab

   >> tutorial.Mouse

   ans = 


   Object tutorial.Mouse

   :: mouse class ::

    MOUSE_ID        dob         sex
    ________    ____________    ___

      0         '2017-03-01'    'M'
    100         '2017-05-12'    'F'

   2 tuples (0.09 s)

Inserting multiple entries at a time
------------------------------------

You can insert multiple entries at a time by passing in an array of tuples (cells) or array of structures into the
table's ``insert`` method. Let's prepare a few more entries
and insert them all together.

.. code-block:: matlab

  data = [
    {1, '2016-11-19', 'M'},
    {2, '2016-11-20', 'U'},
    {5, '2016-12-25', 'F'}
  ]

  % now insert all at once
  insert(tutorial.Mouse, data)

Verify the insert:

.. code-block:: matlab

   >> tutorial.Mouse

   ans = 


   Object tutorial.Mouse

    :: mouse class ::

    MOUSE_ID        dob         sex
    ________    ____________    ___

      0         '2017-03-01'    'M'
      1         '2016-11-19'    'M'
      2         '2016-11-20'    'U'
      5         '2016-12-25'    'F'
    100         '2017-05-12'    'F'

   5 tuples (0.0941 s)

You can also do the same with an array of structures:

.. code-block:: matlab

  data(1) = struct(...
    'mouse_id', 10, 'dob', '2017-01-01', 'sex', 'F');
  data(2) = struct(...
    'mouse_id', 11, 'dob', '2017-01-03', 'sex', 'F')
  
  % insert them all
  insert(tutorial. Mouse, data)

This results in:

.. code-block:: matlab

  >> tutorial.Mouse

  ans = 


  Object tutorial.Mouse

   :: mouse class ::

    MOUSE_ID        dob         sex
    ________    ____________    ___

      0         '2017-03-01'    'M'
      1         '2016-11-19'    'M'
      2         '2016-11-20'    'U'
      5         '2016-12-25'    'F'
     10         '2017-01-01'    'F'
     11         '2017-01-03'    'F'
    100         '2017-05-12'    'F'

  7 tuples (0.0273 s)

.. _matlab-duplicate-entry:

Data integrity
--------------
One of the key features of DataJoint is data integrity - a series of checks and restrictions to make sure that
our data remains consistent through its life in the data pipeline. 

Data integrity in DataJoint starts at data
entry. What does this mean? Well **data duplication** is prevented by checking and rejecting entries with already existing primary
key values. You can see this check in action by trying to insert a new entry with ``mouse_id`` that already exists
in the table.

.. code-block:: matlab

  >> insert(tutorial.Mouse,{0, '2015-03-03', 'U'})  % mouse
  Error using mym
  Duplicate entry '0' for key 'PRIMARY'

  Error in dj.Connection/query (line 174)
                mym(self.connId, queryStr, v{:});

  Error in dj.Relvar/insert (line 272)
            self.schema.conn.query(command, blobs{:});

As you can see, trying to make a duplicate entry results in an error. As you step through the tutorial,
you will see more examples of how DataJoint ensures data integrity at every step of the way (but without
requiring much effort from your side).

What's next?
------------
Now that you have successfully entered some data into your first table, the data pipeline has some data to work
with. In the 
:doc:`next section <querying-data>`, we will look at how to query and fetch data from your table!

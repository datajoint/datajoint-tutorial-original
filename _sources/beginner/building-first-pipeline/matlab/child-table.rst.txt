Defining dependent tables
=========================

In this section, we will create another **manual** table to store information about each experimental
session. In doing so, we will see how to **link** two tables via dependencies, expressing how
one table **depends** on another table.

Defining ``tutorial.Session`` table
-----------------------------------

Now we have defined the ``Mouse`` table to store and identify all mice in our lab, we would like to
define a table called ``Session`` that will keep track of data related to all mouse experiments.

When designing a new table, it is always a good idea to start by identify the set of attributes that  
can be used to uniquely identify an entry in the table - this is the primary key.
From the descriptions given back in :doc:`../index`, 1) an experiment session involves
one mouse, 2) you can record from the same mouse on different days and 3) you could perform experiments on multiple mice per day. Putting this all together, we see that each experiment
can be uniquely identified by knowing 1) on which mouse it was performed on **and** 2) on which
day the experiment was performed on.

Given this we would want to each entry (row) of ``tutorial.Session`` table to be identified by the combination of
the ``tutorial.Mouse`` identity and the session date. Now, notice that this means every entry of ``tutorial.Session`` must
have a corresponding entry in the ``tutorial.Mouse`` table, reflecting the fact that you cannot perform an
experiment without a mouse! In other words, the ``Session`` table **depends** on the ``Mouse``
table.

DataJoint lets you formalize this relationship by expressing this dependency in the table's definition. Let's take
a look at how ``tutorial.Session`` table may be defined:

.. code-block:: matlab
   :emphasize-lines: 3

    %{
    # experiment session
    -> tutorial.Mouse
    session_date: date            # session date
    ---
    experiment_setup: int         # experiment setup ID
    experimenter: varchar(128)    # name of the experimenter
    %}

    classdef Session < dj.Manual
    end


The definition of the ``tutorial.Session`` table looks very similar to that of ``tutorial.Mouse`` except for one notable
difference. We have this peculiar arrow notation ``-> tutorial.Mouse`` in the table definition.

.. note::
  This table uses a new data type called ``varchar``, which stands for variable-length characters.
  You can use this data type to store string values up to the number specified in parenthesis. In this
  case, the name of the ``experimenter`` can be up to 128 characters long.


``->`` for dependency specification
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This arrow notation states that this table (``tutorial.Session``) **depends** on the following table, in this
case ``tutorial.Mouse``. Let's go ahead and instantiate the table to see what the table would look like:

.. code-block:: matlab


   >> tutorial.Session

   ans = 


   <SQL>
   CREATE TABLE `tutorial`.`session` (
   `mouse_id` int NOT NULL COMMENT "unique mouse id", 
   CONSTRAINT `5da59163bc04` FOREIGN KEY (`mouse_id`) REFERENCES `tutorial`.`mouse` (`mouse_id`) ON UPDATE CASCADE ON DELETE   
   RESTRICT,
   `session_date` date             NOT NULL COMMENT "session date",
   `experiment_setup` int          NOT NULL COMMENT "experimental setup ID",
   `experimenter` varchar(128) NOT NULL COMMENT "name of the  experimenter",
   PRIMARY KEY (`mouse_id`,`session_date`)
   ) ENGINE = InnoDB, COMMENT "experiment session"
   </SQL>

   Object tutorial.Session

  :: experiment session ::

   0 tuples (0.245 s)

Notice how the ``tutorial.Session`` table now includes the ``mouse_id`` as an attribute in its primary key despite 
never explicitly specifying this in the definition. By specifying that ``tutorial.Session`` depends on ``tutorial.Mouse``,
DataJoint automatically added the primary key attributes of the parent table (``tutorial.Mouse``) into
the dependent/child table (``tutorial.Session``). This way, every entry in the ``tutorial.Session`` table will have a
``mouse_id`` which in turn can be used to uniquely identify the mouse in the ``tutorial.Mouse`` table that the experiment was performed on.

Dependency in action
--------------------
Now that we have the ``tutorial.Session`` table defined, let's populate this table with some data, using techniques we
learned in :doc:`inserting-data`. Remember that we can only perform experiments on a mouse that exists in the ``tutorial.Mouse`` table:

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

  7 tuples (0.0627 s)

Let's insert a new session into ``tutorial.Session`` table

.. code-block:: matlab

  >> data = struct(...
        'mouse_id', 0,...
        'session_date', '2017-05-15',...
        'experiment_setup', 0,...
        'experimenter', 'Edgar Walker'...
      )
  >> insert(tutorial.Session, data)
  >> tutorial.Session
  ans = 


  Object tutorial.Session

  :: experiment session ::

    MOUSE_ID    SESSION_DATE    experiment_setup    experimenter
    ________    ____________    ________________    ____________

    0           2017-05-15      0                   [1x12 char] 

  1 tuples (0.0517 s)

Using a valid ``mouse_id``, we were able to successfully insert a new session. Now what would happen
if try to enter a session for a mouse that does **not** exist? Let's try it!

.. code-block:: matlab

  >> data = struct(...
        'mouse_id', 9999,...
        'session_date', '2017-01-01',...
        'experiment_setup', 0,...
        'experimenter', 'Edgar Walker'...
      )

  >> insert(tutorial.Session, data)
  Error using mym
  Cannot add or update a child row: a foreign key
  constraint fails (`tutorial`.`session`, CONSTRAINT
  `5da59163bc04` FOREIGN KEY (`mouse_id`) REFERENCES
  `mouse` (`mouse_id`) ON UPDATE CASCADE)

  Error in dj.Connection/query (line 174)
                mym(self.connId, queryStr, v{:});

  Error in dj.Relvar/insert (line 272)
            self.schema.conn.query(command, blobs{:});

Aha! We get an error message complaining about a 
foreign key constraint. A foreign key constraint is database lingo for the dependency that
links two tables. In this case, the attribute ``mouse_id`` from ``dj_tutorial.session`` table
(this is the underlying table name for the ``tutorial.Session`` table object) is linked to the ``mouse_id``
attribute in ``dj_tutorial.mouse`` table (``tutorial.Mouse`` table) by a "foreign key constraint".

The foreign key constrain ensures that a linked attributes value exists in the target table. In this
case we tried to insert a row with ``mouse_id = 9999`` which does *not* exist in the ``tutorial.Mouse``
table and thus this violates the foreign key constraint.

Integrity with table dependencies
---------------------------------

Defining table dependencies as was done from ``tutorial.Session`` to ``tutorial.Mouse`` allows
DataJoint to enforce data integrity by linking related table entries together. As we saw,
this dependency can prevent us from entering data for an invalid target (such as trying to
record a session for a mouse that doesn't exist). 

Furthermore, DataJoint uses dependencies to ensure that no dependent entires can be left "orphaned". Let's see what we mean by that.

Deleting dependent entries
^^^^^^^^^^^^^^^^^^^^^^^^^^
Remember the ``delete`` method back from :ref:`python-delete-entries`? Let's see what happens 
if we try to delete entries in the ``tutorial.Mouse`` table that have dependent entries in ``tutorial.Session``.

Recall that ``tutorial.Session`` table has an entry that points to mouse with ``mouse_id=0``:

.. code-block:: matlab
  
  >> tutorial.Session
  ans = 


  Object tutorial.Session

  :: experiment session ::

    MOUSE_ID    SESSION_DATE    experiment_setup    experimenter
    ________    ____________    ________________    ____________

    0           2017-05-15      0                   [1x15 char] 

  1 tuples (0.0148 s)

Let's first try deleting an unrelated mouse entry:

.. code-block:: matlab

  >> del(tutorial.Mouse & 'mouse_id = 1')   % delete mouse with ID of 1
 
   ABOUT TO DELETE:
       1 tuples from `tutorial`.`mouse` (manual)

   Proceed to delete? (yes/no) > no

The ``del`` method warns you that you will be deleting one entry from ``tutorial.Mouse``, as expected. Type 'no' to cancel the deletion, and now let's see what happens when we try to delete ``mouse_id=0``:

.. code-block:: matlab

   >> del(tutorial.Mouse & 'mouse_id = 0')   % delete mouse with ID of 0

   ABOUT TO DELETE:
       1 tuples from `tutorial`.`mouse` (manual)
       1 tuples from `tutorial`.`session` (manual)

   Proceed to delete? (yes/no) > 

Notice how ``delete`` method tells you that in addition to the entry in the ``tutorial.Mouse`` table,
an additional entry in the ``tutorial.Session`` table will be deleted as well! Because there are
entries in ``tutorial.Session`` table that **depends** on the entry in ``tutorial.Mouse`` we are about to delete,
we **have to** delete both the parent and the dependent entries all together!

This **cascading delete** ensures that you cannot leave data entries "orphaned" - leaving behind
entries that depends on non-existent parent entries. In addition to the prevention of duplication
entries as we saw in :ref:`matlab-duplicate-entry`, foreign key constraint (dependency) checks and
cascading deletes are a key part of DataJoint's strength in maintaining data integrity.

What's next?
------------
We are progressing well in our data pipeline creation adventure. We have successfully defined a
new table that **depends** on our previous table, thereby starting to form connections or "pipes"
in our data pipeline. With two linked tables, we can now perform even more exciting queries as 
we will cover in the :doc:`next section <more-queries>`.

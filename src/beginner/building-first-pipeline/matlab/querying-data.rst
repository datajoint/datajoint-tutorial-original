Querying and fetching data
==========================

Now that we covered how to insert data into the table, you might be wondering how to retreive it. In this section, we will explore not only how to fetch the data, but how to 
narrow down and only fetch the data you want. But first let's start with the simplest case -
let's fetch all the data in the table.

Fetching all the data
---------------------

You can fetch all the data stored in a table by simply calling the ``fetch`` method on the table object:

.. code-block:: matlab
  
  data = fetch(tutorial.Mouse,'*')    % this retrieves all data in the table

By default the data is retrieved as an array of structures:

.. code-block:: matlab

  >> data

  data = 

  7x1 struct array with fields:

    mouse_id
    dob
    sex

Fetching specific attributes
----------------------------
In the above example we fetched all the attributes (columns) by passing '*' as the second argument. If you are only interested in specific attributes (columns) of the table,
you can specify them. Let's try fetching only the date of birth of all mice.

.. code-block:: matlab

  >> fetch(tutorial.Mouse,'dob')

  ans = 

  7x1 struct array with fields:

    mouse_id
    dob

Note that ``fetch`` always returns the primary key attributes as well as whatever attributes you specify. If you just want the attributes alone, you can use fetchn instead. This can also be used to fetch multiple attributes separately, just pass them as additional arguments:

.. code-block:: matlab

  >> [sex,id]=fetchn(tutorial.Mouse,'sex','mouse_id')

  sex = 

    'M'
    'M'
    'U'
    'F'
    'F'
    'F'
    'F'


  id =

     0
     1
     2
     5
    10
    11
   100

Now that you have seen how to insert and then fetch data from a table, you could already start to use 
tables to store simple data. However, the true power of DataJoint comes about when you 
start combining these operations with DataJoint's simple yet very powerful **query** language.

Querying Data
-------------

The process of **querying** data refers to the searching and narrowing down of the existing data to find
exactly what you need. Rather than retrieving all data and then writing your own parsing function to extract the data you want, you can use DataJoint's query language to narrow things down first and then only
retrieve what you need. Let's take a look, using our ``Mouse`` table as the example.

At the moment, the ``Mouse`` table contains several entries:

.. code-block:: matlab

  > tutorial.Mouse

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

  7 tuples (0.0145 s)

.. note::
  Before moving on, feel free to add more entries into your table using any one of insert methods
  that was covered in :doc:`inserting-data`.

Restricting by attribute value
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's start with a very simple query, looking for an entry with a specific value of an attribute. We
can find information about the mouse with `mouse_id = 0` as follows:

.. code-block:: matlab

  >> tutorial.Mouse & 'mouse_id=0'

  ans = 


  Object tutorial.Mouse

  :: mouse class ::

    MOUSE_ID       dob        sex
    ________    __________    ___

    0           2017-03-01    M  

  1 tuples (0.0228 s)

Let's take a closer look at what just happened. We used the ``&`` (restriction)
operation to **restrict** tutorial.Mouse down to entries that matches the **restriction** ``mouse_id = 0``. Since there is only
one mouse with ``mouse_id = 0`` (recall that ``mouse_id`` is the primary key), we get back only one entry.

Now, let's say we want to list only male mice. This is easily done by:

.. code-block:: matlab

  >> tutorial.Mouse & 'sex="M"'

  ans = 


  Object tutorial.Mouse

  :: mouse class ::

    MOUSE_ID        dob         sex
    ________    ____________    ___

    0           '2017-03-01'    'M'
    1           '2016-11-19'    'M'

  2 tuples (0.0196 s)

Notice that ``"M"`` was surrounded by double quotes (``"``) because the value was non-numeric.

Using inequality in restriction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We can also use inequalities in our query, for eample to search for all mice born after Jan 1, 2017:

.. code-block:: matlab

  >> tutorial.Mouse & 'dob > "2017-01-01"'

  ans = 


  Object tutorial.Mouse

   :: mouse class ::

    MOUSE_ID        dob         sex
    ________    ____________    ___

      0         '2017-03-01'    'M'
     11         '2017-01-03'    'F'
    100         '2017-05-12'    'F'

  3 tuples (0.0194 s)

Or you can find all mice that are **not** male:

.. code-block:: matlab
  
  >> tutorial.Mouse & 'sex!="M"'

  ans = 


   Object tutorial.Mouse

  :: mouse class ::

    MOUSE_ID        dob         sex
    ________    ____________    ___

      2         '2016-11-20'    'U'
      5         '2016-12-25'    'F'
     10         '2017-01-01'    'F'
     11         '2017-01-03'    'F'
    100         '2017-05-12'    'F'

  5 tuples (0.0174 s)

Combining restrictions
^^^^^^^^^^^^^^^^^^^^^^

You can also *combine* multiple restrictions to form more complex queries:

.. code-block:: matlab

  >> tutorial.Mouse & 'dob > "2017-01-01"' & 'sex = "M"'  

  ans = 


  Object tutorial.Mouse

  :: mouse class ::

    MOUSE_ID       dob        sex
    ________    __________    ___

    0           2017-03-01    M  

  1 tuples (0.0181 s)

Restricting by a structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you are only looking for an equivalence of attribute values (i.e. you only need to use ``=`` in the restriction),
you can also use a dictionary to restrict.

For example, the earlier query:

.. code-block:: matlab

  >> tutorial.Mouse & 'sex="M"'

  ans = 


  Object tutorial.Mouse

   :: mouse class ::

    MOUSE_ID        dob         sex
    ________    ____________    ___

    0           '2017-03-01'    'M'
    1           '2016-11-19'    'M'

  2 tuples (0.0156 s)
 
can also be achieved using a dictionary as follows:

.. code-block:: matlab

  >> r.sex = 'M';
  >> tutorial.Mouse & r

  ans = 


  Object tutorial.Mouse

  :: mouse class ::

    MOUSE_ID        dob         sex
    ________    ____________    ___

    0           '2017-03-01'    'M'
    1           '2016-11-19'    'M'

  2 tuples (0.0363 s)

Restricting with a dictionary comes in handy when you want to restrict by multiple attribute values.

Fetching query results
----------------------

Once you are happy with your query, you can fetch only the matching entries by calling fetch on the query
result:

.. code-block:: matlab

  >> fetch(tutorial.Mouse & 'dob > "2017-01-01"' & 'sex = "M"','*')

  ans = 

    mouse_id: 0
         dob: '2017-03-01'
         sex: 'M'

Not only does querying with DataJoint makes retrieving certain subsets of data easier, it also helps you
avoid unnecessary data transfers between the database server and your computer. While you are
forming and previewing queries, the query processing is actually performed by the database server, 
and only minimal data (if any) is transferred between the database server and your computer.

When you call ``fetch`` on the query result, only the relevant data is transfered, thus potentially cutting down
the amount of data that has to be transferred out of the database server to your local machine. Not only does
it save space on your machine, but can also significantly reduce data transfer speed and also help to reduce
load on the database server.

.. _matlab-delete-entries:

Deleting entries
----------------

Now that we have learned how to restrict our selection from a table, it's
time to review how to **delete** entries. You can delete entries by calling the ``del`` method:

.. code-block:: matlab

  >> del(tutorial.Mouse)

  ABOUT TO DELETE:
       7 tuples from `tutorial`.`mouse` (manual)

  Proceed to delete? (yes/no) > 

Type in "no" to cancel the deletion. If you can only
delete all entries, then this would not be too useful. Fortunately, you can delete a restricted
table. For example, if I want to specifically delete the mouse with ID of 0:

.. code-block:: matlab
 
  >> del(tutorial.Mouse & 'mouse_id = 0')   % delete mouse with ID of 0

  ABOUT TO DELETE:
       1 tuples from `tutorial`.`mouse` (manual)

  Proceed to delete? (yes/no) > 


What's next?
------------
In this section, we learned how to fetch data from the table using the ``fetch`` method. We also met our
first query operation, ``&`` (restriction) and learned how it can be used to narrow down your query
results and fetch them. Finally we learned how to delete table entries using the ``delete`` method, and
also learned how to delete only specific entires by using restriction on the table.
As you progress through the tutorials and create more tables, you will learn additional 
operations and how to combine them into more powerful yet intuitive queries.

In the :doc:`next section <child-table>`, we will move forward in our data pipeline creation by creating and **linking** additional
tables together.

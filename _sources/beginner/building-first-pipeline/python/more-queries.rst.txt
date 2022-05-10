Queries with multiple tables
============================

Now that we have more than one table in our data pipeline, you can perform more exciting queries!
In this section, we'll take a look at how we can form queries using multiple tables, and we'll
look at a few new exciting query operators as well!

Restriction by other table
--------------------------
In :doc:`querying-data`, we have seen how you can **restrict** a table by strings and/or dictionaries
to narrow down the query results, returning only the entries that you are interested in. For example,
you can find all male mice with:

.. code-block:: python

  >>> mouse & 'sex = "M"'
  *mouse_id    dob            sex
  +----------+ +------------+ +--------+
  0            2017-03-01     M
  1            2016-11-19     M
   (2 tuples)


It turns out, that we can also use **another table** to restrict a table in a query! Consider the ``Session``
table that we created in :doc:`child-table`.

.. code-block:: python

  >>> session
  *mouse_id    *session_date  experiment_set experimenter
  +----------+ +------------+ +------------+ +------------+
  0            2017-05-15     0              Edgar Walker
  0            2017-05-19     0              Edgar Walker
  5            2017-01-05     1              Fabian Sinz
  100          2017-05-25     1              Jake Reimer
   (4 tuples)

.. note::
  Notice that I have added a frew more entries into the ``Session`` table using insert methods covered
  in :doc:`inserting-data`. Go ahead and add more entries into the table before proceeding.

We can ask questions like "What are all the mice that I have at least one experiment session done on?" by
restricting a table with another table:

.. code-block:: python
  
  >>> mouse & session
  *mouse_id    dob            sex
  +----------+ +------------+ +--------+
  0            2017-03-01     M
  5            2016-12-25     F
  100          2017-05-12     F
   (3 tuples)

and there it goes! Restricting a table ``A`` with another table ``B`` asin ``A & B`` returns all entries in
``A`` with corresponding entries in ``B``!

Combining restricitions
^^^^^^^^^^^^^^^^^^^^^^^

We can now combine multiple restrictions to get more complex queries intuitively!
Let's take a look at a few examples:

**Q.** Give me all sessions recorded for male mice

**A.** We can first get all male mice, and then get sessions corresponding to them.

.. code-block:: python

  >>> male_mice = mouse & 'sex = "M"'  # get all male mice
  >>> male_mice
  *mouse_id    dob            sex
  +----------+ +------------+ +--------+
  0            2017-03-01     M
  1            2016-11-19     M
   (2 tuples)

  >>> session & male_mice    # get all sessions for the male mice
  *mouse_id    *session_date  experiment_set experimenter
  +----------+ +------------+ +------------+ +------------+
  0            2017-05-15     0              Edgar Walker
  0            2017-05-19     0              Edgar Walker
   (2 tuples)

or you could have combine this into one statement as in:

.. code-block:: python

  >>> session & (mouse & 'sex = "M"')
  *mouse_id    *session_date  experiment_set experimenter
  +----------+ +------------+ +------------+ +------------+
  0            2017-05-15     0              Edgar Walker
  0            2017-05-19     0              Edgar Walker
   (2 tuples)

As you get used to the DataJoint queries, you will quickly learn to read above queries as 
"all sessions for mouse with sex male"!

**Q.** Give me all mice that have had an experimental session done on or after 2017-05-19

**A.** Again we can break this into parts first - get all sessions done on or after 2017-05-19 and then
find all mice corresponding to those sessions!

.. code-block:: python

  >>> target_sessions = session & 'session_date >= "2017-05-19"'
  >>> target_sessions
  *mouse_id    *session_date  experiment_set experimenter
  +----------+ +------------+ +------------+ +------------+
  0            2017-05-19     0              Edgar Walker
  100          2017-05-25     1              Jake Reimer
   (2 tuples)

  >>> mouse & target_sessions
  *mouse_id    dob            sex
  +----------+ +------------+ +--------+
  0            2017-03-01     M
  100          2017-05-12     F
   (2 tuples)

Again you could have combined this into a single statement:

.. code-block:: python
  
  >>> mouse & (session & 'session_date >= "2017-05-19"')
  *mouse_id    dob            sex
  +----------+ +------------+ +--------+
  0            2017-03-01     M
  100          2017-05-12     F
   (2 tuples)

Giving us back the same results as expected.


**Q.** I want to know all **female mice** that has experiment session **performed before 2017-05-20**

**A.** This hs more parts but you can again break things up in a couple of way. For example, 
you can first look for all female mice and then restric by all sessions performed before 2017-05-20.

.. code-block:: python

  >>> female_mice = mouse & 'sex = "F"'    # get all female mice
  >>> female_mice
  *mouse_id    dob            sex
  +----------+ +------------+ +--------+
  5            2016-12-25     F
  10           2017-01-01     F
  11           2017-01-03     F
  100          2017-05-12     F
   (4 tuples)

  >>> target_sessions = session & 'session_date < "2017-05-20"'   # all sessions before 2017-05-20
  >>> target_sessions
  mouse_id    *session_date  experiment_set experimenter
  +----------+ +------------+ +------------+ +------------+
  0            2017-05-15     0              Edgar Walker
  0            2017-05-19     0              Edgar Walker
  5            2017-01-05     1              Fabian Sinz
   (3 tuples)

  >>> female_mice & target_sessions
  *mouse_id    dob            sex
  +----------+ +------------+ +--------+
  5            2016-12-25     F
   (1 tuples)

Once again you could express the query in a single line without losing much readability!

.. code-block:: python

  >>> mouse & 'sex = "F"' & (session & 'session_date < "2017-05-20"')
  *mouse_id    dob            sex
  +----------+ +------------+ +--------+
  5            2016-12-25     F
   (1 tuples)

Let's now take a look at one more example.

**Q.** I want all mouse that has **no** experiment sessions performed on it yet.

**A.** Aha! This is one example that would be rather difficult to obtain with what we know already, but there is
an operator just for this - the difference operator ``-``

Difference Operator ``-``
-------------------------

Sometimes you want to find entries that does **not** have any mathcing entries in another table. Well, DataJoint
has an operator just for that! You can use the difference ``-`` operator to find entries that does **not** have
a corresponding entry in another table! Let's see how we can use this to find "all mice without experiement session"

.. code-block:: python
  
  >>> mouse - session
  *mouse_id    dob            sex
  +----------+ +------------+ +--------+
  1            2016-11-19     M
  2            2016-11-20     U
  10           2017-01-01     F
  11           2017-01-03     F
   (4 tuples)

and that's it! When you say ``A - B``, you find all entries in ``A`` that does **not** have a corresponding entries
in ``B``. The difference operator comes in really handy when you want to look for things like missing entries
just like we did.

.. note::
  Unlike restriction ``&``, the difference operator ``-`` only works on tables. If you want to negate the
  condition when restricting by a string (e.g. ``sex = "M"``), simply the negate the statement itself
  (e.g. ``sex != "M"``).

We will wrap up this section by covering one more of the basic but very powerful query operator - join ``*``.

.. _python-join:

Join operator ``*``
-------------------
When working with multiple tables (as in the case of ``Mouse`` and ``Session``), you would sometimes wish to
**combine** these tables into one so that you have all information together. Well, there is an operator for
that! The join operator ``*`` allows you to combine two tables by matching corresponding entries, returning
you one table that has all columns from both tables. Let's take a look at an example:

.. code-block:: python

  >>> mouse * session   # join mouse and session
  *mouse_id    *session_date  dob            sex     experiment_set experimenter
  +----------+ +------------+ +------------+ +--------+ +------------+ +------------+
  0            2017-05-15     2017-03-01     M          0              Edgar Walker
  0            2017-05-19     2017-03-01     M          0              Edgar Walker
  5            2017-01-05     2016-12-25     F          1              Fabian Sinz
  100          2017-05-25     2017-05-12     F          1              Jake Reimer
   (4 tuples)

Notice that you are returne a single table with columns from both the ``Mouse`` and the ``Session`` table, 
giving you all the information you want! You might have noticed that this does **not** list all mouse, however.


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

Why is that? This is because join ``*`` only combines the **matching** entries from the two tables. Because some
mouse did not have matching entries in the ``Session`` table (e.g. ``mouse_id = 2``), it was left out from the
join results. This policy ensures that the returned joined table will not have any missing entries.

You can easily use the result of the join in further query. For example, we can find all mouse-session combination
for male mice with experiment session performed on or after 2017-05-19:

.. code-block:: python

  >>> mouse * session & 'sex = "M"' & 'session_date >= "2017-05-19"'
  *mouse_id    *session_date  dob            sex     experiment_set experimenter
  +----------+ +------------+ +------------+ +--------+ +------------+ +------------+
  0            2017-05-19     2017-03-01     M          0              Edgar Walker
   (1 tuples)

Notice how we were able to use attributes from both ``Mouse`` (``sex``) and ``Session`` (``session_date``)
together.

What's next?
------------
Phew! That was a lot of material but hopefully you saw how you can form powerful queries using DataJoint's
intuitive query language! Go ahead and spend some more time playing with the queries and see if you can come
up with queries to answer any question you can ask about your data! In the :doc:`next section <importing-data>`
we will look into building a table that can load external data automatically!


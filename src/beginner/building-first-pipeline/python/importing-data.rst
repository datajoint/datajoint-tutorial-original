Importing data into a table
===========================

Now that we have tables for organizing mouse and experiment sessions, it's time
for us to load the data recorded during each experimental session!
In this section, we will look at creating an **imported table**, 
a table that will automatically import data from files.

Setting up tables
-----------------
For this section, we will be using mock experimental data to be loaded into the
table. For this to work properly, the content of the ``Session`` table must look
exactly as following for the primary key attributes (``mouse_id`` and ``session_date``)

.. code-block:: python

  *mouse_id    *session_date  experiment_set experimenter
  +----------+ +------------+ +------------+ +------------+
  0            2017-05-15     0              Edgar Walker
  0            2017-05-19     0              Edgar Walker
  5            2017-01-05     1              Fabian Sinz
  100          2017-05-25     1              Jake Reimer
   (4 tuples)

If your ``Session`` table doesn't quite have the same set of primary keys (``mouse_id``
and ``session_date`` combinations) as shown above, make use of the various ``insert`` methods
covered in :doc:`inserting-data` and ``delete`` method covered in :ref:`python-delete-entries`
to adjust your ``Session`` table content until it matches the table shown above.

Remember, because of data integrity constraints, if you are missing some of the mice in the ``Mouse`` table, you may have to insert the 
appropriate mouse into your ``Mouse`` table before you can insert a session corresponding 
to that mouse into the ``Session`` table.

Getting the data
----------------
You can download the (mock) experimental data for the above sessions packaged into a ZIP file
here:

:download:`Experiment data </_static/data/python-data.zip>`

Go ahead and download the ZIP file and unzip the content. Place the ``data`` directory from the
ZIP file somewhere where you'd remember. You will need the full path to this ``data`` directory
to follow the rest of this section. In what follows, we will be refering to the path to the data
simply as ``/path/to/data/`` so be sure to substitute the full path to the ``data`` folder when trying
out the commands below.

The follow are a few examples demonstrating what your data path might look like:

MacOS
^^^^^

If you extract the ``data`` folder into your ``Desktop``, for example, then the path to the
``data`` folder will be something like ``/home/username/Desktop/data`` where you replace ``username``
with your user name for your machine.

Windows
^^^^^^^

On Windows, if you extracted ``data`` folder onto your ``Desktop``, then the full path to the ``data``
folder will look like ``C:\Users\username\Desktop\data`` where you replace ``username`` with
your user name for your machine.

Linux
^^^^^

If you extracted the ``data`` directory to your home folder, then the full path to the ``data``
directory will be something like ``/home/username/data`` where you replace ``username``
with your user name on the machine.

Data files
----------
Inside the ``data`` directory, you will find 4 ``.npy`` (saved NumPy array) files with names like
``data_100_2017-05-25.npy``. As you might have guessed, these are the data for the 4 recording
sessions in the ``Session`` table, and each file are named according to the ``mouse_id`` and
``session_date`` - the attributes of the primary keys - in the format ``data_{mouse_id}_{session_date}.npy``.

Let's take a quick peak at the data content:

.. code-block:: python

  >>> import numpy as np     # import the numpy library
  >>> data = np.load('/path/to/data/data_100_2017-05-25.npy')
  >>> data.shape
  (1000,)

So this particular file contains a NumPy array of length 1000. This represents a recording of 
raw electric activity from a single neuron over 1000 time bins.

Other files contain similar looking data in NumPy array format, giving the electric activity
from a neuron recorded from each session.

We would now like to **import** all these data into a table so that we can maintain and manipuate
all data inside DataJoint.

Imported table
--------------

Unlike the ``Manual`` tables like ``Mouse`` and ``Session`` where new data were entered **manually**
(e.g. via ``insert`` methods), we would now like to create a table called ``Neuron`` whose
table data content is automatically imported from the files above. We can 
achieve this in DataJoint by defining an ``Imported`` table. Just like the ``Manual`` table,
we start by specifiying the table definition:

.. code-block:: python

  @schema
  class Neuron(dj.Imported):
      definition = """
      -> Session
      ---
      activity:  longblob    # electric activity of the neuron
      """

.. note::
  Go ahead and define the above class, thus defining the table inside the database. However,
  keep your class definition around as we will be coming back and adding more content to
  it shortly!

Notice that we have subclassed ``dj.Imported`` instead of ``dj.Manual``, indicating that this is
going to be an "imported" table. Since we record from one neuron in each session, the neuron
can be uniquely identified by knowing which session it was recorded in. Thus the primary key
simply consists of the dependency on ``Session`` (for review on table dependency, take a look
at :doc:`child-table`).

The next bit is interesting. For each neuron, we want to store the recorded electric activity
which is a NumPy array. The table data type ``longblob`` allows us to store an arbitrary array
data (i.e. NumPy array) into the table.

So far the ``Neuron`` doesn't seem to be too much different from a manual table like ``Session``.
One big difference between an imported table (``dj.Imported``) and a manual table (``dj.Manual``)
is the fact an imported table comes with a special method called ``populate``.

``populate`` method
-------------------

A key feature of imported tables is the existence of the
``populate`` method. Let's go ahead and 1) instantiate our new table and 2) call ``populate``
method on it.

.. code-block:: python
  
  >>> neuron = Neuron()
  >>> neuron        # view the content - should be empty
  *mouse_id    *session_date  activity
  +----------+ +------------+ +----------+
  

   (0 tuples)
  >>> neuron.populate()     # call populate method
  ---------------------------------------------------------------------------
  NotImplementedError                       Traceback (most recent call last)
  <ipython-input-211-196e0eb3db4d> in <module>()
  ----> 1 neuron.populate()

  (...message truncated...)

  NotImplementedError: Subclasses of AutoPopulate must implement the method "make"

Notice how calling the ``populate`` method triggered a ``NotImplementedError`` compaining that
the method ``make`` is not defined. To get a better sense of what's going on, let's go
back to our class definition and add a very basic ``make`` method:

.. code-block:: python
  :emphasize-lines: 9,10

  @schema
  class Neuron(dj.Imported):
      definition = """
      -> Session
      ---
      activity:  longblob    # electric activity of the neuron
      """

      def make(self, key):    # make takes a single argument `key`
          print(key)  # let's look a the key content

Here we have added a very basic ``make`` method to the class ``Neuron``. It turns out
that ``make`` takes in a single argument ``key``, so we go ahead and let ``make``
print out the content of the ``key`` argument. Let's now create a new instance and call ``populate``
again:

.. code-block:: python

  >>> neuron = Neuron()
  >>> neuron.populate()
  {'mouse_id': 0, 'session_date': datetime.date(2017, 5, 15)}
  {'mouse_id': 0, 'session_date': datetime.date(2017, 5, 19)}
  {'mouse_id': 5, 'session_date': datetime.date(2017, 1, 5)}
  {'mouse_id': 100, 'session_date': datetime.date(2017, 5, 25)}

This time the call to ``populate`` did not thrown an error but rather printed out four dictionaries.
Staring at these four dictionaries, you might have noticed that these are the primary key values
(``mouse_id`` and ``session_date``) of the four entries from the ``Session`` table!

.. code-block:: python
  
  >>> session
  *mouse_id    *session_date  experiment_set experimenter
  +----------+ +------------+ +------------+ +------------+
  0            2017-05-15     0              Edgar Walker
  0            2017-05-19     0              Edgar Walker
  5            2017-01-05     1              Fabian Sinz
  100          2017-05-25     1              Jake Reimer
   (4 tuples)

So what's going on here? When you call the ``populate`` method of a table, this triggers DataJoint to
lookup all the tables that the target table depends on (i.e. ``Session`` table for ``Neuron``),
and for each possible combination of entries in the dependent (or parent) tables, ``populate``
extracts the primary key values and calls the ``make`` method.

In the case of the ``Neuron`` table, the ``Neuron`` table depends only on ``Session`` table,
and therefore the ``populate`` method went through all entries of ``Session`` and called the ``make``
for each entry in ``Session``, passing in the primary key values as the key`` argument!

So what is this all good for? We can use the fact that ``populate`` calls ``make`` for
every combination of parent tables for ``Neuron`` to automatically visit all ``Session``\ s and load
the neuron data for each session and insert the loaded data into the table. Let's take a look
at what that implementation might be like.

Implementing ``make``
---------------------
Recall that we wanted to load the neuron activity data from each recorded ``Session`` into the
``Neuron`` table. We can now achieve that by implementing a ``make`` method like the following.

.. code-block:: python

  @schema
  class Neuron(dj.Imported):
      definition = """
      -> Session
      ---
      activity:  longblob    # electric activity of the neuron
      """

      def make(self, key):
         # use key dictionary to determine the data file path
         data_file = "/path/to/data/data_{mouse_id}_{session_date}.npy".format(**key)

         # load the data
         data = np.load(data_file)

         # add the loaded data as the "activity" column
         key['activity'] = data

         # insert the key into self
         self.insert1(key)

         print('Populated a neuron for {mouse_id} on {session_date}'.format(**key))

Let's now take a look a the content of ``make`` one step at a time.

.. code-block:: python
   :emphasize-lines: 2,3

      def make(self, key):
         # use key dictionary to determine the data file path
         data_file = "/path/to/data/data_{mouse_id}_{session_date}.npy".format(**key)

         # load the data
         data = np.load(data_file)

         # add the loaded data as the "activity" column
         key['activity'] = data

         # insert the key into self
         self.insert1(key)

         print('Populated a neuron for {mouse_id} on {session_date}'.format(**key))

First of all, we use the passed in ``key`` dictionary containing the ``mouse_id`` and ``session_date``
of a single session to determine the path to the neuron data file recorded in that particular session.
We use the fact that each recording file is named as ``data_{mouse_id}_{session_date}.npy``,
and substitute in the specific session's values to get the file name.

.. note::
  If you are working on Windows, note that you would have to use backslashes ``\`` in place
  of the forward slashes to separate folder names.

.. code-block:: python
   :emphasize-lines: 5,6

      def make(self, key):
         # use key dictionary to determine the data file path
         data_file = "/path/to/data/data_{mouse_id}_{session_date}.npy".format(**key)

         # load the data
         data = np.load(data_file)

         # add the loaded data as the "activity" column
         key['activity'] = data

         # insert the key into self
         self.insert1(key)

         print('Populated a neuron for {mouse_id} on {session_date}'.format(**key))

We then load the data from the ``.npy`` data file, getting a NumPy array that contains the
recorded neuron's activity from that session.


.. code-block:: python
   :emphasize-lines: 8,9

      def make(self, key):
         # use key dictionary to determine the data file path
         data_file = "/path/to/data/data_{mouse_id}_{session_date}.npy".format(**key)

         # load the data
         data = np.load(data_file)

         # add the loaded data as the "activity" column
         key['activity'] = data

         # insert the key into self
         self.insert1(key)

         print('Populated a neuron for {mouse_id} on {session_date}'.format(**key))

The loaded NumPy array data is then assigned to the ``key`` dictionary under attribute name
``activity``. Recall that this is the non-primary key ``longblob`` field that we added to
the ``Neuron`` table to store the recorded neuron's electric activity. After adding this 
attribute, the ``key`` dictionary should now contain three attributes: ``mouse_id``, ``session_date``,
and ``activity``, with values of the first two specifying a specific ``Neuron`` entry and the
value of the ``activity`` holding the recorded activity for that neuron.


.. code-block:: python
   :emphasize-lines: 11,12

      def make(self, key):
         # use key dictionary to determine the data file path
         data_file = "/path/to/data/data_{mouse_id}_{session_date}.npy".format(**key)

         # load the data
         data = np.load(data_file)

         # add the loaded data as the "activity" column
         key['activity'] = data

         # insert the key into self
         self.insert1(key)

         print('Populated a neuron for {mouse_id} on {session_date}'.format(**key))

We then finally insert this dictionary containing a single neuron's activity into ``self``, which
of course points to ``Neuron``! With this implementation of ``make``, when the ``populate``
method is called, ``Neuron`` will be **populated** with recorded neuron's activity from each 
recording session, one a time as desired.

Populating ``Neuron`` table
---------------------------

Go ahead and redefine the ``Neuron`` class with the updated ``make`` method as given
above. And now let's call the ``populate`` method on a new instance of ``Neuron`` again!

.. code-block:: python

  >>> neuron = Neuron()
  >>> neuron.populate()
  Populated a neuron for 0 on 2017-05-15
  Populated a neuron for 0 on 2017-05-19
  Populated a neuron for 5 on 2017-01-05
  Populated a neuron for 100 on 2017-05-25

As expected the call to ``populate`` resulted in 4 neurons being inserted into ``Neuron``, one for
each session! Let's now take a look at its contents:

.. code-block:: python

  >>> neuron
  *mouse_id    *session_date  activity
  +----------+ +------------+ +----------+
  0            2017-05-15     <BLOB>
  0            2017-05-19     <BLOB>
  5            2017-01-05     <BLOB>
  100          2017-05-25     <BLOB>
   (4 tuples)

With a simple call to ``populate`` we were able to get the table content automatically imported
from the data files!

Multiple calls to populate
--------------------------

One very cool feature about ``populate`` is the fact it is **smart** and knows exactly
what still needs to be populated and will only call ``make`` for the missing keys. For example,
let's see what happens if we call ``populate`` on ``Neuron`` table again:

.. code-block:: python

  >>> neuron.populate()

Notice that there was nothing printed out, indicating that **nothing was populated**. This is because the 
``Neuron`` table is already populated with all experiments! This means that you can
call the ``populate`` method on an ``dj.Imported`` as many times as you like without the fear of
triggering unncessary computations.

The power of this feature becomes even more apparent when a new dataset becomes available. Suppose that
you have performed an additional recording session. Insert the following entry into the
``Session`` table:

.. code-block:: python

  >>> session.insert1((100, '2017-06-01', '1', 'Jake Reimer'))

and download the following new recording data and place it into your ``data`` directory:

:download:`data_100_2017-06-01.npy </_static/data/data_100_2017-06-01.npy>`

Once you have inserted a new entry into the ``Session`` table and downloaded the new recording file
into your ``data`` directory, call ``populate`` again on ``Neuron``.

.. code-block:: python

  >>> neuron.populate()
  Populated a neuron for 100 on 2017-06-01

As you can see, the ``populate`` call automatically detected that there is one new entry (key) available
to be populated and called ``make`` on that missing key.

By encompassing the logic of importing data for a single primary key in ``make`` you can now
easily import data from data files into the ``Imported`` table automatically as the data becomes
available.

What's next?
------------
Congratulations for completing this section! This was a lot of material but hopefully you saw how
the simple logic of ``populate`` and ``make`` can make a data importing task very
streamlined and automated! In :doc:`the next and the last section <computed-table>` of this tutorial,
we are going to explore ``computed`` tables that computes something from data in a parent table and stores the results in the data pipeline!


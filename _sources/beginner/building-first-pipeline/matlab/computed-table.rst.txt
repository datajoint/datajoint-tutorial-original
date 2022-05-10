Computation in data pipeline
============================

Welcome to the last (but certainly not the least!) section of the tutorial! Now that we
have some recorded neural data imported into a table (``Neuron``), we are going to perform
some computations and processing, and look at how we can store these results naturally into
tables. In doing so, we are going to meet two remaining major table tiers:
lookup table (``dj.Lookup``) and computed table (``dj.Computed``).

Performing computation on data
------------------------------
Now we have the "raw" electric activities from neurons, we would like to detect spikes automatically.
Before we tackle this challenge, let's first get a better idea about our data by computing a few
statistics on the data such as mean and standard deviation of the electric activity.

Defining computed tables
^^^^^^^^^^^^^^^^^^^^^^^^

A crticial feature of a data pipeline is that not only the raw data (i.e. entered manually or imported
from external source) but also the processed data and computation results reside in the same data
pipeline. A **computed table** is defined by specifying the computation to be performed on data
found in other table(s), and the results are stored inside the table itself.

Just like the imported tables (``dj.Imported``), computed tables (``dj.Computed``) provide the
``populate`` method and ``makeTuples`` method, and therefore provides us with a mechanism to
perform computation on every combination of parent/depended tables!

Let's now define our first computed table ``ActivityStatistics`` that **computes** the statistics
of electric activity **for each neuron in ``Neuron``**.


.. code-block:: matlab

  %{
    # statistics about the activity
    -> tutorial.Neuron
    ---
    mean: float    # mean activity
    stdev: float   # standard deviation of activity
    max: float     # maximum activity
  %}
 
  classdef ActivityStatistics < dj.Computed
    
      methods(Access=protected)
          function makeTuples(self,key)
            
              activity = fetch1(tutorial.Neuron & key,'activity');    % fetch activity as Matlab array
            
              % compute various statistics on activity
              key.mean = mean(activity); % compute mean
              key.stdev = std(activity); % compute standard deviation
              key.max = max(activity);    % compute max
              self.insert(key);
              sprintf('Computed statistics for for %d experiment on %s',key.mouse_id,key.session_date)
            
          end
      end
  end


As usual, let's take a look at it step by step!

.. code-block:: matlab
  :emphasize-lines: 10

  %{
    # statistics about the activity
    -> tutorial.Neuron
    ---
    mean: float    # mean activity
    stdev: float   # standard deviation of activity
    max: float     # maximum activity
  %}
 
  classdef ActivityStatistics < dj.Computed
    
      methods(Access=protected)
          function makeTuples(self,key)
            
              activity = fetch1(tutorial.Neuron & key,'activity');    % fetch activity as Matlab array
            
              % compute various statistics on activity
              key.mean = mean(activity); % compute mean
              key.stdev = std(activity); % compute standard deviation
              key.max = max(activity);    % compute max
              self.insert(key);
              sprintf('Computed statistics for for %d experiment on %s',key.mouse_id,key.session_date)
            
          end
      end
  end

As you might have guessed, you subclass from ``dj.Computed`` to defined a computed table in DataJoint.

.. code-block:: matlab
  :emphasize-lines: 3

  %{
    # statistics about the activity
    -> tutorial.Neuron
    ---
    mean: float    # mean activity
    stdev: float   # standard deviation of activity
    max: float     # maximum activity
  %}
 
  classdef ActivityStatistics < dj.Computed
    
      methods(Access=protected)
          function makeTuples(self,key)
            
              activity = fetch1(tutorial.Neuron & key,'activity');    % fetch activity as Matlab array
            
              % compute various statistics on activity
              key.mean = mean(activity); % compute mean
              key.stdev = std(activity); % compute standard deviation
              key.max = max(activity);    % compute max
              self.insert(key);
              sprintf('Computed statistics for for %d experiment on %s',key.mouse_id,key.session_date)
            
          end
      end
  end

Here each ``ActivityStatistics`` entry **depends** on ``Neuron``. Because the ``ActivityStatistics``
table does not define any additional primary key attribute (i.e. no other attribute entries above 
``---`` separator), each row in the ``ActivityStatistics`` table is uniquely identified by a 
single neuron in the ``Neuron`` table. Each entry in the ``ActivityStatistics`` table has 
non-primary key attributes ``mean``, ``stdev`` and ``max`` to hold the mean, standard deviation
and maximum value of the electric activity, respectively.

Just like imported table (``dj.Imported``), computed tables are equipped with ``populate`` method
which would call the ``makeTuples`` for every combination of dependent/parent tables. In this case,
``ActivityStatistics``'s ``makeTuples`` will be called for every neuron in the ``Neuron`` table. 

Here, for each neuron in the ``Neuron`` table (pointed to by ``key``), we  1) get the value of column 
``activity`` storing the neuron's electric activity as NumPy array, 2) compute various statistics and
store the values into the ``key`` dictionary and 3) insert the dictionary into self (``ActivityStatistics``).

.. note::
  ``fetch`` method will always return a structure, and ``fetchn`` will always return a cell array even if there is only one element. When you know
  that there is only going to be one entry, you can get the attribute value directly by using
  ``fetch1`` instead, as was done here.

With this computation defined, we can trigger activity statistics to be computed for all entries in
``Neuron`` by simply instantiating and calling ``populate`` method on ``ActivityStatistics``:

.. code-block:: matlab

  >> avg  =tutorial.ActivityStatistics

  avg = 


  Object tutorial.ActivityStatistics

  :: statistics about the activity ::

  0 tuples (0.0104 s)

.. code-block:: matlab

  >> populate(tutorial.ActivityStatistics)

  **tutorial.ActivityStatistics: Found 5 unpopulated keys

  Computed statistics for for 0 experiment on 2017-05-15
  Computed statistics for for 0 experiment on 2017-05-19
  Computed statistics for for 5 experiment on 2017-01-05
  Computed statistics for for 100 experiment on 2017-05-25
  Computed statistics for for 100 experiment on 2017-06-01

.. code-block:: matlab

  >> avg

  avg = 


  Object tutorial.ActivityStatistics

  :: statistics about the activity ::

    MOUSE_ID    SESSION_DATE      mean       stdev      max  
    ________    ____________    ________    _______    ______

      0         '2017-05-15'     0.20736    0.40107    2.4816
      0         '2017-05-19'     0.13274    0.29161    1.8281
      5         '2017-01-05'    0.089179    0.23653    1.3739
    100         '2017-05-25'     0.21907    0.32895    1.7638
    100         '2017-06-01'    0.087327    0.23798    1.3245

  5 tuples (0.0575 s)

Great! We just successfully computed various neuronal activity statistics for all neurons in the
``Neuron`` table with a single method call to ``populate``. Computation couldn't really be 
easier than that!

Detecting spikes from neural activity
-------------------------------------

Now we have a better idea of our neuronal activity data, let's try performing the more challenging
computation - the spike detection. As you may know, spike detection is a very challenging (and 
exciting) subject and is a very active area of research!
However, Rather than attempting to implement the state-of-the-art spike detection,
we are going to implement a very simple algorithm where we register a "spike" 
every time the activity **rises above** a certain **threshold** value.

Importantly, this means that the result of our computation (i.e. detected spikes) will depend
a lot on the chosen value of the threshold, and we would like to be able to try a few
different value of threshold to see what works well. In other words, we would like to be able
to run the spike detection algorithm with few different values of **threshold** and compare
the results side-by-side.

This can actually be achieve rather easily by preparing a **lookup table** to store different
values of computation paramters (i.e. threshold values), and compute spikes for **every
combination of neurons and parameter value set**.

Defining Lookup tables
^^^^^^^^^^^^^^^^^^^^^^

Let's go ahead and define a lookup table called ``SpikeDetectionParam`` to contain the
parameters for spike detection, namely the threshold value.
As you might have guessed, you can define a lookup
table by subclassing ``dj.Lookup``. A lookup table is almost identical to a manual table
(``dj.Manual``) but signifies that this table contains values like parameters for computation.

.. code-block:: matlab

  %{
  # Spike detection thresholds
  sdp_id: int      # unique id for spike detection parameter set
  ---
  threshold: float   # threshold for spike detection
  %}
 
  classdef SpikeDetectionParam < dj.Lookup
  end


.. note::
  Notice that we used a field ``sdp_id`` to serve as the primary key for the ``SpikeDetectionParam``
  rather than using ``threshold`` as the primary key, despite the fact that ``threshold`` is the
  only attribute of interest in this table. This is because ``threshold`` is of data type float
  and exact comparison is difficult for float values. In general, it is recommended that you avoid 
  using float data type attribute in your primary key.

Defining ``Spikes`` table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now that we have defined ``SpikeDetectionParam``, let's go ahead and define the computed table for
spike detection and call it ``Spikes``!

.. note::
  It's usually a good diea to call a computed table
  based on what would be the results of the computation rather than naming it based on the
  computation process (i.e. so ``Spikes`` rather than ``SpikeDetection``). 
  This would make sense if you consider the fact that the table will be housing the 
  results of the computation, here the detected neuronal **spikes**.

.. code-block:: matlab

  %{
    # spikes
    -> tutorial.Neuron
    -> tutorial.SpikeDetectionParam
    ---
    spikes: longblob     # detected spikes
    count: int           # total number of detected spikes
  %}
 
  classdef Spikes < dj.Computed
      methods(Access=protected)
          function makeTuples(self, key)
              activity = fetch1(tutorial.Neuron & key, 'activity');
              threshold = fetch1(tutorial.SpikeDetectionParam & key, 'threshold');
 
              above_thrs = activity > threshold;   % find activity above threshold
            rising = diff(above_thrs) > 0; % find rising edge of crossing threshold
            spikes = [0 rising];    % prepend 0 to account for shortening due to np.diff
            count = sum(spikes);   % compute total spike counts
 
            % save results and insert
            key.spikes = spikes;
            key.count = count;
            self.insert(key);
 
            sprintf('Detected %d spikes for mouse_id %d session_date %s using threshold=%2.2f',...
                count, key.mouse_id, key.session_date, threshold)
          end
      end
  end

Alright, let's go through this code step-by-step, first focusing on the definition!

.. code-block:: matlab
  :emphasize-lines: 3,4

  %{
    # spikes
    -> tutorial.Neuron
    -> tutorial.SpikeDetectionParam
    ---
    spikes: longblob     # detected spikes
    count: int           # total number of detected spikes
  %}

Notice that the ``Spikes`` table **depends on both ``Neuron`` and ``SpikeDetectionParam``**!
What does this mean? This means that each entry (detected spikes) in the ``Spikes`` table
is uniquely identified not only by the identify of a neuron (from ``Neuron``) but by the
combination of the neuron identity and **the particular spike detection parameter**
(from ``SpikeDetectionParam``). As you will see, this allows for this table to house
results of spike detection under more than one values for the parameter (i.e. threshold)!


.. code-block:: matlab
  :emphasize-lines: 6,7

  %{
    # spikes
    -> tutorial.Neuron
    -> tutorial.SpikeDetectionParam
    ---
    spikes: longblob     # detected spikes
    count: int           # total number of detected spikes
  %}

As the non-primary-key attributes, ``Spikes`` will contain both the detected ``spikes``
as an array of 0's and 1's with 1's at the position of a spike, and the total ``count`` 
of detected spikes.

Now let's move onto the mean of the computed table - ``makeTuples``:

.. code-block:: matlab
  :emphasize-lines: 2,3

  function makeTuples(self, key)
     activity = fetch1(tutorial.Neuron & key, 'activity');
     threshold = fetch1(tutorial.SpikeDetectionParam & key, 'threshold');
 
     above_thrs = activity > threshold;   % find activity above threshold
     rising = diff(above_thrs) > 0; % find rising edge of crossing threshold
     spikes = [0 rising];    % prepend 0 to account for shortening due to np.diff
     count = sum(spikes);   % compute total spike counts
 
     % save results and insert
     key.spikes = spikes;
     key.count = count;
     self.insert(key);
 
     sprintf('Detected %d spikes for mouse_id %d session_date %s using threshold=%2.2f',...
        count, key.mouse_id, key.session_date, threshold)
  end

One of the first thing we do in ``_make_tuples`` is to fetch relevant data from other tables.
This is a very standard practice when defining ``_make_tuples`` in computed tables, as was
also performed in the ``ActivityStatistics`` table. Here we fetch the neuron's electric
``activity`` Matlab array from the ``Neuron`` table, and the value of the ``threshold`` from
the ``SpikeDetectionParam`` table.

.. code-block:: matlab
  :emphasize-lines: 5-7

  function makeTuples(self, key)
     activity = fetch1(tutorial.Neuron & key, 'activity');
     threshold = fetch1(tutorial.SpikeDetectionParam & key, 'threshold');
 
     above_thrs = activity > threshold;   % find activity above threshold
     rising = diff(above_thrs) > 0; % find rising edge of crossing threshold
     spikes = [0 rising];    % prepend 0 to account for shortening due to np.diff
     count = sum(spikes);   % compute total spike counts
 
     % save results and insert
     key.spikes = spikes;
     key.count = count;
     self.insert(key);
 
     sprintf('Detected %d spikes for mouse_id %d session_date %s using threshold=%2.2f',...
        count, key.mouse_id, key.session_date, threshold)
  end

Using ``activity`` and ``threshold``, we first find and label where ``activity`` value is
above the threshold. This returns an array of 0's and 1's where 1's corresponds to time bins
where neuron's activity was above the threshold, storing this as ``above_thrs``.

We then find out all the timebins at which the activity goes from 0 to 1, signifying times
at which the neuron's activity **raised above the threshold**, storing this into ``rising``!
MATLAB's built-in `diff() <https://www.mathworks.com/help/matlab/ref/diff.html>`_ function
gives us the difference between adjacent values, which is an array one-item shorter that the input.
We adjust this array so that it has the same length as the original ``activity``,
and store the result as our detected ``spikes``! We store the computed ``spikes`` and ``count`` 
by inserting into this (``Spikes``) table!!

.. code-block:: matlab
  :emphasize-lines: 10-13

  function makeTuples(self, key)
     activity = fetch1(tutorial.Neuron & key, 'activity');
     threshold = fetch1(tutorial.SpikeDetectionParam & key, 'threshold');
 
     above_thrs = activity > threshold;   % find activity above threshold
     rising = diff(above_thrs) > 0; % find rising edge of crossing threshold
     spikes = [0 rising];    % prepend 0 to account for shortening due to np.diff
     count = sum(spikes);   % compute total spike counts
 
     % save results and insert
     key.spikes = spikes;
     key.count = count;
     self.insert(key);
 
     sprintf('Detected %d spikes for mouse_id %d session_date %s using threshold=%2.2f',...
        count, key.mouse_id, key.session_date, threshold)
  end

Populating ``Spikes``
^^^^^^^^^^^^^^^^^^^^^

Ok, after our hard work putting implemeting the spike detection algorithm, it's time for
us to run it! Let's instantiate the ``Spikes`` table and ``populate`` it away!

.. code-block:: matlab

  >> spikes=tutorial.Spikes;
  >> spikes

  spikes = 


  Object tutorial.Spikes


  <SQL>
  CREATE TABLE `tutorial`.`__spikes` (
  `mouse_id` int NOT NULL COMMENT "unique mouse id",
  `session_date` date NOT NULL COMMENT "session date",
  CONSTRAINT `rVWU4dxf` FOREIGN KEY (`mouse_id`,`session_date`)   REFERENCES `tutorial`.`_neuron` (`mouse_id`,`session_date`) ON   UPDATE CASCADE ON DELETE RESTRICT,
  `sdp_id` int NOT NULL COMMENT "unique id for spike detection   parameter set",
  CONSTRAINT `gKoJB0lO` FOREIGN KEY (`sdp_id`) REFERENCES   `tutorial`.`#spike_detection_param` (`sdp_id`) ON UPDATE CASCADE   ON DELETE RESTRICT,
  `spikes` longblob      NOT NULL COMMENT "detected spikes",
  `count` int            NOT NULL COMMENT "total number of detected spikes",
  PRIMARY KEY (`mouse_id`,`session_date`,`sdp_id`)
  ) ENGINE = InnoDB, COMMENT "spikes"
  </SQL>

  :: spikes ::

  0 tuples (0.372 s)

  >> populate(tutorial.Spikes) %populate it away!
 
Sadly nothing seems to be happening. Why could this be the case? The answer lies in the
``SpikeDetectionParam`` table:

.. code-block:: matlab

  >> tutorial.SpikeDetectionParam

  ans = 


  Object tutorial.SpikeDetectionParam

  :: Spike detection thresholds ::

  0 tuples (0.00604 s)

Aha! Because ``Spikes`` table performs computation on the every **combination** of ``Neuron``
and ``SpikeDetectionParam``, when there is no entry in ``SpikeDetectionParam``, there was
nothing to be populated!

Filling in ``Lookup`` table
+++++++++++++++++++++++++++

Let's fix this but creating an entry in ``SpikeDetectionParam``. Consulting the statistics
computed for neurons in :ref:`python-neuron-stats`, let's pick a value that is at least 1-2
standard deviation above the mean value. Let's try 0.9 as our threshold! You would fill
in values into a ``Lookup`` table just how you would for a ``Manual`` table:

.. code-block:: matlab

  >> sdp = tutorial.SpikeDetectionParam;
  >> insert(sdp,{0, 0.9});


Here we have assigned the ``threshold`` of 0.9 the ``sdp_id`` of 0.

Running spike detection with multiple parameter values
++++++++++++++++++++++++++++++++++++++++++++++++++++++

Alright, now with ``SpikeDetectionParam`` populated with a parameter, let's try to ``populate``
the ``Spikes`` table once again:

.. code-block:: matlab

  >> populate(tutorial.Spikes)

  **tutorial.Spikes: Found 5 unpopulated keys

  Populating tutorial.Spikes for:
        mouse_id: 0
    session_date: '2017-05-15'
          sdp_id: 0


  ans =

  Detected 27 spikes for mouse_id 0 session_date 2017-05-15 using threshold=0.90
  ans =

  Detected 21 spikes for mouse_id 0 session_date 2017-05-19 using threshold=0.90
  ans =

  Detected 14 spikes for mouse_id 5 session_date 2017-01-05 using threshold=0.90
  ans =

  Detected 35 spikes for mouse_id 100 session_date 2017-05-25 using threshold=0.90
  ans =

  Detected 15 spikes for mouse_id 100 session_date 2017-06-01 using threshold=0.90

Woohoo! This time the algorithm ran, reporting us how the detected spike counts!!

Let's now try running this same algorithm but under different parameter configuration - that is
different values of ``threshold``! Let's try a much smaller ``threshold`` value of say 0.1!
Go ahead and insert this new parameter value into the ``SpikeDetectionParam`` table:

.. code-block:: matlab

  >> sdp = tutorial.SpikeDetectionParam;
  >> insert(sdp,{1, 0.1});

...and re-trigger the ``populate``:

.. code-block:: matlab

  >> populate(tutorial.Spikes)

  **tutorial.Spikes: Found 5 unpopulated keys

  ans =

  Detected 128 spikes for mouse_id 0 session_date 2017-05-15 using threshold=0.10
  ans =

  Detected 135 spikes for mouse_id 0 session_date 2017-05-19 using threshold=0.10
  ans =

  Detected 132 spikes for mouse_id 5 session_date 2017-01-05 using threshold=0.10
  ans =

  Detected 151 spikes for mouse_id 100 session_date 2017-06-01 using threshold=0.10

Wow, that gave rise to a lot more spikes, most likely because the algorithm is now picking up
some noise us spikes!

For fun, let's try slightly bigger value - maybe 1.3?

.. code-block:: matlab

  >> sdp = tutorial.SpikeDetectionParam;
  >> insert(sdp,{2, 1.3});
  >> populate(tutorial.Spikes)

You'll find that appears to have been a bit too big for threshold, causing us to have very few spikes!

Seeing them all together
^^^^^^^^^^^^^^^^^^^^^^^^

Finally, we can look at all of our hard earned spikes under different threshold values by
inspecting the ``Spikes`` table:

.. code-block:: matlab

  >> tutorial.Spikes

  ans = 


  Object tutorial.Spikes

  :: spikes ::

    MOUSE_ID    SESSION_DATE    SDP_ID    count     spikes 
    ________    ____________    ______    _____    ________

      0         '2017-05-15'    0          27      '=BLOB='
      0         '2017-05-15'    1         128      '=BLOB='
      0         '2017-05-15'    2          13      '=BLOB='
      0         '2017-05-19'    0          21      '=BLOB='
      0         '2017-05-19'    1         135      '=BLOB='
      0         '2017-05-19'    2           5      '=BLOB='
      5         '2017-01-05'    0          14      '=BLOB='
      5         '2017-01-05'    1         132      '=BLOB='
      5         '2017-01-05'    2           1      '=BLOB='
    100         '2017-05-25'    0          35      '=BLOB='
    100         '2017-05-25'    1         142      '=BLOB='
    100         '2017-05-25'    2           9      '=BLOB='

          ...

  15 tuples (0.0409 s)

Even better, we can see the values of ``SpikeDetectionParam`` together by :ref:`joining 
<matlab-join>` the two tables together. We can also add the same filtering we previously
learned, by specifying a date:

.. code-block:: matlab

  >> spikes * sdp & 'session_date = "2017-05-15"'

  ans = 


  Object dj.internal.GeneralRelvar

    MOUSE_ID    SESSION_DATE    SDP_ID    count    threshold     spikes 
    ________    ____________    ______    _____    _________    ________

      0         '2017-05-15'    0          27      0.9          '=BLOB='
      0         '2017-05-15'    1         128      0.1          '=BLOB='
      0         '2017-05-15'    1          13      1.3          '=BLOB='
    
          ...

  3 tuples (0.00604 s)

  

What's next?
------------

Congratulations!! You have now reached the end of the **Building your first data pipeline**
tutorial!! You have learned a lot throughout this tutorial, and I hope that you now
see the strengths of DataJoint in buliding data pipeline! Before moving forward,
go ahead and spend some more time playing with the simple but effective data pipeline that
you have built! Try to see if you can improve the algorithm for spike detection or
even start defining a new computation all togehter!

Furthermore your journey doesn't end here! Although we have covered the major topics of DataJoint, there are still a lot of cool features to be explored! Be sure to checkout our
`documentation <http://docs.datajoint.io>`_ and stay tuned for upcoming tutorials covering
advanced topics in DataJoint!

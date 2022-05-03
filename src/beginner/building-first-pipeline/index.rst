Building your first data pipeline
=================================

**Author**: Edgar Y. Walker

**Updated**: 2017-06-10


There is no better way to learn about a tool than to sit down and get your hands dirty using it! In this tutorial, we will learn
DataJoint by building our very first data pipeline. To explain data pipeline design and 
usage, we will assume you are a neuroscientist working with mice, and we will build a simple data pipeline
to collect and process the data from your experiments. If you are not a neuroscientist, or you work with some other kind of data, bear with us - one of the strengths of DataJoint is the ease with which it can be quickly adapted to a variety of experimental scenarios.

.. note::
  This tutorial assumes that you already have installed the DataJoint library for Python or MATLAB and have
  already configured a database server where you can create new database schemas and tables. If you don't
  have either of this, be sure to checkout :doc:`/setting-up/introduction` before moving on!

.. important::
  This tutorial is frequently updated to reflect the latest DataJoint Python and MATLAB library syntax. Be sure to download and
  install the latest DataJoint version before following this tutorial! Refer to :ref:`Installing DataJoint for Python <installing-dj-python>`
  and :ref:`Installing DataJoint for MATLAB <installing-dj-matlab>` for instructions on how to install/upgrade to obtain the latest
  version of DataJoint library.

What's covered in this tutorial?
--------------------------------
In this tutorial, we will walk through the process of designing, creating, and populating data pipelines
step-by-step. In particular, we will cover the following conecepts:

- How to define a new table in DataJoint
- Different table types or *tiers*
- How to insert data into a table manually
- How to query and fetch data from the tables
- How to automatically import data into a table from files
- How to define and automatically populate tables with computation results

Designing data pipelines for your experiments
----------------------------------------------
To design good data pipelines, you need to have a clear understanding of your data and data collection procedure.
As a mouse neuroscientist, lets assume the following about your experiments:

- Your lab houses many mice, and each mouse is identified by a unique ID. You also want to keep track of information
  about each mouse such as their date of birth, gender, and genetic background.
- As a hard working neuroscientist, you perform experiments every day, sometimes working with more
  than one mouse in a day! For each experimental **session**, you would like to record what mouse you worked
  with and when you performed the experiment. You would also like to keep track of other helpful information
  such as the particular collection of equipment or **experimental setup** you worked on.
- Let's assume you're an electrophysiologist. That means that in each experimental **session**, you record electrical activity from a single neuron in each session. You use recording equipment
  that produces separate data files for each neuron you recorded. 

Notice how even in this very simple example there is a lot of related information that you need to keep track of to organize your data. For example, the neural activity you record may depend on the gender and genetic background of the mouse.

Similarly, information about the experimental setup that the data was collected on might be irrelevant for your final data analysis, 
but it also might be critical if you discover some problem with the equipment and have to 
recompute your results on all data collected from that particular setup.

As you will see shortly, with DataJoint, it is not only easy but very natural to create a data pipelines
that can include all of the above information. Now choose your language and move on with the tutorial!

Building in Python
==================

Ready to start building your data pipeline in Python? Proceed to :doc:`python/first-table` now!

.. note::
  To complete this, you must have a properly configured database server and a computer with Python 3.4 or above
  with the DataJoint package already installed and configured to connect to the database. If you don't have this
  set up, refer to :doc:`/setting-up/introduction` to configure your development environment before proceeding.

.. toctree::
   :maxdepth: 2
   :hidden:
   :includehidden:
   :caption: Getting Started

   python/first-table
   python/inserting-data
   python/save-tables
   python/querying-data
   python/child-table
   python/more-queries
   python/importing-data
   python/computed-table


Building in MATLAB
==================

Ready to start building your data pipeline in MATLAB? Proceed to :doc:`matlab/first-table` now!

.. note::
  To complete this, you must have a properly configured database server and a computer with MATLAB 2015b or newer
  with the DataJoint toolbox already installed and configured to connect to the database. If you don't have this
  set up, refer to :doc:`/setting-up/introduction` to configure your development environment before proceeding.

.. toctree::
   :maxdepth: 2
   :hidden:
   :includehidden:
   :caption: Getting Started

   matlab/first-table
   matlab/inserting-data
   matlab/querying-data
   matlab/child-table
   matlab/more-queries
   matlab/importing-data
   matlab/computed-table


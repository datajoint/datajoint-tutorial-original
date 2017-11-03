
.. TODO:
..  - HMM: this is sort more 'tutorial' than 'reference'.. 
..  - mention two main suggested types: schema-per-file, schemaname
..    - ??? the 'split across files' doesn't quite work right thing..
..  - example: schema1, schema2, introduce schema-per-file
..  - show file ingest example via populate  & migrate to 'live' data
..  - schema-per-file with embedded schema object
..  - schema methods: separate schema names
..  - data migration: insert-from-select
..  - work in a reference to the data tiers page somehow

Using Multiple Schemas
======================

Partitioning data into different datasets can be a useful means to categorize
and manage data according to various criteria, such as data type or longetivty,
data readyness or completeness, data sharing and access, or any number of other
factors. In DataJoint, this kind of data partitioning can be accomplished
through the use of multiple database schemas.

.. TODO: does this hold for Matlab?
This is typically done in one of two main ways:

- Embedding the DataJoint 'schema' object within a language module
  which is then utilized from within another project. This is the most
  typical use case.
- Less frequently, multiple schema objects are created within the same
  language module or processing script with differing names, and
  referenced directly as applicable.

The following examples illustrate these methods and how they can be used in
datajoint to support transparent usage of multiple datasets within a single
project.

Using Multiple Schemas in Separate Schema Modules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the most typical use of multiple schemas, separate schemas are defined for
the various datasets used within a set of DataJoint Pipelines.

As an example, it is often the case that some entities will be common to an
entire set of only slightly related DataJoint pipelines. In this case it makes
sense to store the common entities only once in a reference schema which is
later reused within the other pipelines. For example, all experimenters and test
subjects might be recorded in a common 'lab' schema, which is then referred to
within different per-experiment schema to identify which users used performed
certain tasks in the experiment on which subjects. In this case, an example
'lab' schema might look as follows:

.. TODO: Matlab

|python| Python

.. code-block:: python
                
    # lab.py
    import datajoint as dj
    
    schema = dj.schema('labdb', locals())

    @schema 
    class User(dj.Manual):
        definition = """
        user_name:              varchar(64)     # user name
        """


    @schema 
    class Subject(dj.Manual):
        definition = """
        subject_name            varchar(64)     # subject name
        """

From here, the various experiments could then reference the common lab database
as follows:

|python| Python

.. code-block:: python
                
    # experiment1.py
    import datajoint as dj

    import lab
    
    schema = dj.schema('experiment1', locals())

    @schema 
    class Session(dj.Manual):
        definition = """
        -> lab.User
        -> lab.Subject
        session_date:           date            # session date
        ---
        session_result:         tinyint         # session result
        """


As can be seen from the above, the ``lab`` module which contains the schema
object and class definitions for the ``lab`` schema is directly imported in the
``experiment1`` schema definition, and the ``lab.User`` and ``lab.Subject``
tables are subsequently used in defining experiment1's ``Session`` table
against a different ``schema`` object referring to the experiment1 database.

.. TODO: reference to multi language use or table spawning stuffs
   
File-per-schema Convention
--------------------------

In Python, we recommend storing each schema in a single file python module since
this allows a simple means to load and use the schema from interactive sessions
and processing scripts. This also helps to ensure that the 'schema' object is
properly initialized and properly decorates the table classes in the schema.

In this model, common schema configuration information can be hard-coded to
point to a given backend database, or some local external configuration
convention can be used to allow for the use of different development and testing
databases, etc. Using the module name to index the ``dj.config`` dictionary
is one approach that provides a good balance between flexibility and strict
hardcoding. For example the following configuration data:

.. TODO: Matlab

|python| Python

.. code-block:: python

   # configuration in script/interactive environment

   import datajoint as dj
   dj.config['names.lab'] = 'labdb'
   dj.config['names.experiment1'] = 'experiment1'

could then be referenced within the respective 'lab' and 'experiment' schemas as
follows:

.. code-block:: python

   # module containing schema definition

   import datajoint as dj
   schema = dj.schema(dj.config['names.{n}'.format(n=__name__)], locals())

This this will ensure that the configuration variable ``names.<dbname>``
matches the name of the appropriate module, and is safer than hardcoding
the module name within the module since it will stay consistent if
the module is renamed or copied elsewhere for another use.

Foreign Keys and Multiple Schema
--------------------------------
.. TODO?: reference schema n+1 style migration/mgmt here? 

It is important to note that when using pipelines with multiple schema
integrity constraints are maintained across databases - that is, foreign keys
created in child modules will prevent items in the parent schema from being
deleteable.

Multiple-Database Convention
----------------------------

In DataJoint, a single backend database must be used per schema definition, as
some internal datajoint operations rely on this property. Additionally, some
more dangerous operations, such as ``schema.drop`` bypass per-table integrity
checks and operate on the database as a whole; running ``schema.drop`` on a
database used by multiple schema in this case would result in the entire
database being removed and data from all related schema being lost.


Multi-Schema Data Migration Using Schema Objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Less frequently, it is necessary to use multiple schemas via separate schema
objects within the same module or script. This use case is more common in the
case of exploratory schema development or when creating scripts to manage or
migrate the data kept in various DataJoint schemas or any other similar
scenarios when DataJoint schema are used in a temporary fashion.

As an example. let's assume a user has recorded an initial set of experiments
directly in DataJoint using the `lab` and `experiment1` schema from the previous
example, and now, being satisfied with DataJoint as a means to directly record
new experimental data, wishes to import some previous results stored in CSV files
into DataJoint.

To perform the import, our user will create a temporary 'ingest' schema called
`experiment1_ingest` which has a similar set of tables as `lab` and
`experiment1`, and then leverage the `Auto-populate`_ mechanism of DataJoint to
load the previous results from the CSV file. After the ingest is completed, the
user will then transfer the newly imported records into the 'real' `lab` and
`experiment1` schema, so that all of the experimental resuilts will then be
available in a single set of tables for further querying and processing within
DataJoint.

Schema Variable Setup
---------------------

Since the import will dealing with three schemas, `experiment1_ingest`, as well
as the actual `experiment1` and `lab` schema, our example ingest will also
utilize three schema objects. The first, `ingest_schema`, will refer to the
temporary ingest schema and will be created here. The other two schema objects
will refer to the existing `lab` and `experiment1` schemas and will be discussed
later. We will also need to import some various python modules to deal with
sytem paths and parsing CSV records. Overall, the header portion of the ingest
script will look as follows:

|python| Python

.. code-block:: python

   import os
   import csv

   import datajoint as dj

   # define schema objects
   ingest_schema = dj.schema('experiment1_ingest', locals())

   lab_schema = dj.schema('labdb', locals())
   final_schema = dj.schema('experiment1', locals())

From here, the ingest schema tables can be defined.

Defining the Ingest Tables
--------------------------

First, a Lookup table is constructed to store the list of files to load:

|python| Python

.. code-block:: python

   datadir = '/data/old'

   @ingest_schema
   class FileList(dj.Lookup):
       '''
       Lookup table of import CSV files.
       Format is:
       user_name,subject_name,session_date,session_result
       user1,subject1,2017-09-01,1
       '''
       definition = """
       experiment_file:    varchar(255)    # experiment file
       """
       contents = [[os.path.join(datadir, f)]
                   for f in os.listdir(datadir) if f.endswith('.csv')]


As can be seen here, the contents of the lookup table will be populated with
the files ending with '.csv' in the directory 'datadir'. This table will be
used to assist DataJoint's `populate()` method to work with a user-generated
set of keys later on in the example.

From here, the `lab`-like tables are created to hold the data which will
be later be copied into the actual `lab` schema:

|python| Python

.. code-block:: python
    
    @ingest_schema
    class User(dj.Manual):
        definition = """
        user_name:          varchar(64)     # user name
        """
    
    
    @ingest_schema
    class Subject(dj.Manual):
        definition = """
        subject_name:       varchar(64)     # subject name
        """

Finally, our auto-populating ingest version of the `Session` table is defined:

|python| Python

.. code-block:: python
    
    @ingest_schema
    class Session(dj.Computed):
        definition = """
        -> User
        -> Subject
        session_date:       date            # session date
        ---
        session_result:     tinyint         # session result
        -> FileList
        """
    
        @property
        def key_source(self):
            return FileList()
    
        def _make_tuples(self, key):
            with open(key['experiment_file'], 'r') as infile:
                incsv = csv.DictReader(infile)
                for rec in incsv:
    
                    try:
                        User().insert1((rec['user_name'],))
                    except:  # ignore duplicates
                        pass
    
                    try:
                        Subject().insert1((rec['subject_name'],))
                    except:  # ignore duplicates
                        pass
    
                    Session().insert1(dict(**key, **rec))

The data stored in table is very similar to the `experiment1` copy, but the
table is defined with a few key differences:

- The table type is set to `dj.Computed` in order to allow DataJoint's
  `populate()` method to assist in populating the tables
- The table definition contains an additional reference to our `FileList`
  table, which creates a DataJoint relationship between these tables.
- A `key_source` property method is created which returns the result
  of querying the `FileList` table for all records
- A `_make_tuples` method is defind to parse and load the data from
  each file.

Combined, these changes will cause the `populate()` method to query the
`FileList` table through the `key_source` method to determine which records need
to be computed (which files need to be loaded), and then call `_make_tuples` to
compute the results for that key (to process that file). The result will
be a populated set of tables containing all the data stored in the input files.

Although this might not seem as straightforward as say, looping over the input
files and inserting records manually, this method allows for easy re-loading of
additional data if needed, and, once the idiom is understood, is quite
straightforward and provides a consistent structure for any similar sorts of
operations.

It should also be noted that a real life import method might entail further and
more complicatd processing; this particular example was constructed so that the
CSV file column names matched the table attributes and so record insertion was
fairly straightforward. That said, it is best to keep processing at this stage
as simple as possible, forming a sort of 'cleaned up' copy of the input file
data, and then perform further processing to match the actual experimental
schema within datajoint, so that computations can be cleanly reproduced if
needed.

Now that the ingest table has been constructed, the main processing logic
of loading the data into the ingest schema and copying the results into
the experiment schema can be performed.

Ingesting and Copying
---------------------

Now that the ingest schema has been defined, it is straightforward to
load the data into DataJoint:

|python| Python

.. code-block:: python
    
    Session().populate()

This will load the data as outlined in the previous section. From here,
the ingest data can be inspected and then copied into the production database.

Although this can be done via the usual file-per-module import mechanism, since
we are only dealing with raw database manipulation and don't need to utilize any
custom code within the modules, we can simply instruct datajoint to interact
with their tables directly via the `create_virtual_module` method.

|python| Python

.. code-block:: python
    
   # dj.create_virtual_module(vmodname, dbname)
   lab_schema = dj.create_virtual_module('labdb', 'labdb')
   final_schema = dj.create_virtual_module('experiment1', 'experiment1')

These calls create schema objects which can be used to load the data:

|python| Python

.. code-block:: python
    
   lab_schema.User().insert(User(), skip_duplicates=True)
   lab_schema.Subject().insert(Subject(), skip_duplicates=True)
   final_schema.Session().insert(Session(), ignore_extra_fields=True)

These operations will copy the results from the ingest schema into
the 'virtual module' tables of the 'real' `lab` and `experiment` tables.

In this case, since the insert's are done from a non-'fetched' query, DataJoint
will perform the operation entirely on the server, without needing to transfer
the data through the client for processing, improving the performance of the
copy operation dramatically over a client-side processing loop.

Since the User and Subject data is common to multiple experiments, our
copy operations for these tables instruct DataJoint to skip all duplicate
records to prevent errors in the event that the User or Subject have already
been defined, and DataJoint is also instructed to ignore extra fields in Session
copying, since our ingest schema contains an extra field for the input file
record which is not present in the final version.

From here, the ingest schema can be kept if needed for reference, or removed as
is deemed fit, and the `real` schema can be used for native input of new records
without needing to keep track of the various ingest files from the previous
manual approach.

.. |python| image:: ../_static/img/python-tiny.png
.. |matlab| image:: ../_static/img/matlab-tiny.png

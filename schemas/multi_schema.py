
import os
import csv

import datajoint as dj

schema = dj.schema('tutorial_multischem', locals())


@schema
class FileList(dj.Lookup):
    '''
    Lookup table of import CSV files.
    Format is:
    user, subject, date, result
    user1,subject1,2017-09-01,1
    '''
    definition = """
    experiment_file:    varchar(255)    # experiment file
    """

    contents = [[os.path.join('.', f)]
                for f in os.listdir('.') if f.endswith('.csv')]


@schema
class User(dj.Manual):
    definition = """
    user_name:          varchar(64)     # user name
    """


@schema
class Subject(dj.Manual):
    definition = """
    subject_name:       varchar(64)     # subject name
    """


@schema
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
                except:
                    pass  # allow duplicates

                try:
                    Subject().insert1((rec['subject_name'],))
                except:
                    pass  # allow duplicates

                Session().insert1(dict(**rec, **key))


if __name__ == '__main__':
    Session.populate()
    lab_schema = dj.create_virtual_module('lab', 'tutorial_lab')
    ex1_schema = dj.create_virtual_module('experiment1',
                                          'tutorial_experiment1')
    lab_schema.User().insert(User(), skip_duplicates=True)
    lab_schema.Subject().insert(Subject(), skip_duplicates=True)
    ex1_schema.Session().isnert(Session(), ignore_extra_fields=True)

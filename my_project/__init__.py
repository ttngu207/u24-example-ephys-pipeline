import datajoint as dj
from djsubject import schema as subject
from djlab import schema as lab
from djephys import schema as ephys
from my_project.utils import get_ephys_probe_data_dir, get_ks_data_dir

# ============== Declare "lab" and "subject" schema ==============

lab.declare_tables(dj.schema('u24_lab_'))

subject.declare_tables(dj.schema('u24_subject_'),
                       requirements = {'Source': lab.Source,
                                       'Lab': lab.Lab,
                                       'Protocol': lab.Protocol,
                                       'User': lab.User})

# ============== Declare Session table ==============

schema = dj.schema('u24_experiment_')


@schema
class Session(dj.Manual):
    definition = """
    -> subject.Subject
    session_datetime: datetime
    """


# ============== Declare "ephys" schema ==============

ephys.declare_tables(dj.schema('u24_ephys_'),
                     requirements = {'Subject': subject.Subject,
                                     'Session': Session,
                                     'Location': lab.Location,
                                     'get_npx_data_dir': get_ephys_probe_data_dir,
                                     'get_ks_data_dir': get_ks_data_dir})

# ---- Add neuropixels probes ----

for probe_type in ('neuropixels 1.0 - 3A', 'neuropixels 1.0 - 3B',
                   'neuropixels 2.0 - SS', 'neuropixels 2.0 - MS'):
    ephys.ProbeType.create_neuropixels_probe(probe_type)

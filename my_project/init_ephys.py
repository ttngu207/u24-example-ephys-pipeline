import datajoint as dj
from djsubject import subject
from djlab import lab
from djephys import ephys
from my_project.utils import get_ephys_probe_data_dir, get_ks_data_dir

# ============== Declare "lab" and "subject" schema ==============

lab.declare('u24_lab')

subject.declare('u24_subject',
                dependencies={'Source': lab.Source,
                              'Lab': lab.Lab,
                              'Protocol': lab.Protocol,
                              'User': lab.User})

# ============== Declare Session table ==============

schema = dj.schema('u24_experiment')


@schema
class Session(dj.Manual):
    definition = """
    -> subject.Subject
    session_datetime: datetime
    """


# ============== Declare "ephys" schema ==============

ephys.declare(dj.schema('u24_ephys'),
              dependencies={'Subject': subject.Subject,
                            'Session': Session,
                            'Location': lab.Location,
                            'get_npx_data_dir': get_ephys_probe_data_dir,
                            'get_ks_data_dir': get_ks_data_dir})

# ---- Add neuropixels probes ----

for probe_type in ('neuropixels 1.0 - 3A', 'neuropixels 1.0 - 3B',
                   'neuropixels 2.0 - SS', 'neuropixels 2.0 - MS'):
    ephys.ProbeType.create_neuropixels_probe(probe_type)

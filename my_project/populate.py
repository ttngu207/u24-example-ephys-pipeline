import numpy as np
from my_project.init_ephys import ephys

populate_settings = {'reserve_jobs': True, 'suppress_errors': True, 'display_progress': True}

# populate "dj.Imported" tables
for tbl in ephys._table_classes:
    if np.any([c.__name__ == 'Imported' for c in tbl.__bases__]):
        print(f'--- Populating {tbl.__name__} ---')
        tbl.populate(**populate_settings)

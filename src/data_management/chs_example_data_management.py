import pandas as pd
import sys
from bld.project_paths import project_paths_join as ppj

if __name__ == '__main__':
    dataset_name = sys.argv[1]
    data = pd.read_stata(ppj('IN_DATA', '{}.dta'.format(dataset_name)))

    data['caseid'] = data['caseid'] - 1
    data['period'] = data['period'] - 1
    data = data.drop(
        ['dy1', 'dy2', 'dy3', 'dy4', 'dy5', 'dy6', 'dQ1'], axis=1)

    data.to_stata(ppj("OUT_DATA", "final/{}_ready.dta".format(dataset_name)))

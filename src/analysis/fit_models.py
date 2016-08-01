from skillmodels import CHSModel
from bld.project_paths import project_paths_join as ppj
import pandas as pd
from pandas import DataFrame
import json
import sys


if __name__ == '__main__':
    model_name, dataset_name = sys.argv[1:3]
    with open(ppj('IN_MODEL_SPECS', '{}.json'.format(model_name))) as j:
        model_dict = json.load(j)

    dataset = pd.read_stata(ppj('OUT_DATA', 'final/{}.dta'.format(dataset_name)))

    mod = CHSModel(model_name, dataset_name, model_dict, dataset)
    res = mod.fit()

    df = DataFrame(data=res.params, columns=['params'], index=res.param_names)
    df['se'] = res.bse
    df['pvalues'] = res.pvalues
    df['tvalues'] = res.tvalues

    df.reset_index(inplace=True)

    result_path = ppj('OUT_ANALYSIS', '{}_{}/results_df.csv').format(
        model_name, dataset_name)

    df.to_csv(result_path)



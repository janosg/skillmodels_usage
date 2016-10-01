from skillmodels import SkillModel
from bld.project_paths import project_paths_join as ppj
import pandas as pd
from pandas import DataFrame
import json
import sys


if __name__ == '__main__':
    model_name, dataset_name, estimator = sys.argv[1:4]

    # load the model dict from a json file in src.model_specs
    with open(ppj('IN_MODEL_SPECS', '{}.json'.format(model_name))) as j:
        model_dict = json.load(j)

    # load the dataset from a dta file in bld.out.data
    dataset = pd.read_stata(ppj('OUT_DATA', '{}.dta'.format(dataset_name)))

    # create an instance of SkillModel
    mod = SkillModel(model_dict=model_dict, dataset=dataset,
                     estimator=estimator,
                     model_name=model_name, dataset_name=dataset_name)

    # call its fit method to estimate the model
    res = mod.fit()

    # create a pandas DataFrame containing the parameters and standard errors
    df = DataFrame(data=res.params, columns=['params'], index=res.param_names)
    df['se'] = res.bse
    df['pvalues'] = res.pvalues
    df['tvalues'] = res.tvalues
    df.reset_index(inplace=True)
    # extract the results dictionary
    res_dict = res.optimize_dict
    # save the DataFrame and res_dict
    df_path = ppj('OUT_ANALYSIS', '{}_{}/results_df.csv').format(
        model_name, dataset_name)
    dict_path = ppj('OUT_ANALYSIS', '{}_{}/results_dict.json'.format(
        model_name, dataset_name))
    df.to_csv(df_path)
    with open(dict_path, 'w') as j:
        json.dump(res_dict, j)

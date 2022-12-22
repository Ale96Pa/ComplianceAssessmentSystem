import pandas as pd
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import src.config as conf
import src.utils.process_mining as pm
import src.utils.format_dataset as dat
import src.models.regression as reg
import src.models.probability as prob
import src.validation as val
import ground_truths as gt

"""
Inputs of the system
"""
LOG = conf.log
MODEL = conf.model
sep = conf.separator
case_k = conf.case_key
act_k = conf.activity_key
ts_k = conf.timestamp_key

features = conf.features
# cost_k = conf.cost_key
first_run = conf.first_run

"""
Sysytem support (read only)
"""
log_by_case = conf.data_by_case

"""
Benchmark support
"""
alpha = conf.alpha
gt_file = conf.ground_truth_file
param_file = conf.parameters_gts
log_bmk = conf.log_by_case_benchmark


if __name__ == "__main__":

    # ## Create ground truths and store them
    # gt1 = gt.build_gt1(log_by_case,case_k)
    # gt2 = gt.build_gt2(LOG,log_by_case,sep,case_k,ts_k)
    # df_gts = pd.merge(gt1, gt2, how='inner', on=[case_k])
    # gt3 = gt.build_gt3(LOG,log_by_case,sep,case_k,ts_k)
    # df_gts = pd.merge(df_gts, gt3, how='inner', on=[case_k])
    
    # op = "opened_at"
    # cl = "closed_at"
    # numemp = "sys_mod_count"
    # pr = "priority"
    # for fract in alpha:
    #     gt4 = gt.build_gt4(log_by_case, case_k, op, cl, numemp, fract)
    #     gt5 = gt.build_gt5(log_by_case, case_k, numemp, pr, fract)
    #     df_gts = pd.merge(df_gts, gt4, how='inner', on=[case_k])
    #     df_gts = pd.merge(df_gts, gt5, how='inner', on=[case_k])
    # df_gts.to_csv(gt_file,index=False)
    # df_full = pd.merge(pd.read_csv(log_by_case),df_gts, how='inner', on=[case_k])
    # df_full.to_csv(log_bmk,index=False)

    ## Apply all the models to each ground truth
    df_full = pd.read_csv(log_bmk)
    all_activities, all_deviations = dat.detect_process_elements(log_by_case)
    list_all_params = []
    cols = [col for col in df_full.columns if 'gt' in col]
    for gt_k in cols:
        mod_1 = reg.linear_regression(log_bmk,case_k,gt_k,all_deviations)
        mod_1["model_id"] = "1-"+gt_k
        print("mod1")
        mod_2 = reg.extra_trees_regression(log_bmk,case_k,gt_k,all_deviations)
        mod_2["model_id"] = "2-"+gt_k
        print("mod2")
        mod_3 = prob.causal_probability(log_bmk,case_k,[gt_k],all_deviations,all_activities)
        mod_3["model_id"] = "3-"+gt_k
        print("mod3")
        mod_4 = prob.causal_probability(log_bmk,case_k,[gt_k]+features,all_deviations,all_activities)
        mod_4["model_id"] = "4-"+gt_k
        print("mod4")
        list_all_params+=[mod_1,mod_2,mod_3,mod_4]
        print(gt_k)

    ## Evaluate the different cost models
    dat.write_models_parameters(list_all_params,param_file)
    val.compare_models(log_bmk, case_k, gt_k, param_file)

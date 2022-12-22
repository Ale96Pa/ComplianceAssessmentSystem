import pandas as pd
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import src.config as conf
import src.utils.process_mining as pm
import src.utils.format_dataset as dat
import src.models.regression as reg
import src.models.probability as prob
import src.validation as val

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
cost_k = conf.cost_key
cat_k = conf.category_key
first_run = conf.first_run

"""
Auxiliary support
"""
log_by_case = conf.data_by_case
parameter_file = conf.parameters_file
report_file = conf.report_file

if __name__ == "__main__":
    if first_run:
        print("First run configuration")
        log = pm.getLog(LOG,sep,case_k,act_k,ts_k)
        if type(log) == bool:
            print("Error in parsing the log")
            exit()
        if pm.compute_trace_alignment(log,MODEL,case_k,log_by_case) == False:
            print("Error while performing trace alignment")
            exit()
        dat.format_dataset_by_incidents(LOG,log_by_case,sep,case_k,act_k,ts_k)
        print("End configuration")
    
    all_activities, all_deviations = dat.detect_process_elements(log_by_case)
    mod_1 = reg.linear_regression(log_by_case,case_k,cost_k,all_deviations)
    mod_2 = reg.extra_trees_regression(log_by_case,case_k,cost_k,all_deviations)
    mod_3 = prob.causal_probability(log_by_case,case_k,[cost_k],all_deviations,all_activities)
    mod_4 = prob.causal_probability(log_by_case,case_k,[cost_k]+features,all_deviations,all_activities)

    dat.write_models_parameters([mod_1,mod_2,mod_3,mod_4],parameter_file)

    val.compare_models(log_by_case, case_k, cost_k, parameter_file)
    val.make_report(log_by_case, case_k, cost_k, cat_k, parameter_file, all_deviations, report_file)
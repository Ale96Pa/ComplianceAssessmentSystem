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
first_run = conf.first_run

"""
Auxiliary support
"""
log_by_case = conf.data_by_case
parameter_file = conf.parameters_file
report_file = conf.report_file

if __name__ == "__main__":
    print()
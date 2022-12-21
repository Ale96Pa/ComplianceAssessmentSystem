"""IM
Inputs
"""
log = "inputs/IM-log.csv"
model = "inputs/IM-model.pnml"

separator = ";"
case_key = "incident_id"
activity_key = "event"
timestamp_key = "timestamp"

features = ['category','made_sla','knowledge','u_priority_confirmation','priority',
        'reassignment_count','reopen_count']
cost_key = "fitness" #TODO: controllare dinamicamente

"""
Support dataset
"""
data_by_case = "src/dataset/utils_data/log_by_case.csv"
parameters_file = "src/dataset/results/parameters.csv"


"""
Configuration parameters
"""
first_run=False
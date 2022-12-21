import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import src.config as conf
import src.utils.process_mining as pm
import src.utils.format_dataset as dat

### ONLY THE FIRST TIME
# format dataset
# run trace alignment

"""
Inputs of the system
"""
LOG = conf.log
MODEL = conf.model
sep = conf.separator
case_k = conf.case_key
act_k = conf.activity_key
ts_k = conf.timestamp_key
first_run = conf.first_run

"""
Auxiliary support
"""
log_by_case = conf.data_by_case

if __name__ == "__main__":
    print("System initialized")
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
        
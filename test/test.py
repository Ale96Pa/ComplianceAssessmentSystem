import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import src.config as conf
import src.utils.process_mining as pm
import src.utils.format_dataset as dat

LOG = conf.log
MODEL = conf.model
ALIGNMENT = conf.data_by_case

if __name__ == "__main__":
    print("Start TEST")

    ## First Configuration TEST
    # print("Start TRACE ALIGNMENT test ...")
    # log = pm.getLog(LOG,";", "incident_id", "event", "timestamp")
    # if log == False:
    #     print("Failed log parsing test")
    # if pm.compute_trace_alignment(log, MODEL, "incident_id", "test.csv") == False:
    #     print("Failed trace alignment test")
    # else:
    #     os.remove("test.csv")
    # print("... PASSED")

    # print("Start FORMAT DATASET test ...")
    # dat.format_dataset_by_incidents(LOG,ALIGNMENT,"incident_id",";")
    # print("... PASSED")

import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import src.config as conf
import src.utils.process_mining as pm
import src.utils.format_dataset as dat
import src.models.regression as reg
import src.models.probability as prob
import src.validation as val

LOG = conf.log
MODEL = conf.model
ALIGNMENT = conf.data_by_case
PARAMFILE = conf.parameters_file

if __name__ == "__main__":
    print("Start TEST")

    ## First Configuration TEST
    print("Start TRACE ALIGNMENT test ...")
    log = pm.getLog(LOG,";", "incident_id", "event", "timestamp")
    if log == False:
        print("Failed log parsing test")
    if pm.compute_trace_alignment(log, MODEL, "incident_id", "test.csv") == False:
        print("Failed trace alignment test")
    else:
        os.remove("test.csv")
    print("... PASSED")

    print("Start FORMAT DATASET test ...")
    dat.format_dataset_by_incidents(LOG,ALIGNMENT,"incident_id",";")
    print("... PASSED")

    ## Automatic models TEST
    acts, devs = dat.detect_process_elements(ALIGNMENT)
    p1 = reg.linear_regression(ALIGNMENT,"incident_id","fitness_cost",devs)
    print(p1)
    p2 = reg.extra_trees_regression(ALIGNMENT,"incident_id","fitness_cost",devs)
    print(p2)
    p3 = prob.causal_probability(ALIGNMENT,"incident_id",["fitness_cost"],devs,acts)
    print(p3)

    # Validation and report TEST
    val.compare_models(ALIGNMENT, "incident_id", "fitness_cost", PARAMFILE)
    val.make_report(ALIGNMENT, "incident_id", "fitness_cost", "category", PARAMFILE, devs, "foo.pdf")

    print("END TEST")
    

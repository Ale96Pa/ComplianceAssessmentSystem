import csv
import pm4py
import pandas as pd
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.algo.conformance.alignments.petri_net import algorithm as alignments

"""
This function gets event log from csv or xes file and return error in case of
wrong input file format
"""
def getLog(inputFile, separator, case_k, activity_k, timestamp_k):
    if ".csv" in inputFile:
        log_csv = pd.read_csv(inputFile, sep=separator)
        log_csv = pm4py.format_dataframe(log_csv, case_id=case_k, 
            activity_key=activity_k, timestamp_key=timestamp_k)
        log_csv = dataframe_utils.convert_timestamp_columns_in_df(log_csv)
        event_log = log_converter.apply(log_csv)
        return event_log
    elif ".xes" in inputFile:
        return pm4py.read_xes(inputFile)
    else:
        print("Wrong log file format!")
        return False

"""
This function formats the results of the trace alignment into cost model
notation in which: s=skip, r=repetition, m=mismatch
"""
def compute_trace_alignment(log, modelFile, case_k, alignment_file):

    # Compute trace alignment
    try:
        model_net, initial_marking, final_marking = pnml_importer.apply(modelFile)
        aligned_traces = alignments.apply_log(log, model_net, initial_marking, final_marking)
    except:
        return False

    # Format trace alignment in cost model notation
    i=0
    resAlignments = []
    for trace in aligned_traces:
        traceFormat = ""
        for j in range(0,len(trace["alignment"])):
            events = trace["alignment"][j]

            if j == 0 or j == len(trace["alignment"])-1:
                if events[0] == events[1]:
                    traceFormat+=str(events[0])
                elif events[0] == ">>":
                    traceFormat+="s"+str(events[1])
                elif events[1] == ">>":
                    traceFormat+="r"+str(events[0])
                traceFormat+=";"
            else:
                if events[0] == events[1]:
                    traceFormat+=str(events[0])
                elif events[0] == ">>":
                    traceFormat+="s"+str(events[1])
                elif events[1] == ">>": #repetition/mismatch
                    prev_event = trace["alignment"][j-1][0]
                    next_event = trace["alignment"][j+1][0]
                    if events[0] == prev_event or events[0] == next_event:
                        traceFormat+="r"+str(events[0])
                    else:
                        traceFormat+="m"+str(events[0])
                traceFormat+=";"

        resAlignments.append({
            case_k: log[i].__getitem__(0)[case_k],
            "trace": traceFormat,
            "fitness": trace["fitness"],
            "fitness_cost": 1-trace["fitness"]
        })
        i+=1

    # Write log with fitness and cost model notation in auxiliary file
    with open(alignment_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=resAlignments[0].keys())
        writer.writeheader()
        writer.writerows(resAlignments)

    return resAlignments
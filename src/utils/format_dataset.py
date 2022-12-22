import pandas as pd
import pm4py
import csv

def format_dataset_by_incidents(original_log, alignment_file, separator, case_k, activity_k, timestamp_k):
    if ".xes" in original_log:
        df_log = pm4py.convert_to_dataframe(pm4py.read_xes(original_log))
    else:
        df_log = pd.read_csv(original_log, sep=separator)
    df_log = df_log.drop_duplicates(subset=case_k, keep="last")

    df_align = pd.read_csv(alignment_file)
    df_merged = pd.merge(df_log, df_align, how='outer', on=[case_k])
    df_merged = df_merged.loc[:, ~df_merged.columns.isin([activity_k, timestamp_k])]

    df_merged.to_csv(alignment_file,index=False)

def detect_process_elements(log_by_case):
    with open(log_by_case) as csv_r:
        reader = csv.DictReader(csv_r)
        activities = []
        deviations = []
        for row in reader:
            all = row["trace"].split(";")
            for i in range(0,len(all)):
                elem = all[i]
                if len(elem) == 1:
                    activities.append(elem)
                if len(elem) == 2:
                    deviations.append(elem)

    activities = list(dict.fromkeys(activities))
    deviations = list(dict.fromkeys(deviations))
    return activities, deviations

def write_models_parameters(models_list, parameter_file):
    with open(parameter_file, 'w', newline='') as param_obj:            
        dict_writer = csv.DictWriter(param_obj, models_list[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(models_list)

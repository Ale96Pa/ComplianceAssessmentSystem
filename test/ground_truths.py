import pandas as pd
import csv
from datetime import datetime
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import src.config as conf

# """
# First creation of ground truth file
# """
# def create_gt_file(incidents, gt_file):
#     if not os.path.isfile(gt_file):
#         df_inc = pd.read_csv(incidents)[["incident", "trace"]]
#         df_inc.to_csv(gt_file, index=False)

# """
# Clean ground truth from main file
# """
# def remove_gt(gt_file, gt_id):
#     df = pd.read_csv(gt_file)
#     df = df.drop([gt_id], axis=1)
#     df.to_csv(gt_file, index=False)

# """
# Function to add a new ground truth to the existing benchmark of ground truth
# """
# def add_gt(gt_dict, gt_file):
#     existing_gt = pd.read_csv(gt_file)
#     new_gt = pd.DataFrame(gt_dict)
#     df = pd.merge(existing_gt, new_gt, how='inner', on=['incident'])
#     df.to_csv(gt_file, index=False)

"""
Ground Truth 1 (GT1)
Cost(non compliance) = fitness
"""
def build_gt1(log_by_case, case_k, fract=1):
    df_log = pd.read_csv(log_by_case)[[case_k, "fitness_cost"]]
    df_log.rename(columns = {'fitness_cost':'gt1_1'}, inplace = True)
    return df_log
    # l_dict = []
    # with open(incidents, 'r') as read_inc:
    #     csv_inc_reader = csv.DictReader(read_inc)
    #     for row in csv_inc_reader:
    #         for dic in aligns:
    #             if dic["incident_id"] == row["incident"]:
    #                 l_dict.append({"incident":row["incident"], "gt1_1":1-float(dic["fitness"])})
    # add_gt(l_dict, gt_file)


"""
Ground Truth 2 (GT2)
Cost of non-compliance of each trace according to [Kieninger]
[Kieninger] Axel Kieninger, Florian Berghoff, Hansj ̈org Fromm, and Gerhard Satzger.
Simulation-Based Quantification of Business Impacts Caused by Service Incidents.
"""
def build_gt2(log, log_by_case, separator, case_k, ts_k, fract=1):
    df_original = pd.read_csv(log, sep=separator)
    df_log_case = pd.read_csv(log_by_case)[[case_k,"trace"]]
    grouped_by_case = df_original.groupby([case_k])
    l_dict = []

    for caseID, item in grouped_by_case:
        single_case_df = grouped_by_case.get_group(caseID)
        trace_ID = single_case_df[case_k].to_list()[0]

        trace = df_log_case.query(case_k+" == '"+str(trace_ID)+"'")["trace"].to_string()
        activities = trace.split(";")
        timestamps = single_case_df[ts_k].to_list()

        durations = []
        for i in range(1,len(timestamps)):
            start = datetime.strptime(timestamps[i-1], "%d/%m/%Y %H:%M")
            close = datetime.strptime(timestamps[i], "%d/%m/%Y %H:%M")
            durations.append(round((close-start).total_seconds()/3600, 2))
        avgDuration = sum(durations)/len(durations)

        cost=0
        counter_miss=0
        for i in range(0,len(activities)):
            if "s" in activities[i]:
                cost += avgDuration
                counter_miss+=1
            elif "r" in activities[i] or "m" in activities[i]:
                start = datetime.strptime(timestamps[i-counter_miss-1], "%d/%m/%Y %H:%M")
                close = datetime.strptime(timestamps[i-counter_miss], "%d/%m/%Y %H:%M")
                cost += round((close-start).total_seconds()/3600, 2)
        l_dict.append({case_k:trace_ID, "gt2_"+str(fract):abs(cost)})
    # add_gt(l_dict, gt_file)
    return pd.DataFrame(l_dict)

"""
Ground Truth 3 (GT3)
Cost of traces for SLA violations according to [Moura]
[Moura] MOURA, Antão, et al. A quantitative approach to IT investment allocation to 
improve business results. In: Seventh IEEE International Workshop on Policies 
for Distributed Systems and Networks (POLICY'06). IEEE, 2006. p. 9 pp.-95.
"""
def convertRiskValues(str):
    if str == "1 - Critical":
        return 4
    elif str == "2 - High" or str == "1 - High":
        return 3
    elif str == "3 - Moderate" or str == "2 - Medium":
        return 2
    else:
        return 1
def build_gt3(log, log_by_case, separator, case_k, ts_k, fract=1):
    df_original = pd.read_csv(log, sep=separator)
    df_log_case = pd.read_csv(log_by_case)[[case_k,"trace"]]
    grouped_by_case = df_original.groupby([case_k])
    l_dict = []

    for caseID, item in grouped_by_case:
        single_case_df = grouped_by_case.get_group(caseID)
        trace_ID = single_case_df[case_k].to_list()[0]

        trace = df_log_case.query(case_k+" == '"+str(trace_ID)+"'")["trace"].to_string()
        activities = trace.split(";")
        timestamps = single_case_df[ts_k].to_list()

        activities = [item for item in activities if "s" not in item]
        prio_val = convertRiskValues(df_original["priority"].to_list()[0])
        
        cost = 0
        for i in range(0,len(activities)):
            if len(activities[i])>1 and i>0:
                start = datetime.strptime(timestamps[i-1], "%d/%m/%Y %H:%M")
                close = datetime.strptime(timestamps[i], "%d/%m/%Y %H:%M")
                cost = round((close-start).total_seconds()/3600, 2)*prio_val
        l_dict.append({case_k:trace_ID, "gt3_"+str(fract):abs(cost)})    
    
    return pd.DataFrame(l_dict)


"""
Ground Truth 4 (GT4)
Cost of the trace based on person-hours metric according to [Dumas]
[Dumas] Marlon Dumas, Marcello La Rosa, Jan Mendling, Hajo A Reijers, et al.
Fundamentals of business process management, volume 1. Springer, 2013.
"""
def build_gt4(log_by_case, case_k, open_k, close_k, numemp_k, fract):
    l_dict = []
    with open(log_by_case, 'r') as read_inc:
        csv_inc_reader = csv.DictReader(read_inc)
        for row in csv_inc_reader:
            start = datetime.strptime(row[open_k], "%d/%m/%Y %H:%M")
            close = datetime.strptime(row[close_k], "%d/%m/%Y %H:%M")
            num_employee = row[numemp_k]
            cost = round((close-start).total_seconds()/3600)*int(num_employee)
            l_dict.append({case_k:row[case_k], "gt4_"+str(fract):cost*fract})
    # add_gt(l_dict, gt_file)
    return pd.DataFrame(l_dict)


"""
Ground Truth 5 (GT5)
Cost of the traces according to the model defined in [4]
[4] Sasha Romanosky. Examining the costs and causes of cyber incidents.
Journal of Cybersecurity, page tyw001, August 2016.
"""
def build_gt5(log_by_case, case_k, numemp_k, priority_k, fract):
    l_dict = []
    with open(log_by_case, 'r') as read_inc:
        csv_inc_reader = csv.DictReader(read_inc)
        for row in csv_inc_reader:
            num_employee = row[numemp_k]
            impact = convertRiskValues(row[priority_k])
            cost = 2.67*int(num_employee)*impact
            l_dict.append({case_k:row[case_k], "gt5_"+str(fract):cost*fract})
    # add_gt(l_dict, gt_file)
    return pd.DataFrame(l_dict)
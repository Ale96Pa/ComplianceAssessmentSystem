import pandas as pd
import csv
from datetime import datetime
import pm4py
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import src.config as conf

def format_dataset_by_incidents(original_log, alignment_file, separator, case_k, activity_k, timestamp_k):

    if ".xes" in original_log:
        df_log = pm4py.convert_to_dataframe(pm4py.read_xes(original_log))
    else:
        df_log = pd.read_csv(original_log, sep=separator)
    df_log = df_log.drop_duplicates(subset=case_k, keep="first")

    df_align = pd.read_csv(alignment_file)
    df_merged = pd.merge(df_log, df_align, how='outer', on=[case_k])
    df_merged = df_merged.loc[:, ~df_merged.columns.isin([activity_k, timestamp_k])]

    df_merged.to_csv(alignment_file,index=False)

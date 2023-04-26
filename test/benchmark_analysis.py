import pandas as pd
import csv
import numpy as np
import sklearn.metrics as metrics
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import src.validation as val
import src.config as conf
pd.options.mode.chained_assignment = None


"""
Create the benchmark with all the observations for each experiment.
An experiment is a different combination of model and ground truth.
"""
def create_bmk_file(log_by_case, param_file, gt_file, bmk_file, case_k):
    df_gt = pd.read_csv(gt_file)
    counter_bmk = 1

    full_df = pd.DataFrame()
    with open(param_file, 'r') as read_param:
        param_reader = csv.DictReader(read_param)
        for row in param_reader:
            model_id = row["model_id"]
            gt_id = model_id.split("-")[1]
            df_cost = val.compute_cost(log_by_case, case_k, row)

            dg_gt_single = df_gt[[case_k,gt_id]].rename(columns={gt_id: "gt"})
            df = pd.merge(dg_gt_single, df_cost, how='inner', on=[case_k])
            df.insert(0, 'id', counter_bmk)
            df.insert(1, 'model_id', model_id)

            if counter_bmk == 1:
                full_df = df
            else:
                full_df = full_df.append(df)
            counter_bmk += 1
            print(counter_bmk)
            
    full_df.to_csv(bmk_file, index=False)

"""
Plot benchmark analyses
"""
def get_model_name(model_id):
    if model_id == 0:
        return "Fitness"
    elif model_id == 1:
        return "Extra Trees Regression"
    elif model_id == 2:
        return "Linear Regression"
    elif model_id == 3:
        return "Causal Probability (cost)"
    else:
        return "Causal Probability (all)"

def plot_bmk_analyses(gt_file, parameter_file, bmk_file):
    gt_df = pd.read_csv(gt_file)
    df_params = pd.read_csv(parameter_file)
    df_bmk = pd.read_csv(bmk_file)
    dic_gt = {}
    for gt in gt_df.columns:
        if "gt" in gt and "_1" in gt:
            dic_gt[gt] = gt_df[gt].to_list()

    gts = list(dic_gt.keys())

    normalDict = {}
    for gt_k in gts:
        raw = dic_gt[gt_k]
        normalDict[gt_k] = [float(i)/max(raw) for i in raw]

    ## 1A. Cost Trend between Ground Truths
    fig, ax = plt.subplots(figsize=[20, 7])
    fig.suptitle('Ground Truths Cost Distribution')
    for gt_k in gts:
        ax.set_xlabel(gt_k)
        ysmoothed = gaussian_filter1d(normalDict[gt_k], sigma=30)
        ticks = list(range(0, len(ysmoothed)))
        ax.plot(ticks, ysmoothed, label=gt_k.split("_")[0])    
    plt.legend()
    plt.xlabel("Traces")
    plt.ylabel("Cost")
    # plt.rcParams.update({'font.size': 22})
    plt.savefig('test/benchmark/plots/gts_trend.png', bbox_inches='tight')
    # plt.show()

    ## 2. Cost Trend against each Ground Truth    
    fig, axs = plt.subplots(5, 1)
    fig.set_figwidth(20)
    fig.set_figheight(10)
    j=0
    for gt_k in gts:
        ax = axs[j]
        for i in range(1,5):
            model_id = str(i)+"-"+gt_k
            df = df_bmk.query("model_id == "+"'"+model_id+"'")["cost_model"]
            normalCost = (df-df.min())/(df.max()-df.min())
            ysmoothed = gaussian_filter1d(normalCost.to_list(), sigma=30)
            ticks = list(range(0, len(ysmoothed)))
            ax.plot(ticks, ysmoothed, label=get_model_name(i))

        df = df_bmk.query("model_id == "+"'"+model_id+"'")["gt"]
        normalCost = (df-df.min())/(df.max()-df.min())
        ysmoothed = gaussian_filter1d(normalCost.to_list(), sigma=30)
        ticks = list(range(0, len(ysmoothed)))
        ax.plot(ticks, ysmoothed, label=gt_k.split("_")[0])
        ax.legend()
        ax.set_xlabel("Traces")
        ax.set_ylabel("Cost")
        j+=1
    plt.savefig('test/benchmark/plots/cost_vs_gt.png', bbox_inches='tight')
    # plt.show()

    ## 3. Model Analysis for each metric
    dict_mse = {}
    dict_mae = {}
    dict_med = {}
    l_mse=[]
    l_mae=[]
    l_mad=[]
    x = gt_df["gt1_1"]
    x = (x-x.min())/(x.max()-x.min())
    for gt in gt_df.columns:
        if gt == "gt1_1" or gt == "incident_id":
            continue
        y = gt_df[gt]
        y = (y-y.min())/(y.max()-y.min())
        l_mse.append(metrics.mean_squared_error(y, x))
        l_mae.append(metrics.mean_absolute_error(y, x))
        l_mad.append(metrics.median_absolute_error(y, x))
    dict_mse["0"] = l_mse
    dict_mae["0"] = l_mae
    dict_med["0"] = l_mad

    for i in range(1,5):
        mod_df = df_params[df_params["model_id"].str.contains(str(i)+"-")]
        mod_df = mod_df[~mod_df["model_id"].str.contains("gt1")]
        dict_mse[str(i)] = mod_df["mse"].to_list()
        dict_mae[str(i)] = mod_df["mae"].to_list()
        dict_med[str(i)] = mod_df["mad"].to_list()
    list_dict = [dict_mse, dict_mae, dict_med]

    for i in range(0,len(list_dict)):
        if i==0:
            err = "MSE"
        elif i==1:
            err = "MAE"
        else:
            err = "MAD"
        plot_dict = list_dict[i]
        fig, ax = plt.subplots()
        fig.set_figwidth(15)
        fig.set_figheight(7)
        fig.suptitle(err+" distribution")

        models=[]
        for e in plot_dict.keys():
            models.append(get_model_name(int(e)))
        ax.set_xticklabels(models)
        ax.boxplot(plot_dict.values())
        plt.savefig('test/benchmark/plots/metrics_'+err+'.png', bbox_inches='tight')
        # plt.show()
            

    ## Best benchmark analysis
    dfMse=df_params.query("mse == "+str(df_params["mse"].min()))
    dfMed=df_params.query("mad == "+str(df_params["mad"].min()))
    dfMae=df_params.query("mae == "+str(df_params["mae"].min()))
    df_best = dfMse.append(dfMed, ignore_index=True).append(dfMae, ignore_index=True).drop_duplicates(subset='model_id', keep="first")
    # print(df_best)

import seaborn as sns
def plot_false_positive(bmk_file):
    df_gt = pd.read_csv(bmk_file)
    grouped_by_bmk = df_gt.groupby(["id"])

    fig, axs = plt.subplots(1, 4)
    fig.set_figwidth(18)
    fig.set_figheight(4)
    j=0
    num=2
    for caseID, item in grouped_by_bmk:
        single_case_df = grouped_by_bmk.get_group(caseID)
        experient_id = list(single_case_df["model_id"])[0]
        if "_1" not in experient_id or "3-" not in experient_id: continue
    
        # single_case_df["cost_model"] = (single_case_df["cost_model"]-np.min(single_case_df["cost_model"]))/(np.max(single_case_df["cost_model"])-np.min(single_case_df["cost_model"]))
        binsP = np.percentile(single_case_df["cost_model"], [0, 50, 100])
        labelP=['L','H']
        if len(binsP) != len(set(binsP)): continue
        single_case_df['y_pred'] = pd.cut(x=single_case_df['cost_model'], bins=binsP, labels=labelP, duplicates="drop")
        
        # single_case_df["gt"] = (single_case_df["gt"]-np.min(single_case_df["gt"]))/(np.max(single_case_df["gt"])-np.min(single_case_df["gt"]))
        binsT = np.percentile(single_case_df["gt"], [0, 50, 100])
        labelT=['L','H']
        if len(binsT) != len(set(binsT)): continue
        single_case_df['y_true'] = pd.cut(x=single_case_df['gt'], bins=binsT, labels=labelT, duplicates="drop")

        y_pred = single_case_df["y_pred"]
        y_true = single_case_df["y_true"]
        TP, FP, FN, TN = 0,0,0,0
        for pp, tt in zip(y_pred, y_true):
            if pp==tt and pp=="H": TN+=1
            elif pp==tt and pp=="L": TP+=1
            elif pp!=tt and pp=="L": FP+=1
            else: FN+=1
            # there is no case for FN, TN
        FPR = FP/(TN+FP)

        confusion_m = np.matrix([[TP, FP], [FN, TN]])
        annot_text = np.matrix([["TP\n"+str(TP), "FP\n"+str(FP)], ["FN\n"+str(FN), "TN\n"+str(TN)]])
        sns.heatmap(confusion_m, linewidth=0.5,annot=annot_text,fmt="s",yticklabels=False,xticklabels=False,ax=axs[j])
        axs[j].set_title("GT"+str(num))
        # ax.tick_params(left=False, bottom=False)
        j+=1
        num+=1
    plt.savefig('test/benchmark/results_plots/false_positive_rate.png', bbox_inches='tight')


if __name__ == "__main__":
    plot_false_positive(conf.benchmark_file)
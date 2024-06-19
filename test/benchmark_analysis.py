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
        return "ETR"
    elif model_id == 2:
        return "LR"
    elif model_id == 3:
        return "CP"
    else:
        return "CP (all)"
def get_color_name(model_id):
    if model_id == 0:
        return "Fitness"
    elif model_id == 1:
        return "#984ea3"
    elif model_id == 2:
        return "#e41a1c"
    elif model_id == 3:
        return "#377eb8"
    elif model_id == 4:
        return "#4daf4a"
    else:
        return "#000000"

def plot_bmk_analyses(gt_file, parameter_file, bmk_file):
    plt.rcParams.update({'font.size': 26})

    gt_df = pd.read_csv(gt_file)
    df_params = pd.read_csv(parameter_file)
    df_bmk = pd.read_csv(bmk_file)
    dic_gt = {}
    for gt in gt_df.columns:
        if "gt" in gt and "_1" in gt:
            dic_gt[gt] = gt_df[gt].to_list()

    gts = list(dic_gt.keys())#[1:]

    normalDict = {}
    for gt_k in gts:
        raw = dic_gt[gt_k]
        normalDict[gt_k] = [float(i)/max(raw) for i in raw]

    ## 1A. Cost Trend between Ground Truths
    fig, ax = plt.subplots(figsize=[18, 7])
    # fig.suptitle('Ground Truths Cost Distribution')
    for gt_k in gts:
        ax.set_xlabel(gt_k)
        ysmoothed = gaussian_filter1d(normalDict[gt_k], sigma=30)
        ticks = list(range(0, len(ysmoothed)))
        ax.plot(ticks, ysmoothed, label=gt_k.split("_")[0], linewidth=2)    
    leg = plt.legend(ncols=3)
    for line in leg.get_lines():
        line.set_linewidth(4.0)
    plt.xlabel("Trace IDs")
    plt.ylabel("Cost value")
    # plt.rcParams.update({'font.size': 22})
    plt.savefig('test/benchmark/results_plots/gts_trend.png', bbox_inches='tight')
    # plt.show()

    # ## 2. Cost Trend against each Ground Truth    
    # fig, axs = plt.subplots(2,2)
    # fig.set_figwidth(20)
    # fig.set_figheight(10)
    # j=0
    # for gt_k in gts:
    #     l,t=0,0
    #     if j==0: l,t=0,1
    #     elif j==1: l,t=0,0
    #     elif j==2: l,t=1,0
    #     else: l,t=1,1
    #     ax = axs[l][t]
    #     for i in range(1,5):
    #         model_id = str(i)+"-"+gt_k
    #         df = df_bmk.query("model_id == "+"'"+model_id+"'")["cost_model"]
    #         normalCost = (df-df.min())/(df.max()-df.min())
    #         if "4" in gt_k:# and i==2: 
    #             normalCost= [x * 2 for x in normalCost]
    #             ysmoothed = gaussian_filter1d(normalCost, sigma=30)
    #         elif "3" in gt_k and i==3: 
    #             normalCost= [x * 2 for x in normalCost]
    #             ysmoothed = gaussian_filter1d(normalCost, sigma=30)
    #         elif "5" in gt_k and i==3: 
    #             normalCost= [x * 2 for x in normalCost]
    #             ysmoothed = gaussian_filter1d(normalCost, sigma=30)
    #         else: ysmoothed = gaussian_filter1d(normalCost.to_list(), sigma=30)
    #         ticks = list(range(0, len(ysmoothed)))
    #         ax.plot(ticks, ysmoothed, label=get_model_name(i), color=get_color_name(i))

    #     df = df_bmk.query("model_id == "+"'"+model_id+"'")["gt"]
    #     normalCost = (df-df.min())/(df.max()-df.min())
    #     ysmoothed = gaussian_filter1d(normalCost.to_list(), sigma=30)
    #     ticks = list(range(0, len(ysmoothed)))
    #     if gt_k=='gt2_1': ax.plot(ticks, ysmoothed, label='gt3', color=get_color_name(gt_k))
    #     elif gt_k=='gt3_1': ax.plot(ticks, ysmoothed, label='gt2', color=get_color_name(gt_k))
    #     else: ax.plot(ticks, ysmoothed, label=gt_k.split("_")[0], color=get_color_name(gt_k))
        
    #     leg = ax.legend(fontsize='medium', ncols=3)
    #     for line in leg.get_lines():
    #         line.set_linewidth(4.0)

    #     if l==1: ax.set_xlabel("Trace IDs")
    #     ax.set_ylabel("Estimated Trace Cost")
    #     ax.set_ylim(0,0.75)
    #     j+=1
    # plt.savefig('test/benchmark/results_plots/cost_vs_gt.png', bbox_inches='tight')
    # # plt.show()

    # ## 3. Model Analysis for each metric
    # plt.rcParams.update({'font.size': 22})
    # dict_mse = {}
    # dict_mae = {}
    # dict_med = {}
    # l_mse=[]
    # l_mae=[]
    # l_mad=[]
    # x = gt_df["gt1_1"]
    # x = (x-x.min())/(x.max()-x.min())
    # for gt in gt_df.columns:
    #     if gt == "gt1_1" or gt == "incident_id":
    #         continue
    #     y = gt_df[gt]
    #     y = (y-y.min())/(y.max()-y.min())
    #     l_mse.append(metrics.mean_squared_error(y, x))
    #     l_mae.append(metrics.mean_absolute_error(y, x))
    #     l_mad.append(metrics.median_absolute_error(y, x))
    # dict_mse["0"] = l_mse
    # dict_mae["0"] = l_mae
    # dict_med["0"] = l_mad

    # for i in range(1,5):
    #     mod_df = df_params[df_params["model_id"].str.contains(str(i)+"-")]
    #     mod_df = mod_df[~mod_df["model_id"].str.contains("gt1")]
    #     dict_mse[str(i)] = mod_df["mse"].to_list()
    #     dict_mae[str(i)] = mod_df["mae"].to_list()
    #     dict_med[str(i)] = mod_df["mad"].to_list()
    # list_dict = [dict_mse, dict_mae, dict_med]

    # for i in range(0,len(list_dict)):
    #     if i==0:
    #         err = "MSE"
    #     elif i==1:
    #         err = "MAE"
    #     else:
    #         err = "MAD"
    #     plot_dict = list_dict[i]
    #     fig, ax = plt.subplots()
    #     fig.set_figwidth(15)
    #     fig.set_figheight(7)
    #     fig.suptitle(err+" distribution")

    #     del plot_dict["0"]
    #     del plot_dict["4"]

    #     plot_pdict={}
    #     plot_pdict["1"]=plot_dict["2"]
    #     plot_pdict["2"]=plot_dict["1"]
    #     plot_pdict["3"]=plot_dict["3"]

    #     models=[]
    #     for e in plot_pdict.keys():
    #         models.append(get_model_name(int(e)))
    #     ax.set_xticklabels(models)
    #     box = ax.boxplot(plot_pdict.values(),patch_artist=True)
    #     for patch, color in zip(box['boxes'], ["#66c2a5", "#8da0cb", "#fc8d62"]):
    #         patch.set_facecolor(color)
    #     plt.savefig('test/benchmark/results_plots/metrics_'+err+'.png', bbox_inches='tight')
    #     # plt.show()
            

    # ## Best benchmark analysis
    # dfMse=df_params.query("mse == "+str(df_params["mse"].min()))
    # dfMed=df_params.query("mad == "+str(df_params["mad"].min()))
    # dfMae=df_params.query("mae == "+str(df_params["mae"].min()))
    # df_best = dfMse.append(dfMed, ignore_index=True).append(dfMae, ignore_index=True).drop_duplicates(subset='model_id', keep="first")
    # # print(df_best)

import seaborn as sns
def plot_false_positive(bmk_file, modelID="4-"):
    df_gt = pd.read_csv(bmk_file)
    grouped_by_bmk = df_gt.groupby(["id"])

    plt.rcParams.update({'font.size': 14})
    fig, axs = plt.subplots(2, 2)
    fig.set_figwidth(8)
    fig.set_figheight(4)
    j=0
    i=0
    num=2
    for caseID, item in grouped_by_bmk:
        single_case_df = grouped_by_bmk.get_group(caseID)
        experient_id = list(single_case_df["model_id"])[0]
        if "_1" not in experient_id or modelID not in experient_id: continue
    
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
            if pp==tt and pp=="H": TP+=1
            elif pp==tt and pp=="L": TN+=1
            elif pp!=tt and pp=="L": FN+=1
            else: FP+=1
        FPR = FP/(TN+FP)

        confusion_m = np.matrix([[TP, FP], [FN, TN]])
        annot_text = np.matrix([["TP\n"+str(TP), "FP\n"+str(FP)], ["FN\n"+str(FN), "TN\n"+str(TN)]])

        print("GT"+str(num)+"accuracy ("+str(round((TP+TN)/(TP+TN+FP+FN),2))+"), precision ("+str(round(TP/(TP+FP),2))+"), recall ("+str(round(TP/(TP+FN),3))+")")

        if num==2: 
            i=0
            j=0
        elif num==3:
            i=0
            j=1
        elif num==4:
            i=1
            j=0
        else:
            i=1
            j=1
        sns.heatmap(confusion_m, vmin=0,vmax=24000, linewidth=0.5,annot=annot_text,fmt="s",yticklabels=False,xticklabels=False,ax=axs[i][j],cmap="Blues")
        axs[i][j].set_title("GT"+str(num))
        # ax.tick_params(left=False, bottom=False)
        num+=1
    plt.savefig('test/benchmark/results_plots/false_positive_rate.png', bbox_inches='tight')


if __name__ == "__main__":
    # plot_false_positive(conf.benchmark_file, "4-")
    gt_file = conf.ground_truth_file
    param_file = conf.parameters_gts
    bmk_file = conf.benchmark_file
    plot_bmk_analyses(gt_file, param_file, bmk_file)
import pandas as pd
import csv
import numpy as np
import sklearn.metrics as metrics
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
pd.options.mode.chained_assignment = None

def normalize_df_col(df, cols):
    for c in cols:
            mdev = df[c].median()
            df = df[np.abs(df[c]-mdev)/mdev <= 2]
            df[c] = (df[c]-df[c].min()) / (df[c].max()-df[c].min())
    return df

"""
This function calculates the cost of each trace according to the proposed
cost model
"""
def compute_cost(log_by_case, case_k, parameter_dict):
    df_log = pd.read_csv(log_by_case)
    
    l_costs=[]
    for index, row in df_log.iterrows():
        current_deviations = row["trace"].split(";")
        cost=0
        countR = countM = 0
        costR = costS = costM = 0
        for dev in current_deviations:
            if dev in parameter_dict.keys():
                if len(dev)>1 and "r" in dev:
                    countR+=1
                    costR+=float(parameter_dict[dev])
                elif len(dev)>1 and "s" in dev:
                    costS+=float(parameter_dict[dev])
                elif len(dev)>1 and "m" in dev:
                    countM+=1
                    costM+=float(parameter_dict[dev])
        cost=costS+(costR*countR/len(current_deviations))+(costM*countM/len(current_deviations))
        l_costs.append({case_k: row[case_k], "cost_model": cost})

    return pd.merge(df_log[case_k], pd.DataFrame(l_costs), how='inner', on=[case_k])

"""
This function compares the different automatic approaches to estimate costs and
select the one with lowest error
"""
def compare_models(log_by_case, case_k, cost_k, parameter_file):
    df_log = pd.read_csv(log_by_case)

    results = []
    with open(parameter_file) as csv_r:
        reader = csv.DictReader(csv_r)
        for param_dict in reader:
            df_model = compute_cost(log_by_case, case_k, param_dict)
            df = pd.merge(df_log[[case_k, cost_k]], df_model, how='inner', on=[case_k])
            df = normalize_df_col(df, [cost_k, "cost_model"])

            if len(df)>0:
                y = df[cost_k].to_list()
                x = df["cost_model"].to_list()
                mse = metrics.mean_squared_error(y, x)
                mae = metrics.mean_absolute_error(y, x)
                mad = metrics.median_absolute_error(y, x)
                param_dict["mse"] = mse
                param_dict["mae"] = mae
                param_dict["mad"] = mad
                results.append(param_dict)

    with open(parameter_file, 'w', newline='') as param_obj:            
        dict_writer = csv.DictWriter(param_obj, results[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(results)


"""
This function selects the model with minimum error and produce the final report
"""
def make_report(log_by_case, case_k, cost_k, cat_k, parameter_file, deviations, report_file):
    df_param = pd.read_csv(parameter_file)
    best_model = df_param[df_param["mse"] == df_param["mse"].min()].to_dict("records")[0]

    df_log = pd.read_csv(log_by_case)
    df_model = compute_cost(log_by_case, case_k, best_model)
    df = pd.merge(df_log, df_model, how='inner', on=[case_k])
    
    final_report = PdfPages(report_file)

    ## PLOT1: GT vs cost model distribution
    sortedDf = df.sort_values(by=[cost_k])
    cost_gt = sortedDf[cost_k]
    cost_model = sortedDf["cost_model"]
    normalGt =(cost_gt-cost_gt.min())/(cost_gt.max()-cost_gt.min())
    normalModel = (cost_model-cost_model.min())/(cost_model.max()-cost_model.min())
    x = range(len(cost_gt))

    fig, ax = plt.subplots(figsize=[20, 7])
    fig.suptitle('Non-compliance cost trend')
    ax.set_xlabel("Traces")
    ax.set_ylabel("Cost")
    plt.plot(x, normalModel.tolist(), label = "cost model")
    plt.plot(x, normalGt.tolist(), label = cost_k+"-based cost")
    plt.legend()
    final_report.savefig(fig)
    # plt.show()

    ## PLOT2: cost model distribution
    costDf = df["cost_model"]
    normalCost =(costDf-costDf.min())/(costDf.max()-costDf.min())
    fig, ax = plt.subplots(figsize=[7, 10])
    fig.suptitle('Non-compliance cost distribution')
    ax.set_xlabel("Cost")
    ax.boxplot(normalCost)
    final_report.savefig(fig)
    # plt.show()

    ## PLOT3: Barchart quantity low-medium-high-critical
    dfCat = pd.DataFrame()
    dfCat["severity"] = pd.cut(x=normalCost, bins=[-1, 0.01, 0.39, 0.69, 0.89, 1], 
    labels=['None', 'Low', 'Medium', 'High', 'Critical'])
    severityDf = dfCat.groupby("severity")['severity'].count().to_dict()
    
    data = severityDf.values()
    labels = list(severityDf.keys())
    fig, ax = plt.subplots()
    ax.set_xticks(range(len(data)), labels)
    ax.set_xlabel('Severity')
    ax.set_ylabel('Number of occurrences')
    ax.set_title('Non-compliance severity distribution')
    ax.bar(range(len(data)), data, color=['#1a9641','#a6d96a','#ffffbf','#fdae61','#d7191c'])
    for i in range(len(labels)):
            ax.text(i, severityDf[labels[i]], severityDf[labels[i]], ha = 'center')
    final_report.savefig(fig)
    # plt.show()

    ## PLOT 4: Table with all deviations weights
    del best_model["model_id"]
    del best_model["mse"]
    del best_model["mae"]
    del best_model["mad"]
    sortedDeviations = {k: round(v,2) for k, v in sorted(best_model.items(), key=lambda item: item[1], reverse=True)}
    fig, ax = plt.subplots(figsize=[20, 7])
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    df_sortedDeviations = pd.DataFrame.from_dict([sortedDeviations])
    table = ax.table(cellText=df_sortedDeviations.values, 
    colLabels=df_sortedDeviations.columns, loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    fig.tight_layout()
    final_report.savefig(fig)
    # plt.show()

    ## PLOT 5: Analysis per activity and deviation category (occurrences)
    dictCount = {}
    for dev in deviations:
        dictCount[dev] = df["trace"].str.contains(dev).sum()

    fig, axs = plt.subplots(1, 3)
    fig.set_figwidth(20)
    fig.set_figheight(7)

    missK=[]
    missVal=[]
    repK=[]
    repVal=[]
    mismK=[]
    mismVal=[]
    for k in dictCount.keys():
        if "s" in k:
            missK.append(k)
            missVal.append(dictCount[k])
        elif "r" in k:
            repK.append(k)
            repVal.append(dictCount[k])
        else:
            mismK.append(k)
            mismVal.append(dictCount[k])

    axs[0].set_title("Skipping Deviations")
    axs[0].bar(missK, missVal, color=['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00'])
    for i in range(len(missK)):
            axs[0].text(i, dictCount[missK[i]], dictCount[missK[i]], ha = 'center')

    axs[1].set_title("Repeatition Deviations")
    axs[1].bar(repK, repVal, color=['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00'])
    for i in range(len(repK)):
        axs[1].text(i, dictCount[repK[i]], dictCount[repK[i]], ha = 'center')

    axs[2].set_title("Mismatch Deviations")
    axs[2].bar(mismK, mismVal, color=['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00'])
    for i in range(len(mismK)):
        axs[2].text(i, dictCount[mismK[i]], dictCount[mismK[i]], ha = 'center')
    final_report.savefig(fig)
    # plt.show()

    ## PLOT 6: Analysis of critical incidents
    grouped_by_category = df.groupby([cat_k])
    dictCat = {}
    cTot=0
    for category, item in grouped_by_category:
        cat_df = grouped_by_category.get_group(category)
        c = 0
        for inc in cat_df[case_k].to_list():
            c += df.loc[df[case_k] == inc]["cost_model"].to_list()[0]

        dictCat[str(category)] = round(c)
        cTot+=c

    sortedDictCat = {k: v for k, v in sorted(dictCat.items(), key=lambda item: item[1], reverse=True)}

    fig, ax = plt.subplots(figsize=[20, 7])
    ax.bar(sortedDictCat.keys(), sortedDictCat.values())
    ax.set_ylabel('Cost')
    ax.set_title(cat_k)
    cats = list(sortedDictCat.keys())
    for i in range(len(cats)):
        ax.text(i, sortedDictCat[cats[i]], sortedDictCat[cats[i]], ha = 'center')
    ax.set_xticklabels(cats, rotation=45, ha='right')
    final_report.savefig(fig)
    # plt.show()

    final_report.close()
    
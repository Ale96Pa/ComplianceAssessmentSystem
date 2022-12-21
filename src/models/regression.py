import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import ExtraTreesRegressor

"""
Apply multiple linear regression model between two dataframe:
X is formed as [case_id, trace]
Y is formed as [case_id, cost]
"""
def linear_regression(log_by_case, case_k, cost_k, deviations):
    df = pd.read_csv(log_by_case)
    df_trace = df[[case_k, "trace"]]
    df_cost = df[[case_k, cost_k]]

    regr_data=[]
    for index, row in df_trace.iterrows():
        dic = {}
        dic[case_k] = row[case_k]
        for dev in deviations:
            dic[dev] = int(row["trace"].count(dev))
        regr_data.append(dic)

    df_X = pd.merge(df_trace, pd.DataFrame(regr_data), how='inner', on=[case_k])
    df = pd.merge(df_X, df_cost, how='inner', on=[case_k])
    
    y = df[cost_k]
    X = df[list(set(df.columns) - set([case_k,"trace",cost_k]))]
    model = LinearRegression().fit(X, y)

    dict_param = {"model_id":1}
    for i in range(0,len(deviations)):
        dict_param[deviations[i]] =  abs(model.coef_[i])
    return dict_param

"""
Apply extra-trees regression model between two dataframe:
X is formed as [case_id, trace]
Y is formed as [case_id, cost]
"""
def extra_trees_regression(log_by_case, case_k, cost_k, deviations):
    df = pd.read_csv(log_by_case)
    df_trace = df[[case_k, "trace"]]
    df_cost = df[[case_k, cost_k]]

    regr_data=[]
    for index, row in df_trace.iterrows():
        dic = {}
        dic[case_k] = row[case_k]
        for dev in deviations:
            dic[dev] = int(row["trace"].count(dev))
        regr_data.append(dic)

    df_X = pd.merge(df_trace, pd.DataFrame(regr_data), how='inner', on=[case_k])
    df = pd.merge(df_X, df_cost, how='inner', on=[case_k])
    
    y = df[cost_k]
    X = df[list(set(df.columns) - set([case_k,"trace",cost_k]))]
    model = ExtraTreesRegressor(n_estimators=100).fit(X, y)

    dict_param = {"model_id":2}
    for i in range(0,len(deviations)):
        dict_param[deviations[i]] = model.feature_importances_[i]
    return dict_param
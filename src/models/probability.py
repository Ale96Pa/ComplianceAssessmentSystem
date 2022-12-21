import pandas as pd

def kProb(ai, oi, features, df, case_k):
    dfA = df[df["trace"].str.contains(ai)] # traces with deviations ai
    dfAO = df[
    (df["trace"].str.contains("s"+ai+";"+oi)) | 
    (df["trace"].str.contains(ai+";"+oi)) | 
    (df["trace"].str.contains(ai+";r"+oi)) | 
    (df["trace"].str.contains(ai+";m"+oi))] # traces going into oi with deviations ai
    
    if len(dfA)<=0 or len(dfAO)<=0:
        return 0

    po=0
    for fi in features:
        poi = 0
        valsFi = df[fi].unique()
        for val in valsFi:
            dfF = df[df[fi] == val] # traces with feature fi
            intersection = pd.merge(dfAO, dfF, how='inner', on=[case_k])
            union = pd.merge(dfA, dfF, how='inner', on=[case_k])

            if len(intersection) > 0:
                pk = len(dfF)/len(df)
                pak = len(intersection)/len(union)
                poi+=pak*pk
        po+=poi
    return po    

def causal_probability(log_by_case, case_k, features, deviations, activities):
    df_log = pd.read_csv(log_by_case)

    if len(features) == 1:
        dictCosts = {"model_id":3}
    else:
        dictCosts = {"model_id":4}
    for ai in deviations:
        for oi in activities:
            poi = kProb(ai, oi, features, df_log, case_k)
            if ai in dictCosts.keys():
                newP = dictCosts[ai]+poi
                dictCosts[ai] = newP
            else:
                dictCosts[ai] = poi
    return dictCosts
import json
import os
import numpy as np
import scipy.stats as stats
from sklearn.metrics import mean_squared_error

main_dir = os.path.join("data", "reddit_data", "NOV_OUTPUT")
folders = []
error = {}
error['mse_overall'] = 0.0
error['kendall_overall'] = 0.0
error['spearman_overall'] = 0.0
error['mse_sub'] = {}
error['kendall_sub'] = {}
error['spearman_sub'] = {}
l_overall_pred = []
l_overall_ground = []

for r, _, _ in os.walk(main_dir):
    folders.append(r)
subs = folders[1:]

for each_sub in subs:
    sub_folder_name = each_sub.split("/")[-1]
    print(sub_folder_name)
    for _, _, w in os.walk(each_sub):
        files = w
    l_sub_pred = []
    l_sub_ground = []
    for each_file in files:
        with open(os.path.join(each_sub, each_file), "r") as filepointer:
            results = json.load(filepointer)
        y_pred = results['from_to_pred'] + 1.0
        y_ground = results['original_to_pred'] + 1.0
        l_sub_pred.append(y_pred)
        l_sub_ground.append(y_ground)
        l_overall_pred.append(y_pred)
        l_overall_ground.append(y_ground)
    n_pred = np.array(l_sub_pred)
    n_ground = np.array(l_sub_ground)
    tau, _ = stats.kendalltau(n_ground, n_pred)
    spr, _ = stats.spearmanr(n_ground, n_pred)
    mse = mean_squared_error(np.log(n_ground), np.log(n_pred))
    if np.isnan(tau):
        tau = 0.0
    if np.isnan(spr):
        spr = 0.0
    error['kendall_sub'][sub_folder_name] = tau
    error['spearman_sub'][sub_folder_name] = spr
    error['mse_sub'][sub_folder_name] = mse

n_pred = np.array(l_overall_pred)
n_ground = np.array(l_overall_ground)
tau, _ = stats.kendalltau(n_ground, n_pred)
spr, _ = stats.spearmanr(n_ground, n_pred)
mse = mean_squared_error(np.log(n_ground), np.log(n_pred))
error['kendall_overall'] = tau
error['spearman_overall'] = spr
error['mse_overall'] = mse

filesub_folder_name = os.path.join("data", "reddit_data",
                                   "evaluation_metric_nov_10.json")
print(filesub_folder_name)
with open(filesub_folder_name, "w") as f:
    json.dump(error, f, indent=True)

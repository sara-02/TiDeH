"""
Author: Sarah Masud
Copyright (c): Sarah Masud
"""

import os
import json
import numpy as np
import scipy.stats as stats
import argparse

parser = argparse.ArgumentParser(description='Input Params')
parser.add_argument('--m', help='month, either oct or nov')
args = parser.parse_args()
month = args.m if args.m else 'nov'

main_dir = os.path.join("data", "reddit_data")
output_dir = os.path.join(main_dir, month.upper() + "_OUTPUT")

folders = []
feature_list_input = []
feature_list_output = []
k = 10
cascade = np.array([2, 3, 4, 5]) * k
for r, _, _ in os.walk(output_dir):
    folders.append(r)
folders = folders[1:]
for each_sub in folders:
    sub_red = each_sub.split("/")[-1]
    for _, _, f in os.walk(os.path.join(output_dir, sub_red)):
        file_list = f
    for each_file in file_list:
        features_i = []
        features_o = []
        with open(os.path.join(output_dir, sub_red, each_file), "r") as f:
            results = json.load(f)
        pred_count = int(results["from_to_pred"])
        total_pred_length = int(results["total_pred_at"])
        ground_count = int(results["original_to_pred"])
        if pred_count == 0 and ground_count == 0:
            continue
        total_ground_length = total_pred_length - pred_count + ground_count
        feature_list_input.append(list(cascade <= total_ground_length))
        feature_list_output.append(list(cascade <= total_pred_length))

l_pred = []
l_ground = []
n = len(feature_list_input)
for i in range(n):
    f1 = feature_list_input[i]
    f2 = feature_list_output[i]
    for ground, pred in zip(f1, f2):
        l_ground.append(ground)
        l_pred.append(pred)
np_ground = np.array(l_ground).astype(float)
np_pred = np.array(l_pred).astype(float)
tau, _ = stats.kendalltau(np_ground, np_pred)
spr, _ = stats.spearmanr(np_ground, np_pred)
results = {}
results["tau_cascade_overall"] = tau
results["spr_cascade_overall"] = spr
result_filename = os.path.join(main_dir,
                               "evaluation_cascade_k" + str(k) + month +".json")
with open(result_filename,"w") as f:
	json.dump(results, f, indent=True)

print("tau", tau)
print("spr", spr)
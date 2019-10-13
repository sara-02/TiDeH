import json
import os
import subprocess
import sys


main_dir = os.path.join("data", "reddit_data")
input_dir = os.path.join(main_dir,"NOV_INPUT")
sub_reddit_list = ["1"]
print("###################################")
print("####################################")
print(sub_reddit_list)
print("\n\n")

str_name = ''
error_list = []

try:
    for sub_red in sub_reddit_list:
        print("######################################")
        print("######################################")
        print(sub_red)
        sys.stdout.flush()
        str_name += sub_red +"_"
        for _, _, f in os.walk(
                os.path.join(input_dir, sub_red)):
            file_list = f
        file_list = [f.split(".txt")[0] for f in file_list]
        for each_post in file_list:
            print(each_post)
            sys.stdout.flush()
            cmd = "python3 for_each_hour.py --srd {0} --fl {1}".format(
                sub_red, each_post)
            returned = subprocess.call(cmd, shell=True)
            if returned:
                error_list.append((sub_red, each_post))

except Exception:
    pass

finally:
    err_filename = os.path.join(main_dir, str_name + "error_list_hour.json")
    with open(err_filename, "w") as f:
        json.dump(error_list, f, indent=True)

import json
import os
import subprocess

# main_sub_reddit_list = ['8', '24', '27', '20', '33', '35', '22', '26', '36', '10', '34', '23', '28', '21', '9', '15', '30', '16', '19', '17', '31', '6', '29', '7', '32', '18', '37', '25']
sub_reddit_list = ['6']

main_dir = os.path.join("data", "reddit_data")

str_name = ''
error_list = []

try:
    for sub_red in sub_reddit_list:
        print(sub_red)
        str_name = sub_red +"_"
        for _, _, f in os.walk(
                os.path.join("data", "reddit_data", "OCT_INPUT", sub_red)):
            file_list = f
        file_list = [f.split(".txt")[0] for f in file_list]
        for each_post in file_list:
            print(each_post)
            cmd = "python3 example_optimized.py --srd {0} --fl {1}".format(
                sub_red, each_post)
            returned = subprocess.call(cmd, shell=True)
            if returned:
                error_list.append((sub_red, each_post))

except Exception:
    pass

finally:
    err_filename = os.path.join(main_dir, str_name + "error_list.json")
    with open(err_filename, "w") as f:
        json.dump(error_list, f, indent=True)
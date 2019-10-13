import os

main_dir = os.path.join("data", "reddit_data")
input_dir = os.path.join(main_dir, "NOV_INPUT")
os.mkdir(os.path.join(main_dir, "NOV_OUTPUT_HOUR"))
output_dir = os.path.join(main_dir, "NOV_OUTPUT_HOUR")
folders = []

for r, _, _ in os.walk(input_dir):
    folders.append(r)
folders = folders[1:]
for each_sub in folders:
    sub_folder_name = each_sub.split("/")[-1]
    print(sub_folder_name)
    os.mkdir(os.path.join(output_dir, sub_folder_name))
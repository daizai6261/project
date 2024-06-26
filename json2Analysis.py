import pandas as pd
import os
import csv
import re
import logging
import json
def process_from_excel(excelpath):
    root_df = pd.read_excel(excelpath)
    all_data = json.load(open("C:\\Users\\40198\\Desktop\\danyuan_data_0111_complete.json",'r', encoding='utf-8'))
    path2data = {}
    for data in all_data:
        if data['单元内容'] is None:
            continue
        if data['教材路径'] not in path2data:
            path2data[data['教材路径']] = [data]
        else:
            path2data[data['教材路径']].append(data)
    for id, row in root_df.iterrows():
        if str(root_df.loc[id, "存储路径"]) == "" or "nan" in str(root_df.loc[id, "存储路径"]):
            continue
        book_path = os.path.join(root_df.loc[id, "存储路径"], "book" + str(root_df.loc[id, "书本编号"]))
        # print(book_path)
        if book_path not in path2data:
            continue
        print('#'*100)
        print(book_path)

        for i in range(3):
            logging.debug("***********************************************************")
        logging.info(">> " + book_path)

        build_Analysis_in_book_path(path2data[book_path], book_path, str(root_df.loc[id, "书本编号"]))
import re
pattern_digits_dot = r"\d+\."

def build_Analysis_in_book_path(data_list, book_path, book_num):
    if not os.path.exists(book_path):
        return
    config_path = os.path.join(book_path, "osd_configs")
    if not os.path.exists(config_path):
        return
    # if os.path.exists(os.path.join(config_path, f'Analys_{book_num}.txt')):
    #     return
    units_data = [
            {
                "unit_name": data['单元名'],
                "analysis": data['单元导学'],
                "points": re.sub(pattern_digits_dot, '', data['要点提示'].replace('|','').replace('\n','|'))
            } for data in data_list
        ]
    formatted_text = create_formatted_text(units_data)
    # os.remove(os.path.join(config_path, f'Analys_{book_num}.txt'))
    print(os.path.join(config_path, f'Analys_{book_num}.txt'), file=open('Analys_file_path_list.txt','a', encoding='utf-8'))
    save_to_file(formatted_text, os.path.join(config_path, f'Analys_{book_num}.txt'))

# Define the data for the units


def create_formatted_text(units):
    # Define the header
    header = "单元\t解析\t要点\nUnitName\tAnalys\tPoint\n"


    # Initialize an empty string to hold all the formatted text
    formatted_text = header

    # Loop through each unit and format the information
    for unit in units:
        formatted_text += f"{unit['unit_name']}\t{unit['analysis']}\t{unit['points']}\n"

    return formatted_text


def save_to_file(text, filename):
    # Save the formatted text to a file
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)


# Create the formatted text
# formatted_text = create_formatted_text(units_data)

# Specify the filename you want to save to
filename = "formatted_units.txt"

# Save the formatted text to a file
# save_to_file(formatted_text, filename)
print(f"Formatted text has been saved to {filename}")
if __name__ == '__main__':
    if os.path.exists('Analys_file_path_list.txt'):
        os.remove('Analys_file_path_list.txt')
    process_from_excel(
        excelpath="C:\\Users\\40198\\Desktop\\书本编号路径.xlsx",
    )

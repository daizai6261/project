import pandas as pd
import os
import sys
sys.path.append('D:\Workship\Pelbs\Gen\project\2阶段脚本')
import config

root_df = pd.read_excel(config.book_id_path)

print(root_df)

for id, row in root_df.iterrows():
    book_num = root_df.loc[id, "书本编号"]
    book_name = root_df.loc[id, "书本名称"]
    book_path = os.path.join(root_df.loc[id, "存储路径"], f"book{book_num}")

    explain_path = os.path.join(book_path, "osd_configs", f"Explain_{book_num}_0.txt")

    explain_df = pd.read_csv(explain_path, sep="\t")

    for e_id, e_row in explain_df.iterrows():
        # 音乐标示	原文	讲解内容	级别
        original_text = e_row["原文"]
        explain_content = e_row["讲解内容"]
        if explain_content == "none":
            print(e_row)



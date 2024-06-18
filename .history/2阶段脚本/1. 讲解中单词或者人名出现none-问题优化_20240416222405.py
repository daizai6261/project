import pandas as pd
import os
import sys
sys.path.append('D:\Workship\Pelbs\Gen\project\2阶段脚本')
import config

root_df = pd.read_excel(config.book_id_path)

print(root_df)

for id, row in root_df.iterrows():
    book_name = root_df.loc[id, "书本名称"]
    book_path = os.path.join(root_df.loc[id, "存储路径"], "book"+str(root_df.loc[id, "书本编号"]))

    explain_path = os.path.join(book_path, "osd_configs", f"Explain_16_0.txt")



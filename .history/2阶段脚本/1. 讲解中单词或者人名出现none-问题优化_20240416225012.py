import pandas as pd
import os, re, json
import sys
sys.path.append('D:\Workship\Pelbs\Gen\project\2阶段脚本')
import config
import llm_api

root_df = pd.read_excel(config.book_id_path)

print(root_df)

for id, row in root_df.iterrows():
    book_num = root_df.loc[id, "书本编号"]
    book_name = root_df.loc[id, "书本名称"]
    book_path = os.path.join(root_df.loc[id, "存储路径"], f"book{book_num}")

    explain_path = os.path.join(book_path, "osd_configs", f"Explain_{book_num}_0.txt")
    print(">>", explain_path)
    try:
        explain_df = pd.read_csv(explain_path, sep="\t")
    except:
        print(f"Error: {explain_path} 不存在")
        continue
    if "105" in explain_path:
        for e_id, e_row in explain_df.iterrows():
            # 音乐标示	原文	讲解内容	级别
            # print(">> >>", e_row)
            original_text = e_row["原文"]
            explain_content = e_row["讲解内容"]
            if pd.isna(explain_content):
                with open("./prompts/1. 讲解内容翻译.txt", "r", encoding="utf-8") as f:
                    template = f.read()
                response = llm_api.chat(
                    prompt=template.replace("<<原文>>", original_text),
                    model="gpt-3.5-turbo",
                )
                keyword_json_str = re.findall(r"([\{}][\s\S]*[\}])", response)[0]

                


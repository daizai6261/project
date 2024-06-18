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

    for e_id, e_row in explain_df.iterrows():
        # 音乐标示	原文	讲解内容	级别
        # print(">> >>", e_row)
        original_text = e_row["原文"]
        # 上下文拼接
        context_text = ""
        for i in range(10):
            try:
                if i == 5:
                    context_text = context_text +"\n"+ "【" + explain_df.loc[e_id, "原文"] + "】"
                context_text = context_text +"\n"+ explain_df.loc[e_id + 5 - i, "原文"]
            except:
                continue
        print(">> >> context_text: ", context_text)
        explain_content = e_row["讲解内容"]
        if pd.isna(explain_content):
            with open("./prompts/1. 讲解内容翻译.txt", "r", encoding="utf-8") as f:
                template = f.read()
            try:
                response = llm_api.chat(
                    prompt=template.replace("<<原文>>", original_text),
                    model="gpt-4",
                )
                json_str = re.findall(r"([\{}][\s\S]*[\}])", response)[0]
                json_dict = json.loads(json_str)
                print(json_dict)
                explain_df.loc[e_id, "讲解内容"] = json_dict["讲解内容"]
            except Exception as e:
                print(">> >> Error: ", e)
                continue
                


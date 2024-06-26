import pandas as pd
import numpy as np
import os
import csv
import re
import logging
# 打印日志
logging.basicConfig(
    # level  = logging.DEBUG, # 打印所有中间信息
    level  = logging.INFO, # 只打印基本信息
    format = "%(levelname)s: %(message)s"
)

# 读取 书本编号路径.xlsx 中所有的课本路径，并将每一个课本中的所有相关文件信息读取到一个总表中
# total_df:  (xxx, 13)
# 教材编号                                                      0
# 教材路径               D:\Workship\Pelbs\Books\教材\小学英语\译林\book0
# 教材版本                                                     译林
# 教材名                                                    None
# 年级                                                     None
# 单元名                                                   unit1
# 单元标题                                            I'm Liu Tao
# 单元内容      Unit\nI'm Liu Tao\nStorytime\nHello.I'm Liu Ta...
# 单元内容翻译    翻译文本\n翻译文本\n翻译文本\n翻译文本\n翻译文本\n翻译文本\n翻译文本\n翻译文本...
# 单元导学                                                   None
# 要点提示                                                   None
# 词汇表       hello.,i'm,hi.,good morning!,good afternoon!,g...
# 词汇表翻译                    你好。,=i am 我是,你好。,早上好！,下午好！,晚上好！,汪！
# total_df 的存储位置是在 D:\\Workship\\Pelbs\\Gen\\data\\ 目录下的 单元总表.xlsx
def process_from_excel(excelpath, savepath):
    root_df = pd.read_excel(excelpath)
    total_df = construct_base_excel()
    for id, row in root_df.iterrows():
        if str(root_df.loc[id, "存储路径"]) == "" or "nan" in str(root_df.loc[id, "存储路径"]):
            continue
        book_path = os.path.join(root_df.loc[id, "存储路径"], "book"+str(root_df.loc[id, "书本编号"]))
        book_name = root_df.loc[id, "书本名称"]
        for i in range(3):
            logging.debug("***********************************************************")
        logging.info(">> " + book_path)
        
        book_df = construct_excel_from_book_path(book_path, book_name)

        logging.debug(">> book_df: "+str(book_df.shape))
        logging.debug(book_df.iloc[0] if book_df.shape[0] > 0 else None)
        total_df = pd.concat([total_df, book_df], ignore_index=True)
            
    
    logging.info(total_df.iloc[0] if book_df.shape[0] > 0 else None)
    logging.info(">> total_df: "+str(total_df.shape))

    total_df.to_excel(savepath, index=False)

# 自动读取某个教材目录中的所有相关文件信息读取到一个总表中
# 这个 total_df 与上面的 total_df 不同，这个是从教材目录中自动读取的，上面的是从 excel 中读取的
# total_df 的存储位置是在 C:\\Users\\40198\\Desktop\\课文资源和编号训练数据\\ 目录下的 单元总表.xlsx
def auto_process(root_search_path, savepath):
    root_search = root_search_path
    # version_list = [filename for filename in os.listdir(root_search) if os.path.isdir(os.path.join(root_search,filename))]
    # logging.debug(version_list)

    total_df = construct_base_excel()
    version_list = []
    for root, dirs, files in os.walk(root_search):
        for dir_name in dirs:
            # Checking if "book" is in the folder name
            if "book" in dir_name.lower():
                # Adding the full path of the folder to the list
                version_list.append(root)

    for version in version_list:
        # version_search = os.path.join(root_search, version)
        book_list = [filename for filename in os.listdir(version) if os.path.isdir(os.path.join(version,filename))]
        # logging.debug(book_list)

        

        for book in book_list:
            book_path = os.path.join(version, book)
            print(version, book)
            for i in range(3):
                logging.debug("***********************************************************")
            logging.info(">> " + book_path)
            print(book)
            
            book_df = construct_excel_from_book_path(book_path, book)
            if book_df is None: continue
            logging.debug(">> book_df: "+str(book_df.shape))
            logging.debug(book_df.iloc[0])
            
            total_df = pd.concat([total_df, book_df], ignore_index=True)
            
    
    logging.info(">> total_df: "+str(total_df.shape))
    logging.debug(total_df.head())

    total_df.to_excel(savepath, index=False)

# 构造一个空的具有表头的 df
def construct_base_excel():
    df = pd.DataFrame(columns=['教材编号', '教材路径', '教材版本', '教材名', '年级', '单元名', '单元标题', '单元内容',  '单元内容翻译', '单元导学', '要点提示', '词汇表', '词汇表翻译'])
    return df

# 对每一本书进行处理，返回一个 df
def construct_excel_from_book_path(book_path, book_name=None):
    df = construct_base_excel()
    if not os.path.exists(book_path):
        return df
    unit_cache = {}
    config_path = os.path.join(book_path, "osd_configs")
    if not os.path.exists(config_path):
        return df
    config_files = os.listdir(config_path)
    for config_file in config_files:
        config_file_path = os.path.join(config_path, config_file)
        logging.debug("---------------------------")
        logging.debug(config_file_path)
        if ".meta" in config_file_path:
            continue
        if "AllAudio" in config_file_path:
            try:
                AllAudio_df = pd.read_csv(config_file_path, sep='\t', skiprows=1, engine='python', quoting=csv.QUOTE_NONE, encoding='utf-8')
            except:
                print(">> error: ", config_file_path)
                continue
            logging.debug(AllAudio_df.head())
            for id, row in AllAudio_df.iterrows():
                try:
                    key = str(row["SoundName"]).split("_")[0]

                    if key not in unit_cache:
                        unit_cache[key] = {
                        "单元内容": str(row["Content"]),
                        "单元内容翻译": str(row["Chinese"]),
                    }
                    else:
                        unit_cache[key]["单元内容"] += "\n" + str(row["Content"])
                        unit_cache[key]["单元内容翻译"] += "\n" + str(row["Chinese"])
                except:
                    pass

        elif "Analys" in config_file_path:
            Analys_df = pd.read_csv(config_file_path, sep='\t', skiprows=1, engine='python', quoting=csv.QUOTE_NONE, encoding='utf-8')
            logging.debug(Analys_df.head())
            for id, row in Analys_df.iterrows():
                key = row["UnitName"].split("_")[0]
                if key not in unit_cache:
                    unit_cache[key] = {
                        "单元导学": str(row["Analys"]) if "Analys" in row else None,
                        "要点提示": str(row["Point"]) if "Point" in row else None,
                    }
                else:
                    unit_cache[key]["单元导学"] = str(row["Analys"]) if "Analys" in row else None
                    unit_cache[key]["要点提示"] = str(row["Point"]) if "Point" in row else None
        elif "BookUnit" in config_file_path:
            BookUnit_df = pd.read_csv(config_file_path, sep='\t', skiprows=1, engine='python', quoting=csv.QUOTE_NONE, encoding='utf-8')
            logging.debug(BookUnit_df.head())
            for id, row in BookUnit_df.iterrows():
                key = str(row["UnitName"])
                if key not in unit_cache:
                    unit_cache[key] = {
                        "单元标题": str(row["Title"]),
                    }
                else:
                    unit_cache[key]["单元标题"] = str(row["Title"])
        elif "EnglishFollowup" in config_file_path:
            EnglishFollowup_df = pd.read_csv(config_file_path, sep='\t', skiprows=1, engine='python', quoting=csv.QUOTE_NONE, encoding='utf-8')
            logging.debug(EnglishFollowup_df.head())
            for id, row in EnglishFollowup_df.iterrows():
                key = str(row["SoundName"]).split("_")[0]
                if key not in unit_cache:
                    unit_cache[key] = {
                        "词汇表": str(row["Content"]),
                        "词汇表翻译": str(row["Chinese"]),
                    }
                else:
                    if "词汇表" not in unit_cache[key]:
                        unit_cache[key]["词汇表"] = str(row["Content"])
                        unit_cache[key]["词汇表翻译"] = str(row["Chinese"])
                    else:
                        unit_cache[key]["词汇表"] += "," + str(row["Content"])
                        unit_cache[key]["词汇表翻译"] += "," + str(row["Chinese"])
    match = re.compile(r".年级.册")
    for unit_key in unit_cache:
        df = pd.concat([df, pd.DataFrame({
            '教材编号': book_path.split("book")[-1], 
            '教材路径': book_path, 
            '教材版本': book_path.split("\\")[-2], 
            '教材名': book_name, 
            '年级': match.findall(book_name)[0] if match.findall(book_name) else None, 
            '单元名': unit_key, 
            '单元标题': unit_cache[unit_key].get("单元标题", None),
            '单元内容': unit_cache[unit_key].get("单元内容", None),
            '单元内容翻译': unit_cache[unit_key].get("单元内容翻译", None),
            '单元导学': unit_cache[unit_key].get("单元导学", None),
            '要点提示': unit_cache[unit_key].get("要点提示", None),
            '词汇表': unit_cache[unit_key].get("词汇表", None),
            '词汇表翻译': unit_cache[unit_key].get("词汇表翻译", None)
        }, index=[0])], ignore_index=True)
    return df

if __name__ == '__main__':
    # 自动读取某个教材目录中的所有相关文件信息读取到一个总表中，该目录下有多个教材版本，每个版本文件夹下有多个教材
    # auto_process(
    #     root_search_path="C:\\Users\\40198\\Desktop\\课文资源和编号训练数据\\教材",
    #     savepath="C:\\Users\\40198\\Desktop\\课文资源和编号训练数据\\单元总表.xlsx"
    # )
    
    # 读取 书本编号路径.xlsx 中所有的课本路径，并将每一个课本中的所有相关文件信息读取到一个总表中
    process_from_excel(
        excelpath="C:\\Users\\40198\\Desktop\\书本编号路径.xlsx",
        savepath="C:\\Users\\40198\\Desktop\\单元总表.xlsx"
    )
    # auto_process("C:\\Users\\40198\\Desktop\\book", 'C:\\Users\\40198\\Desktop\\单元总表.xlsx')
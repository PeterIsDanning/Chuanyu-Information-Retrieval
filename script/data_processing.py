import pandas as pd
from typing import List, Tuple

def update_csv_data(file_path: str, new_df: pd.DataFrame, check_column: str = "question") -> None:
    """
    更新 CSV 文件中的数据。

    该函数读取指定的 CSV 文件，检查 `check_column` 列中是否存在新数据，如果不存在则将新数据添加到文件中。

    参数:
        file_path (str): CSV 文件的路径。
        new_df (pd.DataFrame): 包含新数据的 pandas DataFrame。
        check_column (str, optional): 用于检查重复数据的列名，默认为 "question"。

    返回:
        None。该函数直接修改并保存 CSV 文件。
    """

    # 读取 CSV 文件
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"错误: 文件 '{file_path}' 不存在。")
        return

    # 检查并添加新数据
    for _, row in new_df.iterrows():
        if row[check_column] not in df[check_column].values:  # 使用 .values 提高效率
            df.loc[len(df)] = row  # 添加新行

    # 保存到 CSV 文件
    try:
        df.to_csv(file_path, index=False)
        print(f"数据已成功保存到 '{file_path}'")
    except PermissionError:
        print(f"错误: 无法写入文件 '{file_path}'，请检查权限。")


def easymoney_df_generator(
    name_list: List[str], 
    code_list: List[int], 
    title_list: List[str], 
    web_list: List[str], 
    info_list: List[List[str]], 
    abstract_list: List[str]
) -> pd.DataFrame:
    """
    将新闻数据整理成 pandas DataFrame。

    这个函数接收新闻的各个属性列表（公司名称、代码、标题、链接、详细信息、摘要），将它们组合成一个 DataFrame，并对股票代码进行格式化。

    参数:
        name_list: 公司名称列表。
        code_list: 公司代码列表（整数）。
        title_list: 新闻标题列表。
        web_list: 新闻链接列表。
        info_list: 新闻详细信息列表（每个新闻的详细信息为一个列表）。
        abstract_list: 新闻摘要列表。

    返回:
        一个包含新闻信息的 pandas DataFrame，列名为 "name", "code", "title", "web", "item_list" 和 "abstract"。其中，"code" 列的值会被格式化为6位数的字符串。
    """

    df = pd.DataFrame({
        "name": name_list,
        "code": code_list,
        "title": title_list,
        "web": web_list,
        "item_list": info_list,
        "abstract": abstract_list
    })

    # 格式化股票代码为6位数字符串
    df["code"] = df["code"].apply(lambda x: f'{x:06d}') 

    return df
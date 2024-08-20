import pandas as pd
from urllib.parse import urljoin

def sichuan_merge(folder_path, file_name):
    table_1 = pd.read_csv(urljoin(folder_path, "sichuan_1.csv")).iloc[:, [1, 2, 4]]
    table_2 = pd.read_csv(urljoin(folder_path, "sichuan_2.csv")).iloc[:, [1, 2, 4]]
    table_3 = pd.read_csv(urljoin(folder_path, "sichuan_3.csv")).iloc[:, [1, 2, 4]]
    table_4 = pd.read_csv(urljoin(folder_path, "sichuan_4.csv")).iloc[:, [1, 2, 4]]

    table_1.columns = ['website', 'code', 'name']
    table_2.columns = ['website', 'code', 'name']
    table_3.columns = ['website', 'code', 'name']
    table_4.columns = ['website', 'code', 'name']

    table = pd.concat([table_1, table_2, table_3, table_4], ignore_index=True)
    table['code'] = table['code'].apply(lambda x: f'{x:06d}')

    table.to_csv(urljoin(folder_path, file_name), index=False)
    print("数据组合成功")

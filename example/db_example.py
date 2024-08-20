import psycopg2
import csv

# 连接PostgreSQL数据库
conn = psycopg2.connect(
    database="postgres",  
    user="postgres",        
    password="Postgres",  
    host="localhost",      
    port="5432"            
)
print(conn)

# 创建游标对象
cur = conn.cursor()

# 定义建表 SQL 语句
create_table_query = """
CREATE TABLE IF NOT EXISTS 四川上市公司 (
    网址 VARCHAR(255) PRIMARY KEY,
    公司代码 VARCHAR(20),
    公司名称 VARCHAR(255)
);
"""
# 执行建表语句
cur.execute(create_table_query)

# 打开 CSV 文件
with open('data/sichuan.csv', 'r', encoding='utf-8') as f:
    # 创建 CSV 读取器
    reader = csv.reader(f)
    
    # 跳过表头行（如果存在）
    next(reader, None)  

    # 逐行读取数据并插入到数据库
    for row in reader:
        # 构造 SQL 插入语句，注意防止 SQL 注入
        insert_query = """
        INSERT INTO 四川上市公司 (网址, 公司代码, 公司名称)
        VALUES (%s, %s, %s)
        ON CONFLICT (网址) DO NOTHING;  -- 避免重复插入
        """
        cur.execute(insert_query, row)

# 提交事务
conn.commit()

# 执行查询语句
cur.execute("SELECT * FROM 四川上市公司")
# 获取查询结果
rows = cur.fetchall()
# 打印表头和数据
for row in rows:
    print(row)

# 关闭游标和数据库连接
cur.close()
conn.close()
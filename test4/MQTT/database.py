import pymysql


# 创建数据库连接
connection = pymysql.connect(host='stevenhou.xyz',
                             port=3306,
                             user='student00',
                             password='STUDENT00',
                             database='student00')
# 数据库操作器
cursor = connection.cursor()


# 插入数据，写操作需要commit
sql = ''' INSERT INTO stress_data 
      (time, value)
      VALUES
      ('2023-05-01 00:00:00', 1.0),
      ('2023-05-01 00:01:00', 2.0) '''
cursor.execute(sql)
connection.commit()


# 查询数据
sql = 'SELECT time, value FROM stress_data'
cursor.execute(sql)
# 获取并打印查询结果
rows = cursor.fetchall()
for row in rows:
    print(row)
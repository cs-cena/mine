sql执行顺序
(1) from 
(2) on
(3) join  
(4) where 
(5) group by(开始使用select中的别名，后面的语句中都可以使用)
(6) 聚合 avg, sum, count
(7) having 
(8) select 
(9) distinct 
(10) order by 
(11) top


/*
sql时间函数：

时间戳转日期 from_unixtime(61) = '1970-01-01 00:01:01'
日期转时间戳 unix_timestamp('1970-01-01 00:01:01') = 61
时间转日期/年/月/日/小时/分钟/秒 to_date/year/month/day/hour/minute/second
转为具体年月日 to_date('2018-01-01 00:00:00') = '2018-01-01' 
转周 weekofyear
日期比较 datediff('2018-01-03','2018-01-01')  = 2
日期增加/减少 date_add/date_sub(日期,天数)

指定格式时，注意区分大小写
日期转时间戳 unix_timestamp('2018-01-01 00:00:00','yyyy-MM-dd HH:mm:ss')
*/


--sqlit数据类型： NULL, INTEGER, REAL, TEXT, BLOB

--sqlite建表--
CREATE TABLE diary (
    fDate TEXT,
    fPay REAL,
    dText TEXT
);


--sqlite批量插入数据--

insert into Student values
('01' , '赵雷' , '1990-01-01' , '男'),
('02' , '钱电' , '1990-12-21' , '男'),
('03' , '孙风' , '1990-05-20' , '男'),
('04' , '李云' , '1990-08-06' , '男');


--csv导入sqlite--

file_path = r'数据库地址'

conn = sq.connect(file_path)
cur = conn.cursor()

df = pd.read_csv(r'C:\Users\***\Desktop\kanong_users\kanong_users_extend_2019-07-08.csv')

columns = [
    'response', 'topic', 
    'nickname', 'user_group', 
    'register_time', 'last_login_time',
    'lacst_active_time', 'friend',
    'point', 'achieve', 'dollar',
    'flower_coin', 'uid'
]

df.columns = columns

df.to_sql('表名', conn, if_exists='append', index=False)


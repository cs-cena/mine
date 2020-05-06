sql执行顺序
(1) from 
(2) on
(3) join  
(4) where（过滤行）
(5) group by（除聚合语句外，select语句中的每一列都必须在group by子句中给出）
(6) 聚合 avg, sum, count 
(7) having（过滤分组，对分组聚合的值筛选）
(8) select
(9) distinct 
(10) order by 
(11) top/limit

where 与 having 区别：
where 在连表后分组前过滤行，having 在分组后过滤分组。因此 where 先排除的行，不包括在后续分组中。

left join ...on
不管on中的条件如何写，left join 首先要得到左边的所有的行
对于右边的表，如果满足连接条件，则输出值，如果不满足条件，则返回null
也就是说，on中的过滤条件是作为左外连接的连接条件，而不是过滤条件。

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


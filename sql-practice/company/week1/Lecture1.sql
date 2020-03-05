二、1~5  
加法 +
减法 -
乘法 *
除法 /  
取余 %   例子: 3%2  >>> 1

四、1~6
取整 round(源数据，精度)  		round(3.14159,3) >>> 3.142
向下取整 floor 					floor(3.14159)   >>> 3
向上取整 ceil/ceiling			ceil(3.14159)    >>> 4
取0-1中的随机数 rand() 
-----------------------------------------------------------------------------------------
以上函数只能用于数值类型
-----------------------------------------------------------------------------------------

一、1~9
等值/不等值 = / <>
小于/小于等于/大于/大于等于 </<=/>/>=
空值 is null
非空 is not null
比较 like
-----------------------------------------------------------------------------------------
'= 和 like 的区别'
 = 可以用于比较所有基本类型（int数字型、string字符型等），like 只能比较 string
 = 只能用于精确匹配，like 可以模糊匹配

 通配字符 % 任意长度的任意字符
 		      _ 一个字符长度的任意字符
 		      一个中文字符长度是3

- 只有 int数字型 和 日期 可以比较大小，日期越大越接近未来
- string字符型具体内容 和 日期 时要打引号： 'Hello'  '2018-01-01' 
-----------------------------------------------------------------------------------------

三、1~3
逻辑 and/or/not
-----------------------------------------------------------------------------------------
逻辑顺序：not > and > or
可以通过()来改变优先级
1=0 and 1=2 or 1=1  >>> True
1=0 and (1=2 or 1=1)  >>> False
-----------------------------------------------------------------------------------------
练习：
1. 发标时间（cre_dt）在2017年

cre_dt >= '2017-01-01' and cre_dt < '2018-01-01' 【不写时分秒会默认是00:00:00】
year(cre_dt) = '2017'
cre_dt between ('2017-01-01','2018-01-01') 【用between两边都是大于等于/小于等于条件，会多出来一秒】


2. 短信内容（content）同时满足 （1）非空 （2）含关键字‘哈哈哈’ 或 短信内容为‘嘿嘿嘿’

content is not null and (content like '%hahaha%' or content = 'heiheihei')

-----------------------------------------------------------------------------------------

五、1~15
时间戳转日期 from_unixtime(61) = '1970-01-01 00:01:01'
日期转时间戳 unix_timestamp('1970-01-01','yyyy-MM-dd') = 61
时间转日期/年/月/日/小时/分钟/秒 to_date/year/month/day/hour/minute/second
to_date('2018-01-01 00:00:00') = '2018-01-01' 
转周 weekofyear
日期比较 datediff('2018-01-03','2018-01-01')  = 2
日期增加/减少 date_add/date_sub(riqi,tianshu)
-----------------------------------------------------------------------------------------
'时间戳含义'
距离 '1970-01-01 00:00:00'的秒数

日期转时间戳 unix_timestamp('2018-01-01 00:00:00','yyyy-MM-dd HH:mm:ss')
指定格式时，注意区分大小写
-----------------------------------------------------------------------------------------
练习：
1. 发标时间（cre_dt）与注册时间（reg_date）是同一天

datediff(cre_dt,reg_dt) = 0
(unix_timestamp(cre_dt)-unix_timestamp(reg_dt))/3600 < 24  -- 实际含义是24小时内，与同一天的含义有细微差别
to_date(cre_dt) = to_date(reg_dt)

2. 计算发标时间（cre_dt）与修改工作（creationdate）时间差
（1）时间差用小时表示

floor((unix_timestamp(cre_dt)-unix_timestamp(creationdate))/60/60/24)
【返回的数值可能是小数，如果需要整数答案的话需要用函数自行取整】

（2）时间差用天数表示

datediff(cre_dt,creatindate)
【返回的天数差是一个整数】

-----------------------------------------------------------------------------------------

六、1~4
非空查找函数 coalesce(null,null,null,1,null) = 1
if函数 if(condition, true, false)   例子: if(to_date(cre_dt) = to_date(creationdate),1,0) 
条件判断函数 case when userid = userid and (lisingid =listingid or name = name) then result_1 
				when condition 2 then blablabla 
				else result_2 end as hahaha
    例子：是否发标当天xiu gai gong zuo
        case when to_date(cre_dt) = to_date(creationdate) then 1 else 0 end as sfdtxggz
		
		case when xueli = 'dazhuang' then 1 when xueli = 'gaozhong' then 2 else 3 end as num
		xueli | num
	gaozhong  |  2
	dazhuan   |  1

七、1~13、16~21
空格字符串函数 space(2) = '  '  
重复字符串 repeat('ha'，3)  = 'hahaha'  
首字符ascii函数 ascii(a) = 97
左/右补足 lpad/rpad(字符，长度，补足字符)   = ('haha',6,'1') = '11haha'
分割字符 split(源字符，分割识别符) = ('haha','h') = ('a','a')
反转 reverse 
去左/右/两边空格 ltrim/rtrim/trim   trim(' 8008208820 ') >>> '8008208820'

长度 length('abc') = 3
连接 concat ('a','b') ='ab'  concat(firstname,space(2),lastname) = 'yahua  zhuo'
带分隔符连接concat_ws(-，字符)
字符截取substr/substring(字符，起始位置，长度）  substr('abc',2,2) = 'bc'
转大/小写  upper/ucase | lower/lcase upper('Apple') = 'APPLE'

正则替换/解析 暂时不讲
-----------------------------------------------------------------------------------------
练习：
1. 根据身份证号码（idnumber）提取出生年月日 【区分15位和18位】
case when, substr, concat, length

case when length(idnumber) = 18
then substr(idnumber,7,8)
else concat('19',substr(idnumber,7,6))
end as birthday



-----------------------------------------------------------------------------------------
impala基本格式：

drop table if exists 库名.表名1
create table 库名.表名1 as
select 字段1, 字段2
from 库名.表名2
[where 条件]
[order by]



-----------------------------------------------------------------------------------------
练习：
1. 拿出发标时间（cre_dt）在2017年11月至2018年1月之间的客户
  【ods.cmn_listing 所有发标记录表, 有字段：user_id, listing_id, cre_dt】
  
   结果： user_id | listing_id | cre_dt 

create table 库名.表名1 as
select user_id, listing_id,cre_dt
from ods.cmn_listing
where cre_dt >= '2017-11-01' and cre_dt < '2018-01-01'


-----------------------------------------------------------------------------------------
但是需要的数据往往在多个表里，这个时候就要用到表连接（join）
格式:
drop table if exists 库名.表名1
create table 库名.表名1 as
select 字段1, 字段2
from 库名.表名2
xx join 库名.表名3 on 连接条件(主键)
[where 条件]

-----------------------------------------------------------------------------------------
1.left join: 保留左表所有内容，将右表满足连接条件的所需字段连到左表上
2.right join: 保留右表所有内容，将左表满足连接条件的内所需字段连到右表上
3.inner join: 保留两张表均有的内容，并将所需字段连接
4.full join: 笛卡尔积，左表的每一个数据都会和右表的每一个数据匹配一次，数据大时会非常卡

例子：
select a.X, a.Y as Y1, b.Y Y2 
from test.a 
xxx join tast.b 
 on a.X = b.X
 
 表a         表b
X | Y      X | Y
a | 1      c | 4
b | 2      c | 5
c | 3      d | 6

left join 			
X | Y1 | Y2  |
a | 1  | null|		
b | 2  | null|
c | 3  |  4  |
c | 3  |  5  |

right join 
 X  | Y1  | Y2  | b.X 
 c  | 3   |  4  | c
 c  | 3   |  5  | c
null|null |  6  | d

inner join
X | Y1| Y2|
c | 3 | 4 |
c | 3 | 5 |


full join
X1 | X2  | Y1  | Y2 |
a  |  c  |  1  |  4 |
a  |  c  |  1  |  5 |   
a  |  d  |  1  |  6 |      
b  |  c  |  2  |  4 |
b  |  c  |  2  |  5 |
b  |  d  |  2  |  6 |
c  |  c  |  3  |  4 |
c  |  c  |  3  |  5 |
c  |  d  |  3  |  6 |

-----------------------------------------------------------------------------------------
'on条件 和 where条件 的区别'
- on条件：在满足条件时连接，在left/right join 时，即使不满足条件也会保留指定表的数据
- where条件： 一旦不满足条件，该条记录会被删除
例子：
 			表a       			  
 user_id | listing_id  | cre_dt（发标时间）     
  	U1	 |	  L11 	   | 2017-12-02   
  	U1	 | 	  L12      | 2018-01-02 
  	U2	 |	  L21      | 2017-12-31      
  	U3	 |	  L31      | 2018-01-03 

 			表b       			  
 user_id |  creationdate(戳额时间)      
	U1	 | 2018-01-01   
	U1	 | 2018-01-03 
	U2	 | 2017-11-21       
	U3	 | 2018-01-02
(1)
....
left join test.b 
on a.user_id = b.user_id and b.creationdate < a.cre_dt

    			  
 user_id | listing_id  | cre_dt（发标时间）| creationdate(戳额时间)   
  	U1	 |	  L11 	   |  	2017-12-02     |  null                 【不满足条件的行仍会保留】
  	U1	 | 	  L12      |  	2018-01-02     |2018-01-03 
  	U2	 |	  L21      |   	2017-12-31     | 2017-11-21
  	U3	 |	  L31      | 	  2018-01-03     |2018-01-02

(2)
....
left join test.b on a.user_id = b.user_id 
where b.creationdate < a.cre_dt

 user_id | listing_id  | cre_dt（发标时间）| creationdate(戳额时间)   
                                                                    【不满足条件的行会删掉】
	 U1	   | 	  L12      |   	2018-01-02     | 2018-01-03
	 U2	   |	  L21      |  	2017-12-31     | 2017-11-21
	 U3	   |	  L31      | 	  2018-01-03     | 2018-01-02

-----------------------------------------------------------------------------------------
练习：
1. 拿出发标时间（cre_dt）在2017年11月至2018年1月之间的客户
   连接他们的逾期金额（duedate_30_op_pess30） 
  【ods.cmn_listing 所有发标记录表, 有字段：user_id, listing_id, cre_dt】
  【ddm.listing_vintage 所有成交标记录表，有字段:user_id, listing_id, duedate_30_op_pess30 】
   结果： user_id | listing_id | cre_dt | duedate_30_op_pess30

 select a.user_id, a.listing_id,a.cre_dt, b.duedate_30_pess30
 from ods.cmn_listing a
 left join ddm.listing_vintage b on a.listing_id = b.listing_id 
 where cre_dt >= '2017-11-01' and cre_dt < '2018-01-01'


-----------------------------------------------------------------------------------------

八、1~5
聚合函数:
个数统计count
求和sum
平均数avg
最小值/最大值min/max

user_id | month(cre_dt )| sum(duedate_30_op_pess30)
group by 

格式:
drop table if exists 库名.表名1
create table 库名.表名1 as
select 字段1,...,聚合函数
from 库名.表名2
join    on 
[where 条件]
group by
having count(listing_id) >= 2
[order by]

执行顺序：join > where > 聚合函数 > having

-----------------------------------------------------------------------------------------
练习：
1. 拿出发标时间（cre_dt）在2017年11月至2018年1月之间的客户
   计算他们每个月发了几次标，选出发标次数大于1的用户，按月份顺序排序
  【ods.cmn_listing 所有发标记录表, 有字段：user_id, listing_id, cre_dt】
   结果： month | user_id | fbcs(发标次数)
   
create table test.test1 as
 select a.user_id, a.listing_id,a.cre_dt
 from ods.cmn_listing a
 where cre_dt >= '2017-11-01' and cre_dt < '2018-02-01'
 
create table test.test2 as
select substr(cre_dt,1,7) nian_yue, user_id, count(listing_id) fbcs
from test.test1
group by substr(cre_dt,1,7), user_id
having count(listing_id) > 1
 


-----------------------------------------------------------------------------------------
作业：
1. 2017年11月至2018年1月发标用户发表前一个月重置密码次数，筛选其中重置密码次数大于等于2的用户

  【ods.cmn_listing 所有发标记录表, 有字段：user_id, listing_id, cre_dt】
  【ods.useractivity 用户活动记录表，有字段：user_id, act_dt, content】
   (当content中含有关键字'重置密码'时，该条记录为重置密码的记录)
   
   结果： user_id | listing_id | month（发标月份）| 重置密码次数
   
   
   -- 拿出用户

   -- 连接用户修改密码的行为

   -- 计数&筛选


#week1_lecture_1 发标时间（cre_dt）在2017年
year(cre_dt)
cre_dt >= '2017-01-01' and cre_dt < '2018-01-01' 【不写时分秒会默认是00:00:00】
cre_dt between ('2017-01-01', '2018-01-01') 


#week1_lecture_1 短信内容（content）同时满足 （1）非空 （2）含关键字‘哈哈哈’ 或 短信内容为‘嘿嘿嘿’
#逻辑顺序：not > and > or 可以通过()来改变优先级
content IS NOT NULL and (content like '%哈哈哈%' or content = "嘿嘿嘿")


#week1_lecture_1 发标时间（cre_dt）与注册时间（reg_date）是同一天
#to_date('2018-01-01 00:00:00') = '2018-01-01' 
datediff(cre_dt, reg_date) = 0
to_date(cre_dt) = to_date(reg_date)
(unix_timestamp(cre_dt)-unix_timestamp(reg_date)) / 3600 < 24 -- 实际含义是24小时内，与同一天的含义有细微差别


#week1_lecture_1 
#计算发标时间（cre_dt）与修改工作（creationdate）时间差
#（1）时间差用小时表示
(unix_timestamp(cre_dt) - unix_timestamp(creationdate)) / 3600
#（2）时间差用天数表示
datediff(cre_dt, creationdate)


#week1_lecture_1 根据身份证号码（idnumber）提取出生年月日 【区分15位和18位】
case when length(idnumber) = 18 then substring(idnumber,7,8) 
	 else concat("19",substring(idnumber,7,6))
	 end as birthday


#week1_lecture_1 impala基本格式：
drop table if exists test.表名
create table test.表名
select 字段1, 字段2
[where]
[order by]


#week1_lecture_1
#1. 拿出发标时间（cre_dt）在2017年11月至2018年1月之间的客户
#【ods.cmn_listing 所有发标记录表, 有字段：user_id, listing_id, cre_dt】
#结果： user_id | listing_id | cre_dt 
drop table if exists test.aa
create table test.aa
select user_id, listing_id, cre_dt
from ods.cmn_listing
where cre_dt >= '2017-11-01' and cre_dt < '2018-01-01'

#week1_lecture_1 
#拿出发标时间（cre_dt）在2017年11月至2018年1月之间的客户
#计算他们每个月发了几次标，选出发标次数大于1的用户，按月份顺序排序
#【ods.cmn_listing 所有发标记录表, 有字段：user_id, listing_id, cre_dt】
#结果： month | user_id | fbcs(发标次数)

#***易错点***
#执行顺序 where > group by > 聚合函数 > having
#使用聚合函数 必须先group by(分组)
#对聚合函数使用条件，得用having
#group by field1, field2 意味着按 两个字段的组合来分组
#其实作为分组的标准的字段，相当于也去重了
#参考https://www.cnblogs.com/happyWolf666/p/8196147.html
drop table if exists test.bb
create table test.bb
select 
	substr(a.cre_dt,1,7) as month
	,user_id
	,count(listing_id) as fbcs
from ods.cmn_listing
where 
	cre_dt >= '2017-11-01' 
	and cre_dt < '2018-02-01'
	and fbcs > 1 #使用错误！对聚合函数使用条件 需要用having
#漏写 group by。使用聚合函数，必须先有group by
order by month


#更正
select 
	substr(cre_dt,1,7) as month
	,user_id
	,count(listing_id) as fbcs
from ods.cmn_listing
where 
	cre_dt >= '2017-11-01' 
	and cre_dt < '2018-02-01'
#group by user_id #少写month字段，因为某月都有多人多次发标，如果只按user_id分组，相当于对use_id去重，最后结果如下所示。
having fbcs > 1
order by month

2017-12	10001	4
2017-12	10003	4
2018-01	10002	4
2018-01	10004	6
2018-01	10006	9
2018-01	10007	4
2018-01	10008	9
2018-01	10009	4

#最终答案
select 
	substr(cre_dt,1,7) as month
	,user_id
	,count(listing_id) as fbcs
from ods.cmn_listing
where 
	cre_dt >= '2017-11-01' 
	and cre_dt < '2018-02-01'
group by month, userid
having fbcs > 1
order by month

2017-11	10007	2
2017-11	10008	2
2017-12	10001	3
2017-12	10003	3
2017-12	10004	3
2017-12	10006	4
2017-12	10008	5
2018-01	10002	2
2018-01	10004	3
2018-01	10006	4
2018-01	10008	2
2018-01	10009	2

#week1_思考题_1.1
#1. 2017年11月至2018年1月发标用户发表前一个月重置密码次数，筛选其中重置密码次数大于等于2的用户
#【ods.cmn_listing 所有发标记录表, 有字段：user_id, listing_id, cre_dt】
#【ods.useractivity 用户活动记录表，有字段：user_id, act_dt, content】
#(当content中含有关键字'重置密码'时，该条记录为重置密码的记录)
#结果： user_id | listing_id | month（发标月份）| 重置密码次数

/*
sql思路： 1 拿出用户 2 连接用户行为 3 聚合及筛选
在拿用户时以及连表时限制时间
*/


   -- *拿出用户*
   -- 实现cmn_listing 2017年11月至2018年1月发标用户
create table test.test1 as
select a.user_id, a.listing_id, a.cre_dt
from cmn_listing a
where a.cre_dt >= '2017-11-01' and a.cre_dt < '2018-02-01'

   -- *连接用户修改密码的行为*
   -- 实现 连表时用on加条件(保留不符合的，以备之后留下未修改密码的) 发标前一个月(求两个时间的差值) 改密码时间早于发标时间
create table test.test2 as
select a.*, case when b.content like '%重置密码%' then 1 else 0 end num
from test.test1 a
left join test.test2 b
on a.user_id = b.user_id
and datediff(a.cre_dt, b.act_dt) < 30
and a.cre_dt > b.act_dt

   -- *计数&筛选*
   -- 实现 聚合 以及对聚合结果做筛选
create table test.test3 as
select 
	,a.user_id
	,a.listing_id
	,substr(a.cre_dt,1,7) as month
	,sum(num)
from test.test2 a
group by month, listing_id
having num >= 2

#sqlite
select 
	substr(a.cre_dt,1,7) as month
	,a.user_id
	,a.listing_id
	,sum(case when content like "%重置密码%" then 1 else 0 end) num
from cmn_listing a 
left join useractivity b
on a.user_id = b.user_id 
where julianday(a.cre_dt) - julianday(b.act_dt) <= 30 #如果直接用where做筛选，则前一个月内没有改过密码的人就都被排除了
and a.cre_dt > b.act_dt
and a.cre_dt >= '2017-11-01' and a.cre_dt < '2018-02-01'
having num >= 2

#sqlite 更正
select 	
    a.user_id
	,a.listing_id
	,substr(a.cre_dt,1,7) as month
	,sum(case when b.content like '%重置密码%' then 1 else 0 end)num
from cmn_listing a
left join useractivity b
on a.user_id = b.user_id
and julianday(a.cre_dt) - julianday(b.act_dt) <= 30
and a.cre_dt > b.act_dt
where a.cre_dt >= '2017-11-01' and a.cre_dt < '2018-02-01'
group by month, a.user_id, listing_id
having num >= 2

#mysql
select 
	a.substr(cre_dt,1,7) as month
	,a.user_id
	,a.listing_id
	,sum(case when content like "重置密码" then 1 else 0 end) num
from cmn_listing a 
left join useractivity b
on a.user_id = b.user_id
and datediff(a.cre_dt,b.act_dt) <= 30
and a.cre_dt > b.act_dt
where a.cre_dt >= '2017-11-01' and a.cre_dt < '2018-02-01'
group by month, user_id, listing_id
having num >= 2

#week1_思考题_2.1


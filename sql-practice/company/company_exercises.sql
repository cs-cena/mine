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


#week1_思考题_2.1
#sqlite
SELECT 
	a.user_id
	,a.listing_id
	,(CASE WHEN b.principal > 0 THEN 1 ELSE 0 END) AS is_success
	,strftime("%Y-%m", a.cre_dt) AS fb_month
	,c.newvalue
FROM cmn_listing as a 
left join listing_vintage as b 
	on a.listing_id = b.listing_id
left join ppdai_user_log_userupdateinfologs as c
	on a.user_id = c.user_id
	and a.cre_dt > "2017-11-01" and a.cre_dt < "2018-02-01"
	and c.creationdate < a.cre_dt 
	and lower(c.tablefield) like "%qq%"
	and c.newvalue <> c.oldvalue

#mysql
SELECT 
	a.user_id
	,a.listing_id
	,(CASE WHEN b.principal > 0 THEN 1 ELSE 0 END) AS is_success
	,unix_timestamp(a.cre_dt,'yyyy-MM') AS fb_month
	,c.newvalue
FROM cmn_listing as a 
left join listing_vintage as b 
	on a.listing_id = b.listing_id
left join ppdai_user_log_userupdateinfologs as c
	on a.user_id = c.user_id
	and a.cre_dt > unix_timestamp("2017-11-01 00:00:00") 
	and a.cre_dt < unix_timestamp("2018-02-01 00:00:00")
	and c.creationdate < a.cre_dt 
	and lower(c.tablefield) like "%qq%"
	and c.newvalue <> c.oldvalue

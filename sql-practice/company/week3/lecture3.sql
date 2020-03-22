------------------------------------------------------------------------------------------------------------
 作业

mysql 语法, impala里面不适用
1. convert (varchar(10),creationdate,120)
   to_date(creationdate)

    varchar(10)表示的是设置可以存储的最大字符串长度为10个字节

    style数字在转换时间时的含义如下:
    ------------------------------------------------------------------------------------------------------------
    Style(2位表示年份)|  Style(4位表示年份) |   输入输出格式                                    
    ------------------------------------------------------------------------------------------------------------
             0        |  100                |   mon dd yyyy hh:miAM(或PM)              
    ------------------------------------------------------------------------------------------------------------
             1        |  101   美国         |   mm/dd/yy                                       
    ------------------------------------------------------------------------------------------------------------
             2        |  102    ANSI        |   yy-mm-dd                                        
    ------------------------------------------------------------------------------------------------------------
             3        |  103    英法        |   dd/mm/yy                                       
    ------------------------------------------------------------------------------------------------------------
             4        |  104    德国        |   dd.mm.yy                                        
    ------------------------------------------------------------------------------------------------------------
             5        |  105    意大利      |   dd-mm-yy                                        
    ------------------------------------------------------------------------------------------------------------
             6        |  106                |   dd mon yy                                        
    ------------------------------------------------------------------------------------------------------------
             7        |  107                |   mon dd,yy                                        
    ------------------------------------------------------------------------------------------------------------
             8        |  108                |   hh:mm:ss                                         
    ------------------------------------------------------------------------------------------------------------
             9        |  109                |   mon dd yyyy hh:mi:ss:mmmmAM(或PM)
    ------------------------------------------------------------------------------------------------------------
            10        |  110    美国        |   mm-dd-yy                                         
    ------------------------------------------------------------------------------------------------------------
            11        |  111    日本        |   yy/mm/dd                                        
    ------------------------------------------------------------------------------------------------------------
            12        |  112    ISO         |   yymmdd                                           
    ------------------------------------------------------------------------------------------------------------
            13        |  113    欧洲默认值  |   dd mon yyyy hh:mi:ss:mmm(24小时制)  
    ------------------------------------------------------------------------------------------------------------
            14        |  114                |   hh:mi:ss:mmm(24小时制)                    
    ------------------------------------------------------------------------------------------------------------
            20        |  120    ODBC 规范   |    yyyy-mm-dd hh:mi:ss(24小时制)         
    ------------------------------------------------------------------------------------------------------------
            21        |  121                |    yyyy-mm-dd hh:mi:ss:mmm(24小时制) 
    ------------------------------------------------------------------------------------------------------------

2. 使用with(nolock)可以使SQL查询效率增加33%，且查询不受其它排他锁阻塞 

3. select into #表名
   建立临时表
   临时表只在当前连接可见，当关闭连接时，会自动删除表并释放所有空间

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

4. sum 和 count的区别   
   例子：
   userid |  别的什么鬼
   10086  |   'hahaha' 
   10000  |   'hehehe'
   null   |   'blabla'
   95555  |   'xixixi'

   count(userid) >>>> 3
   sum(userid) >>>> 10086+10000+ null +95555 = null  10086+10000 +95555>>>115641

  P.s:使用聚合函数一定不要忘了group by!!!!!

  count(userid) == sum(case when userid is not null then 1 else 0 end)

5. where 条件里因为执行顺序的原因不能对聚合函数进行限制
   执行顺序：join > where > 聚合函数 > having

   having sum(tmm)>= 3


6. 顺序问题：
   先拿出目标客户，再连接他们的相关信息来排序和聚合；
   因为有的表很大，如果将表内所有用户记录拿来排序会非常卡

7. 刚刚重命名的字段不能马上使用新名字
      select substr(creationdate,1,10) as fbnyr .........
      from .................
      where ..................
      group by substr(creationdate,1,10)  

8. row_number()over()是一个字段，应该写在select里面
select 
from(select row_number()over() num
      from 
      where)
  where num = 1

  ==

  create test1
    select row_number()over() num
      from 
      where

      create test2
       select 
   from test1
  where num = 1

9. 成交的状态不止一种

10. datediff(a,b) 是用a的时间减去b的返回天数，a是更接近未来的时间
    例子: select datediff('2018-03-01','2018-01-01')  >>>>59

11. case when xxxx then 聚合函数 end from .... group by ....这样写会报错
    例子：
    CASE WHEN cre_dt >= '2018-04-26' THEN sum(amount) ELSE 0 END
    AnalysisException: select list expression not produced by aggregation output (missing from GROUP BY clause?)

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
建表的区别

drop & create table 删除原表再重新创建

insert overwrite table 覆盖原表，要求新插入数据的数据类型、顺序都与原表一致

insert into table 在原表中插入新内容，要求新插入数据的数据类型、顺序都与原表一致

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

指定信息的提取

1.已知长度、格式
instr(content,指定字符,起始位置) 第一个出现指定字符的位置
substr(内容,起始位置,长度)

例子：
content = '今天我给15013236760发了2333333和15045457870'
（1）提取该短信中的第一个号码
select substr(content, -- 内容
              instr(content,'1') -- 起始位置 
              ,11) -- 长度

（2）提取该短信中的第二个号码

substr(content, -- 内容
        instr(content,    '1',      instr(content,'1')+11),-- 起始位置 
              -- 内容    指定字符       起始位置
        11)-- 长度

练习：
content = '【快捷支付】恭喜您成功支付15.00元，请在【个人中心】-【银行卡】中查看支付详情。【我家门口的银行】'
提取出前2个和最后一个【】中的内容
select substr(content, 
              instr(content, '【')+3，
              instr(content, '】')  -  instr(content, '【') -3) name1

      -- 起始位置:
      -- instr(content, '【')
      -- 长度 = 】位置 - 【位置:
      -- instr(content, '】')  -  instr(content, '【') -3

      ,substr(content,instr(content, '【', instr(content, '】')+3)，instr(content, '】', instr(content, '】')+3) - instr(content, '【', instr(content, '】')+3)-3) name2
      -- 起始位置 
      -- instr(content, '【', instr(content, '】')+3)
      -- 长度 = 】位置 - 第二个【位置
      -- instr(content, '】', instr(content, '】')+3) - instr(content, '【', instr(content, '】')+3)-3

      ,substr(content,起始位置，长度) last_name

      substr(content, 
              instr(content, '【'，-1)+3，
              instr(content, '】'，-1)  -  instr(content, '【'，-1) -3) name1

    如果不好理解的话可以理解像下面这么想：
    1. 第一个【的结束位：instr(content, '【')+3
    2. 第一个】的结束位：instr(content, '】')+3

    3. 第二个【的结束位: instr(content, '【', 第一个】的结束位)  =  instr(content, '【',instr(content, '】')+3)
    4. 第二个】的结束位: instr(content, '】', 第一个】的结束位)  =  instr(content, '】',instr(content, '】')+3)

    5.第一个【】中的长度 = 第一个】的结束位 - 第一个【的结束位 - 3
    6.第二个【】中的长度 = 第二个】的结束位 - 第二个【的结束位 - 3




*2.正则

- 表示字符的规则：
  .   匹配任意一个字符
  []  满足的是一个有限的集合
  [^] 对括号中的东西取反


- 描述数量的规则：
  *    匹配前一个字符出现0次或无限次（即可有可无）    *前面的东西出现多少次
  +    匹配前一个字符出现1次或无限次（即至少有1次）
  ?    匹配前一个字符出现1次或者0次（即0或1次）
  {m}  匹配前一个字符出现m次
  {m.} 匹配前一个字符至少出现m次
  {m,n}匹配前一个字符出现m到n次

- 表示边界的规则：
  ^  匹配字符串开头
  $  匹配字符串结尾

- 匹配分组的规则
  |     匹配左右任意一个
  (ab)  将括号中的字符作为一个分组

  150-2323-6760


- 贪婪模式：尽量匹配多的内容，有时候会使拿出来的东西并不是想要的精确内容
  关闭：在数量修饰符后加上一个？

- regexp_extract(内容,正则表达式,返回第几个括号中的内容)
- regexp_replace(phonenumber, '-', '')


content = '今天我给15013236760发了2333333和15045457870'
- regexp_extract(content, '(^[^0-9]*) ([1][0-9]{10})([^0-9]) (.*$)', 2) -- content中的第一个手机号   another : -- regexp_extract(content, '([^0-9]*) ([1][0-9]{10})([^0-9]) (.*$)', 2
但是这么拿的话，只有content第一次出现的数字就是手机号的时候才行，如果content = '2333333，今天我给15013236760发了15045457870'就不行，如果以手机号开头也不行
regexp_extract(content, '(^|^.*?[^0-9]) ([1][0-9]{10})([^0-9].*$|$)', 2)
可以避免这些问题

 '可疑行为: 该身份证号已经被认证过, 身份证为: ***, 真实姓名为: **, UserAgent 为: PPD-LoanApp/6.1.7 (vivo;vivo X20A;C29B219C72DD771684C165512CBCEC6B;Android/7.1.1'
 regexp_extract (content, '(^[^0-9]+) ([0-9]{18}|[0-9]{15}) (.*$)', 2)


例子：
content = '【快捷支付】恭喜您成功支付15.00元，请在【个人中心】-【银行卡】中查看支付详情。【我家门口的银行】'
提取出前2个和最后一个【】中的内容

select regexp_extract(content,'(^[^【]*)(【)(.*?)(】)(.*$)',3) name1
      ,regexp_extract(content,'(^[^【]*)(【)(.*?)(】)(.*$)',5) content1
.......
select regexp_extract(content1,'(^[^【]*)(【)(.*?)(】)(.*$)',3) name2
      ,regexp_extract(content,'(^.*)(【)(.*?)(】)([^】]*$)',3) last_name

练习：
content = '可疑行为，用已存在身份证，姓名***，身份证****，UserAgent：loan-4.5.0  (vivo;vivo X9;864277036057965;6.0.1;4)'
取出里面的身份证号
regexp_extract(lower('可疑行为，用已存在身份证，姓名***，身份证****，UserAgent：loan-4.5.0  (vivo;vivo X9;864277036057965;6.0.1;4)'),
  '(^[^0-9]*)([^0][0-9]{17}|^[^0][0-9]{14}|^[^0][0-9]{16}x)(.*$)',2)
上课跑不出来的原因是忘记了在前面加select，然后用了一个中文的逗号=。。=

--------------------------------------------------------------------------------------------------------------------

将结构相同的表进行拼接： union all
有时候会将相同类型但是来源不同的时候放在不同的表里，但使用的时候需要结合使用，这时候就需要用到union all

例子：
拿出2017年12月到2018年2月的所有登录成功的用户
2017年登入登出表 ods.tbloginlogby2017
2018年登入登出表 ods.tbloginlogby2018
表中字段: userid, inserttime, result(登录成功，密码错误，账户不存在), ip
select userid, count(inserttime)
from(
select userid,inserttime
from ods.tbloginlogby2017
where inserttime >= '2017-12-01' and result = '登录成功'

union all

select userid,inserttime
from ods.tbloginlogby2018
where inserttime < '2018-03-01' and result = '登录成功'
)a
group by userid
having count(inserttime) > 50

如果想要选出里面登录总登录次数大于50次的用户呢

---------------------------------------------------------------------------------------------------

同IMEI/IMSI/cookie/flash逻辑

假装已有一张存有目标客户的表 test.target_customers
字段：userid, listingid, cre_dt
userid | listingid | cre_dt     | cookie  | userid2
u1     |    l1     | 2018-01-01 | cookie1 | u1
u1     |    l1     | 2018-01-01 | cookie1 | u2

cookie/flash的表：ods.watermark
字段：userid, cookie, flash, inserttime
userid | cookie  | inserttime
u1     | cookie1 | inserttime1
u2     | cookie1 | inserttime2
u2     | cookie2 | inserttime3


imei not ('','0','.','0000-000000-000000000')


-- 选出该用户所有的cookie号
create table test.same_cookie1 stored as parquet as
  select a.*, b.cookie
  from test.target_customers a
  inner join ods.watermark b on a.userid = b.userid
  where b.inserttime < a.cre_dt and b.cookie > 0 

-- 连接上同cookie的用户
create table test.same_cookie0 stored as parquet as
      select a.userid u1, a.listingid, a.cre_dt, a.cookie, b.userid u2
      from test.same_cookie1 a
      inner join ods.watermark b 
      on a.cookie = b.cookie  -- 同cookie
      and a.userid<>b.userid  -- 排除本人
      and b.inserttime < a.cre_dt
      and b.userid > 0

listingid | 123445 | u2 | 2018-01-01 00:00:01
listingid | 123445 | u2 | 2018-01-09 00:00:01

-- 计算同cookie人数
create table test.same_cookie2 stored as parquet as

  select listingid,cookie, count(distinct u2)
  from  test.same_cookie0   
  group by listingid, cookie




IMEI/IMSI的表：ods.mobileinfo
字段：userid, IMEI, IMSI, inserttime

记得排除杂数据~

--------------------------------------------------------------------------------------------------------------------
作业：
1. （1）2017年7-10月的发标用户，最后一次修改的qq
    结果：userid | listingid | cre_dt | last_qq |
   （2）计算发标前历史上曾经同这个qq的人数（排除用户本人）
    结果：userid | listingid | cre_dt | last_qq | u2 |

   发标表：edw.cmn_listing
   字段： userid, listingid, cre_dt
   前台修改记录表：ods.ppdai_user_log_userupdateinfologs 
   字段：userid, creationdate(修改时间),newvalue(新值),oldvalue(旧值),tablefield
   后台修改记录表：ods.ppdai_user_log_user_info_revise_history
   字段：userid, creationdate(修改时间),newvalue(新值),oldvalue(旧值),categoryid=116


2. （1）2017年7-10月的发标用户，发标前7天登入登出中含有可疑行为(description中含有关键字‘可疑行为’)的记录
    结果：userid | listingid | cre_dt | description | 
   （2）提取出所有可疑行为记录中的真实姓名和身份证号
    结果：userid | realname | idnumber

   发标表：edw.cmn_listing
   字段： userid, listingid, cre_dt
   用户活动记录表 ods.user_activity
   字段：userid, description, creationdate
   可疑行为记录样本：
   '可疑行为: 该身份证号已经被认证过, 身份证为: ****, 真实姓名为: **, UserAgent 为: PPD-LoanApp/6.1.7 (vivo;vivo X20A;C29B219C72DD771684C165512CBCEC6B;Android/7.1.1'
substr(description  ,  instr(description,':',instr(description,':'))+2  ,  instr(description,':',instr(description,':',instr(description,':'))+1)-16-(instr(description,':',instr(description,':')+2)   ))       --取身份证

substr(description,  
instr(description,':',instr(description,':')+1)+2,
instr(description,':',instr(description,':',instr(description,':')+1)+1) - 19 - instr(description,':',instr(description,':')+1))



substr(description  ,  instr(description,'名为: ')+8                         ,  instr(description,', UserAgent')- instr(description,'名为: ')+8 )                                                                                  --取名字


instr(description,':',instr(description,':',instr(description,':')+1)-16-(instr(description,':',instr(description,':')+2)   )        )


3. （1）2017年7-10月的发标用户，发标前7天登入登出中含有可疑行为的记录的人是否存在历史同qq中
    结果：u1| listingid | cre_dt | last_qq | u2 | whether_qq
   （2）2017年7-10月的发标用户，出现这种情况的人数
    结果：u1| listingid | cre_dt | renshu |

    身份证用户名对应表 fqz.luanqibazao_ud_temp
    字段: idnumber | userid 


作业答案：
1. （1）2017年7-10月的发标用户，最后一次修改的qq
    结果：userid | listingid | cre_dt | last_qq |
   （2）计算发标前历史上曾经同这个qq的人数（排除用户本人）
    结果：userid | listingid | cre_dt | last_qq | u2 |

   发标表：edw.cmn_listing
   字段： userid, listingid, cre_dt
   前台修改记录表：ods.ppdai_user_log_userupdateinfologs 
   字段：userid, creationdate(修改时间),newvalue(新值),oldvalue(旧值),tablefield
   后台修改记录表：ods.ppdai_user_log_user_info_revise_history
   字段：userid, creationdate(修改时间),newvalue(新值),oldvalue(旧值),tablefield
1.（1）
-- 拿出用户
create table test.t1 as
  select userid, listingid, cre_dt
  from edw.cmn_listing
  where cre_dt >= '2017-07-01' and cre_dt < '2017-11-01'

 -- 连接前后台修改记录
 create table test.t2 as
   select a.userid, a.listingid, a.cre_dt, b.newvalue, b.creationdate
   from edw.cmn_listing a
   left join ods.ppdai_user_log_userupdateinfologs b 
   on a.userid = b.userid 
   and a.cre_dt > b.creationdate
   and lower(b.tablefield) like '%qq%'
   and b.oldvalue <> b.newvalue
   union all
   select a.userid, a.listingid, a.cre_dt, b.newvalue, b.creationdate
   from edw.cmn_listing a
   left join ods.ppdai_user_log_user_info_revise_history b 
   on a.userid = b.userid 
   and a.cre_dt > b.creationdate
   and b.categoryid = 116
   and b.oldvalue <> b.newvalue

-- 排序，选出最后一次修改记录
 create table test.t3 as
  select userid, listingid, cre_dt, newvalue last_qq
  from( 
    select userid, listingid, cre_dt, newvalue, row_number()over(partition by listingid order by creationdate decs) num
    from test.t2
    ) a
  where num = 1

1.(2)
-- 拿出历史上同qq的人
 create table test.t4 as
  select distinct a.*
  from(
    select a.userid, a.listingid, a.cre_dt, a.last_qq, b.userid u2
    from test.t3 a
    left join ods.ppdai_user_log_userupdateinfologs b 
    on a.last_qq = b.newvalue
    and a.cre_dt > b.creationdate
    and lower(b.tablefield) like '%qq%'
    and a.userid <> b.userid
    union all
    select a.userid, a.listingid, a.cre_dt, a.last_qq, b.userid u2
    from test.t3 a
    left join ods.ppdai_user_log_user_info_revise_history b 
    on a.last_qq = b.newvalue
    and a.cre_dt > b.creationdate
    and b.tablefield = 116
    and a.userid <> b.userid
    ) a

-- 计数
 create table test.t5 as
  select userid, listingid, cre_dt, last_qq, count(u2) u2
  from test.t4
  group by userid, listingid, cre_dt, last_qq



2. （1）2017年7-10月的发标用户，发标前7天登入登出中
    含有可疑行为(description中含有关键字‘可疑行为’)的记录
    结果：userid | listingid | cre_dt | description | 
   （2）提取出所有可疑行为记录中的真实姓名和身份证号
    结果：userid | listingid | cre_dt | realname | idnumber

   发标表：edw.cmn_listing
   字段： userid, listingid, cre_dt
   用户活动记录表 ods.user_activity
   字段：userid, description, creationdate
   可疑行为记录样本：
   '可疑行为: 该身份证号已经被认证过, 身份证为: ***, 真实姓名为: **, UserAgent 为: PPD-LoanApp/6.1.7 (vivo;vivo X20A;C29B219C72DD771684C165512CBCEC6B;Android/7.1.1'

2.(1)
-- 拿出可疑记录
create table test.t6 as
  select a.*, b.description
  from test.t1 a
  left join ods.user_activity b 
  on a.userid = b.userid
  and a.cre_dt > b.creationdate
  and b.description like '%可疑行为%'
  and datediff(a.cre_dt, b.creationdate) <= 7

2.(2)
-- 提取记录中的真实姓名和身份证号（用instr、substr）
create table test.t7 as
  select userid, listingid, cre_dt
        ,substr(description, instr(description,'真实姓名为: ')+length('真实姓名为: '), instr(description,', UserAgent 为') - (instr(description,'真实姓名为: ')+length('真实姓名为: '))) realname
        ,substr(description, instr(description,'身份证为: ')+length('身份证为: '), instr(description,', 真实姓名为:') - (instr(description,'身份证为:')+length('身份证为: '))) idnumber
  from test.t6

-- 用正则
create table test.t7 as
  select userid, listingid, cre_dt
        ,regexp_extract(lower(description),'(^[0-9]*)([0-9]{15}|[0-9]{18}|[0-9]{17}x)(.*$)',2) idnumber
        ,regexp_extract(description,
          '(可疑行为: 该身份证号已经被认证过, 身份证为: )([0-9]{15}|[0-9]{18}|[0-9]{17}x)(, 真实姓名为: )(.*)(, UserAgent 为: PPD-LoanApp/6.1.7 (vivo;vivo X20A;C29B219C72DD771684C165512CBCEC6B;Android/7.1.1)',
          4) realname
  from test.t6



3. （1）2017年7-10月的发标用户，发标前7天登入登出中含有可疑行为的记录的人是否存在历史同qq中
    结果：u1| listingid | cre_dt | last_qq | u2 | whether_qq
   （2）2017年7-10月的发标用户，出现这种情况的人数
    结果：u1| listingid | cre_dt | renshu |

    身份证用户名对应表 fqz.luanqibazao_ud_temp
    字段: idnumber | userid 

3.(1)
-- 拿出可疑行为对应的用户
create table test.t8 as
  select a.userid u1, a.listingid, a.cre_dt, b.userid u2
  from test.t7 a
  inner join fqz.luanqibazao_ud_temp b 
  on a.idnumber = b.idnumber

-- 匹配有可疑行为的人是否在同qq中
create table test.t9 as 
  select a.u1, a.listingid, a.cre_dt, b.last_qq, a.u2
        ,case when c.u2 is not null then 1 else 0 end as whether_qq
  from test.t8 a
  left join test.t4 b on a.u1 = b.userid
  left join test.t4 c on a.u1 = c.userid and a.u2 = c.u2

-- 计算人数
create table test.t10 as
  select u1, listingid, cre_dt, count(distinct u2)
  from test.t9
  group by u1, listingid, cre_dt

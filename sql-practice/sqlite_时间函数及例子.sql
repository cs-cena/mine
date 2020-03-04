--查询各学生的年龄，只按年份来算
/*
SELECT st.sid, (strftime('%Y', "now") - strftime('%Y', st.Sage)) as age
FROM Student AS st
*/

--按照出生日期来算，当前月日 < 出生年月的月日则，年龄减一
/*
SELECT st.sid, (CASE WHEN strftime('%m-%d', "now")-strftime('%m-%d', st.Sage) < 0 THEN t.age-1 ELSE t.age END) AS age
FROM Student AS st,
(SELECT st.sid, (strftime('%Y', "now") - strftime('%Y', st.Sage)) as age
FROM Student AS st
) AS t
WHERE t.sid = st.SId
*/


--查询本周过生日的学生
/*
SELECT st.sid, st.sname
FRoM student AS st 
WHERE strftime('2019-%m-%d', st.sage) BETWEEN date('now', 'start of day', '-7 day', 'weekday 1') AND date('now', 'start of day', 'weekday 0');
*/

--weekday N N为周几，一周设定奇怪，56是本周的周五/周六。01234是下周的周天周一到周四
--含义是返回第一个时间参数（或修饰过后的时间）所在周的下一周的周几。会加一周
--SELECT date('now', 'start of day', '-7 day', 'weekday 0')


--查询下周过生日的学生
/*
SELECT st.sid, st.sname
FRoM student AS st 
WHERE strftime('2019-%m-%d', st.sage) BETWEEN date('now', 'start of day', 'weekday 1') AND date('now', 'start of day', '+7 day', 'weekday 0');
*/


--查询本月过生日的学生
/*
SELECT st.sid, st.sname
FRoM student AS st 
WHERE strftime('2019-%m-%d', st.sage) BETWEEN date('now', 'start of month') AND date('now', 'start of month', '+1 month', '-1 day')
*/

--查询下月过生日的学生
/*
SELECT st.sid, st.sname
FRoM student AS st 
WHERE strftime('2019-%m-%d', st.sage) BETWEEN date('now', 'start of month', '+1 month') AND date('now', 'start of month', '+2 month', '-1 day') 
*/
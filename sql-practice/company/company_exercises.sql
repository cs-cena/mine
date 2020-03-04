2.1
#sqlite
SELECT 
	d.user_id
	,d.listing_id
	,strftime("%Y-%m", d.cre_dt) AS fb_month
	,c.newvalue
	,c.oldvalue
FROM (
	SELECT 
		a.*
		,(CASE WHEN b.listing_id IS NOT NULL THEN 1 ELSE 0 END) AS is_success
	FROM cmn_listing as a 
	left join listing_vintage as b 
	on a.listing_id = b.listing_id
	WHERE a.cre_dt > "2017-11-01" AND a.cre_dt < "2018-02-01"
) as d 
left join ppdai_user_log_userupdateinfologs as c 
on d.user_id = c.user_id
WHERE c.creationdate < d.cre_dt and c.tablefield in ("Qq","_QQ","_qQ","_Qq","__QQ")


#mysql
SELECT 
	d.user_id
	,d.listing_id
	,unix_timestamp(d.cre_dt,'yyyy-MM') AS fb_month
	,c.newvalue
	,c.oldvalue
FROM (
	SELECT 
		a.*
		,(CASE WHEN b.listing_id IS NOT NULL THEN 1 ELSE 0 END) AS is_success
	FROM cmn_listing as a 
	left join listing_vintage as b 
	on a.listing_id = b.listing_id
	WHERE a.cre_dt > unix_timestamp("2017-11-01 00:00:00") AND a.cre_dt < unix_timestamp("2018-02-01 00:00:00")
) as d 
left join ppdai_user_log_userupdateinfologs as c 
on d.user_id = c.user_id
WHERE c.creationdate < d.cre_dt and c.tablefield in ("Qq","_QQ","_qQ","_Qq","__QQ")


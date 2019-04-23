1. realtime_shenyang相对realtime_db库特有的表（table_oneself）
```
INSERT INTO realtime_shenyang.table_oneself
(SELECT
	table_shenyang
FROM
	(
		SELECT
			shenyang.TABLE_NAME AS table_shenyang,
			fb.TABLE_NAME AS table_fb
		FROM
			(
				SELECT
					TABLE_NAME
				FROM
					`COLUMNS`
				WHERE
					TABLE_SCHEMA = 'realtime_shenyang'
				GROUP BY
					TABLE_NAME
			) AS shenyang
		LEFT JOIN (
			SELECT
				TABLE_NAME
			FROM
				`COLUMNS`
			WHERE
				TABLE_SCHEMA = 'realtime_db'
			GROUP BY
				TABLE_NAME
		) AS fb ON shenyang.TABLE_NAME = fb.TABLE_NAME
	) AS shenyang_fb_left
WHERE
	table_fb IS NULL)
```

2. realtime_db相对realtime_shenyang库特有的表（table_oneself）
```
INSERT INTO realtime_db.table_oneself
(SELECT
	table_fb
FROM
	(
		SELECT
			shenyang.TABLE_NAME AS table_shenyang,
			fb.TABLE_NAME AS table_fb
		FROM
			(
				SELECT
					TABLE_NAME
				FROM
					`COLUMNS`
				WHERE
					TABLE_SCHEMA = 'realtime_shenyang'
				GROUP BY
					TABLE_NAME
			) AS shenyang
		RIGHT JOIN (
			SELECT
				TABLE_NAME
			FROM
				`COLUMNS`
			WHERE
				TABLE_SCHEMA = 'realtime_db'
			GROUP BY
				TABLE_NAME
		) AS fb ON shenyang.TABLE_NAME = fb.TABLE_NAME
	) AS shenyang_fb_right
WHERE
	table_shenyang IS NULL)
```
	
3. realtime_shenyang相对realtime_db库公共表特有的字段
```
SELECT
	table_shenyang,
	column_shenyang
FROM
	(
		SELECT
			shenyang.TABLE_NAME AS table_shenyang,
			shenyang.COLUMN_NAME AS column_shenyang,
			fb.TABLE_NAME AS table_fb,
			fb.COLUMN_NAME AS column_fb
		FROM
			(
				SELECT
					TABLE_NAME,
					COLUMN_NAME
				FROM
					`COLUMNS`
				WHERE
					TABLE_SCHEMA = 'realtime_shenyang'
				AND TABLE_NAME NOT IN (
					SELECT
						*
					FROM
						realtime_shenyang.table_oneself
				)
			) AS shenyang
		LEFT JOIN (
			SELECT
				TABLE_NAME,
				COLUMN_NAME
			FROM
				`COLUMNS`
			WHERE
				TABLE_SCHEMA = 'realtime_db'
			AND TABLE_NAME NOT IN (
				SELECT
					*
				FROM
					realtime_db.table_oneself
			)
		) AS fb ON shenyang.TABLE_NAME = fb.TABLE_NAME
		AND shenyang.COLUMN_NAME = fb.COLUMN_NAME
	) AS shenyang_fb_left
WHERE
	column_fb IS NULL
```
	
4. realtime_db相对realtime_shenyang库公共表特有的字段
```
SELECT
	table_fb,
	column_fb
FROM
	(
		SELECT
			shenyang.TABLE_NAME AS table_shenyang,
			shenyang.COLUMN_NAME AS column_shenyang,
			fb.TABLE_NAME AS table_fb,
			fb.COLUMN_NAME AS column_fb
		FROM
			(
				SELECT
					TABLE_NAME,
					COLUMN_NAME
				FROM
					`COLUMNS`
				WHERE
					TABLE_SCHEMA = 'realtime_shenyang'
				AND TABLE_NAME NOT IN (
					SELECT
						*
					FROM
						realtime_shenyang.table_oneself
				)
			) AS shenyang
		RIGHT JOIN (
			SELECT
				TABLE_NAME,
				COLUMN_NAME
			FROM
				`COLUMNS`
			WHERE
				TABLE_SCHEMA = 'realtime_db'
			AND TABLE_NAME NOT IN (
				SELECT
					*
				FROM
					realtime_db.table_oneself
			)
		) AS fb ON shenyang.TABLE_NAME = fb.TABLE_NAME
		AND shenyang.COLUMN_NAME = fb.COLUMN_NAME
	) AS shenyang_fb_right
WHERE
	column_shenyang IS NULL
```

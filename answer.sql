-- prepare: clean, transform, fill missing data
CREATE VIEW prepared AS
SELECT
	`Tên sản phẩm` ,
	`Số đã bán` ,
	`Số đã bán` * `Giá` AS `Doanh số`,
	(CASE
		WHEN `Thương hiệu` = '' THEN (CASE
			WHEN `Tên sản phẩm` LIKE '%apple%' THEN "apple"
			WHEN `Tên sản phẩm` LIKE '%xiaomi%' THEN "xiaomi"
			WHEN `Tên sản phẩm` LIKE '%samsung%' THEN "samsung"
			WHEN `Tên sản phẩm` LIKE '%oppo%' THEN "oppo"
			WHEN `Tên sản phẩm` LIKE '%realme%' THEN "realme"
			WHEN `Tên sản phẩm` LIKE '%vertu%' THEN "vertu"
			WHEN `Tên sản phẩm` LIKE '%asus%' THEN "asus"
			WHEN `Tên sản phẩm` LIKE '%redmi%' THEN "redmi"
			WHEN `Tên sản phẩm` LIKE '%lg%' THEN "lg"
			WHEN `Tên sản phẩm` LIKE '%infinix%' THEN "infinix"
			WHEN `Tên sản phẩm` LIKE '%sony%' THEN "sony"
			WHEN `Tên sản phẩm` LIKE '%google%' THEN "google"
			WHEN `Tên sản phẩm` LIKE '%vsmart%' THEN "vsmart"
			WHEN `Tên sản phẩm` LIKE '%vivo%' THEN "vivo"
			WHEN `Tên sản phẩm` LIKE '%kudixiong%' THEN "kudixiong"
			WHEN `Tên sản phẩm` LIKE '%itel%' THEN "itel"
			WHEN `Tên sản phẩm` LIKE '%poco%' THEN "poco"
			WHEN `Tên sản phẩm` LIKE '%tecno%' THEN "tecno"
			WHEN `Tên sản phẩm` LIKE '%nokia%' THEN "nokia"
			WHEN `Tên sản phẩm` LIKE '%galaxy%' THEN "samsung"
			ELSE NULL
		END
	)
		ELSE `Thương hiệu`
	END
	) AS brand,
	(CASE
		WHEN `Link shop` LIKE '%shopee%' THEN 'shopee'
		WHEN `Link shop` LIKE '%tiki%' THEN 'tiki'
		WHEN `Link shop` LIKE '%lazada%' THEN 'lazada'
		ELSE NULL
	END) AS platform
FROM
	`data` d
WHERE
	`Ngành hàng` IN ("Điện Thoại & Máy Tính Bảng", "Chưa phân loại")

CREATE TABLE brand_country (
    brand VARCHAR(255),
    country VARCHAR(255)
);

-- DROP TABLE brand_country;

INSERT INTO brand_country (brand, country) VALUES
('apple', 'Mỹ'),
('xiaomi', 'Trung Quốc'),
('samsung', 'Hàn Quốc'),
('oppo', 'Trung Quốc'),
('realme', 'Trung Quốc'),
('vertu', 'Britain'),
('asus', 'Đài Loan'),
('lg', 'Hàn Quốc'),
('infinix', 'Trung Quốc'),
('sony', 'Nhật'),
('google', 'Mỹ'),
('vsmart', 'Việt Nam'),
('vivo', 'Trung Quốc'),
('kudixiong', 'Trung Quốc'),
('itel', 'Trung Quốc'),
('poco', 'Trung Quốc'),
('tecno', 'Trung Quốc'),
('redmi', 'Trung Quốc'),
('nokia', 'Phần Lan');

-- combines information about the corresponding country with the phone brands
CREATE VIEW merged AS 
SELECT
	p.`Số đã bán`,
	p.`Doanh số`,
	b.country
FROM
	prepared p
JOIN brand_country b ON
	p.brand = b.brand
WHERE
	country IN (
        "Trung Quốc", "Mỹ", "Hàn Quốc"
    )

-- DROP VIEW merged;
	
-- SELECT * FROM `data` AS d;
-- SELECT * FROM prepared p;
-- SELECT * from brand_country;

-- ======================== Answers =========================
-- Question 1
SELECT
	p.brand ,
	sum(p.`Số đã bán`) AS "Số đã bán",
	SUM(P.`Doanh số`) AS "Doanh số"
FROM
	prepared p
GROUP BY
	brand 
	
-- Question 2

SELECT
	m.country,
	sum(m.`Số đã bán`) AS sold
FROM
	merged m
GROUP BY
	m.country
ORDER BY
	sold DESC

-- Question 3

SELECT
	m.country,
	sum(m.`Doanh số`) AS sales
FROM
	merged m
GROUP BY
	m.country
ORDER BY
	sales DESC

-- Question 4

-- Group Galaxy S23 products together
CREATE view samsung as
	select
		(p.`Tên sản phẩm` like '%s23%') as product,
		sum(p.`Số đã bán`) as "Số đã bán",
		sum(p.`Doanh số`) as "Doanh số"
	from
		prepared p
	where
		p.brand = "samsung"
		and p.platform = "shopee"
	group by
		product

-- DROP VIEW samsung;
		
SELECT 
	(CASE
		WHEN s.product = 1 THEN "S23"
		WHEN s.product = 0 THEN "others"
		ELSE NULL
	END
	) AS product,
	round(((s.`Số đã bán`) / (SELECT SUM(`Số đã bán`) FROM samsung)), 4)* 100 AS "Số đã bán %",
	round(((s.`Doanh số`) / (SELECT SUM(`Doanh số`) FROM samsung)), 4) * 100 AS "Doanh số %"
FROM
	samsung s

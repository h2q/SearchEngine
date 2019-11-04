CREATE DATABASE search;
USE search;
DROP TABLE IF EXISTS it;
CREATE TABLE it (
  title varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  url varchar(300) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  url_object_id varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  content longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  crawl_time datetime DEFAULT NULL,
  PRIMARY KEY USING BTREE(url_object_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

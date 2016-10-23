/*
 Navicat MySQL Data Transfer

 Source Server         : RA
 Source Server Type    : MySQL
 Source Server Version : 50711
 Source Host           : localhost
 Source Database       : app_annie

 Target Server Type    : MySQL
 Target Server Version : 50711
 File Encoding         : utf-8

 Date: 10/23/2016 12:09:18 PM
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `Review_info_pokego`
-- ----------------------------
DROP TABLE IF EXISTS `Review_info_pokego`;
CREATE TABLE `Review_info_pokego` (
  `ID` int(10) NOT NULL AUTO_INCREMENT,
  `App` varchar(50) DEFAULT NULL,
  `Country` varchar(20) DEFAULT NULL,
  `Date` varchar(100) DEFAULT NULL,
  `Rating` int(1) DEFAULT NULL,
  `Reviewer_name` varchar(200) DEFAULT NULL COMMENT '[''App'', ''Country'', ''Date'', ''Rating'', ''Review_content'', ''Reviewer_name'', ''Reviewer_title'', ''Vision'']',
  `Review_content` text,
  `Reviewer_title` varchar(1000) DEFAULT NULL COMMENT '[''App'', ''Country'', ''Date'', ''Rating'', ''Review_content'', ''Reviewer_name'', ''Reviewer_title'', ''Vision'']',
  `Vision` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=375277 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
--  Table structure for `page`
-- ----------------------------
DROP TABLE IF EXISTS `page`;
CREATE TABLE `page` (
  `date_` date NOT NULL,
  `category` varchar(300) NOT NULL,
  `page_source` longtext CHARACTER SET utf8mb4
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `rank`
-- ----------------------------
DROP TABLE IF EXISTS `rank`;
CREATE TABLE `rank` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `class` varchar(10) NOT NULL,
  `rank` int(4) NOT NULL,
  `rank_change` varchar(5) DEFAULT NULL,
  `date_` date NOT NULL,
  `time_` timestamp NULL DEFAULT NULL,
  `parent_cat` varchar(200) DEFAULT NULL,
  `category` varchar(200) CHARACTER SET utf8mb4 NOT NULL,
  `app_name` varchar(500) CHARACTER SET utf8mb4 NOT NULL,
  `app_href` varchar(500) NOT NULL,
  `developer` varchar(500) CHARACTER SET utf8mb4 DEFAULT NULL,
  `in_app_charge` int(1) DEFAULT NULL COMMENT 'weather the app have in-app purchases',
  `url` varchar(500) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5504378 DEFAULT CHARSET=latin1;

SET FOREIGN_KEY_CHECKS = 1;

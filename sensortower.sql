/*
Navicat MySQL Data Transfer

Source Server         : down
Source Server Version : 50716
Source Host           : 127.0.0.1:3306
Source Database       : sensortower

Target Server Type    : MYSQL
Target Server Version : 50716
File Encoding         : 65001

Date: 2016-10-23 17:26:35
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for app
-- ----------------------------
DROP TABLE IF EXISTS `app`;
CREATE TABLE `app` (
  `id` int(10) NOT NULL,
  `app_id` varchar(50) NOT NULL,
  `month` varchar(30) NOT NULL,
  `download` varchar(20) NOT NULL,
  `revenue` varchar(20) NOT NULL,
  PRIMARY KEY (`app_id`,`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for page
-- ----------------------------
DROP TABLE IF EXISTS `page`;
CREATE TABLE `page` (
  `id` int(10) DEFAULT NULL,
  `app_id` varchar(50) NOT NULL,
  `page_source` longtext CHARACTER SET utf8mb4 NOT NULL,
  PRIMARY KEY (`app_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.3.12-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win32
-- HeidiSQL Version:             10.1.0.5464
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for proverde
CREATE DATABASE IF NOT EXISTS `proverde` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `proverde`;

-- Dumping structure for table proverde.authorization
CREATE TABLE IF NOT EXISTS `authorization` (
  `request_folio` int(11) NOT NULL,
  `authorized` tinyint(1) DEFAULT NULL,
  `authorization1` tinyint(1) DEFAULT NULL,
  `authorization1_date` datetime DEFAULT NULL,
  `authorization1_by` int(11) DEFAULT NULL,
  `authorization2` tinyint(1) DEFAULT NULL,
  `authorization2_date` datetime DEFAULT NULL,
  `authorization2_by` int(11) DEFAULT NULL,
  `authorization3` tinyint(1) DEFAULT NULL,
  `authorization3_date` datetime DEFAULT NULL,
  `authorization3_by` int(11) DEFAULT NULL,
  PRIMARY KEY (`request_folio`),
  KEY `authorization1_by` (`authorization1_by`),
  KEY `authorization2_by` (`authorization2_by`),
  KEY `authorization3_by` (`authorization3_by`),
  CONSTRAINT `authorization_ibfk_1` FOREIGN KEY (`request_folio`) REFERENCES `request` (`folio`),
  CONSTRAINT `authorization_ibfk_2` FOREIGN KEY (`authorization1_by`) REFERENCES `manager` (`manager_id`),
  CONSTRAINT `authorization_ibfk_3` FOREIGN KEY (`authorization2_by`) REFERENCES `manager` (`manager_id`),
  CONSTRAINT `authorization_ibfk_4` FOREIGN KEY (`authorization3_by`) REFERENCES `manager` (`manager_id`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`authorized` in (0,1)),
  CONSTRAINT `CONSTRAINT_2` CHECK (`authorization1` in (0,1)),
  CONSTRAINT `CONSTRAINT_3` CHECK (`authorization2` in (0,1)),
  CONSTRAINT `CONSTRAINT_4` CHECK (`authorization3` in (0,1))
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table proverde.department
CREATE TABLE IF NOT EXISTS `department` (
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table proverde.employee
CREATE TABLE IF NOT EXISTS `employee` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `user` varchar(50) NOT NULL,
  `department_assigned` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `department_assigned` (`department_assigned`),
  CONSTRAINT `employee_ibfk_1` FOREIGN KEY (`department_assigned`) REFERENCES `department` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table proverde.items
CREATE TABLE IF NOT EXISTS `items` (
  `r_folio` int(11) DEFAULT NULL,
  `description` varchar(100) NOT NULL,
  `chemical` tinyint(1) NOT NULL,
  `unit_measure` varchar(3) NOT NULL,
  `unit_price` float NOT NULL,
  `quantity` int(11) NOT NULL,
  `item_total` float NOT NULL,
  `item_number` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`description`),
  KEY `r_folio` (`r_folio`),
  CONSTRAINT `items_ibfk_1` FOREIGN KEY (`r_folio`) REFERENCES `request` (`folio`) ON DELETE CASCADE,
  CONSTRAINT `CONSTRAINT_1` CHECK (`chemical` in (0,1))
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table proverde.manager
CREATE TABLE IF NOT EXISTS `manager` (
  `department_name` varchar(50) NOT NULL,
  `manager_id` int(11) NOT NULL,
  PRIMARY KEY (`department_name`,`manager_id`),
  KEY `manager_id` (`manager_id`),
  CONSTRAINT `manager_ibfk_1` FOREIGN KEY (`department_name`) REFERENCES `department` (`name`),
  CONSTRAINT `manager_ibfk_2` FOREIGN KEY (`manager_id`) REFERENCES `employee` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table proverde.request
CREATE TABLE IF NOT EXISTS `request` (
  `folio` int(11) NOT NULL AUTO_INCREMENT,
  `employee_id` int(11) NOT NULL,
  `submit_date` datetime NOT NULL,
  `purchase_type` varchar(20) NOT NULL,
  `purchase_order` varchar(20) DEFAULT NULL,
  `cost_center` varchar(20) NOT NULL,
  `account_number` varchar(20) NOT NULL,
  `department_name` varchar(50) NOT NULL,
  `total` float DEFAULT NULL,
  `comments` varchar(256) DEFAULT NULL,
  `file` mediumblob DEFAULT NULL,
  `filename` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`folio`),
  KEY `employee_id` (`employee_id`),
  KEY `department_name` (`department_name`),
  CONSTRAINT `request_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`id`),
  CONSTRAINT `request_ibfk_2` FOREIGN KEY (`department_name`) REFERENCES `department` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;

-- MySQL dump 10.13  Distrib 5.7.22, for Linux (x86_64)
--
-- Host: localhost    Database: DBO_BLOCKCHAIN
-- ------------------------------------------------------
-- Server version	5.7.22-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `contract_data`
--

DROP TABLE IF EXISTS `contract_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contract_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `personalID` varchar(20) NOT NULL,
  `contractAddress` varchar(100) NOT NULL,
  `contractABI` varchar(4000) NOT NULL,
  `userToken` varchar(100) NOT NULL,
  PRIMARY KEY (`id`,`personalID`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `name_UNIQUE` (`personalID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contract_data`
--

LOCK TABLES `contract_data` WRITE;
/*!40000 ALTER TABLE `contract_data` DISABLE KEYS */;
INSERT INTO `contract_data` VALUES (1,'F123456789','0x75FCA9FE8b9C16F060537f28747D560ad52fb616','[{\'type\': \'function\', \'payable\': False, \'outputs\': [{\'name\': \'isRegistered\', \'type\': \'bool\'}], \'name\': \'getUserRegisterTable\', \'inputs\': [{\'name\': \'userID\', \'type\': \'string\'}], \'stateMutability\': \'view\', \'constant\': True}, {\'type\': \'function\', \'payable\': False, \'outputs\': [{\'name\': \'res\', \'type\': \'bool\'}], \'name\': \'setUserRegisterTable\', \'inputs\': [{\'name\': \'userID\', \'type\': \'string\'}], \'stateMutability\': \'nonpayable\', \'constant\': False}, {\'type\': \'function\', \'payable\': False, \'outputs\': [{\'name\': \'isRegistered\', \'type\': \'bool\'}], \'name\': \'isUserRegistered\', \'inputs\': [{\'name\': \'userID\', \'type\': \'string\'}], \'stateMutability\': \'view\', \'constant\': True}, {\'type\': \'constructor\', \'payable\': False, \'inputs\': [], \'stateMutability\': \'nonpayable\'}, {\'name\': \'LogRegisterIsSuccessed\', \'inputs\': [{\'name\': \'sender\', \'indexed\': False, \'type\': \'address\'}, {\'name\': \'isSuccessed\', \'indexed\': False, \'type\': \'bool\'}, {\'name\': \'msg\', \'indexed\': False, \'type\': \'string\'}], \'type\': \'event\', \'anonymous\': False}, {\'name\': \'LogGetRegisterData\', \'inputs\': [{\'name\': \'sender\', \'indexed\': False, \'type\': \'address\'}, {\'name\': \'isSuccessed\', \'indexed\': False, \'type\': \'bool\'}, {\'name\': \'msg\', \'indexed\': False, \'type\': \'string\'}], \'type\': \'event\', \'anonymous\': False}]','0x03512651684648c66f6634f0b3fb7593fd30a14bde3a83558110d4ded6c3f70c');
/*!40000 ALTER TABLE `contract_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `education_data`
--

DROP TABLE IF EXISTS `education_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `education_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userName` varchar(20) NOT NULL,
  `personalID` varchar(20) NOT NULL,
  `birthday` date DEFAULT NULL,
  `schoolName` varchar(20) DEFAULT NULL,
  `department` varchar(20) DEFAULT NULL,
  `grade` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `education_data`
--

LOCK TABLES `education_data` WRITE;
/*!40000 ALTER TABLE `education_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `education_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `finance_data`
--

DROP TABLE IF EXISTS `finance_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `finance_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userName` varchar(20) NOT NULL,
  `personalID` varchar(20) NOT NULL,
  `birthday` date NOT NULL,
  `bankAccount` varchar(45) DEFAULT NULL,
  `amount` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `finance_data`
--

LOCK TABLES `finance_data` WRITE;
/*!40000 ALTER TABLE `finance_data` DISABLE KEYS */;
INSERT INTO `finance_data` VALUES (1,'kobe','F123456789','1996-09-23','1234',1234);
/*!40000 ALTER TABLE `finance_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `personal_data`
--

DROP TABLE IF EXISTS `personal_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `personal_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userName` varchar(45) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `personalID` varchar(10) DEFAULT NULL,
  `marrige` varchar(10) DEFAULT NULL,
  `family` varchar(10) DEFAULT NULL,
  `education` varchar(10) DEFAULT NULL,
  `occupation` varchar(10) DEFAULT NULL,
  `password` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `personalID_UNIQUE` (`personalID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personal_data`
--

LOCK TABLES `personal_data` WRITE;
/*!40000 ALTER TABLE `personal_data` DISABLE KEYS */;
INSERT INTO `personal_data` VALUES (1,'kobe','1996-09-23','F123456789','','','','','123');
/*!40000 ALTER TABLE `personal_data` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-05-16 11:09:18

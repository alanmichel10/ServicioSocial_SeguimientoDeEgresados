CREATE DATABASE  IF NOT EXISTS `seg_egresados5` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `seg_egresados5`;
-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: seg_egresados5
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cuenta`
--

DROP TABLE IF EXISTS `cuenta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cuenta` (
  `idCuenta` int NOT NULL AUTO_INCREMENT,
  `correo` varchar(255) NOT NULL,
  `clave` varchar(255) NOT NULL,
  `idRol` int DEFAULT '2',
  PRIMARY KEY (`idCuenta`),
  UNIQUE KEY `correo` (`correo`),
  KEY `idRol` (`idRol`),
  CONSTRAINT `cuenta_ibfk_1` FOREIGN KEY (`idRol`) REFERENCES `roles` (`idRol`),
  CONSTRAINT `cuenta_ibfk_2` FOREIGN KEY (`correo`) REFERENCES `general` (`Correo_Alumno`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cuenta`
--

LOCK TABLES `cuenta` WRITE;
/*!40000 ALTER TABLE `cuenta` DISABLE KEYS */;
INSERT INTO `cuenta` VALUES (4,'alanmissaeljimenez@gmail.com','1408b3203e908009a518cfb2c14f2102950f77e14266a2528da1448373ed5562',2);
/*!40000 ALTER TABLE `cuenta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estudios`
--

DROP TABLE IF EXISTS `estudios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estudios` (
  `Correo_A` varchar(150) NOT NULL,
  `centroUniversitario` varchar(255) DEFAULT NULL,
  `carrera` varchar(255) DEFAULT NULL,
  `cicloEgreso` varchar(255) DEFAULT NULL,
  `nivelIngles` varchar(255) DEFAULT NULL,
  `titulado` varchar(255) DEFAULT NULL,
  `Promedio` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Correo_A`),
  CONSTRAINT `estudios_ibfk_1` FOREIGN KEY (`Correo_A`) REFERENCES `general` (`Correo_Alumno`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estudios`
--

LOCK TABLES `estudios` WRITE;
/*!40000 ALTER TABLE `estudios` DISABLE KEYS */;
INSERT INTO `estudios` VALUES ('alanmissaeljimenez@gmail.com','CUTONALA','Ciencias computacionales','2022A','B1: Intermedio','En Proceso','99');
/*!40000 ALTER TABLE `estudios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `general`
--

DROP TABLE IF EXISTS `general`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `general` (
  `Correo_Alumno` varchar(150) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `apellidoP` varchar(255) NOT NULL,
  `apellidoM` varchar(255) DEFAULT NULL,
  `sexo` varchar(10) DEFAULT NULL,
  `celular` varchar(15) DEFAULT NULL,
  `codigoPostal` varchar(10) DEFAULT NULL,
  `fechaNacimiento` date DEFAULT NULL,
  `posgrado` varchar(255) DEFAULT NULL,
  `Pais` varchar(45) DEFAULT NULL,
  `Estado` varchar(45) DEFAULT NULL,
  `Ciudad` varchar(45) DEFAULT NULL,
  `Colonia` varchar(45) DEFAULT NULL,
  `Nacionalidad` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Correo_Alumno`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `general`
--

LOCK TABLES `general` WRITE;
/*!40000 ALTER TABLE `general` DISABLE KEYS */;
INSERT INTO `general` VALUES ('alanmissaeljimenez@gmail.com','Alan','Coco','Jimenez','Femenino','56454654','94984','2024-09-01','[\"Maestría en Ingeniería del Agua y la Energía (Profesionalizante)\",\"Maestría en Gestión de Gobiernos Locales\",\"Maestría en Geología\"]','México','14','Guadalajara','Oblatos','Mexicana');
/*!40000 ALTER TABLE `general` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `laboral`
--

DROP TABLE IF EXISTS `laboral`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `laboral` (
  `Correo_Alu` varchar(150) NOT NULL,
  `estatus` varchar(2) DEFAULT NULL,
  `nombre` varchar(255) DEFAULT NULL,
  `Horario_Laboral` varchar(45) DEFAULT NULL,
  `Puesto_Trabajo` varchar(45) DEFAULT NULL,
  `Sector` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Correo_Alu`),
  CONSTRAINT `laboral_ibfk_1` FOREIGN KEY (`Correo_Alu`) REFERENCES `general` (`Correo_Alumno`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `laboral`
--

LOCK TABLES `laboral` WRITE;
/*!40000 ALTER TABLE `laboral` DISABLE KEYS */;
INSERT INTO `laboral` VALUES ('alanmissaeljimenez@gmail.com','No','N/A','N/A','N/A','NoAplica');
/*!40000 ALTER TABLE `laboral` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `idRol` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`idRol`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'Administrador'),(2,'Usuario Normal');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-15 16:18:56

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
-- Table structure for table `aspirante_carrera`
--

DROP TABLE IF EXISTS `aspirante_carrera`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `aspirante_carrera` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Correo_Alumno` varchar(150) DEFAULT NULL,
  `idCarrera` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Correo_Alumno` (`Correo_Alumno`),
  KEY `idCarrera` (`idCarrera`),
  CONSTRAINT `aspirante_carrera_ibfk_1` FOREIGN KEY (`Correo_Alumno`) REFERENCES `general` (`Correo_Alumno`),
  CONSTRAINT `aspirante_carrera_ibfk_2` FOREIGN KEY (`idCarrera`) REFERENCES `carrera` (`idCarrera`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aspirante_carrera`
--

LOCK TABLES `aspirante_carrera` WRITE;
/*!40000 ALTER TABLE `aspirante_carrera` DISABLE KEYS */;
INSERT INTO `aspirante_carrera` VALUES (5,'alan.jimenez1350@alumnos.udg.mx',7),(6,'alan.jimenez1350@alumnos.udg.mx',8),(22,'alanmissaeljimenez@gmail.com',11),(23,'alanmissaeljimenez@gmail.com',13),(28,'pedro11452@gmail.com',8),(29,'alberto.lopez1350@alumnos.udg.mx',6),(30,'alberto.lopez1350@alumnos.udg.mx',7),(31,'alberto.lopez1350@alumnos.udg.mx',8),(32,'qweasdasdaasdcvzx@gmail.com',7),(33,'qweasdasdaasdcvzx@gmail.com',10),(34,'qweasdasdaasdcvzx@gmail.com',11),(35,'alanmissael115@gmail.com',11),(36,'alanmissael115@gmail.com',12),(37,'alanmissael115@gmail.com',13),(38,'olawqweqwe@gmail.com',11),(39,'olawqweqwe@gmail.com',12),(40,'olawqweqwe@gmail.com',13);
/*!40000 ALTER TABLE `aspirante_carrera` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `carrera`
--

DROP TABLE IF EXISTS `carrera`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carrera` (
  `idCarrera` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`idCarrera`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carrera`
--

LOCK TABLES `carrera` WRITE;
/*!40000 ALTER TABLE `carrera` DISABLE KEYS */;
INSERT INTO `carrera` VALUES (1,'Maestría en Movilidad Urbana, Transporte y Territorio'),(2,'Maestría en Ingeniería del Agua y la Energía (Profesionalizante)'),(3,'Maestría en Gestión de Gobiernos Locales'),(4,'Maestría en Geología'),(5,'Maestría en Ciencias en Ingeniería del Agua y la Energía (Investigación)'),(6,'Maestría en Ciencias Antropológicas'),(7,'Maestría en Ciencia de la Ciudad'),(8,'Maestría en Bioética'),(9,'Doctorado en Movilidad Urbana, Transporte y Territorio'),(10,'Doctorado en Investigación Multidisciplinaria en Salud'),(11,'Doctorado en Geología'),(12,'Doctorado en Derechos Humanos'),(13,'Doctorado en Agua y Energía');
/*!40000 ALTER TABLE `carrera` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `coordinador_carrera`
--

DROP TABLE IF EXISTS `coordinador_carrera`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `coordinador_carrera` (
  `idCoordinador` int NOT NULL AUTO_INCREMENT,
  `correo` varchar(255) DEFAULT NULL,
  `idCarrera` int DEFAULT NULL,
  PRIMARY KEY (`idCoordinador`),
  KEY `correo` (`correo`),
  KEY `idCarrera` (`idCarrera`),
  CONSTRAINT `coordinador_carrera_ibfk_1` FOREIGN KEY (`correo`) REFERENCES `cuenta` (`correo`),
  CONSTRAINT `coordinador_carrera_ibfk_2` FOREIGN KEY (`idCarrera`) REFERENCES `carrera` (`idCarrera`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coordinador_carrera`
--

LOCK TABLES `coordinador_carrera` WRITE;
/*!40000 ALTER TABLE `coordinador_carrera` DISABLE KEYS */;
INSERT INTO `coordinador_carrera` VALUES (1,'mae.geologia@cutonala.udg.mx',11),(2,'alanmissaeljimenez@gmail.com',8);
/*!40000 ALTER TABLE `coordinador_carrera` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cuenta`
--

LOCK TABLES `cuenta` WRITE;
/*!40000 ALTER TABLE `cuenta` DISABLE KEYS */;
INSERT INTO `cuenta` VALUES (11,'mae.geologia@cutonala.udg.mx','5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5',1),(16,'alanmissaeljimenez@gmail.com','1343646eb7383f821db37014a23c0ec4f0a2dc38286e9ec217c0b031b804fd22',1),(18,'pedro11452@gmail.com','5ee01b0463585e4fe6362786624a3d7a27bbb95894a675ba808a6cb2bac0c594',2),(19,'alanmissael115@gmail.com','53fb5be1eda434620a0a1b54fa18efd742a6bfe5a2e93e1ba69a20e9f27ede85',2),(20,'olawqweqwe@gmail.com','29b31381b160ddde334d0ac4913f0c57d80009da082daf0a9a566150c54ccaa8',2);
/*!40000 ALTER TABLE `cuenta` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `before_insert_cuenta` BEFORE INSERT ON `cuenta` FOR EACH ROW BEGIN
    SET NEW.clave = SHA2(NEW.clave, 256);
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

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
INSERT INTO `estudios` VALUES ('alan.jimenez1350@alumnos.udg.mx','CUTONALA','Ciencias computacionales','2022A','B1: Intermedio','En Proceso','93'),('alanmissael115@gmail.com','CUTONALA','Ciencias computacionales','asdsd','A2-B1: Pre-intermedio','En Proceso','99'),('alanmissaeljimenez@gmail.com','asda','sdasd','2022A','A1-A2: Básico','No','93'),('alberto.lopez1350@alumnos.udg.mx','CUTONALA','Ciencias computacionales','2022A','B1: Intermedio','En Proceso','99'),('olawqweqwe@gmail.com','CUTONALA','asd','asda','B1: Intermedio','En Proceso','99'),('pedro11452@gmail.com','CUTONALA','Ciencias computacionales','2022A','B1: Intermedio','En Proceso','93'),('qweasdasdaasdcvzx@gmail.com','CUTONALA','sadasd','2022A','A2-B1: Pre-intermedio','En Proceso','99');
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
INSERT INTO `general` VALUES ('alan.jimenez1350@alumnos.udg.mx','Alan','wsqewdasd','Jimenez','Femenino','56454654','94984','2024-09-02','México','Jalisco','asd','asdsad','asdsad'),('alanmissael115@gmail.com','Alan','ASDA','Jimenez','Femenino','56454654','94984','2024-09-30','México','14','ASD','ASDA','SDSAD'),('alanmissaeljimenez@gmail.com','Alan','sadsda','Jimenez','Femenino','56454654','94984','2024-09-01','México','14','dasd','asd','asdasd'),('alberto.lopez1350@alumnos.udg.mx','Alberto Emmanuel','Lopez','Torres','Masculino','56454654','94984','2024-07-01','México','14','Guadalajara','Jauja','Mexicana'),('mae.geologia@cutonala.udg.mx','Nombre','ApellidoP','ApellidoM','Sexo','Celular','44747','0001-02-05','Pais','Estado','Ciudad','Colonia','Nacionalidad'),('olawqweqwe@gmail.com','Alan','Coco','Jimenez','Femenino','56454654','94984','2024-09-29','México','14','asd','asdas','dasd'),('pedro@gmail.com','PEDRO','Gonzalez','benito','Femenino','56454654','94984','2016-01-04','México','14','asdas','Oblatos','Mexicana'),('pedro11452@gmail.com','PEDRO','Gonzalez','benito','Femenino','56454654','94984','2016-01-04','México','14','asdas','Oblatos','Mexicana'),('qweasdasdaasdcvzx@gmail.com','Alan','Coco','Jimenez','Masculino','56454654','94984','2024-09-29','México','14','Guadalajara','Oblatos','Mexicana');
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
INSERT INTO `laboral` VALUES ('alanmissael115@gmail.com','No','N/A','N/A','N/A','NoAplica'),('alanmissaeljimenez@gmail.com','No','N/A','N/A','N/A','NoAplica'),('olawqweqwe@gmail.com','Si','IBM','7:00am-8:00pm','Gerente de localidad','Privado'),('pedro11452@gmail.com','No','N/A','N/A','N/A','NoAplica');
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'Administrador'),(2,'Usuario Normal'),(3,'coordinador');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'seg_egresados5'
--

--
-- Dumping routines for database 'seg_egresados5'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-10-09  0:59:10

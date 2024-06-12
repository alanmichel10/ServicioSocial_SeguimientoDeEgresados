-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 28-04-2024 a las 06:19:02
-- Versión del servidor: 8.0.35
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `seg_egresados`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cuenta`
--
create database seg_egresados;

use seg_egresados;

CREATE TABLE `cuenta` (
  `idCuenta` int NOT NULL,
  `correo` varchar(255) NOT NULL,
  `clave` varchar(255) NOT NULL,
  `nombre` varchar(255) DEFAULT NULL,
  `apellidoP` varchar(255) DEFAULT NULL,
  `apellidoM` varchar(255) DEFAULT NULL,
  `idRol` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `cuenta`
--

INSERT INTO `cuenta` (`idCuenta`, `correo`, `clave`, `nombre`, `apellidoP`, `apellidoM`, `idRol`) VALUES
(2, 'alan@hotmail.com', 'scrypt:32768:8:1$6YDdW7TS8bRvCPBu$d7b08be24e3ee73abe4f966c12239d5bd9d40016ff93214ba92336b335a2bc3d1b4a70c622bce9dbfe36075c1ff95517d7c14c73036f5db7037a85a59df77575', 'Alan', 'Gomez', 'Tavares', 2),
(3, 'oliver@gmail.com', 'scrypt:32768:8:1$DG8clcNO3OomOwzA$8e916bbb78c22495cc9ac2f1c55e12be89e86e491db6e9e2238c52aa370f4b0da526ceb6329e57473c81c62bacd5911701821de8637b7dae1bfbd3a6542daf66', 'Oliver Demian ', 'Murillo', 'Padilla', 2),
(4, 'admin@admin.com', 'scrypt:32768:8:1$DG8clcNO3OomOwzA$8e916bbb78c22495cc9ac2f1c55e12be89e86e491db6e9e2238c52aa370f4b0da526ceb6329e57473c81c62bacd5911701821de8637b7dae1bfbd3a6542daf66', 'Administrador', 'admin', 'admin', 1),
(5, 'alan@gmail.com', 'scrypt:32768:8:1$jrPSMcFe0rStnmu4$1df9e261dc4fce1a537ef21e0b6deb8428d7f4359793bd455b29df55803cbfdfd612daa8759bb92dba103919158fb4a0b37127f0fcc25de243e9f51469d1eec4', 'Alan', 'Gomez', 'Tavares', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudios`
--

CREATE TABLE `estudios` (
  `idEstudios` int NOT NULL,
  `centroUniversitario` varchar(255) DEFAULT NULL,
  `carrera` varchar(255) DEFAULT NULL,
  `cicloEgreso` varchar(20) DEFAULT NULL,
  `nivelIngles` varchar(20) DEFAULT NULL,
  `titulado` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `estudios`
--

INSERT INTO `estudios` (`idEstudios`, `centroUniversitario`, `carrera`, `cicloEgreso`, `nivelIngles`, `titulado`) VALUES
(1, 'CUT', 'Ingeniería en Ciencias Computacionales', '24B', 'C1-C2', 'En proceso'),
(2, 'CUT', 'Ingeniería en Ciencias Computacionales', '24B', 'B1', 'En proceso');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `general`
--

CREATE TABLE `general` (
  `idGeneral` int NOT NULL,
  `sexo` varchar(10) DEFAULT NULL,
  `curp` varchar(18) DEFAULT NULL,
  `codigoPostal` varchar(10) DEFAULT NULL,
  `codigoEstudiante` varchar(50) DEFAULT NULL,
  `estadoCivil` varchar(20) DEFAULT NULL,
  `fechaNacimiento` date DEFAULT NULL,
  `lugarNacimiento` varchar(255) DEFAULT NULL,
  `celular` varchar(15) DEFAULT NULL,
  `posgrado` varchar(255) DEFAULT NULL,
  `cuenta` int DEFAULT NULL,
  `estudios` int DEFAULT NULL,
  `trabajo` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `general`
--

INSERT INTO `general` (`idGeneral`, `sexo`, `curp`, `codigoPostal`, `codigoEstudiante`, `estadoCivil`, `fechaNacimiento`, `lugarNacimiento`, `celular`, `posgrado`, `cuenta`, `estudios`, `trabajo`) VALUES
(1, 'Hombre', 'gota980810hjcmvl07', '454400', NULL, 'Soltero', '1998-08-10', 'Tlaquepaque', '3333500204', 'Maestría en Movilidad Urbana, Transporte y Territorio', 2, 1, 1),
(2, 'Hombre', 'gota980810hjcmvl07', '454400', NULL, 'Soltero', '1998-08-10', 'Tlaquepaque', '3333500204', 'Maestría en Ciencias en Ingeniería del Agua y la Energía', 5, 2, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `idRol` int NOT NULL,
  `nombre` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`idRol`, `nombre`) VALUES
(1, 'Admin'),
(2, 'Usuario');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `trabajo`
--

CREATE TABLE `trabajo` (
  `idTrabajo` int NOT NULL,
  `estatus` varchar(2) DEFAULT NULL,
  `nombre` varchar(255) DEFAULT NULL,
  `ubicacion` varchar(255) DEFAULT NULL,
  `descripcion` text,
  `antiguedad` varchar(50) DEFAULT NULL,
  `jornadaLaboral` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `trabajo`
--

INSERT INTO `trabajo` (`idTrabajo`, `estatus`, `nombre`, `ubicacion`, `descripcion`, `antiguedad`, `jornadaLaboral`) VALUES
(1, 'No', NULL, NULL, NULL, NULL, NULL),
(2, 'No', NULL, NULL, NULL, NULL, NULL);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `cuenta`
--
ALTER TABLE `cuenta`
  ADD PRIMARY KEY (`idCuenta`),
  ADD UNIQUE KEY `correo` (`correo`),
  ADD KEY `idRol` (`idRol`);

--
-- Indices de la tabla `estudios`
--
ALTER TABLE `estudios`
  ADD PRIMARY KEY (`idEstudios`);

--
-- Indices de la tabla `general`
--
ALTER TABLE `general`
  ADD PRIMARY KEY (`idGeneral`),
  ADD KEY `cuenta` (`cuenta`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`idRol`);

--
-- Indices de la tabla `trabajo`
--
ALTER TABLE `trabajo`
  ADD PRIMARY KEY (`idTrabajo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `cuenta`
--
ALTER TABLE `cuenta`
  MODIFY `idCuenta` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `estudios`
--
ALTER TABLE `estudios`
  MODIFY `idEstudios` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `general`
--
ALTER TABLE `general`
  MODIFY `idGeneral` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `idRol` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `trabajo`
--
ALTER TABLE `trabajo`
  MODIFY `idTrabajo` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `cuenta`
--
ALTER TABLE `cuenta`
  ADD CONSTRAINT `cuenta_ibfk_1` FOREIGN KEY (`idRol`) REFERENCES `roles` (`idRol`);

--
-- Filtros para la tabla `estudios`
--
ALTER TABLE `estudios`
  ADD CONSTRAINT `estudios_ibfk_1` FOREIGN KEY (`idEstudios`) REFERENCES `general` (`idGeneral`);

--
-- Filtros para la tabla `general`
--
ALTER TABLE `general`
  ADD CONSTRAINT `general_ibfk_1` FOREIGN KEY (`cuenta`) REFERENCES `cuenta` (`idCuenta`);

--
-- Filtros para la tabla `trabajo`
--
ALTER TABLE `trabajo`
  ADD CONSTRAINT `trabajo_ibfk_1` FOREIGN KEY (`idTrabajo`) REFERENCES `general` (`idGeneral`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 17-04-2025 a las 08:08:43
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `cadisoft`
--
CREATE DATABASE IF NOT EXISTS `cadisoft` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `cadisoft`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alumnos`
--

CREATE TABLE `alumnos` (
  `idAlumno` int(11) NOT NULL,
  `idusuarios` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `calificaciones`
--

CREATE TABLE `calificaciones` (
  `idCalificacion` int(11) NOT NULL,
  `idAlumno` int(11) NOT NULL,
  `idCurso` int(11) NOT NULL,
  `idInscripcion` int(11) NOT NULL,
  `calificacion` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cursos`
--

CREATE TABLE `cursos` (
  `idCurso` int(11) NOT NULL,
  `idProfesor` int(11) NOT NULL,
  `idDepartamento` int(11) NOT NULL,
  `Materia` varchar(40) NOT NULL,
  `Seccion` varchar(8) DEFAULT NULL,
  `precio_curso` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `departamento`
--

CREATE TABLE `departamento` (
  `idDepartamento` int(11) NOT NULL,
  `departamento` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `facturas`
--

CREATE TABLE `facturas` (
  `idFactura` int(11) NOT NULL,
  `idusuarios` int(11) NOT NULL,
  `total` double NOT NULL,
  `fecha` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `factura_productos`
--

CREATE TABLE `factura_productos` (
  `idFactura_producto` int(11) NOT NULL,
  `idFactura` int(11) NOT NULL,
  `idProducto` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio_unitario` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `horario`
--

CREATE TABLE `horario` (
  `idhorario` int(11) NOT NULL,
  `horario_dia` varchar(10) NOT NULL,
  `horario_hora` time NOT NULL,
  `horario_aula` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `horario_x_curso`
--

CREATE TABLE `horario_x_curso` (
  `idhorario_x_curso` int(11) NOT NULL,
  `idhorario` int(11) NOT NULL,
  `idCurso` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inscripcion`
--

CREATE TABLE `inscripcion` (
  `idInscripcion` int(11) NOT NULL,
  `idAlumno` int(11) NOT NULL,
  `fecha_inscripcion` date NOT NULL,
  `fecha_expiracion` date NOT NULL,
  `es_activa` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `insc_x_cursos`
--

CREATE TABLE `insc_x_cursos` (
  `idinsc_x_cursos` int(11) NOT NULL,
  `idInscripcion` int(11) NOT NULL,
  `idCurso` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `idProducto` int(11) NOT NULL,
  `categoria` varchar(12) NOT NULL,
  `nombre` varchar(20) NOT NULL,
  `precio` decimal(6,2) NOT NULL,
  `stock` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `profesores`
--

CREATE TABLE `profesores` (
  `idProfesor` int(11) NOT NULL,
  `idusuarios` int(11) NOT NULL,
  `especialidad` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registro_familiar`
--

CREATE TABLE `registro_familiar` (
  `idfamilia` int(11) NOT NULL,
  `idAlumno` int(11) NOT NULL,
  `NombrePapa` varchar(12) NOT NULL,
  `ApellidoPapa` varchar(20) NOT NULL,
  `NombreMama` varchar(12) NOT NULL,
  `ApellidoMama` varchar(20) NOT NULL,
  `Telefono` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `idusuarios` int(11) NOT NULL,
  `nombre` varchar(12) NOT NULL,
  `segundoNombre` varchar(12) NOT NULL,
  `apellido` varchar(20) NOT NULL,
  `segundoApellido` varchar(20) NOT NULL,
  `cedula` varchar(8) NOT NULL,
  `email` varchar(50) NOT NULL,
  `contraseña` varchar(200) NOT NULL,
  `rol` varchar(13) NOT NULL,
  `imagen` longblob DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`idusuarios`, `nombre`, `segundoNombre`, `apellido`, `segundoApellido`, `cedula`, `email`, `contraseña`, `rol`, `imagen`) VALUES
(32, 'Juan', 'Andrés', 'Koch', 'Padrón', '30139712', 'juanandreskochp@gmail.com', '$2b$12$bzg9tsH9uaOVMH7dDwZfceSJCgydQ6c8zhK7.mnbDPs.I4pMk9Bty', 'administrador', NULL);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `alumnos`
--
ALTER TABLE `alumnos`
  ADD PRIMARY KEY (`idAlumno`),
  ADD KEY `usuario_a_idx` (`idusuarios`);

--
-- Indices de la tabla `calificaciones`
--
ALTER TABLE `calificaciones`
  ADD PRIMARY KEY (`idCalificacion`),
  ADD KEY `curso_fk_idx` (`idCurso`),
  ADD KEY `alumno_fk_idx` (`idAlumno`),
  ADD KEY `inscripcion_calificacion_fk` (`idInscripcion`);

--
-- Indices de la tabla `cursos`
--
ALTER TABLE `cursos`
  ADD PRIMARY KEY (`idCurso`),
  ADD UNIQUE KEY `Seccion_UNIQUE` (`Seccion`),
  ADD KEY `profesor_fk_idx` (`idProfesor`);

--
-- Indices de la tabla `departamento`
--
ALTER TABLE `departamento`
  ADD PRIMARY KEY (`idDepartamento`);

--
-- Indices de la tabla `facturas`
--
ALTER TABLE `facturas`
  ADD PRIMARY KEY (`idFactura`),
  ADD KEY `usuarios_facturas_idx` (`idusuarios`);

--
-- Indices de la tabla `factura_productos`
--
ALTER TABLE `factura_productos`
  ADD PRIMARY KEY (`idFactura_producto`),
  ADD KEY `factura_idx` (`idFactura`),
  ADD KEY `idProduco_idx` (`idProducto`);

--
-- Indices de la tabla `horario`
--
ALTER TABLE `horario`
  ADD PRIMARY KEY (`idhorario`);

--
-- Indices de la tabla `horario_x_curso`
--
ALTER TABLE `horario_x_curso`
  ADD PRIMARY KEY (`idhorario_x_curso`),
  ADD KEY `horario_fk_idx` (`idhorario`),
  ADD KEY `curso_horario_fk_idx` (`idCurso`);

--
-- Indices de la tabla `inscripcion`
--
ALTER TABLE `inscripcion`
  ADD PRIMARY KEY (`idInscripcion`),
  ADD KEY `alumno_inscripcion_idx` (`idAlumno`);

--
-- Indices de la tabla `insc_x_cursos`
--
ALTER TABLE `insc_x_cursos`
  ADD PRIMARY KEY (`idinsc_x_cursos`),
  ADD KEY `inscripcion_aux_idx` (`idInscripcion`),
  ADD KEY `curso_aux_idx` (`idCurso`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`idProducto`);

--
-- Indices de la tabla `profesores`
--
ALTER TABLE `profesores`
  ADD PRIMARY KEY (`idProfesor`),
  ADD KEY `usuario_p_idx` (`idusuarios`);

--
-- Indices de la tabla `registro_familiar`
--
ALTER TABLE `registro_familiar`
  ADD PRIMARY KEY (`idfamilia`),
  ADD KEY `alumno_familia_fk` (`idAlumno`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`idusuarios`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `alumnos`
--
ALTER TABLE `alumnos`
  MODIFY `idAlumno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `calificaciones`
--
ALTER TABLE `calificaciones`
  MODIFY `idCalificacion` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `cursos`
--
ALTER TABLE `cursos`
  MODIFY `idCurso` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `departamento`
--
ALTER TABLE `departamento`
  MODIFY `idDepartamento` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `facturas`
--
ALTER TABLE `facturas`
  MODIFY `idFactura` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `factura_productos`
--
ALTER TABLE `factura_productos`
  MODIFY `idFactura_producto` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `horario`
--
ALTER TABLE `horario`
  MODIFY `idhorario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `horario_x_curso`
--
ALTER TABLE `horario_x_curso`
  MODIFY `idhorario_x_curso` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `inscripcion`
--
ALTER TABLE `inscripcion`
  MODIFY `idInscripcion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `insc_x_cursos`
--
ALTER TABLE `insc_x_cursos`
  MODIFY `idinsc_x_cursos` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `idProducto` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `profesores`
--
ALTER TABLE `profesores`
  MODIFY `idProfesor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT de la tabla `registro_familiar`
--
ALTER TABLE `registro_familiar`
  MODIFY `idfamilia` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `idusuarios` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `alumnos`
--
ALTER TABLE `alumnos`
  ADD CONSTRAINT `usuario_a` FOREIGN KEY (`idusuarios`) REFERENCES `usuarios` (`idusuarios`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `calificaciones`
--
ALTER TABLE `calificaciones`
  ADD CONSTRAINT `alumno_fk` FOREIGN KEY (`idAlumno`) REFERENCES `alumnos` (`idAlumno`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `curso_fk` FOREIGN KEY (`idCurso`) REFERENCES `cursos` (`idCurso`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `inscripcion_calificacion_fk` FOREIGN KEY (`idInscripcion`) REFERENCES `inscripcion` (`idInscripcion`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `cursos`
--
ALTER TABLE `cursos`
  ADD CONSTRAINT `profesor_fk` FOREIGN KEY (`idProfesor`) REFERENCES `profesores` (`idProfesor`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Filtros para la tabla `facturas`
--
ALTER TABLE `facturas`
  ADD CONSTRAINT `usuarios_facturas` FOREIGN KEY (`idusuarios`) REFERENCES `usuarios` (`idusuarios`);

--
-- Filtros para la tabla `factura_productos`
--
ALTER TABLE `factura_productos`
  ADD CONSTRAINT `factura` FOREIGN KEY (`idFactura`) REFERENCES `facturas` (`idFactura`),
  ADD CONSTRAINT `idProduco` FOREIGN KEY (`idProducto`) REFERENCES `productos` (`idProducto`);

--
-- Filtros para la tabla `horario_x_curso`
--
ALTER TABLE `horario_x_curso`
  ADD CONSTRAINT `curso_horario_fk` FOREIGN KEY (`idCurso`) REFERENCES `cursos` (`idCurso`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `horario_fk` FOREIGN KEY (`idhorario`) REFERENCES `horario` (`idhorario`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `inscripcion`
--
ALTER TABLE `inscripcion`
  ADD CONSTRAINT `alumno_inscripcion` FOREIGN KEY (`idAlumno`) REFERENCES `alumnos` (`idAlumno`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `insc_x_cursos`
--
ALTER TABLE `insc_x_cursos`
  ADD CONSTRAINT `curso_aux` FOREIGN KEY (`idCurso`) REFERENCES `cursos` (`idCurso`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `inscripcion_aux` FOREIGN KEY (`idInscripcion`) REFERENCES `inscripcion` (`idInscripcion`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `profesores`
--
ALTER TABLE `profesores`
  ADD CONSTRAINT `usuario_p` FOREIGN KEY (`idusuarios`) REFERENCES `usuarios` (`idusuarios`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `registro_familiar`
--
ALTER TABLE `registro_familiar`
  ADD CONSTRAINT `alumno_familia_fk` FOREIGN KEY (`idAlumno`) REFERENCES `alumnos` (`idAlumno`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

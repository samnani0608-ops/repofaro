# RepoFaro — Technical Architecture

**Versión:** 0.1.0  
**Estado:** Propuesta inicial  
**Arquitectura:** Modular  
**Lenguaje principal:** Python

## 1. Introducción

Este documento describe la arquitectura técnica de RepoFaro, sus componentes principales, responsabilidades y mecanismos de comunicación.

El objetivo es establecer una organización modular que facilite el mantenimiento, las pruebas y la incorporación de nuevas funcionalidades.

## 2. Estructura del proyecto

El proyecto utilizará una organización basada en el modelo `src layout` de Python.

```text
src/repofaro/
├── __init__.py
├── __main__.py
├── cli.py
├── scanner.py
├── detector.py
├── models.py
├── rules/
│   ├── __init__.py
│   ├── engine.py
│   ├── common.py
│   ├── python.py
│   └── cpp.py
└── reporters/
    ├── __init__.py
    ├── terminal.py
    └── json_report.py
```

## 3. Componentes principales

### 3.1 CLI

Archivo: `cli.py`

Responsabilidades:

- Recibir argumentos del usuario.
- Validar las opciones de ejecución.
- Iniciar el proceso de análisis.
- Gestionar los resultados y errores de ejecución.

### 3.2 Project Scanner

Archivo: `scanner.py`

Responsabilidades:

- Recorrer directorios.
- Identificar archivos y carpetas.
- Aplicar exclusiones.
- Registrar información estructural del proyecto.

El scanner no modificará los archivos analizados.

### 3.3 Project Detector

Archivo: `detector.py`

Responsabilidades:

- Identificar tecnologías mediante archivos característicos.
- Analizar múltiples indicadores.
- Determinar posibles tecnologías del proyecto.
- Registrar las evidencias utilizadas para la detección.

### 3.4 Models

Archivo: `models.py`

Contendrá las estructuras de datos utilizadas por los diferentes componentes.

Se contemplan las siguientes entidades:

- ProjectSnapshot: información estructural del proyecto.
- ProjectProfile: tecnologías identificadas y evidencias.
- Finding: hallazgo generado por una regla.
- ScanReport: resultado completo de una auditoría.

### 3.5 Rule Engine

Directorio: `rules/`

El motor ejecutará las reglas de evaluación correspondientes al proyecto analizado.

Se organizarán las reglas según su ámbito:

- common.py: reglas generales.
- python.py: reglas específicas de Python.
- cpp.py: reglas específicas de C++.

El motor será responsable de recopilar los hallazgos.

### 3.6 Reporters

Directorio: `reporters/`

Responsabilidades:

- Presentar resultados en terminal.
- Exportar resultados estructurados a JSON.

Los reporters no realizarán análisis ni modificarán el proyecto examinado.

## 4. Flujo de información

El proceso general seguirá esta secuencia:

1. El usuario proporciona una ruta mediante la CLI.
2. El scanner inspecciona el directorio.
3. El detector identifica las tecnologías.
4. El motor de reglas ejecuta las evaluaciones correspondientes.
5. Se recopilan los hallazgos.
6. El reporter presenta o exporta los resultados.

## 5. Pruebas

El directorio `tests/` contendrá las pruebas automatizadas.

Se utilizarán fixtures para representar diferentes tipos de proyectos y situaciones de análisis.

Las pruebas se desarrollarán utilizando Pytest.

## 6. Tecnologías

| Tecnología | Propósito |
|---|---|
| Python | Desarrollo principal |
| Git | Control de versiones |
| GitHub | Repositorio y colaboración |
| Pytest | Pruebas automatizadas |
| SQLite | Persistencia futura |
| GTK4 + libadwaita | Interfaz gráfica futura |

## 7. Principios arquitectónicos

### Modularidad

Cada componente tendrá responsabilidades delimitadas.

### Extensibilidad

Se podrán incorporar nuevas reglas y tecnologías sin modificar innecesariamente los componentes existentes.

### Mantenibilidad

El código deberá ser comprensible, organizado y acompañado de pruebas.

### Seguridad

El sistema funcionará inicialmente en modo de solo lectura y no ejecutará código de los proyectos analizados.

### Eficiencia

Se evitarán operaciones innecesarias y se tendrá en cuenta el consumo de memoria.

## 8. Evolución prevista

La arquitectura podrá evolucionar para incorporar:

- Nuevos detectores tecnológicos.
- Reglas configurables.
- Persistencia mediante SQLite.
- Informes HTML.
- Interfaz gráfica GTK4.
- Nuevos sistemas de análisis.

Estas funcionalidades se incorporarán progresivamente según las necesidades del producto.
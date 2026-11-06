# RepoFaro

**Local Project Structure & Quality Auditor**

RepoFaro es una herramienta de análisis local diseñada para desarrolladores independientes. Su objetivo es inspeccionar la estructura de proyectos de software, identificar posibles problemas organizativos y proporcionar recomendaciones para mejorar su calidad y mantenibilidad.

## Objetivo

Facilitar la evaluación de proyectos de software mediante un sistema de análisis modular, extensible y adaptable a diferentes lenguajes y tecnologías.

## Características previstas

- Análisis de estructuras de directorios.
- Detección automática de tecnologías.
- Evaluación mediante reglas configurables.
- Identificación de problemas organizativos.
- Recomendaciones de buenas prácticas.
- Generación de informes desde la terminal.
- Exportación de resultados a JSON.

## Tecnologías

- Python
- Git
- SQLite (planificado)
- Pytest (planificado)

## Filosofía del proyecto

RepoFaro busca ofrecer diagnósticos útiles y comprensibles.

No pretende imponer una única estructura universal para todos los proyectos. Sus evaluaciones deberán considerar el lenguaje, las herramientas y el contexto del proyecto analizado.

Los resultados distinguirán entre problemas importantes, advertencias y recomendaciones.

## Seguridad

RepoFaro tendrá inicialmente un funcionamiento de solo lectura.

No deberá ejecutar código de los proyectos analizados, modificar sus archivos ni realizar conexiones externas para completar una auditoría.

## Estado del desarrollo

**Versión actual:** 0.1.0

**Estado:** Planificación inicial.

El desarrollo comenzará con una interfaz CLI y un conjunto reducido de funcionalidades.

## Roadmap

- [ ] Definición de requisitos.
- [ ] Diseño de arquitectura.
- [ ] Implementación del Project Scanner.
- [ ] Implementación del Project Detector.
- [ ] Desarrollo del Rule Engine.
- [ ] Generación de informes.
- [ ] Pruebas automatizadas.
- [ ] Primera versión distribuible.

## Licencia

Pendiente de selección.
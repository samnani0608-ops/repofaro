# RepoFaro — Software Requirements Specification

**Versión del documento:** 0.1.0  
**Estado:** Borrador inicial.

## 1. Propósito

Definir los requisitos funcionales y no funcionales de RepoFaro, una herramienta local para analizar estructuras de proyectos de software y generar recomendaciones sobre su organización y mantenimiento.

## 2. Usuarios objetivo

Desarrolladores independientes, estudiantes de programación y personas que mantienen proyectos de software propios.

## 3. Alcance del MVP

La primera versión funcional deberá permitir:

1. Inspeccionar un directorio local.
2. Identificar su estructura de archivos y carpetas.
3. Detectar tecnologías mediante archivos característicos.
4. Ejecutar reglas de evaluación.
5. Presentar hallazgos y recomendaciones.
6. Exportar los resultados a JSON.

## 4. Requisitos funcionales

### RF-001 — Selección del proyecto

El sistema deberá aceptar una ruta local como argumento de entrada.

### RF-002 — Validación de rutas

El sistema deberá comprobar que la ruta proporcionada existe y corresponde a un directorio válido.

### RF-003 — Exploración de archivos

El sistema deberá recorrer recursivamente el directorio seleccionado e identificar archivos y subdirectorios.

No deberá seguir enlaces simbólicos durante la exploración inicial.

### RF-004 — Exclusión de directorios

El sistema deberá permitir excluir directorios que no aporten información relevante, como `.git`, `.venv`, `node_modules`, `build` y `__pycache__`.

### RF-005 — Detección tecnológica

El sistema deberá identificar tecnologías mediante archivos característicos y múltiples indicadores cuando sea necesario.

Las primeras tecnologías objetivo serán Python, Node.js y C/C++.

### RF-006 — Evaluación mediante reglas

El sistema deberá ejecutar un conjunto de reglas para identificar problemas, advertencias y recomendaciones.

### RF-007 — Resultados estructurados

Cada hallazgo deberá contener, como mínimo:

- Identificador de regla.
- Título.
- Severidad.
- Descripción.
- Recomendación.

### RF-008 — Informe de terminal

El sistema deberá presentar los resultados de manera comprensible mediante la CLI.

### RF-009 — Exportación JSON

El sistema deberá permitir exportar los resultados de una auditoría a formato JSON.

## 5. Requisitos no funcionales

### RNF-001 — Seguridad

El sistema deberá funcionar en modo de solo lectura.

No ejecutará código de los proyectos analizados.

### RNF-002 — Rendimiento

El sistema deberá evitar operaciones innecesarias y mantener un consumo de memoria razonable.

### RNF-003 — Modularidad

Los componentes deberán mantener responsabilidades independientes.

### RNF-004 — Mantenibilidad

El código deberá utilizar nombres descriptivos, tipado cuando corresponda y documentación razonable.

### RNF-005 — Compatibilidad

La primera versión tendrá como objetivo sistemas Linux.

### RNF-006 — Confiabilidad

Las funcionalidades principales deberán disponer de pruebas automatizadas.

## 6. Fuera del alcance inicial

Las siguientes características no formarán parte del MVP:

- Interfaz gráfica.
- Corrección automática de problemas.
- Análisis mediante inteligencia artificial.
- Base de datos e historial de auditorías.
- Análisis estático profundo del código fuente.
- Servicios en la nube.
- Integraciones externas.

Estas funcionalidades podrán reconsiderarse en versiones futuras.

## 7. Criterios de finalización del MVP

El MVP se considerará funcional cuando pueda:

1. Recibir y validar una ruta.
2. Analizar la estructura del proyecto.
3. Reconocer tecnologías compatibles.
4. Ejecutar reglas de evaluación.
5. Mostrar los resultados en terminal.
6. Exportar un informe JSON.
7. Superar las pruebas automatizadas principales.
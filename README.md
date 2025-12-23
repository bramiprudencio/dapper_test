# 🏛️ Legislación AI Monitor - Colombia

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql)
![Gemini AI](https://img.shields.io/badge/AI-Gemini_1.5-8E75B2?style=for-the-badge&logo=google)

Este proyecto es una solución de **Ingeniería de Datos automatizada** que monitorea, extrae, procesa y visualiza los Proyectos de Ley del Congreso de la República de Colombia. 

Utiliza un pipeline ETL (Extract, Transform, Load) contenerizado que integra **Inteligencia Artificial (Google Gemini)** para categorizar automáticamente las leyes en sectores económicos, permitiendo análisis en tiempo real mediante un dashboard de Metabase.

## ⚡ Características Principales

* **Scraping Avanzado:** * Bypass de protecciones básicas mediante manejo de sesiones y headers.
    * Descarga y procesamiento de archivos Excel (60k+ registros) **en memoria RAM** (Streams) sin generar archivos temporales en disco.
* **Clasificación Híbrida con IA:**
    * Sistema inteligente que combina reglas de palabras clave (rápido/gratis) con **Google Gemini 1.5 Flash** para categorizar leyes complejas.
* **Persistencia Robusta:**
    * Uso de PostgreSQL como Data Warehouse.
    * Inserción masiva optimizada (Batch Inserts) para manejar grandes volúmenes de datos.
* **Infraestructura como Código:**
    * Despliegue completo con un solo comando usando Docker Compose.
    * Servicio de visualización (Metabase) pre-integrado.
* **Automatización:**
    * Sistema de "Schedule" interno que ejecuta la actualización diariamente a la medianoche.

## 🏗️ Arquitectura del Sistema

```mermaid
graph TD
    A[Congreso Web] -->|Download Stream| B(Scraper Python 3.11)
    B -->|Categorización| C{AI Service}
    C -->|API Request| D[Google Gemini]
    C -->|Keywords| B
    B -->|Batch Insert| E[(PostgreSQL)]
    F[Metabase] -->|Query| E
    G[Usuario] -->|Visualiza| F
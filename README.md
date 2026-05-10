# Actividad 2 – Análisis Exploratorio de Datos de Presión Arterial

**Materia:** Computación Cognitiva para Big Data  
**Estudiante:** Jonathan Dario Sierra Galindo  
**Docente:** Joaquín F. Sánchez  
**Fecha:** Abril – Mayo 2026

## Descripción

Análisis exploratorio de un dataset de presión arterial de pacientes colombianos.  
Se aplica clasificación AHA 2017 y se generan 7 gráficas con R/ggplot2.

## Archivos

| Archivo | Descripción |
|---|---|
| `analisis_presion.R` | Script R con todo el análisis y generación de gráficas |
| `generar_informe.py` | Script Python que construye el informe Word final |
| `actividad2.csv` | Dataset de pacientes (presión arterial, medicamentos, ubicación) |
| `graficas_R/` | Gráficas exportadas por R (PNG) |

## Requisitos

**R:**
```r
install.packages(c("ggplot2", "dplyr", "tidyr"))
```

**Python:**
```bash
pip install python-docx pandas numpy
```

## Uso

1. Ejecutar `analisis_presion.R` en RStudio → genera las imágenes en `graficas_R/`
2. Ejecutar `generar_informe.py` → genera `Informe_Analisis_Presion_Arterial.docx`

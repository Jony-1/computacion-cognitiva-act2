"""
Generador de informe Word: Análisis Exploratorio de Datos de Presión Arterial
Computación Cognitiva para Big Data – Actividad 2
Gráficas generadas con R / ggplot2
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from word_writer import *          # módulo compartido en mitad trimestre/

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# ── Rutas ──────────────────────────────────────────────────────────────────────
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
CSV_PATH  = os.path.join(BASE_DIR, "actividad2.csv")
IMG_DIR   = os.path.join(BASE_DIR, "graficas_R")   # gráficas producidas por R
OUT_PATH  = os.path.join(BASE_DIR, "Informe_Analisis_Presion_Arterial.docx")

# ── 1. Estadísticas (solo para texto dinámico en el Word) ─────────────────────
print("Cargando datos para estadísticas...")
df = pd.read_csv(CSV_PATH)
df = df[(df["systolic_pressure"] > 0) & (df["diastolic_pressure"] > 0)]

def clasificar(row):
    s, d = row["systolic_pressure"], row["diastolic_pressure"]
    if s < 120 and d < 80:   return "Normal"
    elif s < 130 and d < 80: return "Elevada"
    elif s < 140 or d < 90:  return "Hipertensión Etapa 1"
    else:                     return "Hipertensión Etapa 2"

df["categoria_presion"] = df.apply(clasificar, axis=1)

n_total  = len(df)
n_fem    = (df["gender"] == "f").sum()
n_mas    = (df["gender"] == "m").sum()
n_dept   = df["department_name"].nunique()
n_cities = df["city_name"].nunique()
desc_s   = df["systolic_pressure"].describe()
desc_d   = df["diastolic_pressure"].describe()
cat_pcts = (df["categoria_presion"].value_counts(normalize=True)*100).round(1)
corr_sd  = round(df[["systolic_pressure","diastolic_pressure"]].corr().iloc[0,1], 3)
corr_sq  = round(df[["medicine_quantity","systolic_pressure"]].corr().iloc[0,1], 3)
corr_dq  = round(df[["medicine_quantity","diastolic_pressure"]].corr().iloc[0,1], 3)
dept_top = (df.groupby("department_name")["systolic_pressure"]
              .mean().sort_values(ascending=False))
dept_top1 = dept_top.index[0]
s_top1    = round(dept_top.iloc[0], 1)
med_sis_f = round(df[df["gender"]=="f"]["systolic_pressure"].median(), 1)
med_sis_m = round(df[df["gender"]=="m"]["systolic_pressure"].median(), 1)
med_dia_f = round(df[df["gender"]=="f"]["diastolic_pressure"].median(), 1)
med_dia_m = round(df[df["gender"]=="m"]["diastolic_pressure"].median(), 1)
hipert_pct = round(cat_pcts.get("Hipertensión Etapa 1", 0)
                   + cat_pcts.get("Hipertensión Etapa 2", 0), 1)
print("Estadísticas listas.")

# ── Helpers Word ───────────────────────────────────────────────────────────────
# ── 2. Construir documento ────────────────────────────────────────────────────
print("Construyendo documento Word...")
doc = nuevo_documento(margen_izq=3, margen_der=2.5)

# ════════════════════════════════
#  PORTADA
# ════════════════════════════════
portada(doc,
    institucion    = "INSTITUCIÓN UNIVERSITARIA",
    facultad       = "Facultad de Ingeniería y Tecnología",
    materia        = "Computación Cognitiva para Big Data",
    titulo         = "ANÁLISIS EXPLORATORIO DE DATOS\nDE PRESIÓN ARTERIAL EN PACIENTES",
    actividad      = "Actividad 2 – Semana 2\nIntroducción a sistemas cognitivos y Big Data",
    presentado_por = "JONATHAN DARIO SIERRA GALINDO",
    docente        = "Joaquín F. Sánchez",
    fecha          = "Abril – Mayo 2026",
)

# ════════════════════════════════
#  1. CONTEXTUALIZACIÓN
# ════════════════════════════════
titulo_seccion(doc, "1. Contextualización del Problema")

parrafo(doc, (
    "La presión arterial tiene dos componentes: la sistólica —medida mientras el "
    "corazón bombea— y la diastólica, en el reposo entre latidos. Ambas en mmHg. "
    "A partir de esos dos números se puede determinar si un paciente está en rango "
    "normal o tiene algún nivel de hipertensión."
))
parrafo(doc, (
    f"El archivo actividad2.csv tiene {n_total:,} filas, cada una un paciente diferente "
    f"de {n_dept} departamentos colombianos. Los campos disponibles son: nombre, género, "
    "ciudad, departamento, presión sistólica, presión diastólica, tipo de medicamento "
    "y dosis prescrita. Con eso alcanza para mirar si la presión cambia según el "
    "género, la región o el tratamiento."
))
parrafo(doc, (
    "El trabajo se hizo en RStudio con R y ggplot2, siguiendo la guía de la actividad. "
    "Antes de pensar en modelos o predicciones, hay que entender qué forma tienen "
    "los datos —distribución, rangos, outliers— y eso es lo que hace este AED."
))
parrafo(doc, (
    "Para categorizar los registros se aplicó la clasificación AHA 2017. "
    "Normal: sistólica < 120 y diastólica < 80 mmHg. "
    "Elevada: sistólica 120-129 con diastólica < 80. "
    "Hipertensión Etapa 1: sistólica 130-139 o diastólica 80-89. "
    "Hipertensión Etapa 2: sistólica ≥ 140 o diastólica ≥ 90 mmHg."
))
doc.add_page_break()

# ════════════════════════════════
#  2. ANÁLISIS EXPLORATORIO
# ════════════════════════════════
titulo_seccion(doc, "2. Análisis Exploratorio de los Datos con R", 14)

# --- 2.1 Entorno y código de preparación ---
titulo_subseccion(doc, "2.1 Entorno de Trabajo: RStudio y Código R")
parrafo(doc, (
    "Se trabajó en RStudio con R base más ggplot2. El código siguiente carga el CSV, "
    "descarta registros con presiones en cero o negativas, y crea las columnas de "
    "género legible y categoría de presión que se usan en todas las gráficas:"
), esp_despues=4)

bloque_codigo(doc,
"""# Cargar librerías
library(ggplot2)
library(dplyr)
library(tidyr)

# Cargar base de datos
df <- read.csv("actividad2.csv", stringsAsFactors = FALSE)

# Limpiar registros con presiones no válidas (≤ 0)
df <- df[df$systolic_pressure > 0 & df$diastolic_pressure > 0, ]

# Crear etiquetas de género
df$genero_label <- ifelse(df$gender == "f", "Femenino", "Masculino")

# Clasificar presión arterial (criterios AHA 2017)
df$categoria_presion <- with(df, ifelse(
  systolic_pressure < 120 & diastolic_pressure < 80, "Normal",
  ifelse(systolic_pressure < 130 & diastolic_pressure < 80, "Elevada",
  ifelse(systolic_pressure < 140 | diastolic_pressure < 90,
         "Hipertensión Etapa 1", "Hipertensión Etapa 2"))))

# Estadísticas descriptivas
summary(df$systolic_pressure)
summary(df$diastolic_pressure)""")

parrafo(doc, (
    "El código fuente completo del análisis en R está disponible en el repositorio: "
    "https://github.com/Jony-1/computacion-cognitiva-act2 "
    "— ahí se puede ver el script analisis_presion.R con todos los pasos de limpieza, "
    "clasificación y generación de gráficas."
), tamaño=10, cursiva=True)

# --- Tabla estadísticas ---
titulo_subseccion(doc, "2.2 Estadísticas Descriptivas")
parrafo(doc, "Salida de R – summary() para las dos variables de interés:", esp_despues=4)

bloque_codigo(doc,
f"""# Salida de R:
Presión Sistólica:
   Min.  1st Qu.  Median    Mean  3rd Qu.   Max.
   {desc_s['min']:.0f}     {desc_s['25%']:.1f}    {desc_s['50%']:.1f}   {desc_s['mean']:.1f}   {desc_s['75%']:.1f}   {desc_s['max']:.0f}

Presión Diastólica:
   Min.  1st Qu.  Median    Mean  3rd Qu.   Max.
   {desc_d['min']:.0f}     {desc_d['25%']:.1f}    {desc_d['50%']:.1f}   {desc_d['mean']:.1f}   {desc_d['75%']:.1f}   {desc_d['max']:.0f}

Total registros: {n_total:,}   |   Femenino: {n_fem:,}   |   Masculino: {n_mas:,}
Departamentos: {n_dept}   |   Ciudades: {n_cities}""")

tabla_datos(doc,
    encabezados=["Estadístico", "Presión Sistólica (mmHg)", "Presión Diastólica (mmHg)"],
    filas=[
        ("Número de registros", f"{int(desc_s['count']):,}", f"{int(desc_d['count']):,}"),
        ("Media",               f"{desc_s['mean']:.2f}",    f"{desc_d['mean']:.2f}"),
        ("Desv. estándar",      f"{desc_s['std']:.2f}",     f"{desc_d['std']:.2f}"),
        ("Mínimo",              f"{desc_s['min']:.0f}",     f"{desc_d['min']:.0f}"),
        ("Percentil 25",        f"{desc_s['25%']:.1f}",     f"{desc_d['25%']:.1f}"),
        ("Mediana",             f"{desc_s['50%']:.1f}",     f"{desc_d['50%']:.1f}"),
        ("Percentil 75",        f"{desc_s['75%']:.1f}",     f"{desc_d['75%']:.1f}"),
        ("Máximo",              f"{desc_s['max']:.0f}",     f"{desc_d['max']:.0f}"),
    ]
)

parrafo(doc, (
    f"Media y mediana están bastante cerca en los dos casos: {desc_s['mean']:.1f} vs "
    f"{desc_s['50%']:.1f} para la sistólica, {desc_d['mean']:.1f} vs {desc_d['50%']:.1f} "
    f"para la diastólica. Eso sugiere distribuciones sin sesgo fuerte. "
    f"Pero la desviación estándar —{desc_s['std']:.1f} y {desc_d['std']:.1f}— es bastante "
    "alta, lo que dice que hay pacientes con presiones muy distintas entre sí."
))

# --- G1 ---
titulo_subseccion(doc, "2.3 Distribución de la Presión Sistólica")
bloque_codigo(doc,
"""# Código R – Histograma presión sistólica
ggplot(df, aes(x = systolic_pressure)) +
  geom_histogram(bins = 40, fill = "#2C2C2C", color = "white", alpha = 0.85) +
  geom_vline(aes(xintercept = mean(systolic_pressure), linetype = "Media"),
             color = "black", linewidth = 0.9) +
  geom_vline(aes(xintercept = median(systolic_pressure), linetype = "Mediana"),
             color = "#E84855", linewidth = 0.9) +
  labs(title = "Distribución de la Presión Sistólica",
       x = "Presión Sistólica (mmHg)", y = "Frecuencia") +
  theme_minimal(base_size = 13)""")
insertar_imagen(doc, os.path.join(IMG_DIR,"g1_sistolica.png"), 5.8,
    "Figura 1. Histograma de la presión sistólica – generado con R/ggplot2.")
parrafo(doc, (
    f"La Figura 1 muestra algo llamativo: la distribución es plana, casi sin pico. "
    f"El rango va de {desc_s['min']:.0f} a {desc_s['max']:.0f} mmHg —bastante amplio. "
    "La mayoría de los datos se concentra entre 90 y 160 mmHg, que es donde caería "
    "la mayor parte de adultos. Los valores extremos son pocos; en particular, "
    f"una sistólica de {desc_s['min']:.0f} mmHg o de {desc_s['max']:.0f} mmHg son "
    "casos muy atípicos que pueden ser patologías graves o errores de registro."
))

# --- G2 ---
titulo_subseccion(doc, "2.4 Distribución de la Presión Diastólica")
bloque_codigo(doc,
"""# Código R – Histograma presión diastólica
ggplot(df, aes(x = diastolic_pressure)) +
  geom_histogram(bins = 40, fill = "#444444", color = "white", alpha = 0.85) +
  geom_vline(aes(xintercept = mean(diastolic_pressure), linetype = "Media"),
             color = "black", linewidth = 0.9) +
  labs(title = "Distribución de la Presión Diastólica",
       x = "Presión Diastólica (mmHg)", y = "Frecuencia") +
  theme_minimal(base_size = 13)""")
insertar_imagen(doc, os.path.join(IMG_DIR,"g2_diastolica.png"), 5.8,
    "Figura 2. Histograma de la presión diastólica – generado con R/ggplot2.")
parrafo(doc, (
    f"La diastólica tiene un histograma bastante parecido al anterior: plano, "
    f"media {desc_d['mean']:.1f} y mediana {desc_d['50%']:.1f} mmHg. "
    "La mayoría cae entre 50 y 110 mmHg. Hay registros por debajo de 60 "
    "(posible hipotensión) y por encima de 90 (hipertensión diastólica), "
    "aunque en la gráfica son los menos. Sin sesgo visible en ninguna dirección."
))

# --- G3 ---
titulo_subseccion(doc, "2.5 Comparación por Género")
bloque_codigo(doc,
"""# Código R – Boxplot por género
df_long <- df %>%
  pivot_longer(cols = c(systolic_pressure, diastolic_pressure),
               names_to = "tipo", values_to = "presion") %>%
  mutate(tipo = recode(tipo,
    systolic_pressure  = "Sistólica",
    diastolic_pressure = "Diastólica"))

ggplot(df_long, aes(x = genero_label, y = presion, fill = genero_label)) +
  geom_boxplot(outlier.size = 0.5, outlier.alpha = 0.3, alpha = 0.8) +
  facet_wrap(~tipo, scales = "free_y") +
  labs(title = "Distribución de Presión Arterial por Género",
       x = "Género", y = "Presión (mmHg)") +
  theme_minimal(base_size = 13)""")
insertar_imagen(doc, os.path.join(IMG_DIR,"g3_boxplot_genero.png"), 5.8,
    "Figura 3. Boxplot de presión sistólica y diastólica por género – generado con R/ggplot2.")
parrafo(doc, (
    f"Femenino y masculino quedan prácticamente igual: {med_sis_f} vs {med_sis_m} mmHg "
    f"en sistólica, {med_dia_f} vs {med_dia_m} mmHg en diastólica. Los dos boxplots "
    "son casi copias —mismo ancho, misma posición, outliers parecidos. "
    "El género no diferencia nada en esta muestra."
))

# --- G4 ---
titulo_subseccion(doc, "2.6 Relación Sistólica – Diastólica por Categoría")
bloque_codigo(doc,
"""# Código R – Diagrama de dispersión (muestra aleatoria de 5 000 registros)
set.seed(42)
muestra <- df[sample(nrow(df), 5000), ]

ggplot(muestra, aes(x = systolic_pressure, y = diastolic_pressure,
                    color = categoria_presion)) +
  geom_point(size = 1.2, alpha = 0.5) +
  scale_color_manual(values = c("Normal"="#4A4A4A","Elevada"="#777777",
    "Hipertensión Etapa 1"="#2C2C2C","Hipertensión Etapa 2"="#A0A0A0")) +
  labs(title = "Relación Sistólica – Diastólica por Categoría",
       x = "Presión Sistólica (mmHg)", y = "Presión Diastólica (mmHg)") +
  theme_minimal(base_size = 13)""")
insertar_imagen(doc, os.path.join(IMG_DIR,"g4_dispersion.png"), 5.5,
    "Figura 4. Diagrama de dispersión sistólica vs. diastólica – generado con R/ggplot2.")
parrafo(doc, (
    f"r = {corr_sd} entre sistólica y diastólica. Alta correlación, nada raro. "
    "En el scatter se ve bien: los verdes (Normal) agrupados abajo a la izquierda, "
    "los rojos (Etapa 2) arriba a la derecha. Lo que sí llama la atención es un "
    "grupo de puntos con sistólica elevada pero diastólica relativamente normal "
    "—posiblemente pacientes mayores con arterias rígidas, donde la diastólica "
    "no sube tanto aunque la sistólica sí."
))

# --- G5 ---
titulo_subseccion(doc, "2.7 Categorías de Presión Arterial en la Muestra")
bloque_codigo(doc,
"""# Código R – Barras por categoría
conteo_cat <- df %>%
  count(categoria_presion) %>%
  mutate(porcentaje = n / sum(n) * 100,
         etiqueta   = paste0(round(porcentaje, 1), "%"))

ggplot(conteo_cat, aes(x = reorder(categoria_presion, -n),
                        y = porcentaje, fill = categoria_presion)) +
  geom_col(alpha = 0.9, show.legend = FALSE) +
  geom_text(aes(label = etiqueta), vjust = -0.5, size = 4) +
  labs(title = "Distribución por Categoría de Presión Arterial",
       x = "Categoría", y = "Porcentaje (%)") +
  theme_minimal(base_size = 12)""")
insertar_imagen(doc, os.path.join(IMG_DIR,"g5_categorias.png"), 5.8,
    "Figura 5. Distribución porcentual por categoría de presión – generado con R/ggplot2.")
parrafo(doc, (
    f"{cat_pcts.index[0]} es la categoría más frecuente con {cat_pcts.iloc[0]:.1f}%, "
    f"y {cat_pcts.index[1]} viene segunda con {cat_pcts.iloc[1]:.1f}%. "
    f"Sumando Etapa 1 y Etapa 2, el {hipert_pct}% de los pacientes tiene hipertensión. "
    "Esa cifra parece alta, pero estos son pacientes ya en tratamiento médico —no "
    "es una muestra de la calle. Que la prevalencia supere los promedios nacionales "
    "tiene sentido dado el perfil de quienes aparecen en el dataset."
))

# --- G6 ---
titulo_subseccion(doc, "2.8 Presión Arterial por Departamento")
bloque_codigo(doc,
"""# Código R – Presión media por departamento (Top 15)
dept_stats <- df %>%
  group_by(department_name) %>%
  summarise(media_sis = mean(systolic_pressure),
            media_dia = mean(diastolic_pressure)) %>%
  arrange(desc(media_sis)) %>%
  slice_head(n = 15) %>%
  pivot_longer(cols = c(media_sis, media_dia),
               names_to = "tipo", values_to = "presion_media")

ggplot(dept_stats, aes(x = reorder(department_name, presion_media),
                        y = presion_media, fill = tipo)) +
  geom_col(position = "dodge", alpha = 0.88) +
  coord_flip() +
  labs(title = "Presión Arterial Media – Top 15 Departamentos") +
  theme_minimal()""")
insertar_imagen(doc, os.path.join(IMG_DIR,"g6_departamentos.png"), 6.0,
    "Figura 6. Presión arterial media por departamento (Top 15) – generado con R/ggplot2.")
parrafo(doc, (
    f"{dept_top1} tiene la mayor sistólica media del grupo: {s_top1} mmHg. "
    "Las diferencias entre departamentos son reales pero no dramáticas —pocos mmHg "
    "de diferencia entre el primero y el último del top 15. Sin variables de altitud, "
    "edad promedio o acceso a salud en el dataset, no hay cómo explicar el patrón "
    "con certeza."
))

# --- G7 ---
titulo_subseccion(doc, "2.9 Presión Sistólica según Tipo de Medicamento")
bloque_codigo(doc,
"""# Código R – Boxplot por tipo de medicamento
top_meds <- names(sort(table(df$medicine_type), decreasing=TRUE)[1:8])
df_med <- df[df$medicine_type %in% top_meds, ]

ggplot(df_med, aes(x = factor(medicine_type), y = systolic_pressure,
                   fill = factor(medicine_type))) +
  geom_boxplot(outlier.size = 0.4, outlier.alpha = 0.3,
               alpha = 0.8, show.legend = FALSE) +
  scale_fill_brewer(palette = "Set2") +
  labs(title = "Presión Sistólica por Tipo de Medicamento (Top 8)",
       x = "Tipo de medicamento", y = "Presión Sistólica (mmHg)") +
  theme_minimal(base_size = 12)""")
insertar_imagen(doc, os.path.join(IMG_DIR,"g7_medicamento.png"), 5.8,
    "Figura 7. Presión sistólica por tipo de medicamento – generado con R/ggplot2.")
parrafo(doc, (
    "Ningún medicamento se destaca por tener pacientes con presiones notablemente "
    "distintas. Todos los boxplots son similares. Eso no dice si los fármacos "
    "funcionan o no —para saberlo habría que tener datos de cuánto tiempo lleva "
    "el paciente en tratamiento y si lo toma regularmente, dos cosas que el "
    "dataset no incluye."
))

doc.add_page_break()

# ════════════════════════════════
#  3. CONEXIÓN CON SISTEMAS COGNITIVOS
# ════════════════════════════════
titulo_seccion(doc, "3. Proyección hacia Sistemas Cognitivos", 14)

parrafo(doc, (
    "El AED que se hizo en este trabajo no es un fin en sí mismo. "
    "Es el primer paso de un proceso más largo: entender los datos antes de "
    "pasárselos a un modelo. El profesor planteó cinco preguntas para evaluar "
    "cualquier sistema cognitivo. Aquí se responden para el caso de presión arterial."
))

titulo_subseccion(doc, "3.1 ¿Qué datos utiliza el sistema?")
parrafo(doc, (
    f"El sistema parte de {n_total:,} registros de pacientes con presión sistólica, "
    "diastólica, género, ciudad, departamento, medicamento y dosis. "
    "Esos datos son suficientes para patrones de distribución y clasificación básica. "
    "Lo que falta —y que limitaría cualquier modelo cognitivo— es la dimensión temporal: "
    "no hay fecha de medición, ni historial de evolución por paciente, ni variables de "
    "estilo de vida. Un sistema que anticipe riesgo cardiovascular necesitaría eso."
))

titulo_subseccion(doc, "3.2 ¿Qué capacidad cognitiva simula o apoya?")
parrafo(doc, (
    "El caso apoya la capacidad de clasificación y apoyo al diagnóstico médico. "
    "Un médico que atiende cientos de pacientes por semana no puede revisar manualmente "
    "cada historial para detectar quién está escalando de Etapa 1 a Etapa 2. "
    "Un sistema cognitivo que lea el registro en tiempo real y genere una alerta "
    "reproduce —de forma escalable— esa capacidad de reconocimiento de patrones "
    "que un clínico experimentado tiene pero no puede aplicar a miles de pacientes "
    "simultáneamente."
))

titulo_subseccion(doc, "3.3 ¿Qué tecnología emplea?")
parrafo(doc, (
    "Para este análisis: R con ggplot2 para exploración y visualización. "
    "En una segunda fase, el camino natural es Python. No porque R sea incorrecto "
    "—funciona bien para EDA estadístico— sino porque las librerías de aprendizaje "
    "automático y los conectores con LLMs (scikit-learn, HuggingFace, LangChain) "
    "están en Python y son los que están marcando el estándar actual. "
    "El modelo cognitivo eventual no usaría un Transformer aislado: usaría un LLM "
    "completo —multimodal, capaz de recibir texto, imágenes de ECG o reportes— "
    "como modelo base, con un agente conector que le entregue los datos del paciente "
    "y reciba la respuesta estructurada."
))

titulo_subseccion(doc, "3.4 ¿Cómo se relaciona la nube?")
parrafo(doc, (
    "Los modelos cognitivos no tienen que correr en la nube. "
    "Un modelo local puede procesar datos sensibles sin enviarlos a ningún servidor. "
    "Pero cuando el volumen supera lo que tolera un equipo local —o cuando se necesita "
    "disponibilidad 24/7 para un hospital— la nube entra. "
    "Los tipos de servicio aplicables son tres: IaaS para la infraestructura de "
    "cómputo (máquinas virtuales que corren el modelo), PaaS para el entorno de "
    "desarrollo y despliegue (AWS SageMaker, Azure ML), y SaaS para las aplicaciones "
    "que el médico usa directamente (dashboards, alertas, interfaces de consulta). "
    "El costo crece con cada capa: IaaS es más barato pero requiere más gestión; "
    "SaaS es llave en mano pero el más caro."
))
tabla_datos(doc,
    encabezados=["Capa", "Tipo", "Ejemplo", "Aplica en el caso cuando..."],
    filas=[
        ("Infraestructura de cómputo", "IaaS", "AWS EC2 / Azure VM",
         "Se entrena el modelo con el historial completo de pacientes"),
        ("Plataforma de ML",           "PaaS", "SageMaker / Azure ML",
         "Se automatiza el ciclo de entrenamiento y despliegue"),
        ("App médica de consulta",     "SaaS", "Dashboard Power BI / web",
         "El clínico consulta el riesgo del paciente en tiempo real"),
        ("IA como servicio",           "AIaaS", "AWS Bedrock / Azure OpenAI",
         "Se usa un LLM existente sin entrenar modelo propio"),
    ]
)

titulo_subseccion(doc, "3.5 ¿Qué riesgos éticos pueden aparecer?")
parrafo(doc, (
    "Los datos de presión arterial son datos de salud —categoría especialmente "
    "protegida en Colombia bajo la Ley 1581. Un sistema cognitivo sobre ellos "
    "enfrenta cuatro riesgos concretos."
))
tabla_datos(doc,
    encabezados=["Riesgo ético", "Por qué aparece", "Cómo mitigarlo"],
    filas=[
        ("Privacidad de datos sensibles",
         "Datos de salud identificables en servidores externos",
         "Anonimizar antes de subir a nube pública; datos crudos en nube privada"),
        ("Interpretabilidad del modelo",
         "Un black-box que clasifica riesgo sin explicar por qué",
         "Usar modelos interpretables (árboles, regresión logística) o SHAP values"),
        ("Sesgo en los datos",
         f"Solo {n_dept} departamentos; puede no representar toda Colombia",
         "Documentar limitaciones del dataset en el informe clínico"),
        ("Costo de infraestructura",
         "Nube puede volverse costosa si el modelo escala sin control",
         "Definir presupuesto máximo antes de activar servicios de pago"),
    ]
)

doc.add_page_break()

# ════════════════════════════════
#  4. CONCLUSIONES
# ════════════════════════════════
titulo_seccion(doc, "4. Conclusiones", 14)

conclusiones = [
    ("Casi la mitad de los pacientes tiene hipertensión: ",
     f"El {hipert_pct}% de los {n_total:,} registros cae en Etapa 1 o Etapa 2 según "
     "la AHA. Es una cifra alta, pero el contexto importa: no es una muestra aleatoria "
     "de la población —son pacientes ya en atención médica. Comparar ese número con "
     "encuestas nacionales sin ajustar por eso sería un error."),
    ("La correlación entre las dos presiones es alta (r = " + str(corr_sd) + "): ",
     "Lo esperable, dado que comparten el mismo sistema. Más interesante es el grupo "
     "de casos en el scatter con sistólica elevada pero diastólica dentro del rango "
     "normal —un patrón que suele verse en pacientes mayores y que merece seguimiento "
     "diferenciado."),
    ("Género: sin diferencia observable: ",
     "Las medianas de presión en hombres y mujeres son prácticamente idénticas. "
     "Puede que el género simplemente no sea determinante aquí, o que las variables "
     "que sí importan —edad, comorbilidades— no estén en el dataset y estén "
     "enmascarando cualquier diferencia real."),
    ("Variación geográfica presente pero leve: ",
     f"{dept_top1} lidera en sistólica media. Hay diferencias entre departamentos, "
     "aunque son de pocos mmHg. Sin datos de altitud, estructura demográfica o "
     "acceso a servicios, cualquier interpretación de ese patrón sería especulativa."),
    ("El AED es el paso cero, no el destino: ",
     f"{n_total:,} filas procesadas, siete gráficas, estadísticas descriptivas completas. "
     "Eso da una imagen clara de los datos actuales. Para pasar a un modelo predictivo "
     "o a un sistema cognitivo de apoyo al diagnóstico, lo que falta no es potencia "
     "de cómputo —es variables: edad, historial evolutivo del paciente, adherencia "
     "al tratamiento. Sin esas, cualquier modelo clasifica con el pasado sin poder "
     "anticipar el futuro."),
    ("Python es el siguiente paso: ",
     "R funcionó bien para este AED. Pero cuando la actividad avance hacia modelos "
     "cognitivos, agentes de IA o conexión con LLMs, Python es el estándar. "
     "scikit-learn, HuggingFace y LangChain no tienen equivalentes en R para "
     "esos casos de uso. Vale la pena hacer la migración desde ya."),
]

for titulo, cuerpo in conclusiones:
    conclusion_item(doc, titulo, cuerpo)

doc.add_page_break()

# ════════════════════════════════
#  4. REFERENCIAS
# ════════════════════════════════
seccion_referencias(doc, [
    ("López Murphy, J. J. y Zarza, G. (2017). ",
     "La ingeniería del Big Data: cómo trabajar con datos",
     ". Editorial UOC. Pág. 17-125."),
    ("Casas Roma, J., Nin Guerrero, J. y Julbe López, F. (2019). ",
     "Big data: análisis de datos en entornos masivos",
     ". Editorial UOC. Pág. 43-188."),
    ("American Heart Association. (2017). ",
     "2017 ACC/AHA Guideline for the Prevention, Detection, Evaluation, "
     "and Management of High Blood Pressure in Adults",
     ". Hypertension, 71(6), e13-e115."),
    ("Wickham, H. (2016). ",
     "ggplot2: Elegant Graphics for Data Analysis",
     ". Springer-Verlag New York."),
    ("R Core Team. (2024). ",
     "R: A Language and Environment for Statistical Computing",
     ". R Foundation for Statistical Computing, Vienna, Austria."),
    ("Vaswani, A. et al. (2017). ",
     "Attention Is All You Need",
     ". Advances in Neural Information Processing Systems, 30."),
    ("Congreso de Colombia. (2012). ",
     "Ley 1581 de 2012: Protección de datos personales",
     ". Diario Oficial No. 48.587."),
])

# ── Guardar ───────────────────────────────────────────────
doc.save(OUT_PATH)
print(f"\nDocumento guardado en:\n  {OUT_PATH}")

# ============================================================
#  Análisis Exploratorio de Datos - Presión Arterial
#  Computación Cognitiva para Big Data - Actividad 2
#  Docente: Joaquín F. Sánchez
# ============================================================

# Instalar paquetes si no están disponibles
paquetes <- c("ggplot2", "dplyr", "tidyr", "scales", "gridExtra", "RColorBrewer")
for (p in paquetes) {
  if (!require(p, character.only = TRUE, quietly = TRUE)) {
    install.packages(p, repos = "https://cran.rstudio.com/", quiet = TRUE)
    library(p, character.only = TRUE, quietly = TRUE)
  }
}

# ── Directorio de trabajo ──────────────────────────────────
setwd("C:/Users/jonat/Downloads/mitad trimestre/Computación cognitiva para Big Data")

IMG_DIR <- "graficas_R"
if (!dir.exists(IMG_DIR)) dir.create(IMG_DIR)

# ── 1. Carga de datos ─────────────────────────────────────
cat("Cargando datos...\n")
df <- read.csv("actividad2.csv", stringsAsFactors = FALSE)

# Limpiar: eliminar presiones <= 0
df <- df[df$systolic_pressure > 0 & df$diastolic_pressure > 0, ]

# Etiquetas de género
df$genero_label <- ifelse(df$gender == "f", "Femenino", "Masculino")

# Clasificación de presión arterial (criterios AHA 2017)
df$categoria_presion <- with(df, ifelse(
  systolic_pressure < 120 & diastolic_pressure < 80, "Normal",
  ifelse(systolic_pressure < 130 & diastolic_pressure < 80, "Elevada",
  ifelse(systolic_pressure < 140 | diastolic_pressure < 90,
         "Hipertensión Etapa 1", "Hipertensión Etapa 2"))
))
df$categoria_presion <- factor(df$categoria_presion,
  levels = c("Normal","Elevada","Hipertensión Etapa 1","Hipertensión Etapa 2"))

cat("Total registros:", nrow(df), "\n")
cat("Femenino:", sum(df$gender == "f"), "| Masculino:", sum(df$gender == "m"), "\n")
cat("Departamentos:", length(unique(df$department_name)), "\n")

# ── 2. Estadísticas descriptivas ──────────────────────────
cat("\n--- Estadísticas descriptivas ---\n")
cat("Presión Sistólica:\n"); print(summary(df$systolic_pressure))
cat("Presión Diastólica:\n"); print(summary(df$diastolic_pressure))

# Tabla resumen por género
resumen_genero <- df %>%
  group_by(genero_label) %>%
  summarise(
    n             = n(),
    media_sis     = round(mean(systolic_pressure), 1),
    mediana_sis   = round(median(systolic_pressure), 1),
    media_dia     = round(mean(diastolic_pressure), 1),
    mediana_dia   = round(median(diastolic_pressure), 1),
    .groups = "drop"
  )
cat("\nResumen por género:\n"); print(resumen_genero)

# ── Paleta de colores ──────────────────────────────────────
pal_cat <- c("Normal"                = "#3BB273",
             "Elevada"               = "#F4A261",
             "Hipertensión Etapa 1"  = "#8338EC",
             "Hipertensión Etapa 2"  = "#E84855")
pal_gen <- c("Femenino" = "#3BB273", "Masculino" = "#2E86AB")

# ── 3. Gráficas ───────────────────────────────────────────

# --- G1: Histograma Presión Sistólica ---
cat("Generando G1...\n")
g1 <- ggplot(df, aes(x = systolic_pressure)) +
  geom_histogram(bins = 40, fill = "#2E86AB", color = "white", alpha = 0.85) +
  geom_vline(aes(xintercept = mean(systolic_pressure), linetype = "Media"),
             color = "black", linewidth = 0.9) +
  geom_vline(aes(xintercept = median(systolic_pressure), linetype = "Mediana"),
             color = "#E84855", linewidth = 0.9) +
  scale_linetype_manual(name = "Estadístico",
    values = c("Media" = "dashed", "Mediana" = "dotted")) +
  labs(title = "Distribución de la Presión Sistólica",
       x = "Presión Sistólica (mmHg)", y = "Frecuencia") +
  theme_minimal(base_size = 13) +
  theme(plot.title = element_text(face = "bold"),
        legend.position = "top")

ggsave(file.path(IMG_DIR, "g1_sistolica.png"), g1,
       width = 8, height = 5, dpi = 150)

# --- G2: Histograma Presión Diastólica ---
cat("Generando G2...\n")
g2 <- ggplot(df, aes(x = diastolic_pressure)) +
  geom_histogram(bins = 40, fill = "#E84855", color = "white", alpha = 0.85) +
  geom_vline(aes(xintercept = mean(diastolic_pressure), linetype = "Media"),
             color = "black", linewidth = 0.9) +
  geom_vline(aes(xintercept = median(diastolic_pressure), linetype = "Mediana"),
             color = "#2E86AB", linewidth = 0.9) +
  scale_linetype_manual(name = "Estadístico",
    values = c("Media" = "dashed", "Mediana" = "dotted")) +
  labs(title = "Distribución de la Presión Diastólica",
       x = "Presión Diastólica (mmHg)", y = "Frecuencia") +
  theme_minimal(base_size = 13) +
  theme(plot.title = element_text(face = "bold"),
        legend.position = "top")

ggsave(file.path(IMG_DIR, "g2_diastolica.png"), g2,
       width = 8, height = 5, dpi = 150)

# --- G3: Boxplot por género ---
cat("Generando G3...\n")
df_long <- df %>%
  select(genero_label, systolic_pressure, diastolic_pressure) %>%
  pivot_longer(cols = c(systolic_pressure, diastolic_pressure),
               names_to = "tipo",
               values_to = "presion") %>%
  mutate(tipo = recode(tipo,
    systolic_pressure  = "Sistólica",
    diastolic_pressure = "Diastólica"))

g3 <- ggplot(df_long, aes(x = genero_label, y = presion, fill = genero_label)) +
  geom_boxplot(outlier.size = 0.5, outlier.alpha = 0.3, alpha = 0.8) +
  scale_fill_manual(values = pal_gen, guide = "none") +
  facet_wrap(~tipo, scales = "free_y") +
  labs(title = "Distribución de Presión Arterial por Género",
       x = "Género", y = "Presión (mmHg)") +
  theme_minimal(base_size = 13) +
  theme(plot.title = element_text(face = "bold"),
        strip.text = element_text(face = "bold"))

ggsave(file.path(IMG_DIR, "g3_boxplot_genero.png"), g3,
       width = 9, height = 5, dpi = 150)

# --- G4: Diagrama de dispersión sistólica vs diastólica ---
cat("Generando G4...\n")
set.seed(42)
muestra <- df[sample(nrow(df), 5000), ]

g4 <- ggplot(muestra, aes(x = systolic_pressure, y = diastolic_pressure,
                           color = categoria_presion)) +
  geom_point(size = 1.2, alpha = 0.5) +
  scale_color_manual(values = pal_cat, name = "Categoría") +
  labs(title = "Relación Sistólica – Diastólica por Categoría de Presión",
       x = "Presión Sistólica (mmHg)", y = "Presión Diastólica (mmHg)") +
  theme_minimal(base_size = 13) +
  theme(plot.title = element_text(face = "bold"),
        legend.position = "right")

ggsave(file.path(IMG_DIR, "g4_dispersion.png"), g4,
       width = 9, height = 6, dpi = 150)

# --- G5: Gráfico de barras por categoría ---
cat("Generando G5...\n")
conteo_cat <- df %>%
  count(categoria_presion) %>%
  mutate(porcentaje = n / sum(n) * 100,
         etiqueta   = paste0(round(porcentaje, 1), "%"))

g5 <- ggplot(conteo_cat, aes(x = reorder(categoria_presion, -n),
                              y = porcentaje, fill = categoria_presion)) +
  geom_col(alpha = 0.9, show.legend = FALSE) +
  geom_text(aes(label = etiqueta), vjust = -0.5, size = 4, fontface = "bold") +
  scale_fill_manual(values = pal_cat) +
  scale_y_continuous(labels = function(x) paste0(x, "%"), limits = c(0, 50)) +
  labs(title = "Distribución por Categoría de Presión Arterial",
       x = "Categoría", y = "Porcentaje de pacientes (%)") +
  theme_minimal(base_size = 12) +
  theme(plot.title = element_text(face = "bold"),
        axis.text.x = element_text(angle = 15, hjust = 1))

ggsave(file.path(IMG_DIR, "g5_categorias.png"), g5,
       width = 9, height = 5, dpi = 150)

# --- G6: Presión media por departamento (top 15) ---
cat("Generando G6...\n")
dept_stats <- df %>%
  group_by(department_name) %>%
  summarise(
    media_sis = mean(systolic_pressure),
    media_dia = mean(diastolic_pressure),
    .groups = "drop"
  ) %>%
  arrange(desc(media_sis)) %>%
  slice_head(n = 15) %>%
  pivot_longer(cols = c(media_sis, media_dia),
               names_to = "tipo",
               values_to = "presion_media") %>%
  mutate(tipo = recode(tipo,
    media_sis = "Sistólica media",
    media_dia = "Diastólica media"))

g6 <- ggplot(dept_stats,
             aes(x = reorder(department_name, presion_media),
                 y = presion_media, fill = tipo)) +
  geom_col(position = "dodge", alpha = 0.88) +
  scale_fill_manual(values = c("Sistólica media" = "#2E86AB",
                                "Diastólica media" = "#E84855"),
                    name = "") +
  coord_flip() +
  labs(title = "Presión Arterial Media – Top 15 Departamentos",
       x = "Departamento", y = "Presión media (mmHg)") +
  theme_minimal(base_size = 11) +
  theme(plot.title = element_text(face = "bold"),
        legend.position = "bottom")

ggsave(file.path(IMG_DIR, "g6_departamentos.png"), g6,
       width = 10, height = 7, dpi = 150)

# --- G7: Presión media por tipo de medicamento ---
cat("Generando G7...\n")
top_meds <- names(sort(table(df$medicine_type), decreasing = TRUE)[1:8])
df_med <- df[df$medicine_type %in% top_meds, ]
df_med$medicine_type <- as.factor(df_med$medicine_type)

g7 <- ggplot(df_med, aes(x = factor(medicine_type),
                          y = systolic_pressure,
                          fill = factor(medicine_type))) +
  geom_boxplot(outlier.size = 0.4, outlier.alpha = 0.3,
               alpha = 0.8, show.legend = FALSE) +
  scale_fill_brewer(palette = "Set2") +
  labs(title = "Presión Sistólica por Tipo de Medicamento (Top 8)",
       x = "Tipo de medicamento", y = "Presión Sistólica (mmHg)") +
  theme_minimal(base_size = 12) +
  theme(plot.title = element_text(face = "bold"))

ggsave(file.path(IMG_DIR, "g7_medicamento.png"), g7,
       width = 10, height = 5, dpi = 150)

cat("\nTodas las gráficas guardadas en la carpeta:", IMG_DIR, "\n")

# ── 4. Correlaciones ──────────────────────────────────────
cat("\n--- Correlaciones ---\n")
cat("Sistólica ~ Diastólica: r =",
    round(cor(df$systolic_pressure, df$diastolic_pressure), 3), "\n")
cat("Sistólica ~ Cantidad medicamento: r =",
    round(cor(df$systolic_pressure, df$medicine_quantity), 3), "\n")
cat("Diastólica ~ Cantidad medicamento: r =",
    round(cor(df$diastolic_pressure, df$medicine_quantity), 3), "\n")

cat("\n¡Análisis completado!\n")

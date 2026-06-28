import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from jinja2 import Template

from src.config import get_settings

logger = logging.getLogger(__name__)

PROMPT_VERSION = "1.0"
MODEL_NAME = "gemini-2.0-flash"

SYSTEM_PROMPT = """Eres un analista de visibilidad de marca trabajando para Coca-Cola.
Redacta un informe de marketing profesional y basado en datos usando SOLO las métricas proporcionadas.
NO inventes cifras. Sé conciso y accionable.
Usa la perspectiva del cliente Coca-Cola — el cliente compite contra Pepsi."""

REPORT_TEMPLATE = Template("""\
# BrandSight — Informe de Visibilidad Coca-Cola

**Vídeo:** {{ video_filename }}
**Duración:** {{ duration_sec }}s
**Generado:** {{ generated_at }}
**Cliente:** {{ client }}

---

## Resumen Ejecutivo
{% if balance_label == "coca_cola_dominant" %}
Coca-Cola dominó el tiempo en pantalla con {{ coca_cola.visible_seconds }}s de presencia de marca visible ({{ coca_cola.visibility_pct }}% del total del vídeo), superando a Pepsi por {{ visibility_gap_sec }}s.
{% elif balance_label == "pepsi_dominant" %}
Pepsi lideró el tiempo en pantalla con {{ pepsi.visible_seconds }}s de presencia de marca visible ({{ pepsi.visibility_pct }}% del total del vídeo), por delante de Coca-Cola por {{ visibility_gap_sec }}s. Se recomienda acción.
{% else %}
{% if dominant_brand == "pepsi" %}
Pepsi lideró ligeramente el tiempo en pantalla ({{ pepsi.visible_seconds }}s, {{ pepsi.visibility_pct }}%) frente a Coca-Cola ({{ coca_cola.visible_seconds }}s, {{ coca_cola.visibility_pct }}%). La diferencia ({{ visibility_gap_sec }}s) es menor al umbral de equilibrio — competencia muy reñida.
{% elif dominant_brand == "coca_cola" %}
Coca-Cola lideró ligeramente el tiempo en pantalla ({{ coca_cola.visible_seconds }}s, {{ coca_cola.visibility_pct }}%) frente a Pepsi ({{ pepsi.visible_seconds }}s, {{ pepsi.visibility_pct }}%). La diferencia ({{ visibility_gap_sec }}s) es menor al umbral de equilibrio — competencia muy reñida.
{% else %}
Ambas marcas estuvieron prácticamente equilibradas. Coca-Cola: {{ coca_cola.visible_seconds }}s ({{ coca_cola.visibility_pct }}%). Pepsi: {{ pepsi.visible_seconds }}s ({{ pepsi.visibility_pct }}%). Diferencia: {{ visibility_gap_sec }}s.
{% endif %}
{% endif %}

## Visibilidad de Coca-Cola
- **Segundos visibles:** {{ coca_cola.visible_seconds }}s
- **Porcentaje de visibilidad:** {{ coca_cola.visibility_pct }}%
- **Número de detecciones:** {{ coca_cola.detection_count }}
- **Confianza media:** {{ "%.1f"|format(coca_cola.avg_confidence * 100) }}%

## Visibilidad Competitiva de Pepsi
- **Segundos visibles:** {{ pepsi.visible_seconds }}s
- **Porcentaje de visibilidad:** {{ pepsi.visibility_pct }}%
- **Número de detecciones:** {{ pepsi.detection_count }}
- **Confianza media:** {{ "%.1f"|format(pepsi.avg_confidence * 100) }}%

## Comparativa Competitiva
| Métrica | Coca-Cola | Pepsi | Diferencia |
|---------|-----------|-------|------------|
| Visibilidad (s) | {{ coca_cola.visible_seconds }} | {{ pepsi.visible_seconds }} | {{ visibility_gap_sec }} |
| Visibilidad (%) | {{ coca_cola.visibility_pct }} | {{ pepsi.visibility_pct }} | {{ "%.1f"|format(coca_cola.visibility_pct - pepsi.visibility_pct) }} |
| Detecciones | {{ coca_cola.detection_count }} | {{ pepsi.detection_count }} | — |

**Marca dominante:** {{ dominant_brand }}
**Balance:** {{ balance_label }}

## Insights de Marketing
{% if balance_label == "coca_cola_dominant" %}
- La presencia de marca de Coca-Cola es sólida; mantener el posicionamiento actual en patrocinios.
- Seguir invirtiendo en los tipos de escenas donde Coca-Cola lidera (eventos deportivos, primeros planos, tomas de público).
- Monitorizar la visibilidad de Pepsi en nuevas categorías de contenido como alerta temprana de cambios competitivos.
{% elif balance_label == "pepsi_dominant" %}
- La mayor visibilidad de Pepsi requiere atención inmediata — revisar los contratos de patrocinio para este tipo de contenido.
- Considerar aumentar los activos de marca Coca-Cola (pancartas, neveras, equipamiento de atletas) en momentos de alta exposición.
- Analizar las marcas de tiempo específicas donde Pepsi lidera y atacar esas ubicaciones.
{% else %}
{% if dominant_brand == "pepsi" %}
- Pepsi lidera por un margen estrecho — vigilar de cerca este segmento y reforzar la presencia de Coca-Cola antes de que la brecha crezca.
- Centrarse en los momentos donde Pepsi aparece y buscar mayor visibilidad o exclusividad de Coca-Cola.
- Hacer seguimiento de esta métrica a lo largo del tiempo; la tendencia actual favorece a Pepsi.
{% elif dominant_brand == "coca_cola" %}
- Coca-Cola lidera por un margen estrecho — una pequeña inversión podría consolidar la ventaja frente a Pepsi.
- Centrarse en los momentos donde ambas marcas aparecen y buscar exclusividad o mayor presencia de Coca-Cola.
- Hacer seguimiento de esta métrica a lo largo del tiempo; una tendencia hacia el dominio de Pepsi sería una señal de alerta temprana.
{% else %}
- El terreno de juego está nivelado — una inversión focalizada podría inclinar la balanza a favor de Coca-Cola.
- Centrarse en los momentos donde ambas marcas aparecen y buscar exclusividad o mayor presencia de Coca-Cola.
- Hacer seguimiento de esta métrica a lo largo del tiempo para detectar cambios competitivos.
{% endif %}
{% endif %}

## Recomendación
{% if balance_label == "coca_cola_dominant" %}
Reforzar las ubicaciones ganadoras. La estrategia actual de Coca-Cola está dando resultados — proteger y expandir.
{% elif balance_label == "pepsi_dominant" %}
Aumentar la visibilidad de marca Coca-Cola en este segmento de contenido, priorizando los momentos donde Pepsi lidera según las métricas anteriores.
{% else %}
{% if dominant_brand == "pepsi" %}
Reforzar la visibilidad de Coca-Cola en este segmento: Pepsi lidera por poco y la competencia está muy reñida.
{% elif dominant_brand == "coca_cola" %}
Consolidar la ligera ventaja actual de Coca-Cola con inversión en ubicaciones donde ya lidera.
{% else %}
Invertir en ubicación diferenciada para crear una ventaja clara de Coca-Cola frente al equilibrio actual entre ambas marcas.
{% endif %}
{% endif %}

---
*Informe generado por BrandSight AI · Modelo: {{ model_name }}*
""")


def _generar_respaldo(payload: dict) -> str:
    """Plantilla Jinja2 de respaldo cuando la API LLM no está disponible."""
    return REPORT_TEMPLATE.render(
        **payload,
        generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        model_name="jinja2-respaldo",
    )


def _generar_con_gemini(payload: dict, api_key: str) -> tuple[str, str]:
    """Llama a la API de Gemini con las métricas y devuelve (texto_informe, nombre_modelo)."""
    import google.generativeai as genai

    genai.configure(api_key=api_key)

    prompt = f"""\
Métricas de Visibilidad BrandSight:
- Vídeo: {payload['video_filename']} ({payload['duration_sec']}s)
- Coca-Cola: {payload['coca_cola']['visible_seconds']}s ({payload['coca_cola']['visibility_pct']}%)
  Detecciones: {payload['coca_cola']['detection_count']} · Confianza media: {payload['coca_cola']['avg_confidence']}
- Pepsi: {payload['pepsi']['visible_seconds']}s ({payload['pepsi']['visibility_pct']}%)
  Detecciones: {payload['pepsi']['detection_count']} · Confianza media: {payload['pepsi']['avg_confidence']}
- Marca dominante: {payload['dominant_brand']}
- Balance: {payload['balance_label']} (diferencia: {payload['visibility_gap_sec']}s)

Redacta un informe de marketing conciso con estas secciones:
1. Resumen Ejecutivo
2. Visibilidad de Coca-Cola
3. Visibilidad Competitiva de Pepsi
4. Comparativa Competitiva
5. Insights de Marketing (2-3 viñetas)
6. Recomendación para Coca-Cola

Usa perspectiva del cliente Coca-Cola. Tono profesional. NO inventes cifras. El informe debe estar en español."""

    modelo = genai.GenerativeModel(MODEL_NAME, system_instruction=SYSTEM_PROMPT)
    respuesta = modelo.generate_content(
        contents=[prompt],
        generation_config={
            "temperature": 0.3,
            "max_output_tokens": 800,
        },
    )
    return respuesta.text, MODEL_NAME


def generate_marketing_report(payload: dict) -> tuple[str, str]:
    """Genera un informe a partir de los datos de visibilidad.

    Args:
        payload: Diccionario con las claves:
            video_filename, duration_sec, client, competitor,
            coca_cola (dict), pepsi (dict), dominant_brand,
            visibility_gap_sec, balance_label.

    Returns:
        (texto_informe, nombre_modelo) — nombre_modelo será "jinja2-respaldo"
        si la llamada a la API falla.
    """
    config = get_settings()
    api_key = config.gemini_api_key

    if api_key:
        try:
            logger.info("Llamando a Gemini para el informe de marketing…")
            return _generar_con_gemini(payload, api_key)
        except Exception as exc:
            logger.warning("Fallo en la llamada a Gemini — usando plantilla Jinja2 de respaldo: %s", exc)

    logger.info("Usando plantilla Jinja2 de respaldo para el informe.")
    return _generar_respaldo(payload), "jinja2-respaldo"


def save_report_to_file(
    video_id: int,
    report_text: str,
    output_dir: Optional[Path] = None,
) -> Path:
    """Guarda el informe markdown en ``data/outputs/report_{video_id}.md``."""
    config = get_settings()
    config.ensure_dirs()
    out_dir = output_dir or config.outputs_dir
    report_path = out_dir / f"report_{video_id}.md"
    report_path.write_text(report_text, encoding="utf-8")
    return report_path

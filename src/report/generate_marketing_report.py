import json
from pathlib import Path

from jinja2 import Template

from src.config import get_settings

PROMPT_VERSION = "v1"

SYSTEM_PROMPT = (
    "You are a brand visibility analyst working for Coca-Cola. "
    "Write a concise marketing report using only the provided metrics. "
    "Be professional and data-driven. Do not invent numbers."
)

REPORT_TEMPLATE = Template("""# BrandSight Marketing Report

## Executive Summary
Video **{{ video_filename }}** ({{ duration_sec }}s) shows Coca-Cola at **{{ coca_cola.visibility_pct }}%** screen time ({{ coca_cola.visible_seconds }}s) vs Pepsi at **{{ pepsi.visibility_pct }}%** ({{ pepsi.visible_seconds }}s). Dominant brand: **{{ dominant_brand }}**.

## Coca-Cola Visibility
- Screen time: {{ coca_cola.visible_seconds }}s ({{ coca_cola.visibility_pct }}%)
- Detections: {{ coca_cola.detection_count }}
- Avg confidence: {{ coca_cola.avg_confidence }}

## Pepsi Competitive Visibility
- Screen time: {{ pepsi.visible_seconds }}s ({{ pepsi.visibility_pct }}%)
- Detections: {{ pepsi.detection_count }}
- Avg confidence: {{ pepsi.avg_confidence }}

## Competitive Comparison
Visibility gap: **{{ visibility_gap_sec }}s**. Balance: **{{ balance_label }}**.

## Marketing Insights
- Coca-Cola's share of visible time is {{ coca_cola.visibility_pct }}% in this placement.
- Pepsi appears {{ pepsi.visibility_pct }}% of the video duration.
- Gap of {{ visibility_gap_sec }}s may indicate stronger presence for {{ dominant_brand }}.

## Recommendation for Coca-Cola
{% if balance_label == 'coca_cola_dominant' %}
Maintain current placement strategy; Coca-Cola leads visibility in this clip. Consider reinforcing high-visibility moments in future campaigns.
{% elif balance_label == 'pepsi_dominant' %}
Pepsi leads visibility in this clip. Recommend increasing Coca-Cola logo size, duration, or placement in similar content.
{% else %}
Visibility is balanced. Consider targeted boosts to Coca-Cola presence in key frames to gain competitive edge.
{% endif %}
""")


def _generate_with_gemini(metrics: dict) -> tuple[str, str]:
    import google.generativeai as genai

    settings = get_settings()
    genai.configure(api_key=settings.gemini_api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")
    user_prompt = (
        "Analyze this video visibility data and produce a report with sections: "
        "Executive Summary, Coca-Cola Visibility, Pepsi Competitive Visibility, "
        "Competitive Comparison, Marketing Insights, Recommendation for Coca-Cola.\n\n"
        f"Data:\n{json.dumps(metrics, indent=2)}"
    )
    response = model.generate_content([SYSTEM_PROMPT, user_prompt])
    return response.text, "gemini-2.0-flash"


def _generate_with_openai(metrics: dict) -> tuple[str, str]:
    from openai import OpenAI

    settings = get_settings()
    client = OpenAI(api_key=settings.openai_api_key)
    user_prompt = (
        "Analyze this video visibility data and produce a report with sections: "
        "Executive Summary, Coca-Cola Visibility, Pepsi Competitive Visibility, "
        "Competitive Comparison, Marketing Insights, Recommendation for Coca-Cola.\n\n"
        f"Data:\n{json.dumps(metrics, indent=2)}"
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content or "", "gpt-4o-mini"


def generate_marketing_report(metrics: dict, *, use_llm: bool = True) -> tuple[str, str]:
    settings = get_settings()

    if use_llm and settings.gemini_api_key:
        try:
            return _generate_with_gemini(metrics)
        except Exception:
            pass

    if use_llm and settings.openai_api_key:
        try:
            return _generate_with_openai(metrics)
        except Exception:
            pass

    return REPORT_TEMPLATE.render(**metrics), "template-fallback"


def save_report_to_file(video_id: int, report_text: str, outputs_dir: Path | None = None) -> Path:
    settings = get_settings()
    out_dir = outputs_dir or settings.outputs_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"report_video_{video_id}.md"
    path.write_text(report_text, encoding="utf-8")
    return path

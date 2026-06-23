import unittest
from unittest.mock import patch

from src.config import Settings
from src.report.generate_marketing_report import generate_marketing_report

SAMPLE_PAYLOAD = {
    "video_filename": "demo.mp4",
    "duration_sec": 30.0,
    "client": "Coca-Cola",
    "competitor": "Pepsi",
    "coca_cola": {
        "visible_seconds": 12.5,
        "visibility_pct": 41.7,
        "detection_count": 8,
        "avg_confidence": 0.91,
        "brand": "coca_cola",
    },
    "pepsi": {
        "visible_seconds": 9.0,
        "visibility_pct": 30.0,
        "detection_count": 6,
        "avg_confidence": 0.88,
        "brand": "pepsi",
    },
    "dominant_brand": "coca_cola",
    "visibility_gap_sec": 3.5,
    "balance_label": "coca_cola_dominant",
}


class TestMarketingReportFallback(unittest.TestCase):
    @patch("src.report.generate_marketing_report.get_settings")
    def test_fallback_without_api_key(self, mock_get_settings):
        mock_get_settings.return_value = Settings(gemini_api_key="")

        report_text, model_name = generate_marketing_report(SAMPLE_PAYLOAD)

        self.assertEqual(model_name, "jinja2-respaldo")
        self.assertIn("12.5", report_text)
        self.assertIn("41.7", report_text)
        self.assertIn("jinja2-respaldo", report_text)


if __name__ == "__main__":
    unittest.main()

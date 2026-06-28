import unittest

from src.config import BRAND_COCA_COLA, BRAND_PEPSI
from src.metrics import BrandMetrics, compute_competitive_analysis


def _metrics(coca_seconds: float, pepsi_seconds: float) -> list[BrandMetrics]:
    return [
        BrandMetrics(
            brand=BRAND_COCA_COLA,
            visible_seconds=coca_seconds,
            visibility_pct=0.0,
            detection_count=0,
            avg_confidence=0.0,
        ),
        BrandMetrics(
            brand=BRAND_PEPSI,
            visible_seconds=pepsi_seconds,
            visibility_pct=0.0,
            detection_count=0,
            avg_confidence=0.0,
        ),
    ]


class TestCompetitiveAnalysis(unittest.TestCase):
    def test_pepsi_leads_but_gap_under_threshold(self):
        """Pepsi can lead while balance_label stays balanced (close race)."""
        result = compute_competitive_analysis(_metrics(8.0, 9.0), duration_sec=100.0)
        self.assertEqual(result.dominant_brand, BRAND_PEPSI)
        self.assertEqual(result.balance_label, "balanced")

    def test_coca_leads_but_gap_under_threshold(self):
        result = compute_competitive_analysis(_metrics(9.0, 8.0), duration_sec=100.0)
        self.assertEqual(result.dominant_brand, BRAND_COCA_COLA)
        self.assertEqual(result.balance_label, "balanced")

    def test_pepsi_clear_dominance(self):
        result = compute_competitive_analysis(_metrics(10.0, 20.0), duration_sec=100.0)
        self.assertEqual(result.dominant_brand, BRAND_PEPSI)
        self.assertEqual(result.balance_label, "pepsi_dominant")

    def test_exact_tie(self):
        result = compute_competitive_analysis(_metrics(10.0, 10.0), duration_sec=100.0)
        self.assertEqual(result.dominant_brand, "balanced")
        self.assertEqual(result.balance_label, "balanced")


if __name__ == "__main__":
    unittest.main()

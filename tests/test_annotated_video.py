import unittest
from pathlib import Path
from unittest.mock import patch

from src.annotated_video import persist_annotated_video, resolve_annotated_path


class TestAnnotatedVideoResolution(unittest.TestCase):
    def test_resolve_local_path(self):
        with patch("src.annotated_video.Path.is_file", return_value=True):
            result = resolve_annotated_path("/tmp/annotated_demo.mp4")
        self.assertEqual(result, Path("/tmp/annotated_demo.mp4"))

    def test_resolve_storage_uri(self):
        with patch("src.annotated_video.storage_configured", return_value=True):
            with patch(
                "src.annotated_video.create_signed_crop_url",
                return_value="https://example.com/signed.mp4",
            ):
                result = resolve_annotated_path("storage:brandsight-crops/7/annotated.mp4")
        self.assertEqual(result, "https://example.com/signed.mp4")

    def test_persist_uploads_when_storage_configured(self):
        video_file = Path("/tmp/annotated_demo.mp4")
        with patch("src.annotated_video.ensure_browser_mp4", return_value=video_file):
            with patch("src.annotated_video.storage_configured", return_value=True):
                with patch(
                    "src.annotated_video.upload_storage_file",
                    return_value="storage:brandsight-crops/3/annotated.mp4",
                ) as upload:
                    uri = persist_annotated_video(video_file, 3)
        upload.assert_called_once()
        self.assertEqual(uri, "storage:brandsight-crops/3/annotated.mp4")


if __name__ == "__main__":
    unittest.main()

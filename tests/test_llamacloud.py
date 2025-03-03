import os
import unittest
from unittest.mock import MagicMock, patch

from llamacloud import LlamaCloud, Media


class TestMedia(unittest.TestCase):
    def test_extension(self):
        media = Media("base64data", "PNG")
        self.assertEqual(media.extension, ".png")

    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    @patch("base64.b64decode")
    def test_save(self, mock_b64decode, mock_open):
        mock_b64decode.return_value = b"decoded_data"
        media = Media("base64data", "PNG")
        media.save("test_image")
        
        mock_b64decode.assert_called_once_with("base64data")
        mock_open.assert_called_once_with("test_image.png", "wb")
        mock_open().write.assert_called_once_with(b"decoded_data")


class TestLlamaCloud(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_api_key"
        self.client = LlamaCloud(api_key=self.api_key)

    def test_init_with_api_key(self):
        client = LlamaCloud(api_key="test_key")
        self.assertEqual(client.api_key, "test_key")
        self.assertEqual(client.base_url, "https://api.llamacloud.co")

    @patch.dict(os.environ, {"LLAMA_CLOUD_API_KEY": "env_test_key"})
    def test_init_with_env_var(self):
        client = LlamaCloud()
        self.assertEqual(client.api_key, "env_test_key")

    def test_init_without_api_key(self):
        with patch.dict(os.environ, clear=True):
            with self.assertRaises(ValueError):
                LlamaCloud()

    @patch("httpx.Client")
    def test_generate_image(self, mock_client):
        mock_response = MagicMock()
        mock_response.json.return_value = {"image": "base64_image_data"}
        mock_client.return_value.__enter__.return_value.post.return_value = mock_response

        image = self.client.generate_image(
            model="test_model",
            prompt="test prompt",
            aspect_ratio=LlamaCloud.AspectRatio.SQUARE,
            image_format=LlamaCloud.ImageFormat.PNG,
            seed=42
        )

        self.assertIsInstance(image, Media)
        self.assertEqual(image.base64, "base64_image_data")
        self.assertEqual(image.format, LlamaCloud.ImageFormat.PNG)

    @patch("httpx.Client")
    def test_generate_video(self, mock_client):
        mock_response = MagicMock()
        mock_response.json.return_value = {"video": "base64_video_data"}
        mock_client.return_value.__enter__.return_value.post.return_value = mock_response

        video = self.client.generate_video(
            model="test_model",
            prompt="test prompt",
            quality="high",
            fps=30
        )

        self.assertIsInstance(video, Media)
        self.assertEqual(video.base64, "base64_video_data")
        self.assertEqual(video.format, "MP4")


if __name__ == "__main__":
    unittest.main()

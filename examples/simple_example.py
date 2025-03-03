import os

from llamacloud import LlamaCloud

# Get API key from environment or set it directly
api_key = os.environ["LLAMACLOUD_API_KEY"]

# Initialize the client
client = LlamaCloud(api_key=api_key, base_url="http://api.llamacloud.co")

"""
# Generate an image
print("Generating image...")
image = client.generate_image(
    model="glimmer-v1",
    prompt="a beautiful landscape with mountains and a river",
    aspect_ratio=LlamaCloud.AspectRatio.LANDSCAPE_16_9,
    image_format=LlamaCloud.ImageFormat.PNG,
    seed=42
)
image.save("generated_landscape")  # Saves as "generated_landscape.png"
print("Image saved as generated_landscape.png")

"""

# Generate a video
print("Generating video...")
video = client.generate_video(
    model="wan-v1",
    prompt="a flowing river with trees on the sides",
    quality=LlamaCloud.VideoQuality.LOW,
    fps=20
)
video.save("generated_river")  # Saves as "generated_river.mp4"
print("Video saved as generated_river.mp4")

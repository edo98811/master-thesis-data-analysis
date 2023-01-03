
import requests
from pathlib import Path

# Download from repo
def get_from_github(raw_link, script_name):

  if Path(f"{script_name}").is_file():
    print(f"{script_name}  already exists, skipping download")
  else:
    print(f"Downloading {script_name}")
    # Note: you need the "raw" GitHub URL for this to work
    request = requests.get(raw_link)
    with open(script_name, "wb") as f:
      f.write(request.content)

if __name__ == "__main__":

  script_name = "utils.py"
  raw_link = "https://raw.githubusercontent.com/aladdinpersson/Machine-Learning-Collection/master/ML/Pytorch/image_segmentation/semantic_segmentation_unet/utils.py"
  get_from_github(raw_link, script_name)
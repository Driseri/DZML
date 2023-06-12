import requests
import os

def download_images(synset_id, output_folder):
    url = f"http://www.image-net.org/api/text/imagenet.synset.geturls?wnid={synset_id}"
    response = requests.get(url)
    image_urls = response.text.split("\n")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i, image_url in enumerate(image_urls):
        try:
            response = requests.get(image_url, timeout=5)
            if response.status_code == 200:
                with open(os.path.join(output_folder, f"{synset_id}_{i}.jpg"), "wb") as f:
                    f.write(response.content)
        except Exception as e:
            print(f"Error downloading image {i}: {e}")

# Замените 'n02444819' на идентификатор синсета вашей категории (в данном случае, выдра)
# Замените 'output_folder' на путь к папке, в которую вы хотите сохранить изображения
download_images("n02444819", "output_folder")

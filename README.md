# Storage Service
Handles storage of multi-modal documents. Single API is exposed regardless of the underlying mix of storage systems.
Uses REST and event-driven hybrid architecture:
- REST for direct retrieval of documents by ID.
- Event-driven for asynchronous storage of documents.

Documents are stored in `{storage system}/{user}/{doctype}/{doc}` hierarchy
For example:
```
S3 bucket
|
|-- user1/
|   |
|   |-- thumbnails/
|   |   |-- 36123.jpg
|   |
|   |-- video_scenes/
|   |   |-- 36123_4.jpg
|   |   |-- 36123_9.jpg
|   |
|   |-- videos/
|   |   |-- 36123.mp4
|   |
|   |-- images/
|   |   |-- 36124.jpg
|   |   |-- 36125.png
|   |
|   |-- text/
|       |-- 36127.txt
|
|-- user2/
...
```

## Usage

### Build docker image and run in container
Create `.env` with the following env vars
```
# AWS S3 bucket connection params
AWS_S3_BUCKET_ACCESS_KEY=AKIR...
AWS_S3_BUCKET_SECRET_ACCESS_KEY=R2BOJG1+L+6L5F...
AWS_S3_BUCKET_NAME=multi-modal-docs
AWS_S3_BUCKET_REGION=ap-southeast-1

# Redis connection params
REDIS_HOST=redis-....ap-southeast-1-1.ec2.redns.redis-cloud.com
REDIS_PORT=16221
REDIS_USERNAME=default
REDIS_PASSWORD=ms95Z6...
```

```
docker-compose up
```

### `POST /add`
```
import requests

img_path = 'user1/temp.jpg'
url = 'http://127.0.0.1:5000/add'
files = {'file': open(img_path, 'rb')}  # Specify the file you want to upload

response = requests.post(url, files=files, data={"doc_id": img_path})
print(response.text)
```

### `GET /get/<doc_id>`
```
import requests

url = 'http://127.0.0.1:5000/get/user1/temp.jpg'

response = requests.get(url)
with open('temp.jpg', 'wb') as file:
    file.write(response.content)
print(response.text)
```
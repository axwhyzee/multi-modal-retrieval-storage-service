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

## Installation

Create `.env` with the following env vars
```
# AWS S3 bucket connection params
AWS_S3_BUCKET_ACCESS_KEY=...
AWS_S3_BUCKET_SECRET_ACCESS_KEY=...
AWS_S3_BUCKET_NAME=...
AWS_S3_BUCKET_REGION=...

# Redis connection params
REDIS_HOST=redis-...
REDIS_PORT=...
REDIS_USERNAME=...
REDIS_PASSWORD=...
```

```
# build docker image and run container
docker-compose up
```

## Usage

### `POST /add`
```
import requests

img_path = 'user1/temp.jpg'
url = 'http://127.0.0.1:5001/add'
files = {'file': open(img_path, 'rb')}  # Specify the file you want to upload

response = requests.post(url, files=files, data={"key": img_path, "type": "DOC"})
print(response.text)
```

### `GET /get/<key>`
```
import requests

url = 'http://127.0.0.1:5001/get/user1/temp.jpg'

response = requests.get(url)
with open('temp.jpg', 'wb') as file:
    file.write(response.content)
```
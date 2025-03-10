# Storage Service
Handles storage of multi-modal documents. Single API is exposed regardless of the underlying mix of storage systems.
Uses request-response and event-driven hybrid architecture:
- REST APIs for direct retrieval of documents by ID.
- Event-driven for asynchronous storage of documents.

Documents are stored in `{user}/{doc}/{obj}` hierarchy
For example:
```
S3 bucket
|
|-- user1/
|   |
|   |-- 36123.mp4
|   |-- 36123/
|   |   |-- 0__DOC_THUMBNAIL.png
|   |   |-- 1__CHUNK.png
|   |   |-- 1__CHUNK_THUMBNAIL.png
|   |   |-- 2__CHUNK.png
|   |   |-- 2__CHUNK_THUMBNAIL.png
|   |
|   |-- 36124.pdf
|   |-- 36124/
|   |   |-- 0__DOC_THUMBNAIL.png
|   |   |-- 1__CHUNK.png
|   |   |-- 1__CHUNK_THUMBNAIL.png
|   |   |-- 2__CHUNK.txt
|   |   |-- 3__CHUNK.txt
|   |
|   |-- 36125.jpg
|   |-- 36125/
|   |   |-- 0__DOC_THUMBNAIL.png
|   |   |-- 1__CHUNK.png
|   |   |-- 1__CHUNK_THUMBNAIL.png
|   |
|   |-- 36126.txt
|   |-- 36126/
|       |-- 1__CHUNK.txt
|       |-- 2__CHUNK.txt
|
|-- user2/
...
```

## Setup
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

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

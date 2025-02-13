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
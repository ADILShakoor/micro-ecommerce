from storages.backends.s3 import S3Storage

# configration for defalut access

class MediaStorage(S3Storage):
    location="media"

class StaticFileStorage(S3Storage):
    location="statis"

class ProtectedFileStorage(S3Storage):
    location="protected"
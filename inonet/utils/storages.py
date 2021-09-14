from storages.backends.s3boto3 import S3Boto3Storage


class StaticRootS3Boto3Storage(S3Boto3Storage):
    location = "static"
    default_acl = "public-read"
    querystring_auth=False


class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = "media"
    file_overwrite = False

from cfehome.env import config

# IT may be envirment variable
AWS_ACCESS_KEY_ID=config("AWS_ACCESS_KEY_ID",default=None)
AWS_SECRIT_ACCESS_KEY=config("AWS_SECRIT_ACCESS_KEY",default=None)

# cloud.linode for object storage bucket name as string
"micro_ecommerce.us-estat-1.linodeobject.com"


AWS_S3_SIGNATURE_VERSION="s3v4"
AWS_STORAGE_BUCKET_NAME="micro-ecommerce"
AWS_S3_ENPOINT_URL=f"https://{AWS_STORAGE_BUCKET_NAME}.us-estat-1.linodeobject.com"

AWS_DEFAULT_ACL="public-read"
AWS_S3_USE_SSL=True
# file upload sotrage defalut
DEFAULT_FILE_STORAGE = "cfehome.storages.backends.MediaStorage"
# staticfiles
STATICFILES_STORAGE = "cfehome.storages.backends.MediaStorage"
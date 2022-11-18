from minio import Minio

client = Minio(
    "localhost:9000",
    access_key="Go8BtEuqhYghz6uP",
    secret_key="wVMJvmyi9OgXVwWp6RcPnBPeMiOxsdMu",
    secure=False
)

print(client.list_buckets())
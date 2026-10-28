from qcloud_cos import CosConfig, CosS3Client

secret_id = "AKIDnM9m4gpmyytLzY2377hGroeaVcIpRD4bxrV5Pi1gPvrIQ_wTfB0o6Yq8GOkjJ-bx"
secret_key = "y8LdOf0uhvY4VdbeekI+qdchfvLOOzUUWxt3ee7Gw5w="
token = "ndlfTEtkZZG6HbmrAZYZ3NV5VmaflSAa038e13417c62ea143f71e67df20e3bdbiNn9jMSWKdudzTNw4gc9LmBJZ4FWaLWH2O6dKRNCjAip8lGcsGz_xUEoVCFCJ3Mdp_nghdSREV7aStrsrLAUPXhYGtBwKI-7QKnb3Wpy3_3a8MsSQbzZROqdvPGviNpdSiSixl8aKMUTqfOkQWMKGeNMBopBUG16alk6yJPOQJVmraDLaSPFIGVcTg_wZdeFNkQe1Tp-H0SbdOUoFhr2JRHtbGaO8gldb0bSXimFiTm7qrEsoQZS-0a4k5whsaVqVVTFTQG1M_fqp4hvG8byk9d9qwKzKkJrtd7tKj-tglK-rvDcx7QifJAqcmSGUsPIFDaDb3o2h8Mtknq-Cwe0MuuKwS2uQvftUgvsDD5mpn3FTRWoP_-j6Vf1eaTq5b67LDeonA651-8U-Xw1Fx1HrSqDsiMpMzh7hgx7pkisBE9z9ESkZQSSt-sHCAJruL6q94aowukY3LSSsSaGD4MpGNkAefJqLKX0SD1QZiDFp8VNfDtPnCpUdEsSaHNH_XDnh_hTXKEMiTf7-cpVvEeeuq4W6lb0bhc4mkE30q5Su-PZ7gjZCuFvzWm-mqX6DkTFcJWtggYzvdqeOwP7IB3rjByp1nKuo1MsTfRKGTuW7w1DtTgFTV5BvZH7pWOZXHZujyAv9FSw9jxGwejet40eo5SOGWX9OkcuL8ml09GL65VwFBzUVoRqx0eNM2OA_GkwVhyoLxjYgvE3wZi1nhzNBKRz-hIZq-nCZGybhzpPv-DPOn-izg3kQOu8v_BuJ_xIfc83K6ciLjbRM_xoRiX-qhlcedAxBFV7FhO0B2AZgBY"
region = "ap-shanghai"
bucket = "ima-share-kb-1258344701"
cos_key = "5/c3UYDO8B6JpzhiqPpCtG8B/file_manager/01a0bdb4cd17705f9ced53c7619c9c52.md"
local_file = r"D:\Claw\蓝创中心水电费结算表_2026年6-7月.md"

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token)
client = CosS3Client(config)

with open(local_file, "rb") as f:
    body = f.read()

resp = client.put_object(
    Bucket=bucket,
    Body=body,
    Key=cos_key,
    ContentType="text/markdown; charset=utf-8",
)
print("ETag:", resp.get("ETag"))
print("HTTPStatusCode:", resp.get("HTTPStatusCode"))

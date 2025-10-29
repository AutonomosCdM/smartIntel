# Cloud Object Storage Setup Guide

**Purpose**: Configure IBM Cloud Object Storage (COS) for watsonx.ai Text Extraction API

---

## 🎯 Why We Need COS

watsonx.ai Text Extraction API requires:
1. **Input**: PDFs stored in Cloud Object Storage bucket
2. **Output**: Extraction results written back to COS bucket
3. **Credentials**: HMAC credentials to access COS

Cannot upload PDFs directly - must be in COS first.

---

## 📋 Step 1: Create Cloud Object Storage Instance

### Via IBM Cloud Web Console

1. **Go to IBM Cloud Catalog**:
   - https://cloud.ibm.com/catalog

2. **Search for "Object Storage"**:
   - Select "Cloud Object Storage" (not "File Storage" or "Block Storage")

3. **Create Service**:
   - Name: `procure-genius-cos` or `watsonx-documents`
   - Plan: **Lite** (free tier, 25GB storage)
   - Resource group: Default
   - Click **Create**

4. **Service Created**:
   - Note the service name
   - Go to service dashboard

---

## 📋 Step 2: Create Bucket

### In COS Dashboard

1. **Create Bucket**:
   - Click "Create bucket"
   - Select "Customize your bucket"

2. **Bucket Configuration**:
   - Name: `procure-genius-pdfs` (must be globally unique)
   - Resiliency: **Regional** (faster, cheaper for single region)
   - Location: **us-south** (same as watsonx.ai)
   - Storage class: **Smart Tier** (auto-optimization)

3. **Advanced Settings** (Optional):
   - Encryption: IBM-managed (default)
   - Object versioning: Disabled
   - Activity tracking: Disabled (for hackathon)

4. **Create Bucket**:
   - Click "Create bucket"
   - Bucket created successfully

---

## 📋 Step 3: Generate HMAC Credentials

### What are HMAC Credentials?

HMAC (Hash-based Message Authentication Code) credentials provide S3-compatible access:
- Access Key ID (like username)
- Secret Access Key (like password)

### Create HMAC Credentials

1. **Go to Service Credentials**:
   - In COS dashboard, click "Service credentials" (left sidebar)

2. **Create New Credential**:
   - Click "New credential"
   - Name: `watsonx-extraction-hmac`
   - Role: **Writer** (needed for both read and write)

3. **Include HMAC Credential** (CRITICAL):
   - Expand "Advanced options"
   - Check ✅ **"Include HMAC Credential"**
   - This generates S3-compatible access keys

4. **Create Credential**:
   - Click "Add"
   - Credential created

5. **View Credential**:
   - Click "View credentials" (eye icon)
   - Copy the JSON credentials

### Credential Structure

```json
{
  "apikey": "...",
  "cos_hmac_keys": {
    "access_key_id": "your_access_key_id",
    "secret_access_key": "your_secret_access_key"
  },
  "endpoints": "https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints",
  "iam_apikey_description": "...",
  "iam_apikey_name": "...",
  "iam_role_crn": "...",
  "iam_serviceid_crn": "...",
  "resource_instance_id": "crn:v1:bluemix:public:cloud-object-storage:global:..."
}
```

**Important Fields**:
- `cos_hmac_keys.access_key_id`: Your COS access key
- `cos_hmac_keys.secret_access_key`: Your COS secret key
- `resource_instance_id`: COS instance CRN

---

## 📋 Step 4: Configure .env File

Add COS credentials to `.env`:

```bash
# Cloud Object Storage Configuration
COS_API_KEY=<from apikey field>
COS_INSTANCE_ID=<from resource_instance_id field>
COS_ACCESS_KEY_ID=<from cos_hmac_keys.access_key_id>
COS_SECRET_ACCESS_KEY=<from cos_hmac_keys.secret_access_key>
COS_ENDPOINT=https://s3.us-south.cloud-object-storage.appdomain.cloud
COS_BUCKET_NAME=procure-genius-pdfs

# watsonx.ai will use these for Text Extraction
COS_AUTH_ENDPOINT=https://iam.cloud.ibm.com/identity/token
```

### Finding Your Endpoint

1. Go to COS dashboard
2. Click "Buckets" → Select your bucket
3. Click "Configuration"
4. Find "Endpoints" section
5. Copy **"Public"** endpoint for **us-south**

Common endpoints:
- **us-south**: `https://s3.us-south.cloud-object-storage.appdomain.cloud`
- **us-east**: `https://s3.us-east.cloud-object-storage.appdomain.cloud`
- **eu-gb**: `https://s3.eu-gb.cloud-object-storage.appdomain.cloud`

---

## 📋 Step 5: Test COS Connection

### Using Python SDK

```python
#!/usr/bin/env python3
"""Test IBM Cloud Object Storage connection."""

import os
from dotenv import load_dotenv
import ibm_boto3
from ibm_botocore.client import Config

load_dotenv()

# COS credentials
cos_credentials = {
    "access_key_id": os.getenv("COS_ACCESS_KEY_ID"),
    "secret_access_key": os.getenv("COS_SECRET_ACCESS_KEY"),
    "endpoint_url": os.getenv("COS_ENDPOINT"),
}

# Create COS client
cos_client = ibm_boto3.client(
    "s3",
    aws_access_key_id=cos_credentials["access_key_id"],
    aws_secret_access_key=cos_credentials["secret_access_key"],
    endpoint_url=cos_credentials["endpoint_url"],
    config=Config(signature_version="s3v4")
)

# Test: List buckets
print("Testing COS connection...")
buckets = cos_client.list_buckets()
print(f"✅ Connected! Found {len(buckets['Buckets'])} buckets:")
for bucket in buckets['Buckets']:
    print(f"  - {bucket['Name']}")

# Test: Upload a test file
bucket_name = os.getenv("COS_BUCKET_NAME")
test_content = b"Hello from watsonx!"
cos_client.put_object(
    Bucket=bucket_name,
    Key="test.txt",
    Body=test_content
)
print(f"✅ Test file uploaded to {bucket_name}/test.txt")

# Test: List objects in bucket
objects = cos_client.list_objects_v2(Bucket=bucket_name)
if "Contents" in objects:
    print(f"✅ Found {len(objects['Contents'])} objects in bucket:")
    for obj in objects["Contents"]:
        print(f"  - {obj['Key']} ({obj['Size']} bytes)")

print("\n🎉 COS connection successful!")
```

Save as `scripts/test_cos_connection.py` and run:

```bash
python scripts/test_cos_connection.py
```

---

## 📋 Step 6: Upload PDFs to COS

### Bulk Upload Script

```python
#!/usr/bin/env python3
"""Upload Carozzi PDFs to Cloud Object Storage."""

import os
from pathlib import Path
from dotenv import load_dotenv
import ibm_boto3
from ibm_botocore.client import Config

load_dotenv()

# COS client
cos_client = ibm_boto3.client(
    "s3",
    aws_access_key_id=os.getenv("COS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("COS_SECRET_ACCESS_KEY"),
    endpoint_url=os.getenv("COS_ENDPOINT"),
    config=Config(signature_version="s3v4")
)

bucket_name = os.getenv("COS_BUCKET_NAME")

# Upload all PDFs from data/demo
pdf_dirs = [
    Path("data/demo/financials"),
    Path("data/demo/contracts")
]

for pdf_dir in pdf_dirs:
    if not pdf_dir.exists():
        continue

    for pdf_file in pdf_dir.glob("*.pdf"):
        # Upload to COS
        key = f"{pdf_dir.name}/{pdf_file.name}"
        print(f"Uploading {pdf_file.name} → {key}...")

        with open(pdf_file, "rb") as f:
            cos_client.put_object(
                Bucket=bucket_name,
                Key=key,
                Body=f.read()
            )

        print(f"✅ Uploaded: {key}")

print("\n🎉 All PDFs uploaded to COS!")
```

Save as `scripts/upload_pdfs_to_cos.py` and run:

```bash
python scripts/upload_pdfs_to_cos.py
```

---

## 📋 Step 7: Update Text Extraction Script

Now we can use `run_job()` with COS references:

```python
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models.extractions import TextExtractionsV2

# Initialize client
extraction_client = TextExtractionsV2(
    credentials=Credentials(api_key=WATSONX_API_KEY, url=WATSONX_URL),
    project_id=WATSONX_PROJECT_ID
)

# Document reference (input from COS)
document_reference = {
    "type": "connection_asset",
    "connection": {
        "endpoint_url": COS_ENDPOINT,
        "access_key_id": COS_ACCESS_KEY_ID,
        "secret_access_key": COS_SECRET_ACCESS_KEY
    },
    "location": {
        "bucket": COS_BUCKET_NAME,
        "path": "financials/EEFF_Anual_2023.pdf"
    }
}

# Results reference (output to COS)
results_reference = {
    "type": "connection_asset",
    "connection": {
        "endpoint_url": COS_ENDPOINT,
        "access_key_id": COS_ACCESS_KEY_ID,
        "secret_access_key": COS_SECRET_ACCESS_KEY
    },
    "location": {
        "bucket": COS_BUCKET_NAME,
        "path": "extractions/EEFF_2023_results.json"
    }
}

# Extraction steps
steps = {
    "ocr": {
        "enabled": True,
        "languages": ["en", "es"]
    },
    "table_processing": {
        "enabled": True
    }
}

# Run extraction job
job_details = extraction_client.run_job(
    document_reference=document_reference,
    results_reference=results_reference,
    steps=steps,
    results_format="markdown"
)

print(f"Job ID: {job_details['metadata']['id']}")
print(f"Status: {job_details['entity']['status']['state']}")
```

---

## 📋 Step 8: Monitor Extraction Job

```python
# Get job status
job_id = extraction_client.get_job_id()
details = extraction_client.get_job_details(job_id)

print(f"Job state: {details['entity']['status']['state']}")

# Wait for completion
import time
while details['entity']['status']['state'] not in ['completed', 'failed']:
    time.sleep(5)
    details = extraction_client.get_job_details(job_id)
    print(f"Status: {details['entity']['status']['state']}")

if details['entity']['status']['state'] == 'completed':
    print("✅ Extraction completed!")

    # Download results from COS
    result = cos_client.get_object(
        Bucket=COS_BUCKET_NAME,
        Key="extractions/EEFF_2023_results.json"
    )
    extracted_text = result['Body'].read().decode('utf-8')
    print(extracted_text[:500])
```

---

## ✅ Success Criteria

After completing setup:

- [ ] COS instance created (Lite plan)
- [ ] Bucket created (`procure-genius-pdfs`)
- [ ] HMAC credentials generated
- [ ] Credentials added to `.env`
- [ ] COS connection tested
- [ ] PDFs uploaded to bucket
- [ ] Text Extraction job runs successfully
- [ ] Results retrieved from COS

---

## 🔍 Troubleshooting

### Error: "NoSuchBucket"
**Solution**: Check bucket name in `.env` matches actual bucket name

### Error: "SignatureDoesNotMatch"
**Solution**: Verify HMAC credentials are correct, regenerate if needed

### Error: "AccessDenied"
**Solution**: Ensure service credential has "Writer" role, not just "Reader"

### Error: "Endpoint does not exist"
**Solution**: Verify endpoint matches your bucket's region

---

## 💰 Cost Considerations

**Lite Plan (Free)**:
- 25GB storage
- 20K GET requests/month
- 2K PUT requests/month

**Hackathon Usage**:
- ~10 PDFs × 2MB = 20MB storage (well under limit)
- ~100 API calls total (extraction + downloads)
- **Cost**: $0 (Lite plan sufficient)

---

**Next Steps**:
1. Create COS instance and bucket via IBM Cloud console
2. Generate HMAC credentials
3. Update `.env` with COS credentials
4. Run `scripts/test_cos_connection.py`
5. Run `scripts/upload_pdfs_to_cos.py`
6. Test text extraction with `run_job()`

---

**Last Updated**: 2025-10-29
**Maintained by**: Autonomos Lab

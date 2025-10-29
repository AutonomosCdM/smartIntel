#!/usr/bin/env python3
"""Test IBM Cloud Object Storage connection and setup.

This script:
1. Tests COS connection with HMAC credentials
2. Lists existing buckets
3. Tests bucket access
4. Uploads a test file
5. Lists objects in bucket
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"


def print_header(text: str):
    """Print formatted header."""
    print(f"\n{BLUE}{BOLD}{'='*60}{RESET}")
    print(f"{BLUE}{BOLD}{text}{RESET}")
    print(f"{BLUE}{BOLD}{'='*60}{RESET}\n")


def print_success(text: str):
    """Print success message."""
    print(f"{GREEN}✅ {text}{RESET}")


def print_error(text: str):
    """Print error message."""
    print(f"{RED}❌ {text}{RESET}")


def print_warning(text: str):
    """Print warning message."""
    print(f"{YELLOW}⚠️  {text}{RESET}")


def print_info(text: str):
    """Print info message."""
    print(f"{BLUE}ℹ️  {text}{RESET}")


def test_credentials():
    """Test that COS credentials are set."""
    print_header("1. Checking COS Credentials")

    required_vars = {
        "COS_ACCESS_KEY_ID": "COS Access Key ID",
        "COS_SECRET_ACCESS_KEY": "COS Secret Access Key",
        "COS_ENDPOINT": "COS Endpoint URL",
        "COS_BUCKET_NAME": "COS Bucket Name",
    }

    all_set = True
    for var_name, var_description in required_vars.items():
        value = os.getenv(var_name)
        if value:
            # Mask secret key
            if "SECRET" in var_name:
                masked_value = f"{value[:10]}...{value[-5:]}"
            else:
                masked_value = value
            print_success(f"{var_description}: {masked_value}")
        else:
            print_error(f"{var_description}: NOT SET")
            all_set = False

    return all_set


def test_connection():
    """Test COS connection."""
    print_header("2. Testing COS Connection")

    try:
        import ibm_boto3
        from ibm_botocore.client import Config

        print_info("Creating COS client...")

        cos_client = ibm_boto3.client(
            "s3",
            aws_access_key_id=os.getenv("COS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("COS_SECRET_ACCESS_KEY"),
            endpoint_url=os.getenv("COS_ENDPOINT"),
            config=Config(signature_version="s3v4")
        )

        print_success("COS client created")

        # List buckets
        print_info("Listing buckets...")
        buckets = cos_client.list_buckets()

        bucket_count = len(buckets.get("Buckets", []))
        print_success(f"Connected! Found {bucket_count} bucket(s):")

        for bucket in buckets.get("Buckets", []):
            bucket_name = bucket["Name"]
            creation_date = bucket.get("CreationDate", "Unknown")
            print_info(f"  - {bucket_name} (created: {creation_date})")

        return cos_client

    except Exception as e:
        print_error(f"Connection failed: {e}")
        print_info(f"Error type: {type(e).__name__}")
        return None


def test_bucket_access(cos_client):
    """Test access to specific bucket."""
    print_header("3. Testing Bucket Access")

    bucket_name = os.getenv("COS_BUCKET_NAME")

    try:
        print_info(f"Checking bucket: {bucket_name}")

        # Try to list objects
        response = cos_client.list_objects_v2(Bucket=bucket_name, MaxKeys=10)

        if "Contents" in response:
            object_count = len(response["Contents"])
            print_success(f"Bucket accessible! Contains {object_count} object(s)")

            for obj in response["Contents"]:
                key = obj["Key"]
                size = obj["Size"]
                print_info(f"  - {key} ({size:,} bytes)")
        else:
            print_warning("Bucket is empty (no objects found)")
            print_success("But bucket is accessible!")

        return True

    except Exception as e:
        print_error(f"Cannot access bucket: {e}")
        print_info("Check that bucket name in .env matches actual bucket name")
        return False


def test_upload(cos_client):
    """Test uploading a file to bucket."""
    print_header("4. Testing File Upload")

    bucket_name = os.getenv("COS_BUCKET_NAME")

    try:
        test_content = b"Hello from watsonx.ai PDF extraction pipeline! This is a test file."
        test_key = "test/connection_test.txt"

        print_info(f"Uploading test file to: {bucket_name}/{test_key}")

        cos_client.put_object(
            Bucket=bucket_name,
            Key=test_key,
            Body=test_content
        )

        print_success(f"Test file uploaded successfully!")

        # Verify upload by downloading
        print_info("Verifying upload by downloading...")
        response = cos_client.get_object(Bucket=bucket_name, Key=test_key)
        downloaded_content = response["Body"].read()

        if downloaded_content == test_content:
            print_success("Upload verified! Downloaded content matches.")
        else:
            print_warning("Downloaded content doesn't match uploaded content")

        # Clean up test file
        print_info("Cleaning up test file...")
        cos_client.delete_object(Bucket=bucket_name, Key=test_key)
        print_success("Test file deleted")

        return True

    except Exception as e:
        print_error(f"Upload test failed: {e}")
        return False


def main():
    """Run all COS tests."""
    print_header("IBM Cloud Object Storage Connection Test")

    # Test 1: Credentials
    if not test_credentials():
        print_error("\n⚠️  Missing COS credentials. Please configure .env file.")
        print_info("See docs/GUIDES/CLOUD_OBJECT_STORAGE_SETUP.md for setup instructions")
        return 1

    # Test 2: Connection
    cos_client = test_connection()
    if not cos_client:
        return 1

    # Test 3: Bucket access
    if not test_bucket_access(cos_client):
        return 1

    # Test 4: Upload
    if not test_upload(cos_client):
        return 1

    # Summary
    print_header("Test Summary")
    print_success("🎉 All COS tests passed!")
    print_info("\nYour Cloud Object Storage is ready for:")
    print_info("  ✅ Storing PDF documents")
    print_info("  ✅ watsonx.ai Text Extraction API")
    print_info("  ✅ Extraction results storage")

    print_info("\nNext steps:")
    print_info("  1. Run: python scripts/upload_pdfs_to_cos.py")
    print_info("  2. Run: python scripts/test_pdf_extraction_cos.py")
    print_info("  3. Integrate with Document Field Extractor")

    return 0


if __name__ == "__main__":
    sys.exit(main())

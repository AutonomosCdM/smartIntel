#!/usr/bin/env python3
"""Upload Carozzi PDFs to IBM Cloud Object Storage.

This script uploads all PDFs from data/demo/ to COS bucket for
watsonx.ai Text Extraction processing.
"""

import os
import sys
from pathlib import Path
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


def print_info(text: str):
    """Print info message."""
    print(f"{BLUE}ℹ️  {text}{RESET}")


def create_cos_client():
    """Create COS client."""
    try:
        import ibm_boto3
        from ibm_botocore.client import Config

        return ibm_boto3.client(
            "s3",
            aws_access_key_id=os.getenv("COS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("COS_SECRET_ACCESS_KEY"),
            endpoint_url=os.getenv("COS_ENDPOINT"),
            config=Config(signature_version="s3v4")
        )
    except Exception as e:
        print_error(f"Failed to create COS client: {e}")
        return None


def upload_pdf(cos_client, pdf_path: Path, cos_key: str):
    """Upload single PDF to COS."""
    bucket_name = os.getenv("COS_BUCKET_NAME")

    try:
        file_size_mb = pdf_path.stat().st_size / 1024 / 1024
        print_info(f"Uploading: {pdf_path.name} ({file_size_mb:.2f} MB)")

        with open(pdf_path, "rb") as f:
            cos_client.put_object(
                Bucket=bucket_name,
                Key=cos_key,
                Body=f.read()
            )

        print_success(f"  ✓ Uploaded to: {bucket_name}/{cos_key}")
        return True

    except Exception as e:
        print_error(f"  ✗ Upload failed: {e}")
        return False


def main():
    """Upload all PDFs to COS."""
    print_header("Upload PDFs to Cloud Object Storage")

    # Create COS client
    print_info("Connecting to Cloud Object Storage...")
    cos_client = create_cos_client()
    if not cos_client:
        return 1

    bucket_name = os.getenv("COS_BUCKET_NAME")
    print_success(f"Connected to bucket: {bucket_name}")

    # Find all PDFs
    pdf_dirs = [
        Path("data/demo/financials"),
        Path("data/demo/contracts")
    ]

    all_pdfs = []
    for pdf_dir in pdf_dirs:
        if pdf_dir.exists():
            pdfs = list(pdf_dir.glob("*.pdf"))
            all_pdfs.extend([(pdf_dir.name, pdf) for pdf in pdfs])

    if not all_pdfs:
        print_error("No PDF files found in data/demo/")
        return 1

    print_info(f"Found {len(all_pdfs)} PDF file(s) to upload\n")

    # Upload each PDF
    uploaded_count = 0
    failed_count = 0

    for category, pdf_path in all_pdfs:
        cos_key = f"{category}/{pdf_path.name}"

        if upload_pdf(cos_client, pdf_path, cos_key):
            uploaded_count += 1
        else:
            failed_count += 1

    # Summary
    print_header("Upload Summary")

    if uploaded_count == len(all_pdfs):
        print_success(f"🎉 All {uploaded_count} PDFs uploaded successfully!")
    else:
        print_info(f"Uploaded: {uploaded_count}/{len(all_pdfs)}")
        if failed_count > 0:
            print_error(f"Failed: {failed_count}")

    # List uploaded files
    print_info("\nVerifying uploads...")
    try:
        response = cos_client.list_objects_v2(Bucket=bucket_name)

        if "Contents" in response:
            print_success(f"Bucket now contains {len(response['Contents'])} objects:")
            for obj in response["Contents"]:
                key = obj["Key"]
                size_mb = obj["Size"] / 1024 / 1024
                print_info(f"  - {key} ({size_mb:.2f} MB)")
        else:
            print_error("Bucket appears empty after upload")

    except Exception as e:
        print_error(f"Could not verify uploads: {e}")

    print_info("\nNext step: Run text extraction with COS")
    print_info("  python scripts/test_pdf_extraction_cos.py")

    return 0 if failed_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

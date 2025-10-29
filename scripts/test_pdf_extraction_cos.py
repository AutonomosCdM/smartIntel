#!/usr/bin/env python3
"""Test watsonx.ai Text Extraction API with Cloud Object Storage.

This script demonstrates the complete PDF extraction pipeline:
1. PDF stored in COS bucket
2. watsonx.ai Text Extraction job submitted
3. Job monitored until completion
4. Results retrieved from COS
"""

import json
import os
import sys
import time
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


def print_warning(text: str):
    """Print warning message."""
    print(f"{YELLOW}⚠️  {text}{RESET}")


def print_info(text: str):
    """Print info message."""
    print(f"{BLUE}ℹ️  {text}{RESET}")


def initialize_clients():
    """Initialize watsonx.ai and COS clients."""
    print_header("1. Initializing Clients")

    try:
        from ibm_watsonx_ai import Credentials
        from ibm_watsonx_ai.foundation_models.extractions import TextExtractionsV2
        import ibm_boto3
        from ibm_botocore.client import Config

        # watsonx.ai client
        print_info("Creating watsonx.ai client...")
        extraction_client = TextExtractionsV2(
            credentials=Credentials(
                api_key=os.getenv("WATSONX_API_KEY"),
                url=os.getenv("WATSONX_URL")
            ),
            project_id=os.getenv("WATSONX_PROJECT_ID")
        )
        print_success("watsonx.ai client created")

        # COS client
        print_info("Creating COS client...")
        cos_client = ibm_boto3.client(
            "s3",
            aws_access_key_id=os.getenv("COS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("COS_SECRET_ACCESS_KEY"),
            endpoint_url=os.getenv("COS_ENDPOINT"),
            config=Config(signature_version="s3v4")
        )
        print_success("COS client created")

        return extraction_client, cos_client

    except Exception as e:
        print_error(f"Failed to initialize clients: {e}")
        return None, None


def run_extraction_job(extraction_client, input_path: str, output_path: str):
    """Run text extraction job with COS."""
    print_header("2. Submitting Text Extraction Job")

    try:
        # Document reference (input from COS)
        document_reference = {
            "type": "connection_asset",
            "connection": {
                "endpoint_url": os.getenv("COS_ENDPOINT"),
                "access_key_id": os.getenv("COS_ACCESS_KEY_ID"),
                "secret_access_key": os.getenv("COS_SECRET_ACCESS_KEY")
            },
            "location": {
                "bucket": os.getenv("COS_BUCKET_NAME"),
                "path": input_path
            }
        }

        # Results reference (output to COS)
        results_reference = {
            "type": "connection_asset",
            "connection": {
                "endpoint_url": os.getenv("COS_ENDPOINT"),
                "access_key_id": os.getenv("COS_ACCESS_KEY_ID"),
                "secret_access_key": os.getenv("COS_SECRET_ACCESS_KEY")
            },
            "location": {
                "bucket": os.getenv("COS_BUCKET_NAME"),
                "path": output_path
            }
        }

        # Extraction steps (configuration)
        steps = {
            "ocr": {
                "enabled": True,
                "languages": ["en", "es"]  # English and Spanish
            },
            "table_processing": {
                "enabled": True
            }
        }

        print_info(f"Input: {os.getenv('COS_BUCKET_NAME')}/{input_path}")
        print_info(f"Output: {os.getenv('COS_BUCKET_NAME')}/{output_path}")
        print_info("Configuration: OCR (en, es) + Table Processing")

        print_info("\nSubmitting job...")

        # Submit extraction job
        job_details = extraction_client.run_job(
            document_reference=document_reference,
            results_reference=results_reference,
            steps=steps,
            results_format="markdown"
        )

        job_id = job_details["metadata"]["id"]
        job_state = job_details["entity"]["status"]["state"]

        print_success(f"Job submitted successfully!")
        print_info(f"Job ID: {job_id}")
        print_info(f"Initial state: {job_state}")

        return job_id

    except Exception as e:
        print_error(f"Failed to submit extraction job: {e}")
        print_info(f"Error type: {type(e).__name__}")
        print_info(f"Error details: {str(e)}")
        return None


def monitor_job(extraction_client, job_id: str, timeout: int = 300):
    """Monitor extraction job until completion."""
    print_header("3. Monitoring Job Progress")

    start_time = time.time()
    check_interval = 5  # seconds

    try:
        while True:
            elapsed = int(time.time() - start_time)

            if elapsed > timeout:
                print_error(f"Job timeout after {timeout} seconds")
                return False

            # Get job status
            details = extraction_client.get_job_details(job_id)
            job_state = details["entity"]["status"]["state"]
            running_time = details["entity"]["status"].get("running_at", "")

            print_info(f"[{elapsed}s] Job state: {job_state}")

            if job_state == "completed":
                print_success(f"\n✅ Job completed in {elapsed} seconds!")
                return True

            elif job_state == "failed":
                failure_reason = details["entity"]["status"].get("failure", {})
                print_error(f"\n❌ Job failed!")
                print_error(f"Reason: {failure_reason}")
                return False

            elif job_state in ["queued", "running"]:
                # Job still processing
                time.sleep(check_interval)
                continue

            else:
                print_warning(f"Unknown job state: {job_state}")
                time.sleep(check_interval)

    except KeyboardInterrupt:
        print_warning("\n⚠️  Monitoring interrupted by user")
        return False
    except Exception as e:
        print_error(f"Error monitoring job: {e}")
        return False


def retrieve_results(cos_client, output_path: str, save_path: Path):
    """Retrieve extraction results from COS."""
    print_header("4. Retrieving Results from COS")

    bucket_name = os.getenv("COS_BUCKET_NAME")

    try:
        print_info(f"Downloading from: {bucket_name}/{output_path}")

        response = cos_client.get_object(Bucket=bucket_name, Key=output_path)
        result_content = response["Body"].read().decode("utf-8")

        print_success(f"Results downloaded ({len(result_content):,} chars)")

        # Save to local file
        save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(result_content)

        print_success(f"Results saved to: {save_path}")
        print_info(f"File size: {save_path.stat().st_size / 1024:.2f} KB")

        return result_content

    except Exception as e:
        print_error(f"Failed to retrieve results: {e}")
        return None


def analyze_results(results: str):
    """Analyze extraction quality."""
    print_header("5. Analyzing Extraction Quality")

    if not results:
        print_error("No results to analyze")
        return

    try:
        # Try to parse as JSON
        try:
            result_data = json.loads(results)
            print_info("Results format: JSON")
        except json.JSONDecodeError:
            result_data = results
            print_info("Results format: Text/Markdown")

        # Basic metrics
        content_str = str(result_data)
        print_info(f"Total characters: {len(content_str):,}")
        print_info(f"Total words (approx): {len(content_str.split()):,}")

        # Check for financial indicators
        financial_keywords = [
            "ingreso", "revenue", "costo", "cost", "ganancia", "profit",
            "activo", "asset", "pasivo", "liability",
            "CLP", "millones", "million", "M$", "MM$",
            "Carozzi", "estado", "financiero", "financial", "statement"
        ]

        found_keywords = [kw for kw in financial_keywords if kw.lower() in content_str.lower()]
        print_info(f"Financial keywords found: {len(found_keywords)}/{len(financial_keywords)}")

        if found_keywords:
            print_success(f"Found: {', '.join(found_keywords[:8])}")

        # Show preview
        preview_length = 500
        print_info(f"\nPreview (first {preview_length} chars):")
        print("-" * 60)
        print(content_str[:preview_length])
        if len(content_str) > preview_length:
            print("...")
        print("-" * 60)

        # Overall assessment
        if len(content_str) > 1000 and len(found_keywords) > 5:
            print_success("\n✅ Extraction quality: EXCELLENT")
            print_success("Ready for Document Field Extractor!")
        elif len(content_str) > 500 and len(found_keywords) > 3:
            print_info("\n⚠️  Extraction quality: GOOD")
            print_info("Contains financial data, may need refinement")
        else:
            print_error("\n❌ Extraction quality: POOR")
            print_error("Review extraction configuration")

    except Exception as e:
        print_error(f"Error analyzing results: {e}")


def main():
    """Main test function."""
    print_header("watsonx.ai Text Extraction with Cloud Object Storage")

    # Configuration
    input_pdf = "financials/EEFF_Anual_2023.pdf"  # Path in COS
    output_results = "extractions/EEFF_2023_markdown.json"  # Path in COS
    local_save_path = Path("data/processed/extractions/EEFF_2023_extraction.json")

    # Step 1: Initialize clients
    extraction_client, cos_client = initialize_clients()
    if not extraction_client or not cos_client:
        return 1

    # Step 2: Submit extraction job
    job_id = run_extraction_job(extraction_client, input_pdf, output_results)
    if not job_id:
        return 1

    # Step 3: Monitor job
    job_completed = monitor_job(extraction_client, job_id, timeout=300)
    if not job_completed:
        print_error("\nJob did not complete successfully")
        return 1

    # Step 4: Retrieve results
    results = retrieve_results(cos_client, output_results, local_save_path)
    if not results:
        return 1

    # Step 5: Analyze results
    analyze_results(results)

    # Summary
    print_header("Test Summary")
    print_success("🎉 Text Extraction Pipeline Completed Successfully!")

    print_info("\nWhat we accomplished:")
    print_info("  ✅ PDF stored in Cloud Object Storage")
    print_info("  ✅ Text extraction job submitted to watsonx.ai")
    print_info("  ✅ Job monitored to completion")
    print_info("  ✅ Results retrieved from COS")
    print_info("  ✅ Extraction quality analyzed")

    print_info("\nNext steps:")
    print_info("  1. Process remaining EEFF PDFs (2015-2022)")
    print_info("  2. Extract contract PDFs")
    print_info("  3. Configure Document Field Extractor for structured data")
    print_info("  4. Build automated batch processing pipeline")

    return 0


if __name__ == "__main__":
    sys.exit(main())

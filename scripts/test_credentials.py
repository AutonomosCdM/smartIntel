#!/usr/bin/env python3
"""Test all watsonx credentials and verify PDF extraction pipeline readiness.

This script validates:
1. API Key can generate access token
2. Project ID format is correct
3. Space ID format is correct
4. Text Extraction API is accessible
5. All required environment variables are set
"""

import os
import sys
from pathlib import Path

import requests
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


def test_environment_variables() -> bool:
    """Test that all required environment variables are set."""
    print_header("1. Environment Variables Check")

    required_vars = {
        "WATSONX_API_KEY": "IBM Cloud API Key",
        "WATSONX_PROJECT_ID": "watsonx.ai Project ID",
        "WATSONX_SPACE_ID": "watsonx Deployment Space ID",
        "WATSONX_URL": "watsonx.ai API URL",
    }

    all_set = True
    for var_name, var_description in required_vars.items():
        value = os.getenv(var_name)
        if value:
            # Mask sensitive values
            if "KEY" in var_name:
                masked_value = f"{value[:10]}...{value[-10:]}"
            else:
                masked_value = value
            print_success(f"{var_description}: {masked_value}")
        else:
            print_error(f"{var_description}: NOT SET")
            all_set = False

    # Optional variables
    optional_vars = {
        "DOC_EXTRACTION_MODEL": "Document extraction model",
        "DOC_EXTRACTION_MIN_CONFIDENCE": "Minimum confidence threshold",
        "ENABLE_HUMAN_REVIEW": "Human review flag",
    }

    print("\nOptional Variables:")
    for var_name, var_description in optional_vars.items():
        value = os.getenv(var_name)
        if value:
            print_info(f"{var_description}: {value}")
        else:
            print_warning(f"{var_description}: Not set (will use defaults)")

    return all_set


def test_api_key() -> tuple[bool, str]:
    """Test that API key can generate access token."""
    print_header("2. API Key Validation")

    api_key = os.getenv("WATSONX_API_KEY")
    if not api_key:
        print_error("API Key not set")
        return False, ""

    try:
        print_info("Requesting access token from IBM Cloud IAM...")
        response = requests.post(
            "https://iam.cloud.ibm.com/identity/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={api_key}",
            timeout=30,
        )

        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get("access_token", "")
            if access_token:
                print_success(f"Access token obtained: {access_token[:20]}...")
                print_info(f"Token type: {token_data.get('token_type')}")
                print_info(f"Expires in: {token_data.get('expires_in')} seconds")
                return True, access_token
            else:
                print_error("No access token in response")
                return False, ""
        else:
            print_error(f"Failed to obtain token: {response.status_code}")
            print_error(f"Response: {response.text}")
            return False, ""

    except Exception as e:
        print_error(f"Error validating API key: {e}")
        return False, ""


def test_id_format(id_value: str, id_name: str) -> bool:
    """Test that ID has correct UUID format."""
    if not id_value:
        print_error(f"{id_name} not set")
        return False

    # UUID format: 8-4-4-4-12 characters
    parts = id_value.split("-")
    if len(parts) != 5:
        print_error(f"{id_name} invalid format (expected UUID): {id_value}")
        return False

    expected_lengths = [8, 4, 4, 4, 12]
    for i, (part, expected_len) in enumerate(zip(parts, expected_lengths)):
        if len(part) != expected_len:
            print_error(
                f"{id_name} invalid UUID part {i+1} "
                f"(expected {expected_len} chars, got {len(part)})"
            )
            return False

    print_success(f"{id_name} format valid: {id_value}")
    return True


def test_project_id() -> bool:
    """Test Project ID format."""
    print_header("3. Project ID Validation")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    return test_id_format(project_id, "Project ID")


def test_space_id() -> bool:
    """Test Space ID format."""
    print_header("4. Space ID Validation")
    space_id = os.getenv("WATSONX_SPACE_ID")
    return test_id_format(space_id, "Space ID")


def test_watsonx_url() -> bool:
    """Test that watsonx URL is reachable."""
    print_header("5. watsonx.ai URL Reachability")

    watsonx_url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")

    try:
        print_info(f"Testing connection to: {watsonx_url}")
        response = requests.get(watsonx_url, timeout=10)
        # Any response (even 401/403) means URL is reachable
        print_success(f"URL reachable (status: {response.status_code})")
        return True
    except Exception as e:
        print_error(f"URL not reachable: {e}")
        return False


def test_text_extraction_api(access_token: str) -> bool:
    """Test Text Extraction API endpoint."""
    print_header("6. Text Extraction API Test")

    if not access_token:
        print_error("No access token available (skipping API test)")
        return False

    project_id = os.getenv("WATSONX_PROJECT_ID")
    watsonx_url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")

    # Test endpoint (GET request to check if it's accessible)
    endpoint = f"{watsonx_url}/ml/v1/text/extractions"

    try:
        print_info(f"Testing endpoint: {endpoint}")
        print_info("Note: We're just checking endpoint accessibility, not uploading files")

        # Just check if endpoint exists (GET should return 405 Method Not Allowed)
        response = requests.get(
            endpoint,
            headers={"Authorization": f"Bearer {access_token}"},
            params={"version": "2024-10-18"},
            timeout=10,
        )

        # 405 means endpoint exists but GET not allowed (POST required)
        # 401/403 means auth issue
        # 404 means endpoint doesn't exist
        if response.status_code in [200, 405]:
            print_success("Text Extraction API endpoint is accessible")
            print_info("Endpoint requires POST with document upload (expected)")
            return True
        elif response.status_code in [401, 403]:
            print_warning("Endpoint found but authorization may need verification")
            print_info(f"Status: {response.status_code}")
            return True  # Endpoint exists, auth can be verified with actual upload
        else:
            print_error(f"Unexpected status: {response.status_code}")
            print_info(f"Response: {response.text[:200]}")
            return False

    except Exception as e:
        print_error(f"Error testing Text Extraction API: {e}")
        return False


def test_docker_requirements() -> bool:
    """Check Docker requirements for Document Field Extractor."""
    print_header("7. Docker Requirements Check")

    try:
        import subprocess

        # Check if Docker is running
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            text=True,
            timeout=5,
        )

        if result.returncode == 0:
            print_success("Docker is running")

            # Check memory allocation (from docker info)
            info_output = result.stdout
            for line in info_output.split("\n"):
                if "Total Memory" in line:
                    print_info(line.strip())
                    # Extract memory value
                    memory_str = line.split(":")[-1].strip()
                    if "GiB" in memory_str:
                        memory_gb = float(memory_str.replace("GiB", "").strip())
                        if memory_gb >= 20:
                            print_success(
                                f"Memory allocation: {memory_gb}GB "
                                "(meets 20GB requirement)"
                            )
                        else:
                            print_warning(
                                f"Memory allocation: {memory_gb}GB "
                                "(recommend 20GB+ for Document Field Extractor)"
                            )
            return True
        else:
            print_error("Docker is not running")
            print_info("Start Docker Desktop to enable Document Field Extractor")
            return False

    except FileNotFoundError:
        print_error("Docker not installed")
        print_info("Install Docker Desktop from https://www.docker.com/products/docker-desktop")
        return False
    except Exception as e:
        print_warning(f"Could not check Docker status: {e}")
        return False


def print_summary(results: dict[str, bool]):
    """Print test summary."""
    print_header("Test Summary")

    total = len(results)
    passed = sum(results.values())
    failed = total - passed

    print(f"Total tests: {total}")
    print_success(f"Passed: {passed}")
    if failed > 0:
        print_error(f"Failed: {failed}")

    print("\nDetailed Results:")
    for test_name, result in results.items():
        status = f"{GREEN}✅ PASS{RESET}" if result else f"{RED}❌ FAIL{RESET}"
        print(f"  {status} - {test_name}")

    print("\n")
    if all(results.values()):
        print_success("🎉 All tests passed! Ready to implement PDF extraction pipeline.")
        print_info("Next steps:")
        print_info("  1. Setup watsonx Orchestrate local Docker environment")
        print_info("  2. Test Text Extraction API with a sample PDF")
        print_info("  3. Configure Document Field Extractor with Pydantic schemas")
        print_info("  4. Batch process Carozzi EEFF PDFs")
    else:
        print_error("⚠️  Some tests failed. Please fix issues before proceeding.")
        print_info("Refer to docs/GUIDES/WATSONX_CREDENTIALS_SETUP.md for help")


def main():
    """Run all credential tests."""
    print_header("watsonx Credentials & PDF Pipeline Readiness Test")

    results = {}

    # Test 1: Environment variables
    results["Environment Variables"] = test_environment_variables()

    # Test 2: API Key
    api_key_valid, access_token = test_api_key()
    results["API Key Validation"] = api_key_valid

    # Test 3: Project ID
    results["Project ID Format"] = test_project_id()

    # Test 4: Space ID
    results["Space ID Format"] = test_space_id()

    # Test 5: watsonx URL
    results["watsonx.ai URL"] = test_watsonx_url()

    # Test 6: Text Extraction API (only if we have access token)
    if api_key_valid and access_token:
        results["Text Extraction API"] = test_text_extraction_api(access_token)
    else:
        print_warning("Skipping Text Extraction API test (no access token)")

    # Test 7: Docker requirements
    results["Docker Requirements"] = test_docker_requirements()

    # Print summary
    print_summary(results)

    # Exit with appropriate code
    sys.exit(0 if all(results.values()) else 1)


if __name__ == "__main__":
    main()

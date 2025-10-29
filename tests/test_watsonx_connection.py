"""Test watsonx API connection with real credentials.

These tests are optional and will be skipped if credentials are not available.
Run locally with .env file or CI will skip these tests.
"""

import os

import pytest
import requests
from dotenv import load_dotenv

# Load environment variables (no-op in CI, loads .env locally)
load_dotenv()

API_KEY = os.getenv("WATSONX_API_KEY")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
WATSONX_URL = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")

# Skip all tests if credentials not available
pytestmark = pytest.mark.skipif(
    not API_KEY or not PROJECT_ID,
    reason="watsonx credentials not configured (optional integration test)",
)


def test_api_key_valid():
    """Test that API key can generate access token."""
    print("\n🔑 Testing API Key validity...")

    response = requests.post(
        "https://iam.cloud.ibm.com/identity/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={API_KEY}",
        timeout=30,
    )

    assert response.status_code == 200, f"API Key invalid: {response.text}"
    token_data = response.json()
    assert "access_token" in token_data, "No access token in response"

    print("✅ API Key valid")
    print(f"✅ Access token obtained: {token_data['access_token'][:20]}...")
    return token_data["access_token"]


def test_project_id_format():
    """Test that Project ID has correct format."""
    print("\n🆔 Testing Project ID format...")

    # UUID format: 8-4-4-4-12 characters
    parts = PROJECT_ID.split("-")
    assert len(parts) == 5, f"Invalid UUID format: {PROJECT_ID}"
    assert len(parts[0]) == 8, "Invalid UUID part 1"
    assert len(parts[1]) == 4, "Invalid UUID part 2"
    assert len(parts[2]) == 4, "Invalid UUID part 3"
    assert len(parts[3]) == 4, "Invalid UUID part 4"
    assert len(parts[4]) == 12, "Invalid UUID part 5"

    print(f"✅ Project ID format valid: {PROJECT_ID}")


def test_watsonx_url_reachable():
    """Test that watsonx URL is reachable."""
    print("\n🌐 Testing watsonx URL reachability...")

    response = requests.get(WATSONX_URL, timeout=10)
    # Any response (even 401/403) means URL is reachable
    print(f"✅ watsonx URL reachable: {WATSONX_URL} (status: {response.status_code})")


if __name__ == "__main__":
    print("=" * 60)
    print("watsonx API Connection Test")
    print("=" * 60)

    try:
        test_api_key_valid()
        test_project_id_format()
        test_watsonx_url_reachable()

        print("\n" + "=" * 60)
        print("🎉 All tests passed! watsonx credentials configured correctly.")
        print("=" * 60)
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"❌ Test failed: {e}")
        print("=" * 60)
        raise

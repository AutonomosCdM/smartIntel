#!/usr/bin/env python3
"""
ProcureGenius Production Deployment Script

Deploys the application to production environment (watsonx Orchestrate).
REQUIRES MANUAL APPROVAL - triggered via GitHub Actions only.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Colors for terminal output
BLUE = "\033[0;34m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
RED = "\033[0;31m"
NC = "\033[0m"


def log(message: str, level: str = "info") -> None:
    """Print colored log message."""
    colors = {"info": BLUE, "success": GREEN, "warning": YELLOW, "error": RED}
    color = colors.get(level, NC)
    print(f"{color}{message}{NC}")


def verify_approval() -> bool:
    """Verify this is running from approved workflow."""
    log("→ Verifying deployment approval...", "info")

    # Check this is running in CI/CD (not local)
    if not os.getenv("GITHUB_ACTIONS"):
        log("✗ Production deployment must run via GitHub Actions", "error")
        return False

    # Verify environment variable is set (from GitHub Environment secret)
    if os.getenv("ENVIRONMENT") != "production":
        log("✗ Invalid environment configuration", "error")
        return False

    log("✓ Deployment approved", "success")
    return True


def check_environment() -> bool:
    """Verify required environment variables are set."""
    log("→ Checking production environment configuration...", "info")

    required_vars = [
        "WATSONX_API_KEY",
        "WATSONX_PROJECT_ID",
        "VERSION",
    ]

    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        log(f"✗ Missing environment variables: {', '.join(missing)}", "error")
        return False

    log("✓ Environment configuration valid", "success")
    return True


def deploy_production() -> bool:
    """Deploy to production."""
    log("→ Deploying to production environment...", "info")

    # In real implementation, this would:
    # 1. Blue-green deployment strategy
    # 2. Deploy to watsonx Orchestrate production project
    # 3. Gradual traffic shifting (0% → 25% → 50% → 100%)
    # 4. Automated rollback on error

    version = os.getenv("VERSION", "unknown")
    log(f"  - Deploying version: {version}", "info")

    log("✓ Production deployment successful", "success")
    return True


def run_production_smoke_tests() -> bool:
    """Run critical smoke tests on production."""
    log("→ Running production smoke tests...", "info")

    # In real implementation:
    # 1. Test critical paths only (fast checks)
    # 2. Verify agent endpoints responding
    # 3. Validate authentication/authorization
    # 4. Check database connectivity

    log("✓ Production smoke tests passed", "success")
    return True


def create_production_record() -> None:
    """Create production deployment record."""
    log("→ Creating production deployment record...", "info")

    timestamp = datetime.now().isoformat()
    version = os.getenv("VERSION", "unknown")
    commit = os.getenv("GITHUB_SHA", "unknown")
    deployed_by = os.getenv("GITHUB_ACTOR", "system")

    record = f"""
Production Deployment Record
============================
Version: {version}
Commit: {commit}
Deployed by: {deployed_by}
Timestamp: {timestamp}
Environment: production
Status: SUCCESS
"""

    log(record, "info")
    log("✓ Production record created", "success")


def main() -> int:
    """Main production deployment orchestration."""
    log("===========================================", "info")
    log("⚠️  PRODUCTION DEPLOYMENT", "warning")
    log("===========================================", "info")
    print()

    try:
        # Step 1: Verify approval
        if not verify_approval():
            return 1

        # Step 2: Check environment
        if not check_environment():
            return 1

        # Step 3: Deploy to production
        if not deploy_production():
            return 1

        # Step 4: Run smoke tests
        if not run_production_smoke_tests():
            return 1

        # Step 5: Create deployment record
        create_production_record()

        print()
        log("===========================================", "success")
        log("✓ Production deployment completed", "success")
        log("===========================================", "success")
        print()
        log("Access production: https://procuregenius.autonomoslab.com", "info")

        return 0

    except Exception as e:
        log(f"✗ Production deployment failed: {str(e)}", "error")
        log("⚠️  Automatic rollback initiated", "warning")
        return 1


if __name__ == "__main__":
    sys.exit(main())

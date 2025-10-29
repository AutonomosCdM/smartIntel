# GitHub Configuration Guide

**Status**: ⚠️ PLACEHOLDERS CONFIGURED - UPDATE BEFORE USE

This guide explains how to update GitHub secrets and configure deployment approvals for the smartIntel project.

---

## Current Status

### ✅ Configured

| Component | Status | Details |
|-----------|--------|---------|
| **Repository** | ✅ Active | https://github.com/AutonomosCdM/smartIntel |
| **CI/CD Workflows** | ✅ Deployed | 3 workflows in `.github/workflows/` |
| **GitHub Secrets** | ⚠️ Placeholders | 4 secrets created, need real values |
| **Environment** | ⚠️ Incomplete | `production-approval` created, needs reviewers |

### ⚠️ Requires Action

1. **Update watsonx API credentials** (before first deploy)
2. **Configure production reviewers** (before production deploy)
3. **Test CI pipeline** (after secrets updated)

---

## 1. Update GitHub Secrets

### Current Placeholder Secrets

```bash
WATSONX_API_KEY_STAGING        = "PLACEHOLDER_STAGING_API_KEY_UPDATE_BEFORE_USE"
WATSONX_PROJECT_ID_STAGING     = "PLACEHOLDER_STAGING_PROJECT_ID_UPDATE_BEFORE_USE"
WATSONX_API_KEY_PRODUCTION     = "PLACEHOLDER_PRODUCTION_API_KEY_UPDATE_BEFORE_USE"
WATSONX_PROJECT_ID_PRODUCTION  = "PLACEHOLDER_PRODUCTION_PROJECT_ID_UPDATE_BEFORE_USE"
```

### How to Get watsonx Credentials

1. **Go to IBM Cloud**: https://cloud.ibm.com/
2. **Navigate to watsonx.ai**: Dashboard → AI/ML → watsonx.ai
3. **Create/Select Project**:
   - Projects → Create new project (or select existing)
   - Note the **Project ID** (found in Project settings)
4. **Generate API Key**:
   - Profile → API keys → Create an IBM Cloud API key
   - Copy and save securely (only shown once)

### Update Secrets via GitHub CLI

```bash
# Update Staging credentials
gh secret set WATSONX_API_KEY_STAGING --body "your-actual-staging-api-key" --repo AutonomosCdM/smartIntel
gh secret set WATSONX_PROJECT_ID_STAGING --body "your-actual-staging-project-id" --repo AutonomosCdM/smartIntel

# Update Production credentials
gh secret set WATSONX_API_KEY_PRODUCTION --body "your-actual-production-api-key" --repo AutonomosCdM/smartIntel
gh secret set WATSONX_PROJECT_ID_PRODUCTION --body "your-actual-production-project-id" --repo AutonomosCdM/smartIntel
```

### Update Secrets via GitHub UI

1. Go to: https://github.com/AutonomosCdM/smartIntel/settings/secrets/actions
2. Click on each secret name
3. Click "Update secret"
4. Paste new value
5. Click "Update secret"

**Verification:**
```bash
# List all secrets (values hidden for security)
gh secret list --repo AutonomosCdM/smartIntel
```

---

## 2. Configure Production Approval

### Current Environment Status

- **Environment**: `production-approval` (created)
- **Reviewers**: ⚠️ NOT CONFIGURED
- **Protection**: Manual approval required before production deploy

### Configure Reviewers (GitHub UI - Recommended)

1. **Go to Environments**:
   - https://github.com/AutonomosCdM/smartIntel/settings/environments

2. **Click on `production-approval`**

3. **Add Required Reviewers**:
   - Scroll to "Environment protection rules"
   - Check "Required reviewers"
   - Add your username: `AutonomosCdM`
   - Click "Save protection rules"

4. **Optional Settings**:
   - **Wait timer**: 0 minutes (deploy immediately after approval)
   - **Allow administrators to bypass**: Keep enabled (for emergencies)
   - **Prevent self-review**: Disabled (allows you to approve your own deploys)

### How Production Deploys Will Work

```
1. Developer tags release:
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin v1.0.0

2. GitHub Actions triggers production-gate.yml

3. Workflow runs pre-flight checks (tests, build)

4. ⏸️  PAUSES and requests your approval

5. You review:
   - Go to: https://github.com/AutonomosCdM/smartIntel/actions
   - Click on the workflow run
   - Click "Review deployments"
   - Select "production-approval"
   - Add comment (optional)
   - Click "Approve and deploy"

6. Deployment proceeds to production

7. Post-deploy validation runs

8. You receive notification (success or failure)
```

---

## 3. Test CI Pipeline

### Option A: Test via Pull Request

```bash
# Create test branch
git checkout -b test/verify-ci
echo "# CI Test" >> README.md
git add README.md
git commit -m "test: verify CI pipeline configuration"
git push origin test/verify-ci

# Create PR via CLI
gh pr create --title "Test: Verify CI Pipeline" --body "Testing CI configuration with placeholder secrets"

# Watch CI run
gh pr checks
```

**Expected Result**:
- ✅ Lint (ruff) - PASS
- ✅ Type Check (mypy) - PASS
- ✅ Tests (pytest) - PASS (smoke tests only)

**If CI fails with API errors**: Secrets still have placeholder values. This is expected until you update them with real watsonx credentials.

### Option B: Test via Direct Push

```bash
# Make a small change
echo "# CI Update: $(date)" >> README.md
git add README.md
git commit -m "test: verify CI on direct push"
git push origin master

# Watch workflow
gh run watch
```

### Expected Workflow Behavior

| Trigger | Workflow | Expected Action |
|---------|----------|-----------------|
| Push to any branch | `ci.yml` | ✅ Runs lint + test + type check |
| Push to `main` | `ci.yml` + `staging-deploy.yml` | ✅ CI runs, then auto-deploy to staging |
| Push tag `v*` | `production-gate.yml` | ⏸️ CI + pre-flight, then WAITS for approval |

---

## 4. Staging Deployment

### Trigger Staging Deploy

```bash
# Merge to main (or push directly)
git checkout master
git merge test/verify-ci
git push origin master

# Watch deployment
gh run list --workflow=staging-deploy.yml
gh run view --log  # View latest run logs
```

**What Happens**:
1. `ci.yml` runs first (lint, test, build)
2. If CI passes, `staging-deploy.yml` triggers automatically
3. Deploys to staging environment (currently stub, will deploy when implementation ready)
4. Runs smoke tests on staging

**Note**: Deployment scripts are currently stubs. They'll print success messages but won't actually deploy until you implement the real deployment logic in:
- `scripts/deploy-staging.py`
- `scripts/deploy-production.py`

---

## 5. Production Deployment

### Before First Production Deploy

**Checklist**:
- [ ] watsonx API credentials updated (real values, not placeholders)
- [ ] Production reviewer configured (you as approver)
- [ ] Staging tested and validated
- [ ] Deployment scripts implemented (or stub warnings accepted)

### Create Production Release

```bash
# Ensure you're on latest main
git checkout master
git pull origin master

# Create annotated tag
git tag -a v1.0.0 -m "Release v1.0.0: Initial MVP

Features:
- ProcureGenius AI agents
- Predictive intelligence module
- Carozzi demo integration

Tested on staging: https://staging.example.com
Demo video: https://demo-link
"

# Push tag (triggers production workflow)
git push origin v1.0.0

# Monitor workflow
gh run watch
```

### Approve Production Deploy

1. **Check workflow status**:
   ```bash
   gh run list --workflow=production-gate.yml
   ```

2. **Go to Actions page**:
   - https://github.com/AutonomosCdM/smartIntel/actions

3. **Click on the waiting workflow run**

4. **Review deployment request**:
   - Verify all pre-flight checks passed
   - Review commit history
   - Check staging validation

5. **Approve or Reject**:
   - Click "Review deployments"
   - Select `production-approval`
   - Add comment: "Approved for production - Demo ready for hackathon"
   - Click "Approve and deploy"

6. **Monitor deployment**:
   ```bash
   gh run view --log
   ```

---

## 6. Rollback Procedure

### If Production Deploy Fails

```bash
# Find last known good version
git tag -l "v*" --sort=-version:refname | head -5

# Create rollback tag
git tag -a v1.0.1-rollback -m "Rollback to v1.0.0" v1.0.0

# Push rollback tag (triggers production workflow again)
git push origin v1.0.1-rollback

# Approve when ready
# (Same approval process as normal deploy)
```

### Emergency Manual Rollback

If automated rollback fails:

1. **SSH to production server** (or access deployment platform)
2. **Run rollback script**:
   ```bash
   ./scripts/rollback.sh v1.0.0
   ```
3. **Verify health**:
   ```bash
   curl https://api.procuregenius.ai/health
   ```

---

## 7. Troubleshooting

### CI Fails with "Secret not found"

**Symptom**: Workflow fails with "WATSONX_API_KEY_STAGING not found"

**Solution**:
```bash
# Verify secrets exist
gh secret list --repo AutonomosCdM/smartIntel

# Re-set secret
gh secret set WATSONX_API_KEY_STAGING --body "your-api-key"
```

### Staging Deploy Never Triggers

**Symptom**: CI passes but staging deploy doesn't start

**Possible Causes**:
1. Workflow file syntax error:
   ```bash
   # Validate YAML locally
   yamllint .github/workflows/staging-deploy.yml
   ```

2. Workflow disabled:
   - Go to Actions → Workflows → staging-deploy
   - Click "Enable workflow" if disabled

3. Branch protection preventing workflow_run:
   - Check Settings → Branches → main
   - Ensure workflow_run trigger is allowed

### Production Approval Not Showing

**Symptom**: Production workflow runs but no approval button

**Solution**:
1. Go to: https://github.com/AutonomosCdM/smartIntel/settings/environments
2. Click `production-approval`
3. Verify "Required reviewers" is checked and you're listed
4. Re-run workflow:
   ```bash
   gh run rerun <run-id>
   ```

### Deployment Succeeds But Nothing Happens

**Symptom**: Workflow shows success but app not updated

**Cause**: Deployment scripts are stubs (expected during hackathon prep)

**Solution**:
- Implement real deployment logic in `scripts/deploy-*.py`
- OR accept stub behavior and deploy manually for hackathon demo

---

## 8. Security Best Practices

### Never Commit Secrets

**Protected by `.gitignore`**:
- `.env` files
- `*.key`, `*.pem` files
- `config/*.json` (except examples)
- `secrets/` directory

**If you accidentally commit a secret**:
```bash
# Remove from history (DANGEROUS - coordinate with team)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (breaks others' repos)
git push origin --force --all

# Rotate the exposed secret immediately
```

### Secret Rotation

**When to rotate**:
- Every 90 days (good practice)
- After team member leaves
- If secret exposed in logs/commits
- Before major production release

**How to rotate**:
1. Generate new API key in IBM Cloud
2. Update GitHub secret (old key still works)
3. Deploy to staging first
4. Verify staging works
5. Deploy to production
6. Delete old API key in IBM Cloud

---

## 9. GitHub Actions Limits

### Free Tier Limits (Public Repos)

- **Compute**: Unlimited minutes
- **Storage**: 500 MB packages, 1 GB actions cache
- **Concurrent jobs**: 20
- **Job execution time**: 6 hours max

### Optimization Tips

**Cache dependencies**:
```yaml
- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```

**Skip CI for docs**:
```bash
git commit -m "docs: update README [skip ci]"
```

**Use matrix builds for parallel testing**:
```yaml
strategy:
  matrix:
    python-version: [3.11, 3.12]
```

---

## 10. Quick Reference Commands

### Secrets Management
```bash
# List secrets
gh secret list --repo AutonomosCdM/smartIntel

# Set secret
gh secret set SECRET_NAME --body "value"

# Delete secret
gh secret delete SECRET_NAME
```

### Workflow Management
```bash
# List workflows
gh workflow list

# View workflow runs
gh run list --workflow=ci.yml

# Watch live run
gh run watch

# Re-run failed run
gh run rerun <run-id>

# Cancel running workflow
gh run cancel <run-id>
```

### Environment Management
```bash
# List environments (via API)
gh api repos/AutonomosCdM/smartIntel/environments

# View specific environment
gh api repos/AutonomosCdM/smartIntel/environments/production-approval
```

---

## Next Steps

1. **Now**: Update secrets with real watsonx credentials
2. **Before Dev**: Configure production reviewers
3. **After Setup**: Test CI with a small PR
4. **During Hackathon**: Use staging liberally, production carefully
5. **Before Demo**: Ensure production deploy working end-to-end

---

**Last Updated**: 2025-10-29
**Maintained By**: Autonomos Lab - Toto
**Repository**: https://github.com/AutonomosCdM/smartIntel

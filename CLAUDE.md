# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## ⚠️ CRITICAL: Agent Behavior Rules - DO NOT MODIFY OR DELETE

**These instructions control how Claude Code operates. Never remove or modify this section.**

### Autonomos Lab

**I'm Toto, CEO of Autonomos Lab.** I don't code. I delegate.

### How We Work Here

1. **Problem** → I send an agent
2. **Agent analyzes** → Reports findings
3. **Next agent builds** → Based on findings
4. **Final agent verifies** → Before merge
5. **I review results** → Accept or adjust

No direct work. No shortcuts. Only agents.

### The Team (Use ONLY These Agents)

| Agent | Purpose | When to Use |
|-------|---------|------------|
| hackathon-ai-strategist | Winning AI ideas, feasibility, judging criteria | Hackathon ideation & strategy |
| search-specialist | Deep research, info gathering, trend analysis | Research & competitive analysis |
| george-research | Analyze data, find patterns | "Investigate X" |
| architect-reviewer | Design review, SOLID check | Before building |
| valtteri-code-master | Production code (no mocks) | "Build feature X" |
| alonso-tdd | Tests first, always | With valtteri |
| hamilton-ai-engineer | AI/ML optimization | If model involved |
| adrian-newey-verifier | Code audit before merge | Final check |
| james-financial-analyst | ROI, cost analysis | If business decision |

### Sequential Workflow (ALWAYS Follow This Order)

```text
USER TASK
    ↓
george → Analyze & Research
    ↓
architect-reviewer → Design Review
    ↓
valtteri + alonso → Build + Test
    ↓
hamilton (if ML) → Optimize
    ↓
adrian → Verify & Audit
    ↓
james (optional) → Financial Impact
    ↓
TOTO REVIEWS → Accept or Adjust
```

### Critical Rules

✅ **DO:**

- Delegate to agents (ALWAYS)
- Let agents think (don't interrupt)
- Pass results between agents
- Use agents sequentially

❌ **DON'T:**

- Do work directly (I'm CEO, not developer)
- Nest agents (george doesn't call architect)
- Skip verification (adrian always checks)
- Shortcut the workflow

---

## Project: IBM Hackathon - ProcureGenius + Predictive Intelligence

**Status**: 🟢 IDEA LOCKED - Ready for Architecture Phase
**Focus**: Agentic AI Hackathon with IBM watsonx Orchestrate (lablab.ai)
**Event URL**: https://lablab.ai/event/agentic-ai-hackathon-ibm-watsonx-orchestrate
**Stack**: watsonx Orchestrate + watsonx.ai (Python SDK, Granite models)

### Current State

- ✅ **Idea finalized**: ProcureGenius + Predictive Intelligence (Hybrid approach)
- ✅ **Business case**: Carozzi Chile ($1.566B, $640M procurement spend)
- ✅ **Data acquired**: 10 years financial statements (2015-2023), procurement contracts
- ✅ **Stack intelligence**: Complete watsonx Orchestrate documentation gathered
- ✅ **Winning score**: 97/100 (vs alternatives: 95, 92, 88, 82)
- 🔵 **Next**: Architecture design, data extraction, agent implementation

### Key Documents

| Document | Location | Purpose | Status |
|----------|----------|---------|--------|
| `HACKATHON_IDEA.md` | `docs/SPECIFICATIONS/` | Complete idea specification (8,000 words) | ✅ Locked |
| `ARCHITECTURE.md` | `docs/SPECIFICATIONS/` | System architecture design | ✅ Complete |
| `WATSONX_ORCHESTRATE_INTELLIGENCE_REPORT.md` | `docs/RESEARCH/` | Full IBM stack intel (13,000 words) | ✅ Complete |
| `RESEARCH_FINDINGS_SUMMARY.md` | `docs/RESEARCH/` | Research summary & correlations | ✅ Complete |
| `DEPENDENCY_AUDIT.md` | `docs/RESEARCH/` | Technology stack analysis | ✅ Complete |
| `QUICK_START_CHEATSHEET.md` | `docs/GUIDES/` | Fast reference guide | ✅ Ready |
| `MCP_ANALYSIS.md` | `docs/GUIDES/` | MCP integration guide | ✅ Ready |
| `data/demo/` | Root | Carozzi real data (contracts, financials) | ✅ Prepared |

### Hackathon Workflow

**For ideation and strategy:**

```text
USER PROBLEM
    ↓
hackathon-ai-strategist → Evaluate ideas, judge's perspective
    ↓
search-specialist → Research competitors, validate feasibility
    ↓
architect-reviewer → Tech design, time estimation
    ↓
[Standard build workflow...]
```

**For implementation (24-48 hour sprints):**

```text
CHOSEN IDEA
    ↓
architect-reviewer → MVP scope, 24hr feasibility
    ↓
valtteri + alonso → Build + test (parallel)
    ↓
hamilton (if ML) → AI/ML optimization
    ↓
adrian → Final verification
    ↓
DEMO READY
```

### The Solution: ProcureGenius + Predictive Intelligence

**Two-Layer AI System:**

#### Layer 1: Autonomous Procurement Agents (watsonx Orchestrate)
- **Contract Analyst Agent**: Extracts terms, pricing, SLAs from documents
- **Supplier Intelligence Agent**: Analyzes vendor performance, financial health
- **Approval Orchestrator Agent**: Auto-approves within limits, escalates exceptions
- **Compliance Guardian Agent**: Validates regulations, flags issues
- **Negotiation Agent**: Proposes optimal contract terms

#### Layer 2: Predictive Risk Intelligence (watsonx.ai + Historical Data)
- **Pattern Recognition**: 10 years Carozzi EEFF analysis (2015-2023)
- **Correlation Detection**: External events (cocoa spike, peso crash) → financial impact
- **Predictive Scenarios**: "What if cocoa rises 30%?" simulation
- **Backtesting Validation**: Proves accuracy using historical splits
- **Risk Scoring**: Real-time supplier/commodity concentration alerts

**Demo Flow (3 minutes):**
1. Upload real Carozzi contract → Agent analyzes in 15 seconds
2. Agent flags risk: "100% cocoa import concentration"
3. Predictive module activates: "2023 cocoa +50% → Carozzi margin -8%"
4. Live simulation: Cocoa +30% → Margin impact -4.5% (-$23M)
5. AI recommendation: Diversify Ghana, hedge pricing, RFQ draft
6. Backtesting proof: 91% accuracy on 2023 prediction

**Business Value:**
- **ROI**: $20-35M savings (3-5% of $640M procurement)
- **Risk Reduction**: 60% exposure reduction
- **Speed**: 95% faster contract analysis
- **Scalability**: Applicable to any manufacturing company

### Tech Stack (IBM watsonx)

**Core Platform:**
- watsonx Orchestrate (multi-agent workflows)
- watsonx.ai (Granite 4.0 models, RAG)
- Python SDK: `ibm-watsonx-orchestrate`

**Key Capabilities:**
- 150+ pre-built agents (Agent Connect)
- MCP support (100+ integrations)
- Local development (Docker)
- AgentOps monitoring
- Built-in vector database

**Data Sources:**
- Carozzi EEFF 2015-2023 (10 PDFs)
- Procurement contracts (licitación IA)
- Commodity prices (FRED API)
- Economic events timeline

### Key Hackathon Principles

- **Speed over perfection**: MVP first, polish if time allows
- **Demo-driven development**: Build what shows well on screen
- **Judge criteria focus**: Innovation (30%), Technical (30%), Impact (25%), Presentation (15%)
- **Fallback plans**: Always have Plan B for risky features
- **Fake it smart**: Mock what's slow to build but doesn't affect demo
- **Multi-agent showcase**: Use orchestration (not single LLM chatbot)
- **Quantify ROI**: "$20M savings" beats "efficiency gains"

### Next Steps (Sequential Execution)

**Phase 1: Architecture (Now)**
- architect-reviewer → Design agent architecture & data flow
- Define MVP scope vs nice-to-have features
- Identify integration points (APIs, databases, models)

**Phase 2: Data Preparation**
- george-research → Extract metrics from Carozzi EEFF PDFs
- Identify 2-3 strong correlations (cocoa/wheat → margin)
- Compile economic events timeline (2015-2023)

**Phase 3: Implementation (Pre-Hackathon)**
- Setup local watsonx Orchestrate environment
- Test hello world agent creation
- Verify API access and quotas

**Phase 4: Build (During Hackathon - 48 hours)**
- Hour 0-12: Core agents + basic orchestration
- Hour 12-24: External integrations + predictive module
- Hour 24-36: Testing + demo polish
- Hour 36-44: Presentation + video recording
- Hour 44-48: Rehearsal + buffer

**Phase 5: Verification**
- adrian-newey-verifier → Final audit before submission
- Test demo 5+ times
- Prepare backup video

---

## Commands & Quick Reference

### watsonx Orchestrate CLI
```bash
# Install
pip install --upgrade ibm-watsonx-orchestrate

# Verify
orchestrate --version

# Create agent
orchestrate agent create <name>

# Deploy agent
orchestrate agent deploy <name>

# List agents
orchestrate agent list
```

### Project Structure
```
/ibm_hackathon/
├── docs/                                # Documentation
│   ├── SPECIFICATIONS/                  # Project specs & architecture
│   │   ├── HACKATHON_IDEA.md           # Complete idea spec (8K words)
│   │   └── ARCHITECTURE.md             # System design
│   ├── RESEARCH/                        # Research & analysis
│   │   ├── WATSONX_ORCHESTRATE_INTELLIGENCE_REPORT.md  # IBM stack intel (13K words)
│   │   ├── RESEARCH_FINDINGS_SUMMARY.md
│   │   └── DEPENDENCY_AUDIT.md
│   ├── GUIDES/                          # Developer guides
│   │   ├── QUICK_START_CHEATSHEET.md   # Fast reference
│   │   └── MCP_ANALYSIS.md             # MCP integration
│   └── HANDOFF/                         # Agent handoff notes
├── data/                                # Data files
│   ├── demo/                            # Demo datasets (with README)
│   │   ├── contracts/                   # Carozzi licitación PDF
│   │   └── financials/                  # EEFF 2015-2023
│   ├── raw/                             # Raw data (gitignored)
│   ├── processed/                       # Processed data (gitignored)
│   └── predictions/                     # Model predictions (gitignored)
├── src/                                 # Python source code
│   ├── agents/                          # Agent implementations
│   ├── orchestration/                   # Workflow logic
│   ├── predictive/                      # Pattern recognition & ML
│   ├── integrations/                    # External API integrations
│   └── utils/                           # Helpers & utilities
├── tests/                               # Test suite
│   ├── unit/                            # Unit tests
│   ├── integration/                     # Integration tests
│   └── fixtures/                        # Test fixtures
├── notebooks/                           # Jupyter notebooks (EDA)
├── scripts/                             # Automation scripts
│   ├── local-setup.sh                   # Developer setup
│   ├── run-tests.sh                     # Test runner
│   ├── deploy-staging.py                # Staging deployment
│   └── deploy-production.py             # Production deployment
├── config/                              # Configuration files
│   └── .env.example                     # Environment template
├── .github/workflows/                   # CI/CD pipelines
│   ├── ci.yml                           # Lint, test, build
│   ├── staging-deploy.yml               # Auto-deploy to staging
│   └── production-gate.yml              # Manual production gate
├── pyproject.toml                       # Python project config
├── Makefile                             # Developer commands
├── .gitignore                           # Git ignore rules
├── .pre-commit-config.yaml              # Pre-commit hooks
├── README.md                            # Project overview
└── CLAUDE.md                            # This file
```

### Key URLs
- **Hackathon Event**: https://lablab.ai/event/agentic-ai-hackathon-ibm-watsonx-orchestrate
- **watsonx Docs**: https://developer.watson-orchestrate.ibm.com/
- **GitHub ADK**: https://github.com/IBM/ibm-watsonx-orchestrate-adk
- **Free Trial**: https://www.ibm.com/products/watsonx-orchestrate

---

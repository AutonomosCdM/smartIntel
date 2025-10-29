# watsonx Orchestrate - Quick Start Cheatsheet

**For:** IBM Hackathon Team - Fast Reference
**Updated:** October 28, 2025

---

## 🚀 FASTEST PATH TO WORKING AGENT (15 MIN)

### Install & Setup
```bash
# Install ADK
pip install --upgrade ibm-watsonx-orchestrate

# Create .env file
cat > .env << EOF
WO_DEVELOPER_EDITION_SOURCE=myibm
WO_ENTITLEMENT_KEY=your-key-here
WATSONX_APIKEY=your-apikey-here
WATSONX_SPACE_ID=your-space-id
EOF

# Start local server
orchestrate server start --env-file=.env
orchestrate env activate local
```

### Hello World Agent
```python
# tools/greetings.py
from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool
def greeting():
    return "Hello World!"
```

```yaml
# greeter.yaml
name: greeter
model: ibm/granite-3-3-8b-instruct
instructions: "Use greeting tool when user says hello"
tools:
  - greeting
```

```bash
# Deploy
orchestrate tools import -k python -f tools/greetings.py
orchestrate agents import -f greeter.yaml
orchestrate chat start
# Open http://localhost:3000
```

---

## 🔑 CRITICAL URLS

| Resource | URL |
|----------|-----|
| **Docs** | https://developer.watson-orchestrate.ibm.com/ |
| **GitHub** | https://github.com/IBM/ibm-watsonx-orchestrate-adk |
| **Free Trial** | https://www.ibm.com/products/watsonx-orchestrate |
| **Hackathon** | https://lablab.ai/event/agentic-ai-hackathon-ibm-watsonx-orchestrate |
| **Agent Catalog** | https://www.ibm.com/products/watsonx-orchestrate/agent-catalog |

---

## 💡 KEY CONCEPTS

### Agent Types
1. **Native Agents** - Built with ADK Python SDK
2. **External Agents** - LangGraph, CrewAI, BeeAI integration
3. **Pre-Built Agents** - 150+ from catalog

### Three Ways to Build
1. **No-Code UI** - 5 minutes, no coding
2. **Python SDK** - Full control, flexible
3. **Import Existing** - Connect external agents

### Multi-Agent Patterns
- **Supervisor** - Orchestrator routes to specialists
- **Chain** - Agent A → Agent B → Agent C
- **Parallel** - Multiple agents work simultaneously

---

## 🛠️ ESSENTIAL CLI COMMANDS

```bash
# Environment Management
orchestrate env list                    # List all environments
orchestrate env activate local          # Switch environment

# Agent Management
orchestrate agents import -f agent.yaml # Deploy agent
orchestrate agents list                 # List deployed agents
orchestrate agents logs --agent-id <id> # View logs

# Tool Management
orchestrate tools import -k python -f tool.py    # Import Python tool
orchestrate tools import --from-mcp <mcp-server> # Import MCP tools

# Knowledge Base
orchestrate knowledge-bases create --name "docs"
orchestrate knowledge-bases upload --kb-id <id> --files ./docs/*.pdf

# Server Control
orchestrate server start --env-file=.env
orchestrate server stop
orchestrate chat start  # Launch UI
```

---

## 🏆 HACKATHON WINNING FORMULA

### DO THIS ✅
1. **Solve ONE specific problem well** (not generic chatbot)
2. **Use multi-agent orchestration** (show watsonx features)
3. **Have working demo** (live > slides)
4. **Quantify impact** ("saves 5 hours/week")
5. **Use pre-built tools** (MCP, catalog agents)

### AVOID THIS ❌
1. Scope too large (10+ agents in 48h)
2. No demo (just slides)
3. Generic use case (HR chatbot vs. leave approval agent)
4. Ignoring orchestrate features (just using watsonx.ai directly)
5. Complex UI (focus on agent logic)

### Judge Criteria
- **Model Integration (30%)** - Quality of LLM + tool usage
- **Technical (30%)** - Code quality, architecture
- **Impact (25%)** - Real-world value, ROI
- **Presentation (15%)** - Demo clarity, storytelling

---

## 🔥 POWER FEATURES

### RAG (Knowledge Base)
```yaml
# agent.yaml
name: knowledge-agent
model: ibm/granite-3-3-8b-instruct
knowledge_bases:
  - company-docs  # Auto-searches uploaded docs
```

### MCP Tools (Pre-Built Integrations)
```bash
# Import GitHub tools
orchestrate tools import \
  --from-mcp npx @modelcontextprotocol/server-github \
  --config '{"token": "ghp_xxx"}'

# Now agent can: search repos, create issues, read files
```

### Streaming Responses
```bash
# API endpoint: /api/v1/orchestrate/runs/stream
# Format: Server-Sent Events (SSE)
# Use case: Real-time chat UIs
```

### Document Processing
```bash
# Built-in OCR + extraction
# Supports: PDF, DOCX, images
# Features: Table extraction, entity recognition
```

---

## 🐛 COMMON GOTCHAS

| Issue | Fix |
|-------|-----|
| "token_quota_reached" | Free tier limit - contact IBM for more |
| Bearer token expired | Tokens expire after 1h - regenerate |
| Docker memory error | Increase Docker RAM to 20GB+ |
| Agent not using tools | Improve instructions - be explicit |
| Slow responses | Use smaller model (Granite 3.3 8B) |

---

## 📊 MODELS CHEAT SHEET

| Model | Size | Use Case | Speed |
|-------|------|----------|-------|
| `ibm/granite-3-3-8b-instruct` | 8B | General, fast | ⚡⚡⚡ |
| `ibm/granite-4-0-h-small` | 9B | Latest, efficient | ⚡⚡⚡ |
| `meta-llama/llama-3-2-90b-vision-instruct` | 90B | Vision + complex | ⚡ |

**Recommendation:** Start with Granite 3.3 8B (fast, cheap, good quality)

---

## 🔗 INTEGRATION QUICK REFERENCE

### Python Tool
```python
@tool
def my_tool(param: str) -> dict:
    """Tool description for LLM"""
    # Your logic here
    return {"result": param}
```

### OpenAPI Import
```bash
# Import REST API
orchestrate tools import --from-openapi ./api-spec.yaml
```

### Database (via MCP)
```bash
orchestrate tools import \
  --from-mcp npx @modelcontextprotocol/server-postgres \
  --config postgres://user:pass@host:5432/db
```

### LangChain Integration
```python
from langchain_ibm import ChatWatsonx

llm = ChatWatsonx(
    model_id="ibm/granite-3-3-8b-instruct",
    url="https://us-south.ml.cloud.ibm.com",
    apikey="YOUR_API_KEY",
    project_id="YOUR_PROJECT_ID"
)
```

---

## 🎯 HACKATHON TIME BUDGET (48H)

| Hours | Task |
|-------|------|
| 0-4 | Setup, hello world, planning |
| 4-12 | Build core agent + tools |
| 12-24 | External integrations (APIs, DB) |
| 24-36 | Testing, debugging |
| 36-44 | Polish demo, presentation |
| 44-48 | Rehearse, buffer |

---

## 📚 TOP LEARNING RESOURCES

1. **Official Tutorial:** https://developer.watson-orchestrate.ibm.com/tutorials/tutorial_1_hello_world
2. **Thomas Suedbroecker Blog:** https://suedbroecker.net (CLI guides)
3. **Ruslan Magana Blog:** https://ruslanmv.com/blog (multi-agent examples)
4. **Hello Orchestrate Repo:** https://github.com/ruslanmv/hello-watsonx-orchestrate

---

## 💰 COST OPTIMIZATION

**Free Tier Includes:**
- 30-day trial
- Full platform access
- ADK + Developer Edition
- Token quota (limited, exact amount unclear)

**Best Practices:**
- Use Granite models (cheaper than Llama)
- Cache knowledge base queries
- Limit tool calls per agent run
- Test locally (free) before cloud deployment

---

## 🚨 EMERGENCY CONTACTS

| Need | Resource |
|------|----------|
| Technical issue | IBM Support (if paid) or GitHub issues |
| Hackathon help | Lablab.ai Discord (after registration) |
| Documentation | https://developer.watson-orchestrate.ibm.com/ |
| Community | Stack Overflow (tag: ibm-watsonx) |

---

## 🎬 DEMO CHECKLIST

- [ ] Problem statement (1 min - why does this matter?)
- [ ] Architecture diagram (show multi-agent workflow)
- [ ] Live demo (3-5 min - show it working)
- [ ] Fallback video (if live demo risky)
- [ ] ROI/impact metrics ("saves X hours/week")
- [ ] Technical highlights (RAG, MCP, multi-agent)
- [ ] Q&A prep (anticipate judge questions)

---

## 📝 QUICK TROUBLESHOOTING

```bash
# Check environment
orchestrate env list

# View agent logs
orchestrate agents logs --agent-id <id> --follow

# Test tool independently
python -c "from tools.my_tool import my_tool; print(my_tool('test'))"

# Verify knowledge base
orchestrate knowledge-bases list

# Check server status
docker ps

# Regenerate API token (if expired)
# Go to watsonx Orchestrate UI → Settings → API Details → Generate API Key
```

---

**For Full Details:** See `WATSONX_ORCHESTRATE_INTELLIGENCE_REPORT.md` (13,000 words)

**Ready to Build? Start Here:**
```bash
pip install ibm-watsonx-orchestrate
orchestrate --help
```

Good luck at the hackathon! 🚀

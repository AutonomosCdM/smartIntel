# watsonx Credentials Setup Guide

**Status**: ✅ Trial Active - Need to Extract Credentials

Este guide te ayuda a obtener las credenciales necesarias para configurar watsonx Orchestrate.

---

## 🎯 Lo que necesitamos

```
✅ watsonx Orchestrate Trial - ACTIVO
⏳ API Key - Por obtener
⏳ Project ID - Por obtener
⏳ Workspace/Space ID - Por obtener (si aplica)
```

---

## 📋 Paso 1: Obtener API Key de IBM Cloud

### Opción A: Desde IBM Cloud Console (Recomendado)

1. **Ir a IBM Cloud**:
   - https://cloud.ibm.com/

2. **Acceder a API Keys**:
   - Click en tu perfil (esquina superior derecha)
   - Select "Profile and settings" o "My IBM"
   - Click "API keys" en el menú lateral

3. **Crear API Key**:
   - Click "Create an IBM Cloud API key"
   - Name: `watsonx-orchestrate-hackathon`
   - Description: `API key for IBM Hackathon - ProcureGenius project`
   - Click "Create"

4. **Guardar API Key** (IMPORTANTE):
   ```bash
   # Solo se muestra UNA VEZ
   # Copiar y guardar en lugar seguro
   # Ejemplo: ibmcloud_apikey_abcdefgh12345678
   ```

### Opción B: Desde CLI (si prefieres)

```bash
# Login
ibmcloud login --sso

# Crear API key
ibmcloud iam api-key-create watsonx-orchestrate-hackathon \
  -d "API key for IBM Hackathon" \
  --file watsonx-api-key.json

# Ver API key
cat watsonx-api-key.json | jq -r '.apikey'
```

---

## 📋 Paso 2: Obtener Project ID

### Desde watsonx Orchestrate UI

1. **Ir a tu workspace de watsonx Orchestrate**:
   - https://dl.watson-orchestrate.ibm.com/

2. **Acceder a Project Settings**:
   - Click en el menú de hamburguesa (☰) arriba a la izquierda
   - Selecciona "Projects" o "My Projects"
   - Click en el proyecto activo (o crea uno nuevo)

3. **Ver Project ID**:
   - En la página del proyecto, click "Settings" o "Manage"
   - Buscar "Project ID" o "GUID"
   - Copiar el ID (formato: `12345678-1234-1234-1234-123456789abc`)

### Alternativamente: Desde watsonx.ai

1. **Ir a watsonx.ai**:
   - https://dataplatform.cloud.ibm.com/wx

2. **Seleccionar proyecto**:
   - Projects → View all projects
   - Click en tu proyecto (o crea uno nuevo: "New project")

3. **Obtener Project ID**:
   - En el proyecto, click "Manage" tab
   - Scroll down hasta "General"
   - Copiar "Project ID"

---

## 📋 Paso 3: Verificar Credenciales Localmente

### Test rápido con curl

```bash
# Reemplazar con tus valores reales
export WATSONX_API_KEY="tu-api-key-aqui"
export WATSONX_PROJECT_ID="tu-project-id-aqui"

# Test 1: Generar token de acceso
curl -X POST \
  'https://iam.cloud.ibm.com/identity/token' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d "grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=$WATSONX_API_KEY"

# Si funciona, recibirás un JSON con "access_token"
```

### Test con Python

```python
# test_watsonx_credentials.py
import os
import requests

API_KEY = os.getenv("WATSONX_API_KEY")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

# Generar token
token_response = requests.post(
    "https://iam.cloud.ibm.com/identity/token",
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    data=f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={API_KEY}"
)

if token_response.status_code == 200:
    print("✅ API Key válida")
    access_token = token_response.json()["access_token"]
    print(f"✅ Access token obtenido: {access_token[:20]}...")
else:
    print("❌ API Key inválida")
    print(token_response.text)
```

Ejecutar:
```bash
export WATSONX_API_KEY="tu-key"
export WATSONX_PROJECT_ID="tu-project-id"
python test_watsonx_credentials.py
```

---

## 📋 Paso 4: Actualizar GitHub Secrets

### Una vez verificadas las credenciales:

```bash
# Navegar al proyecto
cd /Users/autonomos_dev/Projects/ibm_hackathon

# Actualizar secrets de STAGING
gh secret set WATSONX_API_KEY_STAGING \
  --body "tu-api-key-real-aqui" \
  --repo AutonomosCdM/smartIntel

gh secret set WATSONX_PROJECT_ID_STAGING \
  --body "tu-project-id-real-aqui" \
  --repo AutonomosCdM/smartIntel

# Actualizar secrets de PRODUCTION (usar mismos valores para hackathon)
gh secret set WATSONX_API_KEY_PRODUCTION \
  --body "tu-api-key-real-aqui" \
  --repo AutonomosCdM/smartIntel

gh secret set WATSONX_PROJECT_ID_PRODUCTION \
  --body "tu-project-id-real-aqui" \
  --repo AutonomosCdM/smartIntel

# Verificar
gh secret list --repo AutonomosCdM/smartIntel
```

### Output esperado:
```
WATSONX_API_KEY_PRODUCTION     Updated 2025-10-29T12:30:00Z
WATSONX_API_KEY_STAGING        Updated 2025-10-29T12:30:00Z
WATSONX_PROJECT_ID_PRODUCTION  Updated 2025-10-29T12:30:00Z
WATSONX_PROJECT_ID_STAGING     Updated 2025-10-29T12:30:00Z
```

---

## 📋 Paso 5: Actualizar .env Local

```bash
# Copiar template
cp config/.env.example .env

# Editar con tus valores
nano .env  # o vim, code, etc.
```

**.env** (ejemplo):
```bash
# watsonx.ai API Configuration
WATSONX_API_KEY=ibmcloud_apikey_abc123def456ghi789
WATSONX_PROJECT_ID=12345678-1234-1234-1234-123456789abc
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# watsonx Orchestrate Configuration
WO_DEVELOPER_EDITION_SOURCE=myibm
WO_ENTITLEMENT_KEY=tu-entitlement-key-si-aplica

# Environment
ENVIRONMENT=local
LOG_LEVEL=DEBUG
DEMO_MODE=true
MAX_WORKERS=4

# External APIs (opcionales por ahora)
FRED_API_KEY=obtener-si-necesitas
WORLD_BANK_API_KEY=free

# Model Configuration
MODEL_NAME=ibm/granite-13b-chat-v2
TEMPERATURE=0.7
MAX_TOKENS=2048
```

**IMPORTANTE**: `.env` está en `.gitignore` - nunca se committeará.

---

## 📋 Paso 6: Probar Integración Local

### Test básico con Python SDK

```bash
# Instalar watsonx SDK
pip install ibm-watsonx-ai

# Crear test script
cat > test_watsonx_integration.py << 'EOF'
"""Test watsonx integration with real credentials."""
import os
from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

# Load credentials
api_key = os.getenv("WATSONX_API_KEY")
project_id = os.getenv("WATSONX_PROJECT_ID")
url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")

if not api_key or not project_id:
    raise ValueError("Missing credentials in .env")

# Initialize model
credentials = {
    "url": url,
    "apikey": api_key
}

parameters = {
    GenParams.DECODING_METHOD: "greedy",
    GenParams.MAX_NEW_TOKENS: 100,
    GenParams.TEMPERATURE: 0.7
}

model = Model(
    model_id="ibm/granite-13b-chat-v2",
    params=parameters,
    credentials=credentials,
    project_id=project_id
)

# Test inference
print("Testing watsonx.ai inference...")
prompt = "What is procurement optimization?"
response = model.generate_text(prompt=prompt)

print(f"✅ Success! Response: {response[:100]}...")
EOF

# Ejecutar test
python test_watsonx_integration.py
```

### Output esperado:
```
Testing watsonx.ai inference...
✅ Success! Response: Procurement optimization is the process of improving the efficiency and effectiveness...
```

---

## 📋 Paso 7: Verificar CI/CD

### Trigger CI con credenciales reales

```bash
# Hacer un pequeño cambio para trigger CI
echo "# watsonx credentials configured" >> README.md
git add README.md
git commit -m "test: verify watsonx integration in CI"
git push origin master

# Monitorear CI
gh run watch
```

### Qué esperar:

1. **CI Pipeline** (ci.yml):
   - ✅ Lint checks
   - ✅ Type checks
   - ✅ Tests (smoke tests pasan)
   - ⏳ Staging deploy intenta correr

2. **Staging Deployment** (staging-deploy.yml):
   - ✅ Debería pasar ahora (antes fallaba por placeholders)
   - ✅ Scripts de deploy ejecutan (aunque sean stubs por ahora)

---

## 🔍 Troubleshooting

### Error: "Invalid API key"

**Síntomas**:
```
401 Unauthorized
{"error": "Invalid API key"}
```

**Solución**:
1. Verificar API key copiada correctamente (sin espacios)
2. Confirmar API key activa en IBM Cloud
3. Regenerar si es necesario:
   - IBM Cloud → API Keys → Delete → Create new

### Error: "Project not found"

**Síntomas**:
```
404 Not Found
{"error": "Project ID not found"}
```

**Solución**:
1. Confirmar Project ID en watsonx.ai Projects
2. Verificar que el proyecto esté activo (no archived)
3. Verificar que API key tenga permisos al proyecto:
   - IBM Cloud → Manage → Access (IAM)
   - Assign access → watsonx.ai → Viewer/Editor role

### Error: "Trial expired"

**Síntomas**:
```
403 Forbidden
{"error": "Trial period has ended"}
```

**Solución**:
1. Verificar días restantes en UI (esquina superior derecha)
2. Si expiró, request extension:
   - Contact IBM support
   - Mention hackathon context
3. O crear nueva cuenta trial (si permitido)

### Error: "Rate limit exceeded"

**Síntomas**:
```
429 Too Many Requests
{"error": "Rate limit exceeded"}
```

**Solución**:
1. Trial tiene límites:
   - ~100 requests/hour
   - ~1000 tokens/minute
2. Implementar retry logic con backoff
3. Cache responses localmente
4. Para hackathon, debería ser suficiente

---

## 📊 Checklist Final

Antes de empezar desarrollo:

- [ ] API Key obtenida y guardada
- [ ] Project ID obtenido y guardado
- [ ] Credenciales probadas localmente (curl o Python)
- [ ] GitHub secrets actualizados (staging + production)
- [ ] .env local creado y configurado
- [ ] watsonx SDK instalado (`pip install ibm-watsonx-ai`)
- [ ] Test de integración pasando
- [ ] CI/CD pipeline verde con credenciales reales
- [ ] Documentación revisada

---

## 🚀 Próximos Pasos

Una vez credenciales configuradas:

1. **Explorar watsonx Orchestrate**:
   - Crear primer agent desde UI
   - Entender el flujo de creación
   - Probar con template existente

2. **Implementar Agents**:
   - Contract Analyst Agent
   - Supplier Intelligence Agent
   - etc.

3. **Build Demo**:
   - Integrar con Carozzi data
   - Crear workflow de orchestration
   - Probar end-to-end

---

**Última actualización**: 2025-10-29
**Mantenido por**: Autonomos Lab

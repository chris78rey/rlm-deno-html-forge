# 🔒 Seguridad y Datos Privados

**Guía completa sobre protección de datos y configuración de seguridad del proyecto**

---

## 1. Principios de Seguridad del Proyecto

### 1.1 Filosofía de Seguridad

Este proyecto sigue el principio de **"privacidad por diseño"**:

```
┌─────────────────────────────────────────────────────────────┐
│                    PRIVACIDAD POR DISEÑO                     │
├─────────────────────────────────────────────────────────────┤
│  ✅ El HTML completo NUNCA sale de tu máquina               │
│  ✅ Solo se envía texto a la IA, nunca estructura HTML       │
│  ✅ Todo el procesamiento ocurre localmente                 │
│  ✅ Los secretos (API keys) nunca se suben a Git            │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Cómo se Protege el HTML

```
EN TU MÁQUINA (LOCAL)
    │
    ▼
    ├─────────────────────────────────────────────────────┐
    │  1. Deno/Pyodide abre el HTML localmente           │
    │  2. Extrae solo el texto visible (sin estructura)  │
    │  3. Divide el texto en fragmentos pequeños         │
    └─────────────────────────────────────────────────────┘
                           │
                           ▼
    ┌─────────────────────────────────────────────────────┐
    │  4. Solo fragmentos de texto se envían a la IA      │
    │     (nunca el HTML completo)                        │
    └─────────────────────────────────────────────────────┘
                           │
                           ▼
    ┌─────────────────────────────────────────────────────┐
    │  5. IA devuelve texto transformado                  │
    └─────────────────────────────────────────────────────┘
                           │
                           ▼
    ┌─────────────────────────────────────────────────────┐
    │  6. Deno aplica transformaciones localmente         │
    │  7. HTML transformado se guarda en output_html/     │
    └─────────────────────────────────────────────────────┘
```

**Importante:** En ningún momento el HTML completo abandona tu máquina.

---

## 2. Archivos NO Subidos a Git

### 2.1 Lista de Exclusión (.gitignore)

El archivo `.gitignore` está configurado para excluir:

```
# Secretos
.env
.env.*
!.env.example

# Configuración local
config.yaml

# Datos reales / privados
input_html/*
!input_html/.gitkeep
output_html/*
!output_html/.gitkeep
reports/*
!reports/.gitkeep
.work/*
!.work/.gitkeep

# Contexto real del proyecto
context/tema.md
!context/tema.example.md
```

### 2.2 ¿Por Qué Cada Archivo?

#### `.env` - Variables de Entorno Secretas

**Contenido:**
```env
OPENROUTER_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
```

**Por qué NO se sube:**
- ❌ Contiene claves de API privadas
- ❌ Si se expone, cualquiera puede usar tu cuenta
- ❌ Puede generar costos no autorizados

**Alternativa pública:**
```env
# .env.example (SÍ se sube)
OPENROUTER_API_KEY=tu_api_key_aqui
```

---

#### `config.yaml` - Configuración Local

**Contenido:**
```yaml
paths:
  input_dir: input_html/
  output_dir: output_html/
  # ... rutas específicas de tu máquina
```

**Por qué NO se sube:**
- ❌ Puede contener rutas absolutas que no funcionan en otras máquinas
- ❌ Puede contener configuración específica del entorno local
- ❌ Puede diferir entre desarrolladores

**Alternativa pública:**
```yaml
# config.example.yaml (SÍ se sube)
paths:
  input_dir: input_html/
  output_dir: output_html/
  # ... valores genéricos
```

---

#### `context/tema.md` - Contenido Real

**Contenido:**
```markdown
# Contexto del documento de la empresa XYZ

Este documento contiene información confidencial sobre
proyectos internos, estrategias de negocio, datos financieros...
```

**Por qué NO se sube:**
- ❌ Contiene información real del documento
- ❌ Puede contener datos sensibles de la organización
- ❌ Información estratégica confidencial

**Alternativa pública:**
```markdown
# context/tema.example.md (SÍ se sube)
# Contexto de ejemplo

Este es un ejemplo de contexto para el documento.
Debes personalizarlo con la información específica de tu caso.
```

---

#### `input_html/*.htm` - Documentos Originales

**Contenido:**
- HTML real con contenido de negocio
- Datos personales o corporativos
- Información confidencial

**Por qué NO se sube:**
- ❌ Documentos originales con contenido real
- ❌ Pueden contener datos sensibles
- ❌ Derechos de autor y privacidad

**Alternativa pública:**
```html
<!-- input_html/ejemplo.html (SÍ se sube) -->
<!DOCTYPE html>
<html>
<body>
  <p>Ejemplo de documento HTML</p>
</body>
</html>
```

---

#### `output_html/` - Resultados

**Contenido:**
- HTML transformado con contenido procesado
- Resultados del procesamiento

**Por qué NO se sube:**
- ❌ Contiene contenido derivado de documentos reales
- ❌ Puede contener información sensible
- ❌ Es propiedad del usuario

---

#### `reports/` - Reportes de Procesamiento

**Contenido:**
- Detalles de qué documentos se procesaron
- Estadísticas de uso
- Contenido de los fragmentos procesados

**Por qué NO se sube:**
- ❌ Puede revelar qué documentos se están procesando
- ❌ Contiene metadatos sensibles
- ❌ Patrones de uso empresarial

---

#### `.work/` - Archivos Temporales

**Contenido:**
- Archivos temporales de procesamiento
- Caché local
- Datos intermedios

**Por qué NO se sube:**
- ❌ No son necesarios para otros usuarios
- ❌ Pueden contener datos temporales
- ❌ Solo útiles en la ejecución actual

---

## 3. Cómo Funciona la Protección

### 3.1 Git Ignore

El archivo `.gitignore` previene que archivos sensibles se agreguen:

```bash
# Verificar qué archivos se ignoran
git status --ignored

# Forzar eliminación de archivos ya trackeados
git rm --cached .env 2>/dev/null
```

### 3.2 Script de Preparación

El script `prepare_public_repo.ps1` limpia el repositorio:

```powershell
# Elimina archivos sensibles del índice Git
git rm -r --cached input_html/ output_html/ reports/ .work/ 2>$null
git rm --cached config.yaml 2>$null
git rm --cached context/tema.md 2>$null
git rm --cached .env 2>$null
```

### 3.3 Entorno Virtual

El entorno virtual `.venv/` también se ignora:

```
.venv/
__pycache__/
*.pyc
```

Esto evita conflictos entre diferentes entornos de desarrollo.

---

## 4. Flujo de Seguridad Completo

### 4.1 Antes de Ejecutar

```
1. Configurar .env (local)
   └─ solo en tu máquina

2. Configurar config.yaml (local)
   └─ solo en tu máquina

3. Colocar HTML en input_html/ (local)
   └─ solo en tu máquina

4. Configurar context/tema.md (local)
   └─ solo en tu máquina
```

### 4.2 Durante la Ejecución

```
1. Python carga .env (local)
   └─ API key solo en memoria

2. Deno procesa HTML (local)
   └─ todo ocurre en tu máquina

3. IA recibe solo texto (fragmentos)
   └─ NUNCA recibe HTML completo

4. Resultados se guardan localmente
   └─ output_html/ y reports/
```

### 4.3 Después de Ejecutar

```
1. Resultados en output_html/ (local)
   └─ solo en tu máquina

2. Reportes en reports/ (local)
   └─ solo en tu máquina

3. Al subir a Git:
   └─ .gitignore excluye datos sensibles
   └─ solo se sube código y documentación
```

---

## 5. Seguridad del Sandbox Deno

### 5.1 Permisos Restringidos

Deno se ejecuta con permisos mínimos:

```bash
deno run \
  --deny-net \           # No acceso a red
  --no-prompt \          # Sin interacción
  --cached-only \        # Solo caché local
  --allow-read=<rutas>   # Solo lectura en rutas específicas
  deno/pyodide_runner.ts
```

### 5.2 Permisos Permitidos

| Permiso | Uso | Seguridad |
|---------|-----|-----------|
| `--allow-read` | Leer HTML de input_html/ | ✅ Solo lectura, rutas limitadas |
| `--deny-net` | No acceso a internet | ✅ Totalmente aislado |
| `--no-prompt` | Sin interacción usuario | ✅ No requiere confirmación |
| `--cached-only` | Solo caché local | ✅ No descarga nada nuevo |

### 5.3 Permisos NO Permitidos

| Permiso | Riesgo | Estado |
|---------|--------|--------|
| `--allow-write` | Puede modificar archivos | ❌ No permitido |
| `--allow-run` | Puede ejecutar comandos | ❌ No permitido |
| `--allow-ffi` | Puede usar bibliotecas nativas | ❌ No permitido |
| `--allow-net` | Puede acceder a internet | ❌ No permitido |

**Nota:** Python maneja la escritura de archivos finales.

---

## 6. Protección de la API Key

### 6.1 Cómo se Almacena

```python
# main.py
from dotenv import load_dotenv
load_dotenv()  # Carga .env en variables de entorno

# openrouter_client.py
api_key = os.environ.get("OPENROUTER_API_KEY")
```

### 6.2 Cómo se Usa

```python
# Solo se usa en memoria durante la ejecución
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
```

### 6.3 Cómo se Protege

```
1. Archivo .env nunca se sube a Git ✅
2. API key solo en variables de entorno ✅
3. Nunca se loguea la API key ✅
4. Nunca se envía la API key a la IA ✅
```

### 6.4 Si la API Key se Expone

**Acciones inmediatas:**

1. **Regenerar la API key** en OpenRouter
2. **Revocar la antigua** en Settings → Keys
3. **Actualizar .env** con la nueva clave
4. **Revisar logs** de uso en OpenRouter

**Comando para limpiar Git:**

```bash
# Si la clave ya fue commiteada
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch .env' \
  --prune-empty --tag-name-filter cat -- --all
```

---

## 7. Mejores Prácticas de Seguridad

### 7.1 Para Usuarios

| Práctica | Descripción |
|----------|-------------|
| ✅ Usar `.env.example` | Nunca modificar `.env.example` |
| ✅ Agregar `.env` a `.gitignore` | Verificar que esté excluido |
| ✅ Rotar API keys periódicamente | Cambiar cada 3-6 meses |
| ✅ Usar límites de costos | Configurar `max_money_spent` |
| ✅ Revisar reportes | Verificar qué se procesó |

### 7.2 Para Desarrolladores

| Práctica | Descripción |
|----------|-------------|
| ✅ No hardcodear secrets | Usar variables de entorno |
| ✅ Validar entradas | Sanitizar HTML de entrada |
| ✅ Loguear sin exponer | No loggear API keys o datos sensibles |
| ✅ Tests aislados | Usar datos de prueba, no reales |
| ✅ Documentar seguridad | Mantener docs actualizados |

### 7.3 Al Compartir el Proyecto

| Acción | Requisito |
|--------|-----------|
| Subir a GitHub público | Ejecutar `prepare_public_repo.ps1` |
| Compartir código | Solo compartir `docs/`, código fuente, ejemplos |
| Compartir configuración | Usar `config.example.yaml` |
| Compartir contexto | Usar `context/tema.example.md` |

---

## 8. Verificación de Seguridad

### 8.1 Verificar .gitignore

```bash
# Ver archivos ignorados
git status --ignored

# Deberías ver:
# ignored:
#   .env
#   config.yaml
#   input_html/
#   output_html/
#   reports/
#   .work/
#   context/tema.md
```

### 8.2 Verificar Commits

```bash
# Ver historia de commits
git log --oneline --all

# Ver archivos en cada commit
git show --name-only <commit-hash>
```

### 8.3 Verificar Archivos Subidos

```bash
# Ver archivos en el repositorio remoto
git ls-tree -r main --name-only
```

**NO deberían aparecer:**
- `.env`
- `config.yaml`
- `input_html/*.htm`
- `context/tema.md`

---

## 9. Escenarios de Seguridad

### 9.1 Escenario 1: Trabajo en Equipo

**Problema:** Múltiples personas necesitan usar el proyecto.

**Solución:**
1. Cada persona crea su propio `.env` local
2. Usa `config.example.yaml` como referencia
3. Comparte solo código, no configuración específica

### 9.2 Escenario 2: Cliente Externo

**Problema:** Cliente necesita ver el código.

**Solución:**
1. Ejecutar `prepare_public_repo.ps1`
2. Subir a repositorio privado o público
3. Cliente clona y configura su propio entorno

### 9.3 Escenario 3: Auditoría de Seguridad

**Problema:** Revisar que no haya datos sensibles.

**Solución:**
```bash
# Buscar datos sensibles en el código
grep -r "OPENROUTER_API_KEY" .
grep -r "sk-" .

# Verificar archivos en Git
git ls-tree -r main --name-only
```

---

## 10. Cifrado de Datos (Opcional)

Si necesitas mayor seguridad, puedes cifrar los documentos:

### 10.1 Con Git Crypt

```bash
# Instalar git-crypt
# Configurar claves
# Cifrar archivos sensibles
```

### 10.2 Con Archivos Cifrados Manualmente

```bash
# Cifrar documento antes de subir
gpg --encrypt --recipient user@email.com documento.html

# Descifrar localmente
gpg --decrypt documento.html.gpg > documento.html
```

### 10.3 Con Docker (Aislamiento)

```yaml
# docker-compose.yml
services:
  app:
    volumes:
      - ./input_html:/app/input:ro
      - ./output_html:/app/output
    environment:
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
```

---

## 11. Cumplimiento y Regulaciones

### 11.1 GDPR (Europa)

- ✅ Datos no salen de la máquina local
- ✅ No se almacenan datos en servidores externos
- ✅ Usuario tiene control total

### 11.2 HIPAA (Salud - USA)

- ⚠️ Requiere configuración adicional
- ⚠️ Verificar que OpenRouter cumpla con HIPAA
- ⚠️ Considerar uso on-premise

### 11.3 SOX (Financiero)

- ✅ Procesamiento local
- ✅ Control de costos configurable
- ✅ Reportes de auditoría

---

## 12. Resumen de Seguridad

```
┌─────────────────────────────────────────────────────────────┐
│                 RESUMEN DE SEGURIDAD                         │
├─────────────────────────────────────────────────────────────┤
│  ✅ HTML nunca sale de tu máquina                           │
│  ✅ Solo se envía texto a la IA (fragmentos)                │
│  ✅ .env nunca se sube a Git                                │
│  ✅ config.yaml nunca se sube a Git                         │
│  ✅ Documentos reales nunca se suben a Git                  │
│  ✅ Deno ejecuta con permisos mínimos                       │
│  ✅ Control de costos configurable                          │
│  ✅ Reportes generados localmente                           │
│  ✅ .gitignore protege datos sensibles                      │
└─────────────────────────────────────────────────────────────┘
```

---

**Documento creado:** 2026-04-26
**Referencia:** `.gitignore`, `README_GITHUB_PUBLICO.md`

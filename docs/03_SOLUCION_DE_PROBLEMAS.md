# 🔧 Solución de Problemas Comunes

**Guía de errores frecuentes y cómo solucionarlos**

---

## Índice de Errores

| Error | Descripción | Solución Rápida |
|-------|-------------|-----------------|
| [1. OPENROUTER_API_KEY no encontrado](#1-openrouter_api_key-no-encontrado) | Falta la API key en `.env` | Crear archivo `.env` con la API key |
| [2. Deno no reconocido](#2-deno-no-reconocido) | Deno no está instalado o no está en PATH | Instalar Deno 2.x+ |
| [3. Pyodide no carga](#3-pyodide-no-carga) | Cache de Deno no preparada | Ejecutar `deno cache` |
| [4. No aparecen archivos en output_html](#4-no-aparecen-archivos-en-output_html) | No hay HTML en input_html/ | Colocar documentos en input_html/ |
| [5. El modelo tarda mucho](#5-el-modelo-tarda-mucho) | Procesamiento muy lento | Ajustar concurrencia |
| [6. Salen símbolos raros](#6-salen-símbolos-raros) | Problema de codificación | Verificar codificación UTF-8 |
| [7. HTML no se transforma](#7-html-no-se-transforma) | No se detectan elementos | Verificar estructura HTML |
| [8. Rate limit de OpenRouter](#8-rate-limit-de-openrouter) | Demasiadas llamadas | Reducir concurrencia |
| [9. Tokens agotados](#9-tokens-agotados) | Sin saldo en cuenta | Recargar cuenta OpenRouter |
| [10. Error de conexión](#10-error-de-conexión) | Problema de red | Verificar conexión a internet |
| [11. Archivos bloqueados](#11-archivos-bloqueados) | Permisos de archivo | Cambiar permisos |
| [12. Python no reconoce módulos](#12-python-no-reconoce-módulos) | Dependencias no instaladas | Instalar requirements.txt |

---

## 1. OPENROUTER_API_KEY no encontrado

### Síntomas

```
Error: OPENROUTER_API_KEY no encontrado en las variables de entorno
```

### Causa

El archivo `.env` no existe o no contiene la API key.

### Solución

**Paso 1: Crear el archivo `.env`**

```powershell
# Windows PowerShell
copy .env.example .env
```

```bash
# Linux/Mac
cp .env.example .env
```

**Paso 2: Editar el archivo `.env`**

Abrir `.env` y añadir tu API key:

```env
OPENROUTER_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
```

**Paso 3: Obtener tu API key**

1. Ve a [openrouter.ai](https://openrouter.ai)
2. Inicia sesión o crea cuenta
3. Ve a **Settings** → **Keys**
4. Genera una nueva API key
5. Cópiala en el archivo `.env`

### Verificación

```bash
# Verificar que el archivo existe
cat .env

# Deberías ver:
OPENROUTER_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
```

---

## 2. Deno no reconocido

### Síntomas

```
'deno' no se reconoce como un comando interno o externo,
programa o archivo por lotes ejecutable.
```

### Causa

Deno no está instalado o no está en el PATH del sistema.

### Solución

**Paso 1: Verificar instalación**

```bash
deno --version
```

**Paso 2: Instalar Deno**

**Windows:**
```powershell
# Con PowerShell (como administrador)
irm https://deno.land/install.ps1 | iex
```

**Linux/Mac:**
```bash
curl -fsSL https://deno.land/install.sh | sh
```

**Paso 3: Reiniciar terminal**

Cierre y abra una nueva terminal para que el PATH se actualice.

### Verificación

```bash
deno --version
```

Debería mostrar algo como:
```
deno 2.x.x
```

---

## 3. Pyodide no carga

### Síntomas

```
Error cargando Pyodide
Failed to load Pyodide
```

### Causa

La caché de Deno no tiene Pyodide preparado.

### Solución

**Ejecutar el comando de caché:**

```bash
deno cache deno/pyodide_runner.ts
```

Este comando descarga y cachea Pyodide la primera vez.

### Verificación

```bash
deno info deno/pyodide_runner.ts
```

Debería mostrar información sobre el módulo cacheado.

---

## 4. No aparecen archivos en output_html/

### Síntomas

La carpeta `output_html/` está vacía después de ejecutar el proceso.

### Causas

1. No hay archivos HTML en `input_html/`
2. Los archivos tienen extensiones incorrectas
3. Error durante el procesamiento

### Solución

**Paso 1: Verificar input_html/**

```bash
# Linux/Mac
ls -la input_html/

# Windows PowerShell
dir input_html\
```

Deberías ver archivos `.html` o `.htm`.

**Paso 2: Verificar extensiones**

Los archivos deben tener extensión `.html` o `.htm`.

**Paso 3: Verificar reportes**

```bash
ls reports/
```

Si hay archivos de reporte, el proceso se ejecutó pero pudo haber errores.

**Paso 4: Revisar reporte**

```bash
cat reports/report.md
```

Busca mensajes de error.

---

## 5. El modelo tarda mucho

### Síntomas

El procesamiento es muy lento.

### Causas

- Concurrencia muy baja
- Demasiados fragmentos por lote
- Modelo lento seleccionado

### Solución

**Opción 1: Aumentar concurrencia**

Editar `config.yaml`:

```yaml
rlm:
  concurrency: 8  # Aumentar de 6 a 8 o más
```

**Opción 2: Usar modelo más rápido**

Editar `config.yaml`:

```yaml
model:
  name: "anthropic/claude-3-haiku"  # Más rápido que Sonnet
```

**Opción 3: Reducir batch_size**

```yaml
rlm:
  batch_size: 20  # Menos fragmentos por llamada
```

### Recomendaciones

| Prioridad | Configuración |
|-----------|---------------|
| Velocidad máxima | `concurrency: 10`, `claude-3-haiku` |
| Calidad máxima | `concurrency: 4`, `claude-3-sonnet` |
| Equilibrio | `concurrency: 6`, `openrouter/auto` |

---

## 6. Salen símbolos raros

### Síntomas

En el HTML transformado aparecen caracteres extraños como `�` o `Ã©`.

### Causa

Problema de codificación de caracteres (UTF-8).

### Solución

**Verificar codificación de archivos de entrada:**

```bash
# Linux/Mac
file input_html/*.html
```

Debería mostrar: `UTF-8 Unicode text`

**Si no es UTF-8, convertir:**

```bash
# Convertir a UTF-8
iconv -f ISO-8859-1 -t UTF-8 archivo.html > archivo_utf8.html
```

**En Windows con PowerShell:**

```powershell
# Leer y guardar como UTF-8
Get-Content archivo.html -Encoding Default | Out-File -Encoding utf8 archivo_utf8.html
```

### Verificación

Los archivos de entrada y salida deben usar codificación UTF-8.

---

## 7. HTML no se transforma

### Síntomas

El HTML de salida es idéntico al de entrada.

### Causas

1. Textos demasiado cortos (menos de `min_text_length`)
2. Elementos HTML no detectados
3. Configuración incorrecta

### Solución

**Paso 1: Verificar longitud mínima**

```yaml
html:
  min_text_length: 8  # Reducir si textos son cortos
```

**Paso 2: Verificar estructura HTML**

Los elementos deben tener texto visible:
```html
<!-- ✅ Se procesará -->
<p>Texto aquí</p>
<span>Texto aquí</span>

<!-- ❌ No se procesará (vacío o muy corto) -->
<p></p>
<span>a</span>
```

**Paso 3: Verificar contexto**

```bash
cat context/tema.md
```

Debe contener instrucciones para la IA.

**Paso 4: Verificar reporte**

```bash
cat reports/report.json
```

Buscar si hay elementos procesados.

---

## 8. Rate limit de OpenRouter

### Síntomas

```
Error: Rate limit exceeded
HTTP 429 Too Many Requests
```

### Causa

Demasiadas llamadas a la API en poco tiempo.

### Solución

**Opción 1: Reducir concurrencia**

```yaml
rlm:
  concurrency: 3  # Reducir de 6 a 3
```

**Opción 2: Esperar y reintentar**

Pausa 1-2 minutos y ejecuta nuevamente.

**Opción 3: Usar modelo con límites más altos**

```yaml
model:
  name: "anthropic/claude-3-haiku"
```

### Prevención

```yaml
rlm:
  concurrency: 4  # Valor conservador
  max_total_calls: 500  # Límite total
```

---

## 9. Tokens agotados

### Síntomas

```
Error: Insufficient credits
HTTP 402 Payment Required
```

### Causa

La cuenta de OpenRouter no tiene saldo suficiente.

### Solución

1. Ve a [openrouter.ai](https://openrouter.ai)
2. Inicia sesión
3. Ve a **Billing** o **Credits**
4. Añade fondos a tu cuenta
5. Reintentar el procesamiento

### Alternativa económica

Usar un modelo más barato:

```yaml
model:
  name: "anthropic/claude-3-haiku"  # Más económico
```

---

## 10. Error de conexión

### Síntomas

```
Error: Connection refused
Error: Network is unreachable
```

### Causa

Problema de conexión a internet o a la API de OpenRouter.

### Solución

**Paso 1: Verificar conexión**

```bash
# Verificar conexión a internet
ping 8.8.8.8

# Verificar conexión a OpenRouter
ping openrouter.ai
```

**Paso 2: Verificar firewall**

- Asegurar que el firewall no bloquea conexiones a `openrouter.ai`
- Puerto 443 (HTTPS) debe estar abierto

**Paso 3: Verificar VPN**

Si usas VPN, verifica que no esté bloqueando la conexión.

---

## 11. Archivos bloqueados

### Síntomas

```
PermissionError: [Errno 13] Permission denied
Error: Acceso denegado
```

### Causa

Permisos de archivo insuficientes.

### Solución

**Windows:**
1. Cierra todos los programas que puedan estar usando los archivos
2. Ejecuta PowerShell como administrador
3. Verifica que no estén abiertos en otro programa

**Linux/Mac:**
```bash
# Dar permisos de escritura
chmod -R u+rwx input_html/ output_html/ reports/
```

---

## 12. Python no reconoce módulos

### Síntomas

```
ModuleNotFoundError: No module named 'tqdm'
ImportError: cannot import name 'AppConfig'
```

### Causa

Dependencias no instaladas.

### Solución

**Paso 1: Activar entorno virtual**

```powershell
# Windows
.venv\Scripts\activate
```

```bash
# Linux/Mac
source .venv/bin/activate
```

**Paso 2: Instalar dependencias**

```bash
pip install -r requirements.txt
```

**Paso 3: Verificar instalación**

```bash
pip list
```

Deberías ver las dependencias instaladas.

---

## 13. Error en el procesamiento de lotes

### Síntomas

```
Error: Batch X falló: ...
```

### Causa

Error en un lote específico de fragmentos.

### Solución

El sistema automáticamente reintenta hasta `max_repair_attempts` (3 por defecto).

Si persiste:

1. Verificar el reporte para identificar el fragmento problemático
2. Reducir `batch_size` en `config.yaml`
3. Aumentar `max_repair_attempts`

---

## 14. Problemas con Deno sandbox

### Síntomas

```
Permission denied
Access denied
```

### Causa

Deno no tiene permisos para leer los archivos.

### Solución

**Verificar permisos de Deno:**

```bash
deno run --allow-read deno/pyodide_runner.ts
```

El sistema ya debería configurar los permisos correctamente. Si persiste:

**Windows:**
- Asegurar que Deno tenga acceso a las carpetas
- Verificar que no estén bloqueadas por antivirus

**Linux/Mac:**
```bash
chmod -R u+rwx input_html/
```

---

## 15. Problemas de memoria

### Síntomas

```
OutOfMemoryError
Memory allocation failed
```

### Causa

Documentos muy grandes o muchos documentos simultáneos.

### Solución

**Reducir concurrencia:**

```yaml
rlm:
  concurrency: 2
  batch_size: 15
```

**Procesar por lotes:**
1. Dividir documentos en carpetas separadas
2. Procesar una carpeta a la vez
3. Aumentar memoria RAM si es posible

---

## Flujo de Diagnóstico Rápido

Si tienes un problema, sigue este flujo:

```
1. ¿El error es inmediato?
   ├─ Sí → Verifica instalación (Python, Deno, dependencias)
   └─ No → Continúa

2. ¿El error ocurre durante el procesamiento?
   ├─ Sí → Revisa reports/ para ver detalles
   └─ No → Continúa

3. ¿Hay archivos en input_html/?
   ├─ No → Coloca archivos HTML
   └─ Sí → Continúa

4. ¿El archivo .env existe?
   ├─ No → Crear con API key
   └─ Sí → Continúa

5. ¿Verificar reporte final
   └─ Revisar reports/report.md para errores específicos
```

---

## Contacto de Soporte

Si después de intentar estas soluciones el problema persiste:

1. **Revisar logs:** `reports/report.json`
2. **Ver documentación:** `docs/00_MEMORIA_DEL_PROYECTO.md`
3. **Consultar repositorio:** https://github.com/chris78rey/rlm-deno-html-forge

---

**Documento creado:** 2026-04-26
**Última actualización:** Ver fecha del archivo

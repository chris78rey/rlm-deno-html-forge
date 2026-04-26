import pyodideModule from "npm:pyodide/pyodide.js";

type Job = {
  action: "extract" | "assemble_many";
  input_dir?: string;
  extensions?: string[];
  html?: {
    min_text_length: number;
    max_text_length: number;
    skip_tags: string[];
    skip_text_regex: string[];
  };
  documents?: Array<{
    source_path: string;
    targets: unknown[];
    replacements: Record<string, string>;
  }>;
};

async function readStdin(): Promise<string> {
  return await new Response(Deno.stdin.readable).text();
}

function ok(data: unknown) {
  console.log(JSON.stringify({ ok: true, ...data }));
}

function fail(message: string, extra: Record<string, unknown> = {}) {
  console.log(JSON.stringify({ ok: false, error: message, ...extra }));
}

function detectEncoding(bytes: Uint8Array): string {
  const utf8Preview = new TextDecoder("utf-8", { fatal: false }).decode(bytes.slice(0, 8192));
  const winPreview = new TextDecoder("windows-1252").decode(bytes.slice(0, 8192));
  const preview = utf8Preview.includes("�") ? winPreview : utf8Preview;
  const m = preview.match(/charset\s*=\s*["']?([a-zA-Z0-9_\-]+)/i);
  const charset = (m?.[1] || "utf-8").toLowerCase();

  if (charset.includes("1252") || charset.includes("iso-8859-1") || charset.includes("latin1")) {
    return "windows-1252";
  }
  return "utf-8";
}

async function readHtmlFile(path: string): Promise<string> {
  const bytes = await Deno.readFile(path);
  const encoding = detectEncoding(bytes);
  return new TextDecoder(encoding).decode(bytes);
}

async function listHtmlFiles(root: string, extensions: string[]): Promise<string[]> {
  const out: string[] = [];
  const allowed = new Set(extensions.map((x) => x.toLowerCase()));

  async function walk(dir: string) {
    for await (const entry of Deno.readDir(dir)) {
      const path = `${dir.replace(/\/$/, "")}/${entry.name}`;
      if (entry.isDirectory) {
        await walk(path);
      } else if (entry.isFile) {
        const dot = entry.name.lastIndexOf(".");
        const ext = dot >= 0 ? entry.name.slice(dot).toLowerCase() : "";
        if (allowed.has(ext)) out.push(path);
      }
    }
  }

  await walk(root);
  out.sort();
  return out;
}

const PY_CODE = String.raw`
import json, re, base64
from html.parser import HTMLParser
from html import escape, unescape

JOB = json.loads(JOB_JSON)

def FINAL_VAR(name):
    globals()["__FINAL_VAR_NAME__"] = name

def _line_offsets(text):
    offsets = [0]
    total = 0
    for line in text.splitlines(True):
        total += len(line)
        offsets.append(total)
    return offsets

def _abs_pos(offsets, line, col):
    idx = max(0, line - 1)
    return None if idx >= len(offsets) else offsets[idx] + col

def _path_hint(stack):
    return " > ".join(stack[-6:])

def _candidate(text, cfg):
    if text is None:
        return False
    s = " ".join(str(text).split())
    if len(s) < int(cfg.get("min_text_length", 8)):
        return False
    if len(s) > int(cfg.get("max_text_length", 1500)):
        return False
    for pat in cfg.get("skip_text_regex", []):
        if re.search(pat, s, flags=re.I):
            return False
    technical = [
        r"^[\w.-]+\.(js|css|png|jpg|jpeg|webp|svg|ico|pdf|zip)$",
        r"^#[a-fA-F0-9]{3,8}$",
        r"^\{\{.*\}\}$",
        r"^\$\{.*\}$",
    ]
    return not any(re.search(p, s) for p in technical)

def _fix_mojibake(text):
    if not text:
        return text
    value = str(text)
    if any(x in value for x in ("Ã", "Â", "â€", "�")):
        try:
            repaired = value.encode("latin1", errors="ignore").decode("utf-8", errors="ignore")
            if repaired:
                value = repaired
        except Exception:
            pass
    repl = {
        "â€œ": "“", "â€�": "”", "â€˜": "‘", "â€™": "’",
        "â€“": "–", "â€”": "—", "Â¿": "¿", "Â¡": "¡",
        "Â°": "°", "Â ": " ", "Â": "",
    }
    for bad, good in repl.items():
        value = value.replace(bad, good)
    return value

def _clean_replacement(value, kind):
    value = unescape(str(value or "")).strip()
    value = _fix_mojibake(value)
    value = value.replace("\ufeff", "")
    value = re.sub(r"[ \t]+", " ", value)
    if kind == "attribute":
        return escape(value, quote=True)
    return escape(value, quote=False)

def _force_utf8_meta(html):
    html = html.replace("\ufeff", "")
    if re.search(r"charset\s*=", html, flags=re.I):
        html = re.sub(r"charset\s*=\s*[\"']?[^\"'\s>]+", "charset=utf-8", html, count=1, flags=re.I)
    elif re.search(r"<head[^>]*>", html, flags=re.I):
        html = re.sub(r"(<head[^>]*>)", r"\1\n<meta charset=\"utf-8\">", html, count=1, flags=re.I)
    return html

class Extractor(HTMLParser):
    def __init__(self, html, path, cfg):
        super().__init__(convert_charrefs=False)
        self.html = html
        self.path = path
        self.cfg = cfg
        self.offsets = _line_offsets(html)
        self.stack = []
        self.targets = []
        self.counter = 1
        self.skip_tags = set([x.lower() for x in cfg.get("skip_tags", [])])

    def next_id(self):
        value = f"T{self.counter:06d}"
        self.counter += 1
        return value

    def handle_starttag(self, tag, attrs):
        tag_l = tag.lower()
        self.stack.append(tag_l)
        if tag_l in self.skip_tags:
            return
        starttag = self.get_starttag_text() or ""
        line, col = self.getpos()
        tag_abs = _abs_pos(self.offsets, line, col)
        if tag_abs is None:
            return
        for attr_name in ("alt", "title", "placeholder", "aria-label"):
            pat = re.compile(rf'({re.escape(attr_name)}\s*=\s*)(["\'])(.*?)\2', re.I | re.S)
            m = pat.search(starttag)
            if not m:
                continue
            raw_value = m.group(3)
            if not _candidate(raw_value, self.cfg):
                continue
            self.targets.append({
                "id": self.next_id(), "kind": "attribute", "tag": tag_l, "attr": attr_name,
                "start": tag_abs + m.start(3), "end": tag_abs + m.end(3),
                "original": raw_value, "path_hint": _path_hint(self.stack),
            })

    def handle_endtag(self, tag):
        tag_l = tag.lower()
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i] == tag_l:
                self.stack = self.stack[:i]
                break

    def handle_data(self, data):
        if not data or not _candidate(data, self.cfg):
            return
        if any(t in self.skip_tags for t in self.stack):
            return
        line, col = self.getpos()
        start = _abs_pos(self.offsets, line, col)
        if start is None:
            return
        end = start + len(data)
        raw_slice = self.html[start:end]
        if raw_slice != data:
            nearby = self.html[start:start + len(data) + 200]
            idx = nearby.find(data)
            if idx >= 0:
                start = start + idx
                end = start + len(data)
            else:
                return
        self.targets.append({
            "id": self.next_id(), "kind": "text", "tag": self.stack[-1] if self.stack else "",
            "attr": None, "start": start, "end": end, "original": data,
            "path_hint": _path_hint(self.stack),
        })

def extract_documents():
    cfg = JOB.get("html", {})
    docs = []
    for item in JOB["files"]:
        parser = Extractor(item["html"], item["path"], cfg)
        parser.feed(item["html"])
        parser.close()
        docs.append({"path": item["path"], "targets": parser.targets, "target_count": len(parser.targets)})
    return {"documents": docs}

def assemble_one(html, targets, replacements):
    edits = []
    errors = []
    for t in targets:
        tid = t.get("id")
        if tid not in replacements:
            continue
        start = int(t["start"])
        end = int(t["end"])
        original = t.get("original", "")
        current = html[start:end]
        if current != original:
            errors.append({"id": tid, "error": "span_mismatch", "expected": original[:120], "current": current[:120]})
            continue
        replacement = _clean_replacement(replacements[tid], t.get("kind", "text"))
        edits.append((start, end, replacement, tid))
    for start, end, replacement, tid in sorted(edits, key=lambda x: x[0], reverse=True):
        html = html[:start] + replacement + html[end:]
    final_html = _force_utf8_meta(html)
    encoded = base64.b64encode(final_html.encode("utf-8")).decode("ascii")
    FINAL_VAR("HTML_FINAL")
    return {"name": "HTML_FINAL", "value_base64": encoded, "bytes": len(final_html.encode("utf-8")), "applied_edits": len(edits), "errors": errors}
`;

try {
  const stdin = await readStdin();
  const job: Job = JSON.parse(stdin);
  const pyodide = await pyodideModule.loadPyodide();

  if (job.action === "extract") {
    if (!job.input_dir || !job.extensions) {
      fail("Faltan input_dir o extensions.");
      Deno.exit(0);
    }
    const files = await listHtmlFiles(job.input_dir, job.extensions);
    const payloadFiles = [];
    for (const path of files) {
      const html = await readHtmlFile(path);
      payloadFiles.push({ path, html });
    }
    pyodide.globals.set("JOB_JSON", JSON.stringify({ ...job, files: payloadFiles }));
    await pyodide.runPythonAsync(PY_CODE);
    const result = pyodide.runPython("json.dumps(extract_documents(), ensure_ascii=False)");
    ok(JSON.parse(result));
  } else if (job.action === "assemble_many") {
    if (!job.documents) {
      fail("Faltan documents.");
      Deno.exit(0);
    }
    const docs = [];
    for (const doc of job.documents) {
      const html = await readHtmlFile(doc.source_path);
      docs.push({ source_path: doc.source_path, html, targets: doc.targets, replacements: doc.replacements });
    }
    pyodide.globals.set("JOB_JSON", JSON.stringify({ ...job, docs }));
    await pyodide.runPythonAsync(PY_CODE);
    const result = pyodide.runPython(`
import json
out=[]
for doc in JOB["docs"]:
    assembled=assemble_one(doc["html"],doc["targets"],doc["replacements"])
    assembled["source_path"]=doc["source_path"]
    out.append(assembled)
json.dumps({"documents":out},ensure_ascii=False)
`);
    ok(JSON.parse(result));
  } else {
    fail(`Acción no soportada: ${(job as Job).action}`);
  }
} catch (err) {
  fail(String(err), { stack: err instanceof Error ? err.stack : undefined });
}

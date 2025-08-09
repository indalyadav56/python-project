import argparse
import json
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pypdf import PdfReader


class InvoiceItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None


class Invoice(BaseModel):
    invoice_number: Optional[str] = Field(default=None, description="Unique invoice identifier")
    invoice_date: Optional[str] = Field(default=None, description="Invoice date in ISO 8601 (YYYY-MM-DD) if possible")
    vendor_name: Optional[str] = None
    vendor_address: Optional[str] = None
    currency: Optional[str] = None
    total_amount: Optional[float] = None
    line_items: List[InvoiceItem] = Field(default_factory=list)


def read_pdf_text(pdf_path: str, max_chars: int = 120_000) -> str:
    reader = PdfReader(pdf_path)
    pages_text: List[str] = []
    for page in reader.pages:
        try:
            page_text = page.extract_text() or ""
        except Exception:
            page_text = ""
        pages_text.append(page_text)
    text = "\n\n".join(pages_text).strip()
    if len(text) > max_chars:
        return text[:max_chars] + "\n\n[TRUNCATED]"
    return text


def build_messages(json_schema: Dict[str, Any], document_text: str, file_name: str) -> List[Dict[str, str]]:
    schema_str = json.dumps(json_schema, ensure_ascii=False)
    system = (
        "You are an expert data extraction engine. "
        "Given a document, extract the requested fields strictly matching the provided JSON Schema. "
        "If a field is unknown or not present, use null. Use numbers for numeric fields. "
        "Dates should be in ISO 8601 (YYYY-MM-DD) if possible. "
        "Output only a single JSON object with no extra commentary."
    )

    user = (
        f"File name: {file_name}\n\n"
        f"JSON Schema to follow:\n{schema_str}\n\n"
        f"Document text begins:\n" + document_text
    )

    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def call_openai(messages: List[Dict[str, str]], model: str) -> Dict[str, Any]:
    from openai import OpenAI

    client = OpenAI()
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
        response_format={"type": "json_object"},
    )
    content = completion.choices[0].message.content or "{}"
    return json.loads(content)


def call_ollama(messages: List[Dict[str, str]], model: str) -> Dict[str, Any]:
    import requests

    base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")

    prompt_parts: List[str] = []
    for m in messages:
        role = m.get("role", "user").upper()
        prompt_parts.append(f"[{role}]\n{m.get('content','')}\n")
    prompt_parts.append("Output only valid minified JSON.")
    prompt = "\n".join(prompt_parts)

    resp = requests.post(
        f"{base_url}/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0},
        },
        timeout=120,
    )
    resp.raise_for_status()
    data = resp.json()
    text = data.get("response", "{}")

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start : end + 1])
            except Exception:
                pass
        return {"raw": text}


def extract_invoice(pdf_path: str, provider: str, model: str, out_path: Optional[str]) -> Dict[str, Any]:
    text = read_pdf_text(pdf_path)
    schema = Invoice.model_json_schema()
    messages = build_messages(schema, text, os.path.basename(pdf_path))

    if provider == "openai":
        result = call_openai(messages, model)
    elif provider == "ollama":
        result = call_ollama(messages, model)
    else:
        raise ValueError("Unsupported provider. Use 'openai' or 'ollama'.")

    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    return result


def detect_provider() -> str:
    if os.environ.get("OPENAI_API_KEY"):
        return "openai"
    if os.environ.get("OLLAMA_MODEL"):
        return "ollama"
    return "openai"


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(description="LLM-powered PDF data extraction example")
    parser.add_argument("--pdf", required=True, help="Absolute path to PDF file")
    parser.add_argument("--schema", default="invoice", choices=["invoice"], help="Extraction schema to use")
    parser.add_argument("--out", default=None, help="Path to write JSON output")
    parser.add_argument("--provider", default=None, choices=["openai", "ollama"], help="LLM provider (auto-detected if omitted)")
    parser.add_argument("--model", default=None, help="LLM model name (e.g., gpt-4o-mini or llama3)")

    args = parser.parse_args()

    if not os.path.isabs(args.pdf):
        raise SystemExit("--pdf must be an absolute path")

    provider = args.provider or detect_provider()
    if provider == "openai":
        model = args.model or os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
        if not os.environ.get("OPENAI_API_KEY"):
            raise SystemExit("OPENAI_API_KEY not set. Export it or use --provider ollama.")
    else:
        model = args.model or os.environ.get("OLLAMA_MODEL", "llama3")

    if args.schema != "invoice":
        raise SystemExit("Only 'invoice' schema is implemented in this example.")

    result = extract_invoice(args.pdf, provider, model, args.out)

    summary_fields = {
        "invoice_number": result.get("invoice_number"),
        "invoice_date": result.get("invoice_date"),
        "vendor_name": result.get("vendor_name"),
        "total_amount": result.get("total_amount"),
        "currency": result.get("currency"),
        "line_items_count": len(result.get("line_items", [])) if isinstance(result.get("line_items"), list) else None,
    }
    print(json.dumps({"provider": provider, "model": model, "summary": summary_fields}, ensure_ascii=False))


if __name__ == "__main__":
    main()

import argparse
import json
import os
import sys
import urllib.request
# Repo root paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
FILINGS_DIR = os.path.join(BASE_DIR, 'filings')
SEC_PDFS_DIR = os.path.join(BASE_DIR, 'sec_pdfs')



DEFAULT_API_URL = "https://gptoss120.limeox.org/v1/chat/completions"
DEFAULT_MODEL = "gptoss120"
DEFAULT_TEMPERATURE = 0.5


def build_messages(html, filename):
    system = (
        "You are an expert editor for the SEC Filings Guide website. "
        "Your output must be valid HTML only (no markdown, no explanations). "
        "Preserve all structure, tags, attributes, ids, classes, links, scripts, "
        "and styles exactly as-is. Only expand the text inside "
        "<p class=\"truncate-text\"> elements. Keep the same meaning and tone, "
        "but make each one noticeably longer and more informative (2–4 sentences). "
        "Do not add or remove sections. Do not alter headings, lists, or buttons. "
        "Return the full HTML document."
    )

    user = (
        f"Update the HTML below for file: {filename}\n\n"
        "Task:\n"
        "- Expand each <p class=\"truncate-text\"> to be more detailed and helpful.\n"
        "- Keep the rest of the HTML identical.\n"
        "- Output only the full HTML.\n\n"
        "HTML:\n"
        f"{html}"
    )

    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def call_llm(api_url, api_key, model, temperature, messages, timeout):
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }
    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        api_url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "llm-expand-filings/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} {exc.reason}: {body}") from exc
    result = json.loads(raw)

    try:
        content = result["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise RuntimeError(f"Unexpected response: {raw}")

    return content


def validate_html(content):
    lower = content.lower()
    if "<html" not in lower or "</html>" not in lower:
        raise RuntimeError("LLM response does not look like full HTML.")
    return content


def process_file(input_path, output_path, api_url, api_key, model, temperature, timeout):
    with open(input_path, "r", encoding="utf-8") as f:
        html = f.read()

    messages = build_messages(html, os.path.basename(input_path))
    content = call_llm(api_url, api_key, model, temperature, messages, timeout)
    content = validate_html(content)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    parser = argparse.ArgumentParser(
        description="Expand filing section text with LLM and save HTML output."
    )
    parser.add_argument(
        "--input",
        default=os.path.join("filings", "10k.html"),
        help="Input HTML file to process (default: filings/10k.html)",
    )
    parser.add_argument(
        "--output-dir",
        default="llm_filings",
        help="Directory to write updated HTML files",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Process all .html files in the filings directory",
    )
    parser.add_argument("--api-url", default=DEFAULT_API_URL)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument(
        "--api-key",
        default=os.environ.get("GPTOSS_API_KEY"),
        help="API key (or set GPTOSS_API_KEY env var)",
    )

    args = parser.parse_args()

    if not args.api_key:
        print("Missing API key. Pass --api-key or set GPTOSS_API_KEY.", file=sys.stderr)
        sys.exit(2)

    os.makedirs(args.output_dir, exist_ok=True)

    if args.all:
        input_dir = os.path.dirname(args.input) or "filings"
        for filename in os.listdir(input_dir):
            if not filename.endswith(".html"):
                continue
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(args.output_dir, filename)
            print(f"Processing {input_path} -> {output_path}")
            process_file(
                input_path,
                output_path,
                args.api_url,
                args.api_key,
                args.model,
                args.temperature,
                args.timeout,
            )
    else:
        input_path = args.input
        output_path = os.path.join(args.output_dir, os.path.basename(args.input))
        print(f"Processing {input_path} -> {output_path}")
        process_file(
            input_path,
            output_path,
            args.api_url,
            args.api_key,
            args.model,
            args.temperature,
            args.timeout,
        )


if __name__ == "__main__":
    main()

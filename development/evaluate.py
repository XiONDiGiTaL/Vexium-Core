#!/usr/bin/env python3
"""Local-only smoke evaluation; not a broad intelligence benchmark."""
import argparse
import ipaddress
import json
import math
from pathlib import Path
import time
import urllib.error
import urllib.parse
import urllib.request

CASES = [
    {'id': 'en-extraction', 'language': 'en', 'prompt': 'Return only JSON with key count and integer value: There are seven notes.', 'expected': {'count': 7}},
    {'id': 'tr-extraction', 'language': 'tr', 'prompt': 'Yalnızca JSON döndür: count anahtarının değeri şu cümledeki not sayısı olsun. Yedi not var.', 'expected': {'count': 7}},
    {'id': 'tr-characters', 'language': 'tr', 'prompt': 'Yalnızca JSON döndür. text anahtarının değeri tam olarak şu metin olsun: I ı İ i ç ğ ö ş ü', 'expected': {'text': 'I ı İ i ç ğ ö ş ü'}},
    {'id': 'tr-arithmetic', 'language': 'tr', 'prompt': 'Yalnızca JSON döndür. result anahtarının değeri 17 + 25 işleminin tam sayı sonucu olsun.', 'expected': {'result': 42}},
    {'id': 'app-uncertainty', 'language': 'en', 'prompt': 'No Kryvex documentation is supplied. Is the existence of a Quantum Sync menu verified? Return only JSON with verified set to a boolean.', 'expected': {'verified': False}},
    {'id': 'tr-help', 'language': 'tr', 'prompt': 'Türkçe yanıt ver. Bir yerel yapay zekâ modelinin hata yapabileceğini iki kısa cümleyle açıkla.'},
    {'id': 'en-help', 'language': 'en', 'prompt': 'In two short English sentences, explain why a local AI model can make mistakes.'},
    {'id': 'es-help', 'language': 'es', 'prompt': 'En dos frases breves en español, explica por qué un modelo local de IA puede equivocarse.'},
    {'id': 'de-help', 'language': 'de', 'prompt': 'Erkläre in zwei kurzen deutschen Sätzen, warum ein lokales KI-Modell Fehler machen kann.'},
    {'id': 'fr-help', 'language': 'fr', 'prompt': 'En deux courtes phrases en français, explique pourquoi un modèle local peut faire des erreurs.'},
]

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise urllib.error.HTTPError(req.full_url, code, 'Redirect refused', headers, fp)

def endpoint(value):
    parsed = urllib.parse.urlsplit(value)
    if parsed.scheme != 'http' or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError('Use an HTTP literal-loopback base URL without credentials, query or fragment')
    if not ipaddress.ip_address(parsed.hostname or '').is_loopback:
        raise ValueError('Only literal loopback addresses are accepted')
    return value.rstrip('/') + '/chat/completions'

def exact_json(text, expected):
    try:
        actual = json.loads(text)
    except (ValueError, TypeError):
        return False
    if not isinstance(actual, dict) or set(actual) != set(expected):
        return False
    return all(type(actual[key]) is type(value) and actual[key] == value for key, value in expected.items())

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', required=True)
    parser.add_argument('--model', required=True)
    parser.add_argument('--label', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--timeout', type=float, default=180)
    args = parser.parse_args()
    if not math.isfinite(args.timeout) or args.timeout <= 0:
        parser.error('--timeout must be finite and positive')
    try:
        url = endpoint(args.base_url)
    except ValueError as exc:
        parser.error(str(exc))
    system = (Path(__file__).parent / 'prompts' / 'kryvex-system.txt').read_text(encoding='utf-8')
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    rows = []
    for case in CASES:
        row = {'id': case['id'], 'language': case['language']}
        payload = {'model': args.model, 'messages': [{'role': 'system', 'content': system}, {'role': 'user', 'content': case['prompt']}], 'temperature': 0, 'max_tokens': 512, 'stream': False}
        started = time.perf_counter()
        try:
            request = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'}, method='POST')
            with opener.open(request, timeout=args.timeout) as response:
                raw = response.read(4 * 1024 * 1024 + 1)
            if len(raw) > 4 * 1024 * 1024:
                raise ValueError('Response exceeded 4 MiB limit')
            data = json.loads(raw)
            choice = data['choices'][0]
            text = choice['message']['content']
            if not isinstance(text, str) or not text.strip():
                raise ValueError('No nonempty assistant text')
            row.update(response=text, finish_reason=choice.get('finish_reason'))
            if 'expected' in case:
                row['expected'] = case['expected']
                row['status'] = 'pass' if exact_json(text, case['expected']) else 'fail'
            else:
                row['status'] = 'needs_human_review'
            if choice.get('finish_reason') == 'length':
                row['status'] = 'fail'
                row['error'] = 'Generation truncated at token limit'
        except Exception as exc:
            row.update(status='error', error=f'{type(exc).__name__}: {exc}')
        row['wall_seconds'] = round(time.perf_counter() - started, 3)
        rows.append(row)
    counts = {status: sum(row['status'] == status for row in rows) for status in ('pass', 'fail', 'error', 'needs_human_review')}
    report = {'label': args.label, 'model': args.model, 'endpoint': url, 'settings': {'temperature': 0, 'max_tokens': 512}, 'scope': 'Synthetic smoke tests only; language quality requires human review; runtime and hardware not measured', 'summary': counts, 'results': rows}
    with Path(args.output).open('x', encoding='utf-8') as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)
        handle.write('\n')
    print(json.dumps(counts))
    return 1 if counts['fail'] or counts['error'] else 0

if __name__ == '__main__':
    raise SystemExit(main())

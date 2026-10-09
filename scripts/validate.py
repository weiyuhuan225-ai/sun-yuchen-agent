#!/usr/bin/env python3
"""Validate corpus relationships and exercise the offline retrieval entry point."""
import ast
from collections import Counter
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlsplit, parse_qs

ROOT = Path(__file__).resolve().parents[1]

def require(condition, message):
    if not condition:
        raise ValueError(message)

def retrieve(payload):
    result = subprocess.run(
        [sys.executable, str(ROOT / 'scripts/retrieve.py'), '--stdin'],
        input=json.dumps(payload, ensure_ascii=False),
        capture_output=True, text=True, encoding='utf-8', check=True,
    )
    return json.loads(result.stdout)

def main():
    data = json.loads((ROOT / 'references/corpus.json').read_text(encoding='utf-8'))
    items = data['items']
    index = {item['id']: item for item in items}
    require(len(index) == len(items), 'Duplicate item IDs')
    counts = Counter(item['kind'] for item in items)
    mapping = {'record':'main_records', 'source':'source_count', 'theme':'themes',
               'principle':'principles', 'boundary':'boundaries',
               'index':'indices', 'course':'course_guides'}
    for kind, meta_key in mapping.items():
        require(counts[kind] == data['metadata'][meta_key], f'Count mismatch: {kind}')
    for alias, target in data['aliases'].items():
        require(target in index, f'Broken alias: {alias}')
    for item in items:
        for target in item.get('references', []) + item.get('source_ids', []):
            require(target in index, f"Missing target: {item['id']} -> {target}")
        if item['kind'] == 'record':
            require(bool(item.get('limitations')), f"Missing limitation: {item['id']}")
            require(bool(item.get('source_ids')), f"Missing source: {item['id']}")
        if item.get('url'):
            url = urlsplit(item['url'])
            require(url.scheme in ('https','http') and bool(url.netloc), f"Invalid URL: {item['id']}")
            require(not ({k.lower() for k in parse_qs(url.query)} & {'token','access_token','api_key','signature','sig','x-amz-signature'}), f"Sensitive URL parameter: {item['id']}")
    for path in ROOT.rglob('*.md'):
        if '.git' in path.parts:
            continue
        text = path.read_text(encoding='utf-8')
        for target in re.findall(r'\]\(([^)]+)\)', text):
            if target.startswith(('http://','https://','#')):
                continue
            file_target = (path.parent / target.split('#')[0]).resolve()
            require(file_target.is_relative_to(ROOT), f'Link escapes project: {path.name}')
            require(file_target.exists(), f'Broken local link: {path.name} -> {target}')
    for path in (ROOT / 'scripts').glob('*.py'):
        ast.parse(path.read_text(encoding='utf-8'))
    exact = retrieve({'ids':['R003','S115','S116']})
    require({i['id'] for i in exact['results']} == {'R003','S115','S116'}, 'Exact ID retrieval failed')
    require(not exact['missing_ids'], 'Known IDs reported missing')
    legal = retrieve({'query':'SEC 2026 民事和解 1000万美元', 'limit':4})
    require('F06' in {i['id'] for i in legal['results']}, 'Legal background note not retrieved')
    require({'S115','S116'} <= {i['id'] for i in legal['supporting_evidence']}, 'Legal primary sources not linked')
    absent = retrieve({'ids':['NOT-A-REAL-RECORD']})
    require(absent['results'] == [] and absent['missing_ids'] == ['NOT-A-REAL-RECORD'], 'Missing ID handling failed')
    print(json.dumps({'status':'passed', 'items':len(items), 'counts':dict(counts),
                      'checks':['metadata','unique IDs','aliases','source references','relative links','Python syntax','retrieval','missing IDs'],
                      'scope':'Local package checks; external pages and model behavior are not re-verified.'}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print(json.dumps({'status':'failed','error':str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(1)

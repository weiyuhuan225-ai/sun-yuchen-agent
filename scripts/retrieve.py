#!/usr/bin/env python3
"""Search the packaged Justin Sun corpus. Standard library only; no network."""
from __future__ import annotations
import argparse
import collections
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SYNONYMS = [
    ['ai', '人工智能', 'agent', '智能体', '代理人'],
    ['营销', '传播', '注意力', '流量', '品牌', 'marketing'],
    ['产品', '用户', '需求', '使用', '体验', 'product'],
    ['稳定币', 'usdd', 'usdt', 'stablecoin', '储备', '补贴', '收益率'],
    ['巴菲特', 'buffett', '午餐', '晚宴', '慈善竞拍'],
    ['监管', 'sec', '证券交易委员会', 'rainberry', '和解', '判决'],
    ['wlfi', 'world liberty', 'worldliberty', '冻结', '特朗普', 'trump'],
    ['职业', '工作', '选择', '创业', '能力', '转行', '机会成本'],
    ['风险', '止损', '成本', '资金', '现金', '损失', '预算'],
    ['比特币', 'bitcoin', 'btc'],
    ['波场', 'tron', 'trx'],
    ['利伯兰', 'liberland', '总理', '国家承认'],
    ['课程', '财富自由', '财务自由', '笔记'],
]
KIND_ALIASES = {'records':'record','themes':'theme','boundaries':'boundary',
                'indices':'index','courses':'course','sources':'source'}

def tokens(text):
    text = re.sub(r'孙宇晨|justin\s+sun',' ',str(text).lower())
    out = re.findall(r'[a-z][a-z0-9_+-]*|\d{4}',text)
    for block in re.findall(r'[\u3400-\u9fff]+',text):
        out.extend(block[i:i+2] for i in range(len(block)-1))
    return out

def text_of(item):
    fields = ['title','summary','topics','limitations','date','event_date',
              'publication_date','medium','grade','body','keywords']
    return ' '.join(str(item.get(k,'')) for k in fields)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--query',default='')
    parser.add_argument('--ids',nargs='+')
    parser.add_argument('--limit',type=int,default=6)
    parser.add_argument('--kind',choices=['all',*KIND_ALIASES],default='all')
    parser.add_argument('--stdin',action='store_true')
    args = parser.parse_args()
    if args.stdin:
        payload = json.load(sys.stdin)
        if not isinstance(payload,dict):
            parser.error('stdin must be a JSON object')
        args.query = str(payload.get('query',args.query))
        args.ids = payload.get('ids',args.ids)
        args.limit = int(payload.get('limit',args.limit))
        args.kind = payload.get('kind',args.kind)
        if args.kind not in ['all',*KIND_ALIASES]:
            parser.error('unknown kind')
    data = json.loads((ROOT/'references/corpus.json').read_text(encoding='utf-8'))
    items = data['items']
    by_id = {i['id']:i for i in items}
    aliases = data.get('aliases',{})
    def resolve(label):
        return by_id.get(aliases.get(label,label))
    missing = []
    if args.ids:
        results = []
        for label in args.ids:
            item = resolve(label)
            if item is not None and item not in results:
                results.append(item)
            elif item is None:
                missing.append(label)
    else:
        query = args.query.strip()
        if not query:
            parser.error('provide --query or --ids')
        if args.kind == 'all':
            pool = [i for i in items if i['kind'] not in ['source','index','course']]
            if re.search(r'课程|笔记|音频|节目|索引|Alan|鲁豫|Lex',query,re.I):
                pool = [i for i in items if i['kind']!='source']
        else:
            pool = [i for i in items if i['kind']==KIND_ALIASES[args.kind]]
        freq = [collections.Counter(tokens(text_of(i))) for i in pool]
        dfs = collections.Counter(t for f in freq for t in f)
        avg_len = sum(sum(f.values()) for f in freq)/max(1,len(freq))
        qweights = {t:1.0 for t in tokens(query)}
        qlower = query.lower()
        for group in SYNONYMS:
            if any((re.search(r'\b'+re.escape(t)+r'\b',qlower) if t.isascii() else t in qlower) for t in group):
                for t in tokens(' '.join(group)):
                    qweights[t] = max(qweights.get(t,0),0.22)
        scored = []
        for item,f in zip(pool,freq):
            score = 0.0
            length = sum(f.values())
            for term,w in qweights.items():
                tf = f[term]
                if tf:
                    inverse = math.log(1+(len(pool)-dfs[term]+.5)/(dfs[term]+.5))
                    score += w*inverse*(tf*2.2)/(tf+1.2*(.25+.75*length/max(1,avg_len)))
            title = item.get('title','').lower()
            score += sum(1.2 for token in tokens(query) if token in title)
            if item['kind'] in ['theme','boundary','principle']:
                score *= 1.07
            if score > 0:
                scored.append((score,item))
        scored.sort(key=lambda x:(-x[0],x[1]['id']))
        results = [dict(item,retrieval_score=round(score,3)) for score,item in scored[:max(1,min(args.limit,20))]]
    supporting = []
    seen = {i['id'] for i in results}
    def add_refs(item,depth=0):
        if depth > 2:
            return
        for ref in item.get('references',[]) + item.get('source_ids',[]):
            found = resolve(ref)
            if found and found['id'] not in seen:
                seen.add(found['id'])
                supporting.append(found)
                add_refs(found,depth+1)
    for item in results:
        add_refs(item)
    output = {'metadata':data['metadata'],'query':args.query or None,
              'results':results,'supporting_evidence':supporting,'missing_ids':missing,
              'note':'材料为编写者摘要／分析，不是逐字稿。检索分数只表示字面相关性，不是事实可信度。当前事件须另行核验。'}
    print(json.dumps(output,ensure_ascii=False,indent=2))

if __name__ == '__main__':
    try:
        main()
    except (OSError,ValueError,TypeError) as exc:
        print(json.dumps({'error':str(exc)},ensure_ascii=False),file=sys.stderr)
        raise SystemExit(1)

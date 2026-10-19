#!/usr/bin/env python3
"""Coteja DOI y PMID de las líneas de referencia agregadas (git diff) contra Crossref/PubMed.
Uso: python3 doi.py archivo1.md [archivo2.md ...]  (desde el repo)"""
import json, re, subprocess, sys, urllib.request, time, unicodedata
def norm(s): return ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if unicodedata.category(c) != 'Mn')
def get(url):
    for _ in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'libro-verif/1.0 (mailto:siev63850@gmail.com)'})
            return json.load(urllib.request.urlopen(req, timeout=20))
        except Exception as e:
            err = e; time.sleep(1)
    return {'_err': str(err)}
for f in sys.argv[1:]:
    diff = subprocess.run(['git', 'diff', '-U0', '--', f], capture_output=True, text=True).stdout
    refs = [l[1:] for l in diff.splitlines() if l.startswith('+') and re.match(r'\+\d+\. ', l)]
    print(f'## {f}: {len(refs)} refs nuevas')
    for r in refs:
        doi = re.search(r'doi:\s*(10\.\S+?)[.;,]?(\s|$)', r, re.I) or re.search(r'doi\.org/(10\.\S+?)[.;,]?(\s|$)', r)
        pmid = re.search(r'PMID:?\s*(\d+)', r)
        autor = norm(re.sub(r'^\d+\.\s*', '', r).split()[0].strip(',.'))
        anio = re.search(r'\b(19|20)\d\d\b', r)
        out = []
        if doi:
            d = get('https://api.crossref.org/works/' + doi.group(1))
            if '_err' in d: out.append(f'DOI ERROR {doi.group(1)}')
            else:
                m = d['message']; t = (m.get('title') or [''])[0]
                fa = norm((m.get('author') or [{}])[0].get('family', '?'))
                y = (m.get('issued', {}).get('date-parts') or [[None]])[0][0]
                ok = (fa in norm(r)) and (anio and str(y) in r)
                out.append(f"DOI {'OK ' if ok else '?? '} {fa} {y} «{t[:90]}»")
        if pmid:
            d = get(f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id={pmid.group(1)}')
            try:
                m = d['result'][pmid.group(1)]; t = m['title']; fa = norm(m['authors'][0]['name'].split()[0]) if m['authors'] else '?'
                y = m['pubdate'][:4]; ok = fa in norm(r) and y in r
                out.append(f"PMID {'OK ' if ok else '?? '} {fa} {y} «{t[:90]}»")
            except Exception: out.append(f'PMID ERROR {pmid.group(1)}')
            time.sleep(0.4)
        if not out: out.append('SIN DOI/PMID')
        print(f"- {r[:110]}\n    " + '\n    '.join(out))

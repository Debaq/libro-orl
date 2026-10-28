import re,json,os,glob,sys
S=sys.argv[1]
def lats(path):
    s=open(path).read()
    W=float(re.search(r'<svg[^>]*width="([\d.]+)"',s).group(1))
    an=json.loads(re.search(r'<metadata id="anclas">(.*?)</metadata>',s,re.S).group(1))
    lados=[l for l in ('OD','OI') if any(k.startswith(l+' ') for k in an)]
    L=len(lados); pw=(W-134-(L-1)*40)/L
    out={}
    for k,(x,y) in an.items():
        p=k.split()
        if len(p)==3:
            i=lados.index(p[0]); x0=70+i*(pw+40)
            out[k]=round((x-x0)/22,2)
        else: out[k]=None
    return out
res={}
for f in open(S+'/abr_cambiadas.txt').read().split():
    a=lats(S+'/salida_vieja/'+f); b=lats('figuras/salida/'+f)
    d={}
    for k in sorted(set(a)|set(b)):
        if a.get(k)!=b.get(k) and (len(k.split())==3):
            d[k]=(a.get(k,'—'),b.get(k,'—'))
    res[f]=d
json.dump(res,open(S+'/lat_cambios.json','w'),ensure_ascii=False,indent=1)
# notas del libro sobre esas figuras
for md in sorted(glob.glob('capitulos/*.md')):
    t=open(md).read()
    for m in re.finditer(r'\n:::figura (\S+) abr ?(\d*)\n(.*?)\n:::',t,re.S):
        caso,n,cuerpo=m.group(1),m.group(2),m.group(3)
        f=f"{caso}_abr"+(f"_{n}" if n and n!='1' else '')+'.svg'
        if f not in res: continue
        d=res[f]
        print(f'\n## {os.path.basename(md)[:3]} {f}')
        print('   cambios:',{k:v for k,v in d.items()})
        for l in cuerpo.split('\n'):
            if l.strip(): print('   ',l[:260])

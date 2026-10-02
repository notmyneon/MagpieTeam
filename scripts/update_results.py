"""Cache official NHL outcomes by exact game ID; never infer a shootout winner."""
import concurrent.futures,json,pathlib,time,urllib.request
ROOT=pathlib.Path(__file__).resolve().parents[1]
rows=json.loads((ROOT/'data.json').read_text())
meta=json.loads((ROOT/'game-meta.json').read_text())
needed={str(v[0]) for v in meta.values()}
pairs={(r['id'].split('-')[0],r['year']) for r in rows}
ALIASES={'L.A':'LAK','T.B':'TBL','S.J':'SJS','N.J':'NJD','PHX':'ARI','ARZ':'ARI','UHC':'UTA'}
def fetch(pair):
 team,year=pair;team=ALIASES.get(team,team)
 url=f'https://api-web.nhle.com/v1/club-schedule-season/{team}/{year}{int(year)+1}'
 for attempt in range(4):
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'MagpieHockey/1.0'})
   with urllib.request.urlopen(req,timeout=40) as resp: data=json.load(resp)
   return data.get('games',[])
  except Exception:
   if attempt==3: return []
   time.sleep(attempt+1)
results_path=ROOT/'results.json'
results=json.loads(results_path.read_text()) if results_path.exists() else {}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
 for games in pool.map(fetch,sorted(pairs)):
  for g in games:
   gid=str(g['id'])
   if gid not in needed or g.get('gameState') not in ('OFF','FINAL'):continue
   h=g['homeTeam'];a=g['awayTeam'];hs=h.get('score');ass=a.get('score')
   if hs is None or ass is None or hs==ass:continue
   end=g.get('gameOutcome',{}).get('lastPeriodType')
   if end not in ('REG','OT','SO'):continue
   results[gid]=[h['abbrev'] if hs>ass else a['abbrev'],end,hs,ass,h['abbrev'],a['abbrev']]
results_path.write_text(json.dumps(results,separators=(',',':'))+'\n')
print(f'Official outcomes: {len(results)} / {len(needed)} games')
missing=needed-set(results)
(ROOT/'results-status.json').write_text(json.dumps({'matched':len(needed-set(missing)),'total':len(needed),'unmatched':sorted(missing)},separators=(',',':')))
if not results: raise SystemExit('No NHL results retrieved; inspect network/API before retrying')

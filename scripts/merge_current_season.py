"""Merge a compact current-season export into existing Magpie JSON."""
import base64,gzip,json,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
source=root/'season-2026.b64'
if not source.exists():
 print('No 2026 payload; skipping merge')
 raise SystemExit(0)
records=json.loads(gzip.decompress(base64.b64decode(source.read_text().strip())))
data_path=root/'data.json'; meta_path=root/'game-meta.json'
data=json.loads(data_path.read_text()); meta=json.loads(meta_path.read_text())
assert records and all(len(a)==12 for a in records)
assert len({(a[0],str(a[1])) for a in records})==len(records)
from collections import Counter
assert set(Counter(str(a[1]) for a in records).values())=={2}
# The official game ID is carried in the existing row key after the team prefix.
new=[]
for a in records:
 team,game,opponent,date,seconds,shots,ga,penalties,blocks,hits,takeaways,gf=a
 game=str(int(game))
 date=str(int(date))
 date=f'{date[:4]}-{date[4:6]}-{date[6:]}'
 rid=f'{team}-{game}'
 new.append({'id':rid,'year':'2026','date':date,'opponent':opponent,
 'minutes':seconds/60,'shotsAgainst':shots,'goalsAgainst':ga,
 'minorPenalties':penalties,'blocked':blocks,'hits':hits,'takeaways':takeaways})
 meta[rid]=[game,gf]
existing={r['id']:r for r in data}
for r in new: existing[r['id']]=r
data=list(existing.values())
assert all(r['id'] in meta for r in data)
assert sum(r['year']=='2026' for r in data)==len(records)
data_path.write_text(json.dumps(data,separators=(',',':'))+'\n')
meta_path.write_text(json.dumps(meta,separators=(',',':'))+'\n')
print(f'Merged {len(new)} 2026 team-game records; {len(data)} total records')

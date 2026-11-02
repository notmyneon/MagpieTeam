"""Aggregate ALL-situation team games into checked hidden similarity profiles."""
import csv,collections,sys,pathlib,math
source=pathlib.Path(sys.argv[1]);output=pathlib.Path(sys.argv[2]);groups={};seen=set();aliases={'T.B':'TBL','L.A':'LAK','N.J':'NJD','S.J':'SJS','PHX':'ARI','ARZ':'ARI','UHC':'UTA'}
fields=['goalsFor','goalsAgainst','shotsOnGoalFor','shotsOnGoalAgainst','xGoalsFor','xGoalsAgainst','xOnGoalFor','xOnGoalAgainst','shotAttemptsFor','shotAttemptsAgainst','unblockedShotAttemptsFor','unblockedShotAttemptsAgainst','highDangerShotsFor','highDangerShotsAgainst','penalityMinutesFor','penalityMinutesAgainst','penaltiesFor','penaltiesAgainst','giveawaysFor','faceOffsWonFor','faceOffsWonAgainst']
with source.open(newline='') as f:
 for r in csv.DictReader(f):
  if r['situation'].strip().lower()!='all':continue
  typ=r['gameId'][4:6]
  if typ not in ['02','03']:continue
  team=aliases.get(r['team'],r['team']);rid=(team,r['gameId']);assert rid not in seen;seen.add(rid)
  scope='regular' if typ=='02' else 'playoffs';key=(team,r['season'],scope);a=groups.setdefault(key,dict(team=team,year=r['season'],scope=scope,gp=0,minutes=0,**{k:0 for k in fields}));a['gp']+=1;a['minutes']+=float(r['iceTime'])/60
  for k in fields:a[k]+=float(r[k])
mapping={'gf60':'goalsFor','ga60':'goalsAgainst','sf60':'shotsOnGoalFor','sa60':'shotsOnGoalAgainst','xgf60':'xGoalsFor','xga60':'xGoalsAgainst','xsf60':'xOnGoalFor','xsa60':'xOnGoalAgainst','hdFor60':'highDangerShotsFor','hdAgainst60':'highDangerShotsAgainst','pim60':'penalityMinutesFor','pimDrawn60':'penalityMinutesAgainst','penalties60':'penaltiesFor','penaltiesDrawn60':'penaltiesAgainst','giveaways60':'giveawaysFor'}
result=[]
for a in groups.values():
 assert a['minutes']>0
 r={k:a[k] for k in ['team','year','scope','gp','minutes']}
 for k,src in mapping.items():r[k]=a[src]*60/a['minutes']
 for k,fr,ag in [('xgShare','xGoalsFor','xGoalsAgainst'),('corsiShare','shotAttemptsFor','shotAttemptsAgainst'),('fenwickShare','unblockedShotAttemptsFor','unblockedShotAttemptsAgainst'),('faceoffShare','faceOffsWonFor','faceOffsWonAgainst')]:r[k]=a[fr]/(a[fr]+a[ag]) if a[fr]+a[ag]>0 else None
 r['shootingPct']=a['goalsFor']/a['shotsOnGoalFor'] if a['shotsOnGoalFor'] else None
 r['savePct']=1-a['goalsAgainst']/a['shotsOnGoalAgainst'] if a['shotsOnGoalAgainst'] else None
 assert all(v is None or not isinstance(v,float) or math.isfinite(v) for v in r.values());result.append(r)
headers=['team','year','scope','gp','minutes',*mapping,'xgShare','corsiShare','fenwickShare','faceoffShare','shootingPct','savePct']
with output.open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=headers);w.writeheader()
 for r in sorted(result,key=lambda r:(r['year'],r['scope'],r['team'])):w.writerow({k:'' if v is None else format(v,'.8f').rstrip('0').rstrip('.') if isinstance(v,float) else v for k,v in r.items()})
print(f'Validated {len(result)} team-season profiles from {len(seen)} team-game rows.')

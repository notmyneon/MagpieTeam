"""Aggregate ALL-situation team games into checked hidden similarity profiles."""
import csv,collections,sys,pathlib,math
source=pathlib.Path(sys.argv[1]);output=pathlib.Path(sys.argv[2]);groups={};seen=set();five={};aliases={'T.B':'TBL','L.A':'LAK','N.J':'NJD','S.J':'SJS','PHX':'ARI','ARZ':'ARI','UHC':'UTA'}
fields=['hitsFor','blockedShotAttemptsAgainst','takeawaysFor','goalsFor','goalsAgainst','shotsOnGoalFor','shotsOnGoalAgainst','xGoalsFor','xGoalsAgainst','xOnGoalFor','xOnGoalAgainst','shotAttemptsFor','shotAttemptsAgainst','unblockedShotAttemptsFor','unblockedShotAttemptsAgainst','highDangerShotsFor','highDangerShotsAgainst','penalityMinutesFor','penalityMinutesAgainst','penaltiesFor','penaltiesAgainst','giveawaysFor','faceOffsWonFor','faceOffsWonAgainst']
with source.open(newline='') as f:
 for r in csv.DictReader(f):
  situation=r['situation'].strip().lower()
  if situation not in ['all','5on5']:continue
  typ=r['gameId'][4:6]
  if typ not in ['02','03']:continue
  team=aliases.get(r['team'],r['team']);scope='regular' if typ=='02' else 'playoffs';key=(team,r['season'],scope)
  if situation=='5on5':
   a=five.setdefault(key,dict(gp=0,gf=0,ga=0,sf=0,sa=0));a['gp']+=1
   for dst,src in [('gf','goalsFor'),('ga','goalsAgainst'),('sf','shotsOnGoalFor'),('sa','shotsOnGoalAgainst')]:a[dst]+=float(r[src])
   continue
  rid=(team,r['gameId']);assert rid not in seen;seen.add(rid)
  scope='regular' if typ=='02' else 'playoffs';key=(team,r['season'],scope);a=groups.setdefault(key,dict(team=team,year=r['season'],scope=scope,gp=0,minutes=0,**{k:0 for k in fields}));a['gp']+=1;a['minutes']+=float(r['iceTime'])/60
  for k in fields:a[k]+=float(r[k])
mapping={'hits60':'hitsFor','blocked60':'blockedShotAttemptsAgainst','takeaways60':'takeawaysFor','gf60':'goalsFor','ga60':'goalsAgainst','sf60':'shotsOnGoalFor','sa60':'shotsOnGoalAgainst','xgf60':'xGoalsFor','xga60':'xGoalsAgainst','xsf60':'xOnGoalFor','xsa60':'xOnGoalAgainst','hdFor60':'highDangerShotsFor','hdAgainst60':'highDangerShotsAgainst','pim60':'penalityMinutesFor','pimDrawn60':'penalityMinutesAgainst','penalties60':'penaltiesFor','penaltiesDrawn60':'penaltiesAgainst','giveaways60':'giveawaysFor'}
result=[]
for a in groups.values():
 assert a['minutes']>0
 r={k:a[k] for k in ['team','year','scope','gp','minutes']}
 for k,src in mapping.items():r[k]=a[src]*60/a['minutes']
 for k,fr,ag in [('xgShare','xGoalsFor','xGoalsAgainst'),('corsiShare','shotAttemptsFor','shotAttemptsAgainst'),('fenwickShare','unblockedShotAttemptsFor','unblockedShotAttemptsAgainst'),('faceoffShare','faceOffsWonFor','faceOffsWonAgainst')]:r[k]=a[fr]/(a[fr]+a[ag]) if a[fr]+a[ag]>0 else None
 r['shootingPct']=a['goalsFor']/a['shotsOnGoalFor'] if a['shotsOnGoalFor'] else None
 r['savePct']=1-a['goalsAgainst']/a['shotsOnGoalAgainst'] if a['shotsOnGoalAgainst'] else None
 fv=five.get((a['team'],a['year'],a['scope']))
 assert fv and fv['gp']==a['gp'],('5v5 coverage',a['team'],a['year'],a['scope'])
 r.update(fiveGF=fv['gf'],fiveGA=fv['ga'],fiveSF=fv['sf'],fiveSA=fv['sa'])
 r['pdo5v5']=(fv['gf']/fv['sf']+1-fv['ga']/fv['sa'])*100 if fv['sf'] and fv['sa'] else None
 assert all(v is None or not isinstance(v,float) or math.isfinite(v) for v in r.values());result.append(r)
headers=['team','year','scope','gp','minutes',*mapping,'xgShare','corsiShare','fenwickShare','faceoffShare','shootingPct','savePct','fiveGF','fiveGA','fiveSF','fiveSA','pdo5v5']
with output.open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=headers);w.writeheader()
 for r in sorted(result,key=lambda r:(r['year'],r['scope'],r['team'])):w.writerow({k:'' if v is None else format(v,'.8f').rstrip('0').rstrip('.') if isinstance(v,float) else v for k,v in r.items()})
print(f'Validated {len(result)} team-season profiles from {len(seen)} team-game rows.')

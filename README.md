# Magpie Hockey Teams

Five views: Standings, Team Cards, Compare, Games, Timeline. No browser uploads. Shared Magpie Hockey and NHL logo assets are served from the player site. Cards include PNG download controls.

Statistics use only ALL situation rows. Magpie is the average individual game score: (Blocks + Hits + Takeaways) / (SA per 60 + Goals Against + Penalties Taken) × 10. Shootout deciding goals do not enter this calculation.

`data.json` contains the game statistics. `game-meta.json` maps row IDs to NHL game ID, goals for and playoff flag. `results.json` stores official NHL winners, ending period and final scores. Regular season and playoffs can be viewed separately. Preseason is available when present. Record totals cover the games present in the dataset.

The Update official NHL results workflow runs when data or lookup code changes, or manually through Actions. It matches official NHL season schedules by exact game ID, commits cached results, and deploys Pages. Tied statistical goals with no official match stay pending, not ties. All 23,230 games were matched at initial publication.

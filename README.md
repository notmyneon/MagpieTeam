# Magpie Team

Static GitHub Pages team Magpie site. Upload these files to the root of a public repository named MagpieTeam. In Settings → Pages select Deploy from a branch, main, / (root).

Data automatically loads from data.json on every visit. Only situation=all is included; each team/game appears once. Season is the starting year (2024 means 2024–25). Both regular-season and playoff games are included, matching the original page.

Formula: (blocked shots + hits + takeaways) / (shots against per 60 + goals against + penalties taken) × 10. Blocks use blockedShotAttemptsAgainst; penalties use penaltiesFor, not minor counts. Minutes use iceTime / 60. Original season and comparison aggregation is preserved.

Card titles and uploaded logos are browser preferences. Hosted statistics do not depend on browser storage. To update statistics, replace data.json in GitHub. This version does not fetch nightly NHL updates.

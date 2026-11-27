# Drinking Observatory

A two-page static site for *Drinking*, a privacy-first cultural memoir of people, places, nights and consequences.

- `index.html`: the public archive (stories, eras, people, places, then and now)
- `submit.html`: the "Tell your story" page. Nothing is published automatically; every submission is reviewed and privacy-checked first.
- `assets/site.css`, `assets/site.js`: styling and interactions
- `.nojekyll`: served as plain files on GitHub Pages

Story cards on the public pages are demonstration records only. The working archive stays private (see the Drinking research repository).

## Checks

`python3 scripts/check_site.py` checks that each page parses, has a title, language and viewport, and that every local link and `#anchor` resolves. The **Site check** workflow runs it, plus a syntax check of `assets/site.js`, on every push and pull request.

`scc-health.json` is read by the SCC Nexus Control Tower.

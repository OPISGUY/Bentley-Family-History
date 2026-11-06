# The family website

Visit [Bentley Family History](https://opisguy.github.io/Bentley-Family-History/). GitHub Pages is enabled. Visitors need no account or payment.

The published branch is `research/charles-william-free-sources-2026-11-04`, deployed from its root. The root landing page forwards visitors to the generated family website in `docs/`; a visible link works if automatic forwarding is unavailable. The default branch also holds the same research and website updates.

## Updating the history

The Markdown files in the repository remain the editable research source. `family-groups.md` supplies the family panels. `scripts/build_site.py` supplies the home page and converts the notes to readable HTML. `site/` contains the styles and interactions.

After changing research or site source, run:

```sh
python scripts/build_site.py
python scripts/check_site.py
node --check site/app.js
```

Commit the changed source and rebuilt `docs/` files together. The build needs only Python's standard library and performs no network requests. The browser needs no external scripts, fonts, analytics or account integration.

The website keeps ambiguous relationships visible and does not publish living generations. Earlier research notes display a notice pointing to the newer conclusions. Do not add a person merely because their name matches.

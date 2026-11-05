# The family website

The website is built and saved in `docs/`. It has a clickable generation-by-generation tree, searchable family groups, story pages, source links and print controls. Visitors need no account. GitHub Pages has not yet been enabled for this repository.

## One-time publishing step

Using the existing GitHub account, open this repository's **Settings → Pages**. Under **Build and deployment**:

1. Choose **Deploy from a branch**.
2. Select the branch containing these files: **ccr-469e384c-x98nc5** (the default branch).
3. Select **/docs**, then **Save**.
4. Wait for GitHub to finish publishing. The Pages settings will show the actual **Visit site** link. Share that link with relatives.

GitHub Pages supports public repositories on GitHub Free. No custom domain, paid upgrade, new service or account is required. [GitHub's instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site).

The website and research changes were merged into the default branch in PR #1. Pages setup remains pending: the available browser was signed out of GitHub, and the connected repository tools do not expose Pages administration. Publication is authorised; another approval is not required.

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

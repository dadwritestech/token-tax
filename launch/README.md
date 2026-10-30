# Launch kit (Tue 2026-11-03)

Nothing here has been posted. Files: `hn.md`, `reddit.md`, `x-thread.md`, `linkedin.md`, `issues.md` (good first issues).

## Launch-day order

1. Make the repo public: `gh repo edit dadwritestech/token-tax --visibility public --accept-visibility-change-consequences`
2. Enable Pages (the workflow skips while the repo is private, and `GITHUB_TOKEN` cannot enable it):
   `gh api -X POST repos/dadwritestech/token-tax/pages -f build_type=workflow`
   then `gh workflow run pages.yml -R dadwritestech/token-tax`. Check that https://dadwritestech.github.io/token-tax/calculator.html loads and counts text.
3. Set the homepage: `gh repo edit dadwritestech/token-tax --homepage https://dadwritestech.github.io/token-tax/`
4. Upload `docs/social.png` under Settings → General → Social preview. There is no API for this.
5. Open the five issues from `issues.md` with the `good first issue` label.
6. Tag and release v0.1.0 (matching CITATION.cff).
7. Post HN first (with the first comment right away), then X, LinkedIn, and the subreddits spaced out over the day. Re-read each subreddit's rules first; see `reddit.md`.

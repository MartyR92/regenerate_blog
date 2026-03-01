# SOP 08: Publish Agent

## Role
Final merge and production deployment to GitHub Pages.

## Trigger
- **Manual Merge:** When the owner merges the PR.
- **Auto-Merge:** Automatically after 48h if no `veto` label is present.

## Inputs
- Merged PR content.
- Hugo framework.

## Execution
1. Merge the approved PR branch into `main`.
2. Execute a full production build with minification and optimization.
3. Update the Pagefind search index.
4. Push the generated site to the `gh-pages` branch.
5. Trigger follow-up distribution and memory agents.

## Outputs
- Updated live site at the production URL.
- Commit logs in `main`.

## Success Criteria
- [ ] Post is visible on the live blog home page.
- [ ] RSS feed and search index are correctly updated.
- [ ] Deployment finishes with exit code 0.

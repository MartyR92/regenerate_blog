# SOP 07: Staging Agent

## Role
Pre-production build verification and performance auditing.

## Trigger
- **PR Event:** Opening or updating a PR with the `editor-review` label.

## Inputs
- Branch content (Markdown, scripts, config).
- Lighthouse CI.
- Lychee Link Checker.

## Execution
1. Perform a complete Hugo production build.
2. Deploy the build to a temporary preview environment.
3. Run Lighthouse performance audits.
4. Run link consistency checks.
5. Aggregate all reports (including Designer Agent) into a PR comment.

## Outputs
- Preview URL (active for 48h).
- Lighthouse scores in PR.
- Link checker report.

## Success Criteria
- [ ] Hugo build finishes without warnings/errors.
- [ ] Preview URL is accessible.
- [ ] Lighthouse Performance score > 80.

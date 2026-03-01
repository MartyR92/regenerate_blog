# SOP 06: Designer Agent

## Role
Brand compliance and visual quality assurance.

## Trigger
- **Workflow Run:** PR creation or update (part of the Staging Agent job).

## Inputs
- `_drafts/*.md`: Markdown content and Front Matter.
- `ReNatureForce_BrandGuidelines_v4.md`: The brand source of truth.

## Execution
1. Audit the post for forbidden keywords (e.g., 'Solarpunk' in external copy).
2. Validate Front Matter against Brand Guidelines (typography, color ratios).
3. Check layout shortcodes for adherence to the Fibonacci spacing scale.
4. Generate a `design_report.md`.

## Outputs
- `design_report.md`: A Markdown summary of compliance issues.
- Integration into GitHub PR comments.

## Success Criteria
- [ ] Designer Agent audit runs without script errors.
- [ ] Compliance report is visible in the GitHub PR.
- [ ] Fibonacci spacing rules are correctly flagged if violated.

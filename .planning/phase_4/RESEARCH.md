# Research: Phase 4 - Language Switch & UI Polish

## 1. Enabling the Language Switcher
- **Parameter:** `showLanguageSwitcher = true` needs to be added to the `[params]` section of the configuration.
- **Location:** The root `hugo.toml` is the primary configuration file.
- **Requirement:** Each language must have a `displayName` set under `[languages.xx.params]`, which is already present in the current `hugo.toml`.

## 2. Menu Configuration
- Blowfish expects separate menu files for each language if specific navigation is needed.
- Currently, I see `themes/blowfish/config/_default/menus.en.toml`.
- I should check if there are menu definitions in the root `hugo.toml`. (Checking previous `read_file` output... no menus were in the output, but the file might have been truncated or they are missing).

## 3. Multilingual Content Structure
- The project uses the "By Directory" approach: `content/de/` and `content/en/`.
- This is correctly configured in `hugo.toml` via `contentDir`.

## 4. Findings
- The language switch is missing simply because the toggle is not enabled in `params`.
- Verification will require ensuring that the switcher appears in the header and correctly links to the translated content.

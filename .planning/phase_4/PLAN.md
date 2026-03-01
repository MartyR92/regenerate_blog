# Plan: Phase 4 - Language Switch & UI Polish

## 1. Enable Language Switcher
- [ ] Edit `hugo.toml` to add `showLanguageSwitcher = true` within the `[params]` block.
- [ ] Ensure `displayName` remains set for both `de` and `en` languages.

## 2. Menu Setup (Optional but recommended)
- [ ] Check if menus are missing in the root `hugo.toml`.
- [ ] If needed, add basic menu entries for both languages to ensure the header is populated.

## 3. Verify Multilingual Linkage
- [ ] Check `hello-world.md` in both `content/de/posts/` and `content/en/posts/`.
- [ ] Ensure they have matching `translationKey` or the same filename (since they are in separate content dirs, Hugo usually matches them by relative path).
- [ ] In this project, `content/de/posts/hello-world.md` and `content/en/posts/hello-world.md` exist. Hugo should automatically link them.

## 4. Verification
- [ ] Run a local build (if `hugo` is available) or verify the configuration logic.
- [ ] Confirm that `showLanguageSwitcher` is the correct parameter for the installed Blowfish version.

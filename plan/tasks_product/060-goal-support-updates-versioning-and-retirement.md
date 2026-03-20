# Goal: Manage updates over time without breaking buyers

- [ ] Add `status` to content items (draft/published/archived).
- [ ] Add “last updated” metadata and show it in UI.
- [ ] Add a safe redirect strategy if slugs change (or prohibit slug changes).
- [ ] Local test: archive an item and ensure it disappears from catalog but does not error if visited directly (show 404 or archived message).
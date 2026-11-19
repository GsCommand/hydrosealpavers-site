# AGENTS.md — HydroSeal Pavers Site

This repo is a static marketing site (HTML/CSS/JS) deployed to production. Your job is to **audit first**, then propose a **minimal, low-risk fix plan**. Don’t “redesign” unless explicitly asked.

## Operating Rules
- **Default mode: READ-ONLY.** Do not change files unless the task explicitly asks for edits.
- If changes are requested later: **small diffs, no rewrites**, and keep existing layout + content structure unless broken.
- Prefer **mobile-first correctness** over desktop flourishes.
- Avoid adding new dependencies or build tooling.

- Avoid selecting `/assets/hero/Jacksonville-paver-sealing-pool-deck.webp` for new or updated pages. Use another project photo.

## Primary Goals (in order)
1) **Mobile reliability** (touch interactions must work consistently)
2) **Visual stability** (no jumps, pops, unexpected zoom/hover behavior on phones)
3) **Performance** (Core Web Vitals basics: LCP/CLS/INP)
4) **Accessibility** (keyboard + screen reader sanity)
5) **Maintainability** (reduce duplicate/conflicting JS/CSS)

## What To Review Deeply
### A) Navigation + Includes
- Header/footer are injected via `data-include` placeholders.
- Verify nav init runs **after** includes injection.
- Look for missing/incorrect lifecycle events (e.g., an `includes:ready` listener with no dispatcher).
- Ensure hamburger, overlay close, scroll lock, and dropdown toggles all work on **iOS Safari + Android Chrome**.
- Detect duplicate nav scripts (e.g., `nav.js` vs `nav-dropdowns.js`) and conflicting event handling (`click` vs `pointerdown`).

### B) “Images pop up odd” / Touch behavior
- Audit hover/focus effects applied to `.card`, images, buttons.
- On touch devices, hover simulation can cause “jump/zoom”. Restrict hover transforms to:
  - `@media (hover:hover) and (pointer:fine)`
- Ensure tap targets don’t move when tapped.

### C) Layout / Overflow / Z-Index
- Hunt global overrides like `overflow: visible !important` applied broadly.
- Identify horizontal scroll causes at 320/375/390/414 widths.
- Validate dropdown overlays and fixed elements don’t block taps.
- Confirm z-index ordering: header, nav panel, overlay, any fixed callbar.

### D) Image System
- Ensure consistent sizing rules:
  - Thumbnails: fixed height + `object-fit: cover`
  - Hero: predictable height and no CLS
- Prefer adding `width`/`height` attributes to reduce layout shift.
- Verify lazy-loading is correct (don’t lazy-load above-the-fold hero imagery).
- Flag oversized image assets and recommend compression/format changes.

### E) JS Quality / Safety
- Look for:
  - syntax errors that stop execution
  - scripts not using `defer`
  - code running before DOM exists
  - event listeners binding multiple times
- Prefer idempotent init functions guarded by data attributes or flags.

### F) CSS Quality / Consistency
- Identify duplicate selectors and conflicting rules.
- Confirm breakpoints are consistent (e.g., 980px/900px/860px).
- Keep transitions reasonable; respect `prefers-reduced-motion`.

### G) Accessibility
- Nav:
  - `aria-controls` matches the menu id
  - `aria-expanded` toggles correctly
  - Esc closes menu/dropdowns
- Focus states visible, no keyboard traps.

## Required Output Format (for any audit)
Provide:
1) **Top 10 issues** ranked as P0 / P1 / P2  
   - P0 = broken / revenue-impacting / mobile blockers  
   - P1 = major UX polish / widespread annoyance  
   - P2 = nice-to-have cleanup
2) For each issue:
   - **Where:** file path(s) and selector/function names
   - **Why:** root cause explanation
   - **Fix:** minimal change recommendation (no rewrites)
3) A **safe execution order** (what to fix first to avoid regressions)

## Change Policy (only when asked to implement)
- Keep diffs small and localized.
- Don’t remove features—only fix bugs and conflicts.
- Don’t introduce new libraries.
- If you remove a file/script, ensure references are removed everywhere.
- After changes, verify:
  - hamburger opens/closes
  - dropdown parents toggle on touch
  - no horizontal scroll on mobile
  - no “card pop/jump” on tap
  - no console errors

## Environments to consider
- iPhone Safari (touch + hover emulation quirks)
- Android Chrome
- Desktop Chrome/Safari

## Definition of “Done” (for fixes)
- Mobile nav works on touch consistently across pages.
- No unexpected image/card “pop” behavior on tap.
- No obvious layout shift above the fold.
- No console errors in production pages.

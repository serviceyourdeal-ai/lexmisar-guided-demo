# LEXMISAR — Controlled LINE Test / PREPARATION ONLY

Status: **NOT APPROVED TO APPLY**. This branch is a preparation workspace. Nothing in this change calls LINE APIs, uses secrets, links users, creates Rich Menus, sets a default, or deploys assets.

## Scope and gates

1. Offline Rich Menu validator (previous PASS) remains the technical input. Note that coordinate checks do **not** prove visual hit-zone alignment or real tap behavior.
2. Access scope: **one confirmed personal LINE user ID only**. No batch operations, broadcast, default Rich Menu, or OA configuration changes.
3. Required future GitHub Environment name: `lexmisar-line-controlled-test`. Configure protection / required reviewers **before** adding production credentials. A reviewer must be independent of the person requesting the run; repository/environment restrictions may differ for public repositories and plan.
4. **Never put real secrets in the repository**, issue or reissue tokens from this code, print IDs or tokens in Action logs, or expose them in artifacts.
5. If/when explicitly approved in a later phase, store a short-lived/least-privilege token where feasible via GitHub Environment Secrets. Required future secret names: `LINE_CHANNEL_ACCESS_TOKEN`, `LINE_TEST_USER_ID`. These are **not configured by this work**.
6. The current live OA and existing default Rich Menu must be inventoried BEFORE any real changes. Keep any existing linked menu mapping for the tester for restoration. If an existing per-user menu cannot be identified or restored safely, STOP; do not proceed with controlled test.
7. No real apply workflow is provided in this phase. Building an apply workflow, configuring secrets, or running it requires **new explicit approval**.

## Future installation outline — for review, NOT a command to run

- Read-only inventory: verify Channel ID, user identity, existing Rich Menus, default state, current per-user linked menu, existing aliases.
- Validate final images/JSON and all LINE request schema limits.
- Reserve unique menu names/aliases for a temporary test, fail on conflict; avoid replacing any alias.
- Create test menus A/B and upload their images. Record only newly-created resource IDs in a protected, private state record; avoid printing user IDs or tokens.
- Create A/B aliases; link A only to the approved test user.
- Test 13 hotspot interactions, manual-message buttons, and A/B switch on that account.
- Provide an explicit fail-safe cleanup plan. No default operation exists in the planned allowlist.

## Rollback design

Rollback must be **per-user and ownership-scoped**:
1. Stop any pending controlled-test runs.
2. Restore the user's pre-test Rich Menu link **if an existing link was recorded**. If there was no pre-test per-user link, unlink the temporary Rich Menu. Do not remove the default OA menu.
3. Delete only aliases and Rich Menus whose IDs were created by this specific test, after checking resource ownership and no other users linked.
4. If resources are partially created or state is unknown, stop automatic cleanup and review manually. Never delete unknown/pre-existing IDs.
5. Confirm tester view, default state, and other users unaffected. Keep a redacted audit summary.

## Gates still pending

- [ ] Reviewed account governance (personal/business-owned GitHub repo, company device policy)
- [ ] Independent review of A/B interactive labels, actual touch alignment, and messaging UX
- [ ] LINE schema and API behavior review
- [ ] Protected GitHub Environment, permissions and secret rotation policy
- [ ] Prior-state inventory and restoration plan
- [ ] Separate approval to add a *disabled-by-default* real apply workflow
- [ ] Separate approval to call API for the single selected user

**Do not Merge branch; do not call LINE API; do not deploy.**

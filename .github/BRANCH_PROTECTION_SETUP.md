# Branch Protection & Trunk-Based Development Setup

This document describes the **one-time manual settings** to configure in the
`Python-Financial-Analyst/pyfian` GitHub repository after the initial push.
These settings enforce a trunk-based development workflow where `main` is the
only long-lived branch and all changes flow through short-lived PRs.

---

## 1. Branch Ruleset for `main`

> **Settings → Rules → Rulesets → New ruleset → New branch ruleset**

| Setting | Value |
|---|---|
| Ruleset name | `protect-main` |
| Enforcement status | Active |
| Target branches | `main` |

### Rules to enable

- [x] **Restrict deletions** — nobody can delete the `main` branch
- [x] **Require linear history** — enforces squash or rebase merges (no merge commits); keeps `git log` clean for trunk-based dev
- [x] **Require a pull request before merging**
  - Required approvals: **1**
  - Dismiss stale pull request approvals when new commits are pushed: ✅
  - Require review from Code Owners: ✅ (uses `.github/CODEOWNERS`)
- [x] **Require status checks to pass**
  - Require branches to be up to date before merging: ✅
  - Add the following required checks:
    - `lint` (from `CI` workflow)
    - `Test (Python 3.11)` (from `CI` workflow)
    - `Test (Python 3.12)` (from `CI` workflow)
    - `Test (Python 3.13)` (from `CI` workflow)
    - `Doctests` (from `CI` workflow)
    - `Build Sphinx docs` (from `CI` workflow)
- [x] **Block force pushes**

---

## 2. General Repository Settings

> **Settings → General**

| Setting | Value |
|---|---|
| Default branch | `main` |
| Allow merge commits | ❌ Disable |
| Allow squash merging | ✅ Enable — default commit message: **PR title and description** |
| Allow rebase merging | ✅ Enable (for advanced users) |
| Automatically delete head branches | ✅ Enable |

---

## 3. GitHub Pages

> **Settings → Pages → Build and deployment**

| Setting | Value |
|---|---|
| Source | **GitHub Actions** (not a branch) |

The `deploy-docs.yml` workflow handles building and publishing automatically
on every push to `main`.

---

## 4. PyPI Trusted Publishing (OIDC)

This enables the `release.yml` workflow to publish to PyPI **without storing
API tokens as secrets**.

### On PyPI (pypi.org)

1. Log in → Your account → **Publishing**
2. Add a **new pending publisher**:

   | Field | Value |
   |---|---|
   | PyPI project name | `pyfian` |
   | Owner | `Python-Financial-Analyst` |
   | Repository name | `pyfian` |
   | Workflow filename | `release.yml` |
   | Environment name | `pypi` |

### On GitHub

> **Settings → Environments → New environment**

Create an environment named **`pypi`** with:
- Protection rule: **Required reviewers** → add `@pabloorazi`

---

## 5. Dependabot Alerts & Security

> **Settings → Security → Code security**

Enable:
- [x] Dependabot alerts
- [x] Dependabot security updates
- [x] Dependabot version updates (already configured in `.github/dependabot.yml`)

---

## 6. Trunk-Based Development Workflow Summary

```
         short-lived feature branch
               ┌─────────────────┐
main ──────────┤  feat/my-change  ├──── squash-merge ──── main
               └─────────────────┘
                    ↑ PR + required
                      status checks
```

1. Cut a branch: `git switch -c feat/short-description`
2. Make small, focused commits (conventional commit format enforced by pre-commit)
3. Open a PR against `main` — CI runs automatically
4. After approval + all checks green → **squash merge** into `main`
5. Branch is auto-deleted
6. To release: `poetry run bumpver update --patch` → push the tag → `release.yml` fires

# Publishing `kb` on Homebrew

To distribute `kb` via Homebrew (`brew install kb`):

## 1. Create a Tap Repository
Create a GitHub repository named `homebrew-kb-cli` under your GitHub account (`hrithikchauhan/homebrew-kb-cli`).

## 2. Add the Formula
Copy `Formula/kb.rb` into the repository under `Formula/kb.rb`.

## 3. Update Release Tag & SHA-256
When creating a release tag (e.g. `v0.1.0`), compute the SHA-256 checksum of the release tarball:

```bash
curl -sL https://github.com/hrithikchauhan/kb-cli/archive/refs/tags/v0.1.0.tar.gz | shasum -a 256
```

Update `url` and `sha256` in `Formula/kb.rb`.

## 4. User Installation
Users can install `kb` via Homebrew tap:

```bash
brew tap hrithikchauhan/kb-cli
brew install kb
```

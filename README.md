# Vexium Core

The local model **Kryvex** runs when you switch the assistant on. This repository
hosts the weights, their checksums and the licence — not code, and no weights in
git. The `.gguf` files live as release assets so an installed Kryvex can fetch
the one it needs, instead of every installer carrying ~2 GB.

| Release | Product | Artifact | Size |
| --- | --- | --- | --- |
| [v2](https://github.com/XiONDiGiTaL/Vexium-Core/releases/tag/v2) (default) | Vexium Core 3B | `vexium-core-3b-q4_k_m.gguf` | 2,104,932,768 B (1.96 GiB) |
| [v1](https://github.com/XiONDiGiTaL/Vexium-Core/releases/tag/v1) | Vexium Core Light | `vexium-core-1.5b-q4_k_m.gguf` | 1,117,320,736 B (1.04 GiB) |

`manifest.json` carries both artifacts with their byte counts, hashes and base
revisions; `SHA256SUMS.txt` covers both files.

## Vexium Core 3B — the default

| Field | Value |
| --- | --- |
| Product | Vexium Core 3B (`vexium-core-3b`) |
| Artifact | `vexium-core-3b-q4_k_m.gguf` |
| Bytes | 2,104,932,768 (1.96 GiB) |
| SHA-256 | `626b4a6678b86442240e33df819e00132d3ba7dddfe1cdc4fbb18e0a9615c62d` |
| Quantisation | Q4_K_M |
| Architecture | `qwen2` |
| Context | 32,768 native, 4,096 used by Kryvex |
| Licence | Apache-2.0 ([LICENSE](LICENSE)) |
| Download | `https://github.com/XiONDiGiTaL/Vexium-Core/releases/download/v2/vexium-core-3b-q4_k_m.gguf` |

An unmodified `qwen2.5-3b-instruct-q4_k_m.gguf` from
[`Qwen/Qwen2.5-3B-Instruct-GGUF`](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF),
revision `7dabda4d13d513e3e842b20f0d435c732f172cbe`, renamed for packaging.

3B is the ceiling for this hosting arrangement: GitHub caps a release asset at
2 GiB, so a 7B or 8B cannot be published here without a second host.

## Vexium Core Light 1.5B

| Field | Value |
| --- | --- |
| Product | Vexium Core Light (`vexium-core-1.5b`) |
| Artifact | `vexium-core-1.5b-q4_k_m.gguf` |
| Bytes | 1,117,320,736 (1.04 GiB) |
| SHA-256 | `6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e` |
| Quantisation | Q4_K_M |
| Base revision | `91cad51170dc346986eccefdc2dd33a9da36ead9` |

Kept for machines already running it: the model id is the filename, so an
existing install keeps its verified file and never re-downloads on upgrade. It
is slower than the 3B in every quality measurement in Kryvex's
`docs/VEXIUM_MODELS.md` §15, which is why it is no longer the default.

## Provenance and notices

- Base models: **Qwen2.5-3B-Instruct** and **Qwen2.5-1.5B-Instruct**, © Alibaba
  Cloud, Apache-2.0.
- Quantisation: published by Qwen; this repository does not re-quantise.
- Packaging: XiONDiGiTaL renames the unmodified files and republishes them. No
  weights were retrained, merged or altered; no behaviour is claimed beyond the
  base models'.
- **Not affiliated with or endorsed by Alibaba Cloud.** "Vexium Core" is Kryvex's
  product name for its local model stack, not a new model.

If you redistribute an artifact, keep this notice, the `LICENSE` and its SHA-256.

## How Kryvex uses it

1. The Vexium page offers **Install Vexium Core 3B** (and **Switch to** it when
   Light is already running).
2. Kryvex downloads the release asset over HTTPS from this repository, hashes it
   while streaming, and only accepts the exact byte count and SHA-256 that the
   installed app already knows. A host outside `github.com` and
   `objects.githubusercontent.com` is refused.
3. The verified file is written to `%APPDATA%\Kryvex\models\` and served by the
   bundled `llama-server` on loopback (`127.0.0.1`). Nothing is uploaded, and no
   request leaves the machine during a conversation.

Kryvex pins the release URL, byte count and hash in its own catalogue, so this
repository cannot change what an installed app will accept.

## Verification

```bash
gh release download v2 --repo XiONDiGiTaL/Vexium-Core --pattern 'vexium-core-3b-q4_k_m.gguf'
sha256sum -c SHA256SUMS-3b.txt
```

## Known limits

A 3B model is still a small model. Kryvex gives it a system prompt and
deterministic tools (arithmetic, units, distance, dates) so it stops guessing at
those, and offers an opt-in web search for facts it cannot know. It is not a
reasoning model and should not be trusted for current facts, legal or medical
advice.

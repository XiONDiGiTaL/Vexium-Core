# Vexium Core

The local model **Kryvex** runs when you switch the assistant on. This repository
hosts the weights, their checksums and the licence — not code. Kryvex itself
contains the `llama.cpp` runtime, the download policy and the chat surface; this
repository exists so the ~1 GB artifact can be fetched on demand instead of
inflating every Kryvex installer.

## What is in the release

| Field | Value |
| --- | --- |
| Product name | Vexium Core 1.5B |
| Artifact | `vexium-core-1.5b-q4_k_m.gguf` |
| Bytes | 1,117,320,736 (1.04 GiB) |
| SHA-256 | `6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e` |
| Quantisation | Q4_K_M |
| Architecture | `qwen2` |
| Context | 32,768 native, 4,096 used by Kryvex |
| Licence | Apache-2.0 ([LICENSE](LICENSE)) |
| Commercial use | Permitted, with the notices below |

The file is the published `qwen2.5-1.5b-instruct-q4_k_m.gguf` artifact from
[`Qwen/Qwen2.5-1.5B-Instruct-GGUF`](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF),
revision `91cad51170dc346986eccefdc2dd33a9da36ead9`, byte for byte. Packaged here
under the product name Kryvex uses, with the Qwen provenance kept intact.

## Provenance and notices

- Base model: **Qwen2.5-1.5B-Instruct**, © Alibaba Cloud, Apache-2.0.
- Quantisation: published by Qwen in the repository above (`Q4_K_M`).
- Packaging: XiONDiGiTaL redistributes the unmodified file as
  `vexium-core-1.5b-q4_k_m.gguf`. No weights were retrained, merged or altered;
  no behaviour is claimed beyond the base model's.
- **Not affiliated with or endorsed by Alibaba Cloud.** "Vexium Core" is
  Kryvex's product name for the local stack, not a new model.

If you redistribute this artifact, keep this notice, the `LICENSE` and the
SHA-256 above.

## How Kryvex uses it

1. The Vexium page offers **Install Vexium Core**.
2. Kryvex downloads the release asset over HTTPS from this repository, hashes it
   while streaming, and only accepts the exact byte count and SHA-256 above.
3. The verified file is written to `%APPDATA%\Kryvex\models\` and served by the
   bundled `llama-server` on loopback (`127.0.0.1`). Nothing is uploaded, and no
   request leaves the machine during a conversation.

Kryvex's downloader pins the exact release URL and hash in its own catalogue;
this repository cannot change what an installed app will accept.

## Verification

```bash
gh release download v1 --repo XiONDiGiTaL/Vexium-Core --pattern 'vexium-core-1.5b-q4_k_m.gguf'
sha256sum -c SHA256SUMS.txt
```

## Known limits

A 1.5B model is a small model. Kryvex gives it a system prompt and deterministic
tools (arithmetic, units, distance, dates) so it stops guessing at those, and
offers an opt-in web search for facts it cannot know. It is not a reasoning
model and should not be trusted for current facts, legal or medical advice.

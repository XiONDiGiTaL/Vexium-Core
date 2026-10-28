# Vexium Core Enhanced: knowledge prototype

This is executable development code, not new model weights, a trained adapter or an installed Kryvex feature. Existing production manifests and model releases are untouched.

## Run

Python 3.9+, standard library only. From this directory:

```sh
python -m unittest -v test_enhanced
python enhanced.py --language tr --query "GPU hızlandırma"
python enhanced.py --query "How do I install a custom GGUF model?"
```

The command prints OpenAI-style messages and source metadata. It does not contact a server, execute tools, read conversations or download anything. A later main-process integration must validate these messages and preserve Kryvex's existing trust boundaries; do not pass a renderer-supplied system message through to the model.

## Implemented

- Explicit Vexium/XiØN identity with upstream attribution distinguished.
- Six English/Turkish reference entries covering installation, custom GGUF, acceleration, browser-search handoff, assistant privacy and workspace tools.
- Source file blob SHA and review date on each returned passage.
- Deterministic keyword retrieval, bounded passage budget and top-k limit.
- Query remains a user message and cannot declare available tools.
- Twelve unit tests. These test application logic, not model intelligence or prompt-injection immunity.

## Limitations and next work

Turkish translations are drafts, not validated fluency. English/Turkish are the only context languages in this prototype; existing production language support is not changed. Token matching is not semantic retrieval and does not handle arbitrary Turkish inflections. Sources are reviewed snapshots, not live state; refresh them when app behavior changes. The source SHA identifies a Git blob, not a pinned repository commit. The module does not fetch or re-verify upstream files at runtime.

Creator identity and research handoff already exist in Kryvex; this work does not claim to invent or replace them. Search handoff is not model-operated browsing. Prompt rules are instructions, not a security boundary.

Next: extend verified product coverage, review translations, add held-out support evaluations, select the strongest practical GPU-backed base, wire context through the existing main-process boundary, and develop a separate licensed training recipe if evaluation supports fine-tuning. No paid training job or hosting action is included.

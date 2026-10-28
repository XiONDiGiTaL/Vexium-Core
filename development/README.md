# Vexium in-house development

Status: development scaffolding, not a trained model or a production release. Existing release assets, manifest.json and default model are unchanged.

## Proposed editions

- Light: retain the existing low-memory fallback.
- Enhanced: select a stronger multilingual base after local evaluation.
- Pro: optional larger base for machines with more available memory.
- Reasoning: optional specialist; must also pass the normal assistant tests.

Edition names are targets, not downloadable artifacts. No base, checksum, hardware requirement or performance improvement is asserted for unreleased editions.

## What belongs to Vexium

This directory starts a maintained Kryvex-specific prompt and evaluation suite. Prompt customization does not change model weights. A future fine-tuned release must record its upstream base revision, training recipe, licensed data provenance, adapter or merged-weight checksums, quantization recipe and comparative evaluation. Never describe repackaged upstream weights as trained in-house.

## Turkish

Turkish is a required evaluation language alongside English, Spanish, German and French. The prompt requests Turkish for Turkish input and preserves Turkish spelling. This is not proof that a base model is fluent. Do not merely add tr to a production capability list: require human-reviewed Turkish results first. Keep training examples separate from held-out evaluation cases.

Changing app facts should be supplied as maintained, user-authorized context rather than memorized through training. UI translation files do not automatically become model knowledge.

## Run an evaluation

Requires Python 3.9 or newer and an already running local OpenAI-compatible model server. No third-party Python packages are required.

```sh
python development/evaluate.py --base-url http://127.0.0.1:8080/v1 --model local-model --label baseline --output baseline.json
```

Use the actual server port and model identifier; the example does not start a server or download weights. Use a different output path for each candidate. Never commit reports containing private server errors or sensitive responses without reviewing them.

The runner accepts literal loopback addresses only and refuses redirects. It sends only the bundled prompt and fixed synthetic evaluation cases. It does not access Kryvex history, user files, app tools or cloud providers.

Machine checks cover simple extraction, arithmetic, Turkish character preservation and unsupported app claims. Language quality and app-help usefulness require human review; a correct JSON format is not evidence of fluency. Recorded latency is request wall time, not tokens per second, memory use or a hardware-independent benchmark. Errors fail the run and are never counted as passes.

## Release gates

1. Compare each candidate with the existing 3B model under documented, comparable runtime, context and hardware settings. Expand this smoke suite before making quality claims.
2. Review Turkish fluency, dotted and dotless I, mixed-language instructions, refusal quality and application terminology with a proficient Turkish reviewer.
3. Verify the exact downloadable artifact, licence, revision, byte count, SHA-256 and runtime compatibility. No placeholder integrity values.
4. Measure load time, request latency and peak resident memory on target machines.
5. Add approved model entries and compatible download handling in Kryvex separately. Nothing in this directory is automatically loaded by the app.
6. Train adapters only on permissioned, licence-compatible data; never silently collect conversations. Evaluate against the untuned base before publishing.

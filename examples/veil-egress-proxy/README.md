# Mask before sending, restore after

Send text to a LibraOS agent or any OpenAI-compatible model without handing it your customers' names, card numbers or
API keys. Direct identifiers are replaced on your machine before the request leaves, and put back in the answer.

```
                  your machine                          │   outside
                                                        │
 your app ─ "Margaret Holloway, 4111 1111 1111 1111" ─► service ─ "[PERSON_1], [ACCOUNT_1]" ─► model
 your app ◄ "Dear Margaret Holloway, ..."            ── service ◄ "Dear [PERSON_1], ..."    ── model
                                                        │
                        the detector and the mapping stay here
```

Detection uses the open weights of [`libraos/veil-detect`](https://huggingface.co/libraos/veil-detect) (Apache-2.0,
about 1 GB, downloaded on first use; a CPU is enough) plus the patterns in `veil_mask.py`, for values with a fixed shape.

| File | What it is |
|---|---|
| `veil_mask.py` | `Detector`, `mask()`, `restore()`: use these directly in your own code |
| `service.py` | A small HTTP service around them, with `libraos`, `openai` and `echo` backends |
| `demo.py` | The round trip against a running service |
| `test_egress.py` | Tests. No model download and no API key |

## Run it

```bash
pip install torch transformers libraos-sdk

python service.py --backend echo     # no key: prints what would leave, and quotes it back
python demo.py
```

```
2. What leaves the machine (6 values masked):

Customer ticket: [PERSON_1] (DOB [DOB_1]) of [COMPANY_1] wrote from [EMAIL_1], phone [PHONE_1]. Her card is
[ACCOUNT_1]. She asks for a refund of $1,240 by 1 March 2027.
```

Ordinary dates, amounts and cities stay as written on purpose: a model needs them to reason.

To use a real model:

```bash
# a LibraOS agent, through libraos-sdk
export LIBRA_OS_URL=https://libraos.your-company.example
export LIBRA_OS_API_KEY=msk_live_...
export LIBRA_OS_AGENT_ID=default
python service.py --backend libraos

# any OpenAI-compatible endpoint; the key, if it needs one, is OPENAI_API_KEY
python service.py --backend openai --base-url https://api.example.com/v1
```

```bash
curl -s http://127.0.0.1:8931/v1/ask -d '{
  "model": "your-model",
  "messages": [{"role": "user", "content": "Write one line to anna.berg@example.org about her refund."}]
}'
```

To see what a request would send, without sending it, post it to `/v1/preview`.

## In your own code

The round trip is three calls around the SDK:

```python
from libraos import Client
from veil_mask import Detector, Mapping, mask, restore

detect = Detector()
mapping = Mapping()  # one per conversation, so one person keeps one placeholder across turns

masked = mask("Write to Anna Berg, anna.berg@example.org, about her refund.", detect, mapping)

async with Client(base_url=url, api_key=key) as c:
    msg = await c.messages.create("default", messages=[{"role": "user", "content": masked}], max_tokens=2000)

text, unresolved = restore(msg.text, mapping)
if unresolved:  # the model made up or garbled a placeholder, so do not show this answer as it is
    raise ValueError(unresolved)
```

Keep the mapping on your side and out of your logs. It holds the originals, so it is as sensitive as the text.

## How it fails

| Situation | What happens | Status |
|---|---|---|
| Masking fails | nothing is sent | 503 `masking_failed` |
| `stream`, `tools`, `metadata`, images, `tool` messages, any other field | refused, nothing is sent: it has not been masked | 400 |
| The model uses a placeholder the mapping does not cover | the answer is not returned | 502 `unresolved_placeholder` |
| The model returns an error | its text is dropped: it can quote the request | 502 `model_error` |
| The model returns no text | reported, not returned as empty | 502 `empty_answer` |

## What this does not do

- **It lowers the risk; it does not remove it.** The detector misses things: 3–5% of mentions on three blind samples of
  US court opinions, per the [model card](https://huggingface.co/libraos/veil-detect). Do not send anything you could
  not accept leaking.
- **Secrets without a known shape rely on the model.** Patterns catch common vendor token prefixes, JWTs, PEM keys, URLs
  with passwords and labelled passwords. A bare random string with no label has no pattern behind it.
- **Names inside other text can stay.** In `/home/[CONTACT_1]/acme-billing/app.py` the project name still leaves.
- **It can mask too much.** The model can tag a city with the street next to it, or a public court as an organization.
  Everything it masks comes back in the answer, but the outside model reasons without it.
- **A surname comes back as the full name.** "Ms. Raman" and "Priya Raman" share a placeholder so the model knows they
  are one person, so an answer's "Ms. [PERSON_1]" restores as "Ms. Priya Raman".
- **This is pseudonymization, not anonymization.** What remains in the text (a job title, an unusual event) can still
  identify someone.
- **Masked code reads differently.** A model may take `host="[CONTACT_1]"` for an unfilled template, and answer about
  that instead of your question.
- **Set `max_tokens` generously.** Reasoning models can spend a small budget thinking and return an empty answer.
- **This is an example.** It has no authentication, so keep it on localhost, and it does not stream or carry tool calls.

## Tests

```bash
pip install pytest libraos-sdk
pytest test_egress.py
```

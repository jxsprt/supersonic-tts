# supersonic-tts

**Stdin-friendly CLI + Python API wrapper for [Supertonic](https://github.com/supertone-inc/supertonic)** — lightning-fast, on-device, multilingual TTS via ONNX Runtime.

No cloud API. No data leaves your machine. 31 languages. 10 voices.

## Why supersonic-tts?

Supertonic's official CLI takes text as a positional argument — awkward for piped input, shell scripts, and AI agents. `supersonic-tts` wraps it with:

- **Stdin support** — pipe text directly: `echo "hello" | supersonic-tts -o out.wav`
- **Hermes Agent integration** — drop-in command-based TTS provider
- **Same engine** — uses supertonic under the hood (supertonic-3, ONNX)

## Install

```bash
pip install supersonic-tts
```

First run auto-downloads the model (~305MB) from HuggingFace.

## Usage

### CLI

```bash
# Read from argument
supersonic-tts "Hello world" -o output.wav

# Read from stdin (piped)
echo "Hello from stdin" | supersonic-tts -o output.wav

# Read from file
cat long_text.txt | supersonic-tts -o output.wav

# Choose voice
supersonic-tts "Crisp and confident" -o output.wav --voice F4

# Multilingual
supersonic-tts "Bonjour le monde" -o french.wav --lang fr --voice F1

# Adjust speed
supersonic-tts "Fast talk" -o fast.wav --speed 1.5

# Higher quality
supersonic-tts "Premium quality" -o premium.wav --steps 10
```

### Python API

```python
from supersonic_tts import SupersonicTTS

tts = SupersonicTTS()
wav, duration = tts.synthesize("Hello world", voice="F4", lang="en")
tts.save("output.wav")
```

### Hermes Agent Integration

Add to `~/.hermes/config.yaml`:

```yaml
tts:
  provider: supersonic-tts
  supersonic-tts:
    type: command
    command: supersonic-tts -o {output_path} --voice {voice} < {input_path}
    voice: F4
    model: supertonic-3
    output_format: wav
    voice_compatible: true
    timeout: 60
```

## Voices

| Voice | Style |
|-------|-------|
| M1 | Lively, upbeat male |
| M2 | Deep, calm male |
| M3 | Authoritative male |
| M4 | Soft, friendly male |
| M5 | Warm, storytelling male |
| F1 | Calm, composed female |
| F2 | Bright, cheerful female |
| F3 | Professional announcer female |
| **F4** | **Crisp, confident female** |
| F5 | Gentle, soothing female |

## Languages

31 languages (supertonic-3): en, ko, ja, ar, bg, cs, da, de, el, es, et, fi, fr, hi, hr, hu, id, it, lt, lv, nl, pl, pt, ro, ru, sk, sl, sv, tr, uk, vi, na (fallback)

## License

MIT (code) — supertonic model uses OpenRAIL-M

"""Core Python API for SupersonicTTS."""

from __future__ import annotations

import time
from typing import Optional, Tuple

import numpy as np

try:
    from supertonic import TTS as _TTS
except ImportError:
    _TTS = None

__version__ = "0.1.0"

# Available voice styles
VOICES = {
    "M1": "Lively, upbeat male",
    "M2": "Deep, calm male",
    "M3": "Authoritative male",
    "M4": "Soft, friendly male",
    "M5": "Warm, storytelling male",
    "F1": "Calm, composed female",
    "F2": "Bright, cheerful female",
    "F3": "Professional announcer female",
    "F4": "Crisp, confident female",
    "F5": "Gentle, soothing female",
}

# Available languages
LANGUAGES = [
    "en", "ko", "ja", "ar", "bg", "cs", "da", "de", "el", "es",
    "et", "fi", "fr", "hi", "hr", "hu", "id", "it", "lt", "lv",
    "nl", "pl", "pt", "ro", "ru", "sk", "sl", "sv", "tr", "uk",
    "vi", "na",
]


class SupersonicTTS:
    """High-level Python wrapper for Supertonic TTS.

    Usage:
        tts = SupersonicTTS()
        wav, duration = tts.synthesize("Hello world", voice="F4", lang="en")
        tts.save(wav, "output.wav")
    """

    def __init__(self, auto_download: bool = True, verbose: bool = False):
        if _TTS is None:
            raise ImportError(
                "supertonic is not installed. Run: pip install supertonic"
            )
        self._tts = _TTS(auto_download=auto_download)
        self._verbose = verbose

    def synthesize(
        self,
        text: str,
        voice: str = "M1",
        lang: str = "en",
        steps: int = 5,
        speed: float = 1.05,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Synthesize speech from text.

        Args:
            text: Text to synthesize.
            voice: Voice style name (M1-M5, F1-F5). Default: M1.
            lang: Language code. Default: en.
            steps: Synthesis quality steps. Default: 5.
            speed: Speech speed multiplier (0.7-2.0). Default: 1.05.

        Returns:
            Tuple of (waveform, duration) where waveform has shape (1, n_samples).
        """
        style = self._tts.get_voice_style(voice_name=voice)

        t0 = time.time()
        wav, duration = self._tts.synthesize(
            text,
            voice_style=style,
            lang=lang,
            total_steps=steps,
            speed=speed,
        )
        elapsed = time.time() - t0

        if self._verbose:
            print(
                f"Generated {float(duration[0]):.2f}s of audio "
                f"in {elapsed:.2f}s (voice={voice})",
                file=__import__("sys").stderr,
            )

        return wav, duration

    def save(self, waveform: np.ndarray, path: str) -> None:
        """Save waveform to a WAV file.

        Args:
            waveform: Audio array from synthesize().
            path: Output file path (should end in .wav).
        """
        self._tts.save_audio(waveform, path)

    @staticmethod
    def list_voices() -> dict:
        """Return dict of {voice_name: description}."""
        return dict(VOICES)

    @staticmethod
    def list_languages() -> list:
        """Return list of supported language codes."""
        return list(LANGUAGES)

    def __repr__(self) -> str:
        return f"SupersonicTTS(voices={len(VOICES)}, languages={len(LANGUAGES)})"

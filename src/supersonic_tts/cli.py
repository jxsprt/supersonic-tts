#!/usr/bin/env python3
"""CLI entry point for supersonic-tts.

Reads text from:
  1. First positional argument
  2. Stdin (piped text)
  3. A file via --input

Usage:
  supersonic-tts "Hello world" -o out.wav
  echo "Hello" | supersonic-tts -o out.wav
  cat file.txt | supersonic-tts -o out.wav --voice F4
  supersonic-tts -o out.wav --input input.txt
"""

from __future__ import annotations

import argparse
import sys
from typing import Optional

from .core import SupersonicTTS


def resolve_text(
    args_text: Optional[str],
    args_input: Optional[str],
) -> Optional[str]:
    """Resolve input text from argument, file, or stdin. Returns None if empty."""
    # 1. From --input file
    if args_input:
        with open(args_input, "r", encoding="utf-8") as f:
            return f.read().strip()

    # 2. From positional argument
    if args_text:
        return args_text.strip()

    # 3. From stdin (only if stdin is not a TTY — i.e. piped)
    if not sys.stdin.isatty():
        try:
            data = sys.stdin.read()
            if data.strip():
                return data.strip()
        except KeyboardInterrupt:
            return None

    return None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="supersonic-tts",
        description="Lightning-fast, on-device, multilingual TTS",
    )
    parser.add_argument(
        "text",
        nargs="?",
        default=None,
        help="Text to synthesize (omit to read from stdin or --input)",
    )
    parser.add_argument(
        "-o", "--output",
        help="Output WAV file path",
    )
    parser.add_argument(
        "--input",
        help="Read input text from a file",
    )
    parser.add_argument(
        "--voice",
        default="M1",
        choices=sorted(SupersonicTTS.list_voices().keys()),
        help="Voice style (default: M1)",
    )
    parser.add_argument(
        "--lang",
        default="en",
        help="Language code (default: en). Use --list-langs to see all.",
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=5,
        help="Synthesis quality steps (default: 5, higher = better)",
    )
    parser.add_argument(
        "--speed",
        type=float,
        default=1.05,
        help="Speech speed (0.7-2.0, default: 1.05)",
    )
    parser.add_argument(
        "--list-voices",
        action="store_true",
        help="List available voice styles and exit",
    )
    parser.add_argument(
        "--list-langs",
        action="store_true",
        help="List supported language codes and exit",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show generation timing info",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    # Handle info commands
    if args.list_voices:
        print("Available voices:")
        for name, desc in SupersonicTTS.list_voices().items():
            print(f"  {name}: {desc}")
        return

    if args.list_langs:
        print("Supported languages:")
        for code in SupersonicTTS.list_languages():
            print(f"  {code}")
        return

    # Validate -o is present for synthesis
    if not args.output:
        parser.print_help()
        print("\nERROR: --output/-o is required for synthesis", file=sys.stderr)
        sys.exit(1)

    # Resolve text
    text = resolve_text(args.text, args.input)
    if not text:
        parser.print_help()
        print("\nERROR: No input text provided. Pass text as argument, pipe to stdin, or use --input.", file=sys.stderr)
        sys.exit(1)

    # Synthesize
    tts = SupersonicTTS(verbose=args.verbose)

    try:
        wav, _duration = tts.synthesize(
            text,
            voice=args.voice,
            lang=args.lang,
            steps=args.steps,
            speed=args.speed,
        )
    except Exception as e:
        print(f"ERROR: Synthesis failed: {e}", file=sys.stderr)
        sys.exit(1)

    # Save
    try:
        tts.save(wav, args.output)
    except Exception as e:
        print(f"ERROR: Failed to save audio: {e}", file=sys.stderr)
        sys.exit(1)

    if args.verbose:
        print(f"Audio saved to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()

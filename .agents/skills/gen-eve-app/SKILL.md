---
name: gen-eve-app
description: Generate CircuitPython applications for Bridgetek EVE display controllers, especially BT817/BT818 boards such as IDM2040-7A or IDM7040 with 800x480 LCDs. Use when Codex needs to create, adapt, or debug code.py projects that initialize EVE hardware and draw text, UI screens, demos, or simple graphics.
---

# Gen EVE App

## Workflow

1. Identify the target board, EVE chip, LCD resolution, and language/runtime. Prefer CircuitPython for IDM2040-style RP2040 boards unless the user asks for C firmware.
2. Inspect the repository for existing Bridgetek examples before creating new files. Reuse local `brteve`, `EVE2`, or board helper modules when present.
3. If no project pattern exists, create a CircuitPython layout with `code.py`, optional `settings.py`, and `lib/` modules.
4. Keep hardware-specific pin mappings isolated in `settings.py` or a board config section near the top of `code.py`.
5. For BT817 800x480 output, initialize the display, clear the screen, then build a display list or coprocessor command list for the requested text or graphics.
6. Include a short run note listing which files to copy to the `CIRCUITPY` drive.

## CircuitPython Defaults

Use these defaults unless local examples or the user specify otherwise:

- Display controller: BT817 or BT818
- Resolution: 800x480
- Entry point: `code.py`
- Background for simple demos: dark, low-glare color
- Text placement: centered unless a specific position is requested
- SPI: mode 0, conservative startup baudrate

Read `references/circuitpython-bt817.md` when creating a new app from scratch or when pin/library assumptions are unclear.

## Output Rules

- Generate runnable files, not only snippets, when the user asks for an app or project.
- Avoid hardcoding unknown pins deep inside the driver; put them in one visible config location.
- Prefer Bridgetek's existing `brteve` APIs when available in the repo or on the board.
- If the repo lacks `brteve`, provide a minimal self-contained driver only for the features needed by the request.
- State unverified board assumptions clearly, especially SPI pins, reset/power-down pin, and LCD timing.

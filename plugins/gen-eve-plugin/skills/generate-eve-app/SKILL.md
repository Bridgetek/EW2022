---
name: generate-eve-app
description: Generate or modify CircuitPython demo applications for the IDM2040 board using Bridgetek EVE/BT817 display patterns from this repository.
---

# Generate EVE App

Use this skill when creating, extending, or reviewing an IDM2040 demo under `IDM2040_demo/`.

## Project Shape

- Entry point: `IDM2040_demo/code.py`.
- Main menu tags: `IDM2040_demo/main_menu/tags_all.py`.
- Board host wrapper: `IDM2040_demo/main_menu/brt_eve_rp2040_dmx.py`.
- Existing demos:
  - `cube/` for 3D bitmap transform rendering.
  - `blinka/` for animated bitmap rendering.
  - `image_viewer/` for JPEG/PNG image browsing and APDS9960 gestures.
  - `dmx512/` for DMX lighting control.
  - `audio_play/` for flash-backed raw audio playback.
  - `video2/` for EVE flash video playback.

## Board And Display Facts

- Use Python 3.11 style, but remember the target is CircuitPython.
- The display stack is `BrtEveRP2040_dmx` plus `BrtEve`.
- EVE display init normally uses `eve.init(resolution="800x480", touch="capacity")`.
- EVE SPI pins are `GP2` clock, `GP3` MOSI, `GP4` MISO, `GP5` CS, `GP7` PDN.
- SD card SPI pins are `GP10` clock, `GP11` MOSI, `GP12` MISO, `GP13` CS.
- DMX uses `GP8` TX, `GP9` RX, `GP16` polarity, and `GP27` driver enable.
- APDS9960 gesture sensor uses I2C on `GP21` SCL and `GP20` SDA.

## Demo Pattern

When adding a new demo:

1. Add a tag to `main_menu/tags_all.py`.
2. Add a menu button in `main_app.drawBtn()` in `IDM2040_demo/code.py`.
3. Add a lazy import and demo launch branch in `main_app.processEvent()`.
4. Put the implementation in `IDM2040_demo/<demo_name>/<demo_name>.py`.
5. Provide a loop with a visible `Back` button or clear gesture exit path.
6. Clear and restore the display before returning to the main menu.

Use this EVE frame pattern:

```python
eve.cmd_dlstart()
eve.VertexFormat(2)
eve.ClearColorRGB(0, 0, 0)
eve.Clear(1, 1, 1)
# draw UI here
eve.Display()
eve.cmd_swap()
eve.flush()
```

For touch buttons:

```python
eve.Tag(tag_back)
eve.cmd_button(700, 5, 85, 35, 30, 0, "Back")
tag = eve.rd32(eve.REG_TOUCH_TAG) & 0xFF
```

For sliders or rotary controls, use `cmd_track()` and read `REG_TRACKER`.

## Asset Rules

- Local assets can be loaded with `cmd_loadimage()` and `eve.load(open(..., "rb"))`.
- Flash-backed assets use hard-coded offsets and `cmd_flashread()`.
- Keep new asset paths relative to the demo folder when the app will run from the CircuitPython drive.
- If adding flash offsets, document the source asset and expected EVE flash image layout.

## Quality Bar

- Add docstrings to new functions and classes.
- Keep generated code small and close to existing style.
- Avoid CPython-only packages in target code.
- Prefer validating with `python -m py_compile` for syntax only; hardware imports will not run on desktop Python.
- Use `plugins/gen-eve-plugin/scripts/scan_eve_project.py` before larger edits.
- Use `plugins/gen-eve-plugin/scripts/validate_eve_project.py` after edits.

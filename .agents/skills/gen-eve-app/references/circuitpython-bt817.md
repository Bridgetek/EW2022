# CircuitPython BT817 Notes

Use this reference when generating a fresh CircuitPython app for an IDM2040/IDM7040-style board with a Bridgetek BT817 and 800x480 LCD.

## Preferred Project Layout

```text
code.py
settings.py
lib/
  bt817_min.py        # only if no brteve library exists
```

## Hardware Assumptions To Surface

Always make these easy to edit:

- SPI SCK, MOSI, MISO
- EVE chip select
- EVE power-down/reset
- LCD width and height
- SPI baudrate

## Minimal App Behavior

For a text demo:

1. Lock and configure SPI mode 0.
2. Reset or power-cycle the BT817 through the power-down/reset pin.
3. Send host commands to wake the controller.
4. Wait until `REG_ID` reads `0x7C`.
5. Program 800x480 LCD timing registers.
6. Enable GPIO/backlight according to the board pattern.
7. Build a display list that clears the screen and draws the requested text.
8. Swap the display list and wait for the coprocessor to finish.

## Common 800x480 Timing Starting Point

These values are common for 7-inch RGB panels, but prefer board examples or the panel datasheet when available:

- HCYCLE: 928
- HOFFSET: 88
- HSIZE: 800
- HSYNC0: 0
- HSYNC1: 48
- VCYCLE: 525
- VOFFSET: 32
- VSIZE: 480
- VSYNC0: 0
- VSYNC1: 3

## Library Choice

If `lib/brteve` or Bridgetek demo modules are present, use them first. If not, generate a minimal local driver for only the commands needed by the app.

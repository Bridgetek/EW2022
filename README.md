# IDM2040-7A-EW2022
The demo applications running on IDM2040-7A for Embedded World 2022 exibition    

![image](https://user-images.githubusercontent.com/13127756/217126707-f9b40f28-f8c2-4580-a13f-614e46b0eaf0.png)


1. The IDM2040-7A is an intelligent display module : see https://brtchip.com/product/idm2040-7a/ for more details

2. LDS SDK firmware: It is a customized circuitPython 7.1.0 run-time built with LDS driver, which shall be the base to run any circuitPython code. It is here:  
      https://github.com/Bridgetek/IDM2040-7A-EW2022/tree/main/LDS_Demo/IDM2040_LDS_SDK_Firmware  
   
   * LDS stands for Long Distance Sensors Bus from Bridgetek, see https://brtsys.com/ldsbus/
   
3. User shall program flash image ["EVE_Flash/BT81X_Flash.bin"](https://github.com/Bridgetek/IDM2040-7A-EW2022/tree/main/EVE_Flash)  into EVE's connected flash with [Eve Asset Builder (EAB)](https://brtchip.com/ic-module/toolchains/).   
4. These example projects depend on the pico-brtEve library   
   https://github.com/Bridgetek/pico-brteve/tree/main/circuitPython/lib/brteve.   
   User shall download it to the folder "lib\brtEve" of ciruitPython drive on your PC when IDM2040 is connected. 
   
5. The following applications are included in this repo: 

![image](https://user-images.githubusercontent.com/13127756/217127490-fb3c0547-5352-4143-9ff9-14cd7b867e6c.png)

## Codex usage

This repository includes local Codex configuration for generating, editing, and
validating IDM2040 EVE CircuitPython demos

### Local plugin

The Codex plugin is located at:

```text
plugins/gen-eve-plugin/
```

Its manifest is:

```text
plugins/gen-eve-plugin/.codex-plugin/plugin.json
```

The repository marketplace entry is:

```text
.agents/plugins/marketplace.json
```

After cloning this repository on another PC, install the plugin from the cloned
workspace:

1. Open the cloned repository folder in Codex.
2. Open the Codex plugin list or marketplace for this workspace.
3. Select the local marketplace named `EAB Agent`.
4. Install:

```text
EAB Agent -> Generate EVE Plugin
```

No external download is needed. The plugin files are already included in this
repository under `plugins/gen-eve-plugin/`.

The plugin provides guidance and assets for creating IDM2040 EVE demos,
including BT817 display setup, touch UI flows, media playback demos, and
supporting CircuitPython project structure.

### Local skills

Codex skills for this repository are stored under:

```text
.agents/skills/
```

The main production skill is:

```text
.agents/skills/gen-eve-app/
```

When this repository is opened as the Codex workspace, this local skill is
available from the repo. Users normally do not need a separate skill install
step. Use it when asking Codex to create, adapt, or debug CircuitPython
applications for Bridgetek EVE display controllers, especially BT817/BT818
boards such as IDM2040-7A or IDM7040 with 800x480 LCDs.

Example prompts:

```text
Use gen-eve-app to create a new IDM2040 demo that draws centered text.
Use gen-eve-app to add a touch button screen under IDM2040_demo/.
Use gen-eve-app to debug why my EVE display list is blank.
```

The plugin also includes a packaged skill at:

```text
plugins/gen-eve-plugin/skills/generate-eve-app/
```

That skill is focused on modifying demos under `IDM2040_demo/`. It documents
the existing demo layout, board pins, menu integration points, asset rules, and
the expected EVE frame drawing pattern.

### Recommended Codex workflow

1. Open this repository as the Codex workspace.
2. Optionally install the `Generate EVE Plugin` from the local plugin list.
3. Ask Codex to use `gen-eve-app` when creating or changing EVE demos.
4. Keep new demo code under `IDM2040_demo/<demo_name>/`.
5. Update `IDM2040_demo/code.py` and `IDM2040_demo/main_menu/tags_all.py` when
   adding a new menu item.
6. Validate changes before copying files to the CircuitPython drive.

### Plugin helper scripts

The plugin includes desktop-safe helper scripts. They do not import target
CircuitPython hardware modules.

Scan the demo project:

```powershell
python plugins/gen-eve-plugin/scripts/scan_eve_project.py
```

Validate common project issues:

```powershell
python plugins/gen-eve-plugin/scripts/validate_eve_project.py
```

Run repository tests before committing:

```powershell
pytest
```

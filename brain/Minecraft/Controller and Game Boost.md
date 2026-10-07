---
tags: [minecraft, controller, performance]
---

# Controller and Game Boost

Part of [[Minecraft]], set up for the [[Convergence modpack]] on 2026-09-27.

## Kayden's Xbox Controller

- **What it is:** the **Controllable** mod (MrCrayfish, 0.21.7, already in the pack) set to Bedrock's default Xbox layout for the Xbox Elite Series 2.
  - Controllable maps controller buttons to any keybind, including modded ones.
  - The **Controlling** mod adds keybind search.
- **Layout file:** `Instances\Convergence\config\controllable\bindings.properties`, with lines like `key.jump=controllable.button.a`.
  - Button names: `a, b, x, y, select, home, start, left_thumb_stick, right_thumb_stick, left_bumper, right_bumper, left_trigger, right_trigger, dpad_up/down/left/right, misc, paddle_one..paddle_four, touchpad`.
  - Modded keybinds go in `key_adapters.properties`, or are set in game.
- **Layout:**

  | Button | Action |
  |---|---|
  | A | jump |
  | B | sneak |
  | X | swap offhand (Bedrock's crafting button; crafting is in the inventory on Java) |
  | Y | inventory |
  | LB / RB | hotbar left / right |
  | LT | use |
  | RT | attack |
  | Left stick click | sprint |
  | Right stick click | pick block |
  | D-pad up | camera |
  | D-pad down | drop |
  | D-pad left | quick-action wheel (Bedrock: emotes) |
  | D-pad right | chat |
  | View | player list |
  | Menu | pause |
  | Paddle 1 | controller settings |
  | Paddle 2 | screenshot |
  | Paddle 3 | advancements |
  | Paddle 4 | free |

- **Branding:** the resource pack `resourcepacks\Kaydens Xbox Controller` renames Controllable's menus to "Kayden's Xbox Controller". It's turned on in `config\defaultoptions\options.txt`, which the Default Options mod copies on the first launch.
- **Kayden's own Bedrock binds:** couldn't be copied. Bedrock isn't installed on this PC, and it saves binds per device, not per account. Ask him for his custom binds if they differ from the defaults.
- **Rebind in game:** Options → Controller Settings → Binding.

## Game Boost

- **Scripts:** `Documents\Minecraft Tools\GameBoost.ps1` and `GameBoost-Undo.ps1`, with desktop shortcuts "Minecraft Game Boost" and "Minecraft Game Boost - Undo". Kayden runs them himself; Claude never runs them.
- **What Game Boost does:**
  - self-elevates (UAC),
  - unloads Jarvis's Ollama model to free VRAM,
  - sets the NVIDIA GPU for every CurseForge and launcher `javaw.exe` (HKCU `UserGpuPreferences`, `GpuPreference=2;`),
  - turns Game Mode on,
  - switches to the High performance power plan,
  - clears the standby RAM cache,
  - lists the apps using the most RAM.
- **What Undo does:** switches back to the Balanced power plan.
- **Pack defaults:** render distance is lowered from 16 to 12 in the pack's default options. Kayden gave the pack 11 GB of RAM in CurseForge.
- **Optional Java flags:** G1 tuning flags (Aikar-style, without AlwaysPreTouch) are on the control page, with a copy button, for CurseForge's Additional arguments.

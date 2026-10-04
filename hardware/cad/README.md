# CAD

> **Status: no CAD model exists yet.** Nothing here is manufacturable. Bracket geometry depends on donor-arm measurements (D2 pivot diameters and fasteners, D10 mounting space) that haven't been taken.

## Concept artifacts available now
| Artifact | What it shows |
|---|---|
| [J2 motor-mount concept](../../docs/img/motor-mount-concept.svg) | Dimensioned concept: donor interface (U-bolt/split collar), plate, motor slots, GT2 20T → 60T belt drive, sector pulley on J2. *Preliminary concept — dimensions to be finalized after donor inspection.* |
| [Mechanical concept](../../docs/img/mechanical-concept.svg) | Side view of the arm with J1/J2/J3, actuator locations and approximate dimensions |

| [End-effector concept](../../docs/img/end-effector-concept.svg) | Adapter plate, dovetail clamp, attachment plate with stop screws |
| [Control panel concept](../../docs/img/control-panel.svg) | Enclosure layout for joystick, buttons, E-stop, LED, jack |

## Motor-mount concept: what it is and isn't
- **Is:** a preliminary interface concept. It shows a U-bolt/split-collar clamp to the donor, a plate with slotted M3 motor holes (±5 mm belt tension), a GT2 20T→60T belt, and a sector pulley clamped to the moving link concentric with J2.
- **Isn't:** a model you can make. Plate size (≈80 × 60 × 5), centre distance (≈50–60) and clamp position are **assumptions** until measurements M2, M8 and M9 exist ([donor-measurements.md](../../docs/donor-measurements.md)).
- **Requires before CAD:** pivot cap Ø (M2.2), J2 fixed-side housing shape (M8.2), free envelope through full travel (M9.2), chosen motor's mounting pattern (after the [trade study](../../docs/actuator-trade-study.md)).

## Planned CAD (after donor measurements)
| Part | Folder | Notes |
|---|---|---|
| Donor reference model (from measurements) | `src/donor/` | Only the interfaces: pivots, spring ends, clearances |
| J2 bracket plate + sector pulley | `src/retrofit/j2/` | From the concept drawing |
| J1 bracket + base pulley | `src/retrofit/j1/` | Same pattern on the clamp body |
| Limit-switch mounts and strikers | `src/retrofit/limits/` | |
| Arca-compatible printed plate + clamp | `src/end-effector/` | |
| Control panel enclosure | `src/panel/` | Joystick, 2 buttons, E-stop, jack |

Tool: FreeCAD (parametric). Exports: STEP + STL in `exports/`. Binaries via Git LFS (see `.gitattributes`). Key parameters (pivot Ø, centre distance, pulley teeth) will live in one spreadsheet so the brackets regenerate when measurements arrive.

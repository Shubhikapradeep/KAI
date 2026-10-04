# V1 / V2 Scope Boundary

> V1 is what the funding request covers and what the design documents describe as "planned". V2 is future work and is **not** funded or designed in detail. Nothing in either column has been built.

## Boundary

| Area | **V1 (this funding request)** | **V2 (future, not funded)** |
|---|---|---|
| Mechanical base | Donor gas-spring monitor arm (provisional: NB F80) | Possibly a lighter-load donor (no ballast) |
| Actuated joints | **2: J1 base yaw, J2 spring arm** | Additional actuators: J3 head swivel, head tilt |
| Optional within V1 | J3 servo **only if** time and budget remain (not in the mandatory BOM) | — |
| Controller | ESP32-S3 | Same |
| Inputs | Joystick, ARM/MODE + SLOW buttons, 2-switch assistive jack | Rotary encoder, display/menu |
| Control mode | Jog (velocity) | **Presets**, closed-loop position, **advanced trajectory planning** (smooth multi-joint moves) |
| Sensing | Limit switches, actuator-rail sense | **Joint sensing** (angle sensors), current sensing |
| Safety system | Hardware E-stop → relay, fuse, limit switches, dead-man, stall timeout, watchdog, safe startup | Current-based stall detection, manual-override clutch |
| End effector | **Basic:** printed Arca-compatible clamp + plate, phone clamp | **Multiple end effectors** (camera mount, tablet holder, metal clamp) |
| Connectivity | Wired panel, USB-C config/logs | **Wireless/computer control** (only with its own safety design) |
| Evaluation | Bench verification of safety functions; informal feedback if possible | Structured user study |

## Rules for keeping the boundary
1. A V2 feature doesn't enter V1 docs as "planned" unless the BOM and safety analysis are updated with it.
2. Every reference to "4 actuated joints", presets, angle sensors, wireless or trajectory planning is labelled V2.
3. If V1 runs out of budget, cut in this order: J3 (already optional) → ballast hardware (if not needed) → never the safety items.

## Why this boundary
- **Budget:** the mandatory V1 BOM is ≈ ₹8,750 (≈ US$99, unverified) with no contingency ([bom.md](bom.md)).
- **Risk:** two joints are enough to demonstrate actuation working *with* a counterbalance, which is the core idea.
- **Reviewability:** a smaller system is easier to verify safely ([safety.md](safety.md)).
- **Honest cost:** without joint sensing, V1 has no presets. That is a real accessibility limitation ([accessibility.md §5](accessibility.md#5-limitations-known-now)).

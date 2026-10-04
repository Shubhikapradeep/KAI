# Design Review — KAI V1 (design stage)

> This review summarizes the current state of the design. It **draws no conclusions that depend on measurements, because none exist.** Nothing has been purchased, built or tested.
>
> Reviewer sign-off (author): ____________ Date: ____________

## 1. What is known
Established from published sources or by design decision:

| Item | Source |
|---|---|
| Preferred donor NB F80: 2–9 kg load range, tilt −30°/+85°, swivel ±90°, 260 mm vertical travel, 2.90 kg mass | Manufacturer page ([donor-selection.md](donor-selection.md)) |
| Fallback donor Green Soul 2–9 kg arm listed at ₹2,890 on 2026-10-04 | Vendor page |
| Half Life Tier 1 = US$30 / 10 h (confirmed in code); Tier 2/3 are placeholders; warm-up up to US$100 | Half Life source code and site ([bom.md](bom.md)) |
| V1 architecture: 2 actuated joints, ESP32-S3, jog control, hardware E-stop | Decisions ([decisions.md](decisions.md), [v1-v2-scope.md](v1-v2-scope.md)) |
| GT2 pulley pitch diameters (20T 12.7 mm, 60T 38.2 mm) | Standard GT2 geometry |
| Torque equations for gravity, spring, residual, dynamic and required torque | [torque-model.md](torque-model.md) |

## 2. What is estimated
| Item | Estimate | Basis |
|---|---|---|
| Donor reach | ~400 mm | Not published; inferred |
| BOM total | ₹8,750 ≈ US$99 | Planning prices, almost all PRICE TO VERIFY |
| Belt ratio | 3:1 | Concept only |
| Example τ_req | 5.5 N·m (device fitted), 9.8 N·m (device removed) | **Illustrative parameters only.** Not a design value |

## 3. What is unknown
- Residual torque vs angle at J2, and friction at all joints
- Whether a ~0.5 kg payload balances without ballast. Every candidate's minimum rated load is 2 kg, so it likely won't
- Gas-spring force and attachment geometry
- Pivot diameters, fasteners and free mounting space
- Actuator model, ratio and stall current, and therefore driver, supply and fuse ratings
- Belt slip torque, and whether it can be both finger-safe and above the snap-up torque
- Whether users find jog-only control acceptable

## 4. What must be measured
In priority order. Full sheet: [donor-measurements.md](donor-measurements.md).

1. **M10** balanced head mass at min, mid and max spring tension (decides ballast)
2. **M7** holding force vs angle, up and down, 3 runs (gives τ_res and τ_f)
3. **M10.4** rise force when the head mass is removed (snap-up hazard)
4. **M2, M8, M9** pivots, attachment points and free space (brackets)
5. **M1, M3, M4, M5** geometry, travel, masses, spring ends (torque model inputs)

## 5. What must be purchased
| Stage | Items | Why first |
|---|---|---|
| First | Donor arm (one unit) | Needed for every measurement; gates actuator selection |
| Borrow, not buy | Force gauge or luggage scale, scale, calipers, test masses | Characterization |
| After measurement | Actuators ×2, driver, supply, belts and pulleys | Sized from data |
| Any time | ESP32-S3, joystick, buttons, E-stop, relay parts, limit switches | Independent of the measurements; allows the bench safety tests |

## 6. Biggest technical risks
| Risk | Why it matters | Mitigation path |
|---|---|---|
| Residual / snap-up torque larger than a compact worm gearmotor can hold through a practical belt | Breaks the actuator plan | Larger gearmotor, linear actuator, or lower payload target |
| No room for brackets at J1/J2 without drilling | Breaks the "no modification" approach | Clamp-on design; alternative donor (Green Soul) |
| Pivot play and backlash in a budget arm | Poor positioning feel | Accept for V1; document |
| Budget has no contingency | One price increase blocks the build | Verify prices before requesting; drop J3 first |
| Ballast adds inertia and changes the balance | Larger τ_dyn and more impact energy | Measure M10; keep speeds low |

## 7. Biggest safety risks
| Risk | Hazard ID |
|---|---|
| Gas-spring snap-up during attachment changes | H1, H9 |
| Force on an obstruction before the belt slips, with no current sensing | H5 |
| Pinch at the parallelogram and belts | H6 |
| Welded relay contact defeating the E-stop | H3 |

Details: [safety.md](safety.md).

## 8. Next physical experiment
**Donor characterization, session 1 (no electronics, no modification):**
1. Buy one donor arm and assemble it per the manufacturer's instructions.
2. With the spring at minimum tension, find the head mass at which the arm holds still at θ ≈ 0 (M10.1). Repeat at mid and max tension.
3. At the V1 spring setting, measure the holding force up and down at 5 angles, 3 runs each (M7).
4. Measure the rise force with the head mass removed (M10.4).
5. Photograph all candidate mounting surfaces with a scale in frame (M8, M9).
6. Enter the data into `tools/torque_model.py`, replacing the example values, and log everything in a dated journal entry.

**Success criterion:** a measured τ_res(θ) curve and a ballast decision. **Not** an actuator purchase in the same session.

## 9. Review outcome
The design is ready for **funding and characterization**. It is **not** ready for actuator purchase or fabrication. Open decisions: ballast (after M10), actuator model and ratio (after M7), whether V1 adds current limiting (after the belt slip test).

# Actuator Selection Framework

> Status: **framework and provisional recommendation only.** No actuator has been purchased or tested. **Final selection happens after donor characterization** (measurements D1–D11 in [mechanical.md §6](mechanical.md#6-measurements-required-before-actuator-selection)). Motors are not chosen for popularity; they are chosen against measured requirements.

## 1. Process

```
Buy donor → measure D1–D11 → compute τ_req, ω, travel, P per joint (mechanical.md §4)
         → screen actuator types (§3) → choose ratio N → check motor torque/speed/current
         → confirm driver + supply ratings → order
```

## 2. Per-joint requirements

Values marked **TBD** are computed from measurements. They are not guesses.

| Quantity | J1 base yaw (V1) | J2 spring arm (V1) | J3 head swivel (optional) |
|---|---|---|---|
| Required static torque | ≈ 0 (vertical axis); friction only: τ_f,J1 **TBD (D8)** | max\|τ_res(θ)\| **TBD (D7)**, at lightest and heaviest head mass | τ_f,J3 **TBD (D8)** |
| Dynamic torque | I_J1·α: I_J1 is large (whole arm about base) **TBD (D1, D3)** | I_J2·α, expected small **TBD** | Small |
| Safety factor | 2 (provisional) | 2 (provisional) | 2 (provisional) |
| Target speed | ≤ 30°/s | ≤ 20°/s | ≤ 30°/s |
| Travel | Limited by donor swivel and cable routing; V1 soft range ≤ ±90° **[A]**, **TBD (D9)** | Full spring-arm pitch range **TBD (D9)** (head vertical travel 260 mm, manufacturer spec) | ±90° (manufacturer swivel spec) |
| Power requirement | P = τ_req·ω, expected a few watts **[E]** | P = τ_req·ω, **TBD** | Small |
| Holding requirement | None. Friction holds yaw | **Must hold τ_res unpowered or powered.** Self-locking strongly preferred | None |
| Preferred type (provisional) | Worm-gear DC gearmotor + belt | **Worm-gear DC gearmotor + belt** | Hobby/robot servo or none |

[A] assumption · [E] estimate

Speed check: a joint at 20°/s turns 3.3 rpm. With a 3:1 belt stage the motor output needs ≈ 10 rpm. Many low-rpm worm gearmotors run in this range, and the final rpm is chosen with the torque.

## 3. Actuator approaches compared

The detailed evaluation is in [actuator-trade-study.md](actuator-trade-study.md).

| Approach | Holds unpowered? | Torque density / cost | Control complexity | Position feedback | Back-drivable (manual move)? | V1 fit |
|---|---|---|---|---|---|---|
| **High-torque hobby servo** (e.g. 20–35 kg·cm class) | No. Must be powered to hold, and hums under load | Good per rupee; limited absolute torque | Very low (PWM) | Internal only; MCU can't read it | No when powered | OK for J3; marginal for J2 if τ_res is large |
| **Worm-gear DC gearmotor** (12 V, low rpm) + belt | **Yes** (self-locking, typical for high-ratio worms) | High output torque, low cost | Low (H-bridge, speed + direction) | None unless added | No | **Best V1 fit for J1, J2** |
| **Spur/planetary DC gearmotor + encoder** | No (back-drivable at moderate ratios) | Good | Medium (closed loop) | Yes (encoder) | Partly | V2 (presets, manual override) |
| **Stepper + gearbox** (NEMA17 + planetary) | Only while energized (holding current, heat) | Good; geared NEMA17 costs more | Medium (driver + accel profiles) | Open-loop; loses steps silently | No | Not preferred: heat, holding current, missed steps |
| **Linear actuator across the parallelogram** | Yes (lead screw) | High force | Low | Some have pots | No | Alternative for J2 if no rotary space (D10) |
| **Window/wiper-type automotive gearmotor** | Usually yes (worm) | Very high torque, heavy, salvage-friendly | Low | None | No | Fallback if τ_res is large; heavy and noisy |

## 4. Provisional V1 recommendation

**J1 and J2: 12 V worm-gear DC gearmotor (low-rpm, compact "worm gearbox" class) driving the joint through a GT2 belt reduction. J3: manual in V1.**

Why this is the simplest realistic option:
1. **Self-locking.** J2 holds against the unknown residual torque, and against the arm-rises-when-unloaded hazard, with zero power and zero control effort. This is the main reason.
2. **Simple control.** Speed and direction from one H-bridge channel. V1 uses joystick velocity control (jog), so no position loop is needed.
3. **Low cost.** It fits a $100 budget alongside the donor arm.
4. **Belt stage** sets the final ratio after measurement and gives a slip-based torque limit.

Known downsides, accepted for V1:
- No manual repositioning by hand while fitted. A clutch is V2.
- No position feedback, so no presets in V1. Joint-angle sensing is V2.
- Worm gearboxes are inefficient, have backlash and can be noisy.
- Motor model, ratio and current are **not chosen** until τ_req exists. The BOM line is an allocation.

**This recommendation is provisional.** It flips to a geared DC motor with encoder, or to a linear actuator for J2, if:
- τ_req at J2 exceeds what a compact worm gearmotor can provide through a practical belt ratio, or
- D10 shows there's no room for a rotary actuator at J2.

## 5. Selection checklist (per joint, once data exists)

- [ ] τ_req computed with SF = 2 at worst-case angle and head mass
- [ ] Motor rated (not stall) torque × N × η ≥ τ_req
- [ ] Joint speed at rated rpm within the target (and limitable in software)
- [ ] Stall current known; driver continuous rating ≥ rated current; fuse sized
- [ ] Self-locking verified on the bench for J2 (after purchase)
- [ ] Mounting pattern compatible with the bracket concept
- [ ] Price verified with two vendors

# Design Decisions (ADRs)

Status meanings: **Proposed** means decided on paper and not validated in hardware. **Open** means not yet decided. **Superseded** means replaced, and kept below for history. **No decision in this log has been validated by a build or measurement.**

## Index

| Topic | ADR |
|---|---|
| Donor-arm retrofit instead of custom arm | [ADR-013](#adr-013--retrofit-a-donor-gas-spring-arm-instead-of-building-a-custom-arm) |
| Gas spring as passive counterbalance | [ADR-025](#adr-025--gas-spring-as-the-passive-counterbalance-ballast-if-needed) |
| Actuator selection deferred until measurement | [ADR-014](#adr-014--actuator-selection-deferred-until-donor-measurement) |
| V1 reduced actuator count | [ADR-019](#adr-019--v1-motorizes-two-joints-j1-j2) |
| Provisional actuator type | [ADR-022](#adr-022--provisional-v1-actuator-worm-gear-dc-gearmotor--belt) |
| Hardware E-stop | [ADR-006](#adr-006--hardware-e-stop-removes-actuator-power) |
| Modular end effector | [ADR-005](#adr-005--arca-swiss--¼-20-end-effector-standard) |
| Accessibility-first controls | [ADR-020](#adr-020--accessibility-first-physical-controls) |
| Payload is a target, not a spec | [ADR-023](#adr-023--payload-and-reach-are-design-targets-not-specifications) |
| Deferring sensors and features | [ADR-021](#adr-021--defer-sensors-and-features-v1-needs-neither-to-work-nor-to-be-safe) |
| Funding tier | [ADR-024](#adr-024--request-the-warm-up-maximum-us100) |

---

## Active decisions

### ADR-013 — Retrofit a donor gas-spring arm instead of building a custom arm
**Status:** Proposed
**Decision:** Use an off-the-shelf gas-spring monitor arm as the structure (preferred: NB North Bayou F80 — [donor-selection.md](donor-selection.md)) and add actuators, controls and safety electronics.
**Alternatives:** a printed hobby-servo arm (the earlier KAI concept) was limited to about 100 g at about 250 mm. A fully custom metal arm is beyond the budget, skills and time available.
**Tradeoffs:** the design depends on one product's geometry. The arm's 2 kg minimum rated load may require ballast. Pivot play in a cheap arm may hurt repeatability.
**Revisit if:** characterization shows no practical actuator mounting, or excessive pivot play.

### ADR-025 — Gas spring as the passive counterbalance; ballast if needed
**Status:** Proposed
**Decision:** The donor's gas spring carries gravity. Actuators handle only the residual torque, friction and acceleration. If the head mass is below the spring's minimum rated load, add ballast at the head instead of modifying the spring.
**Why:** it allows small actuators, and the arm doesn't collapse when power is cut.
**Tradeoffs:** ballast adds inertia and impact energy. Balance changes when the attachment changes. The arm rises when the head mass is removed.

### ADR-018 — Never open or modify the gas spring
**Status:** Proposed
**Why:** a gas spring stores significant energy. Adjustment is done only with the manufacturer's tension mechanism.

### ADR-014 — Actuator selection deferred until donor measurement
**Status:** Proposed
**Decision:** No actuator model is chosen until measurements D1–D11 exist. Sizing uses τ_req = SF·(max|τ_res| + τ_f + τ_dyn) with SF = 2 ([mechanical.md §4](mechanical.md#4-torque-analysis-framework-j2)).
**Why:** the gas spring's residual torque cannot be predicted reliably from listings. Guessing would mean either over-buying or over-claiming.

### ADR-019 — V1 motorizes two joints (J1, J2)
**Status:** Proposed
**Decision:** V1 motorizes J1 (base yaw) and J2 (spring-arm pitch). J3 (head swivel) is an optional stretch goal. Head tilt and rotation stay manual. Four actuated joints is V2.
**Why:** this is the minimum that demonstrates the core idea, which is actuation working with a counterbalance. It fits the budget and halves the integration risk.

### ADR-022 — Provisional V1 actuator: worm-gear DC gearmotor + belt
**Status:** Proposed — provisional until the measurements exist. **Resolves** ADR-016.
**Decision:** use 12 V worm-gear DC gearmotors driving J1 and J2 through GT2 belt reductions.
**Why:**
- They are self-locking, so J2 holds the arm against the residual torque and the arm-rises hazard with no power.
- They need only simple H-bridge control and are cheap.
- The belt sets the final ratio and slips under overload.

**Tradeoffs:** the arm can't be moved by hand while the motors are fitted, there is backlash, and the motors are noisy. Alternatives are compared in [actuator-selection.md](actuator-selection.md).

### ADR-006 — Hardware E-stop removes actuator power
**Status:** Proposed
**Decision:** a latching NC E-stop sits in series with relay K1's coil, and K1 switches the actuator rail. The firmware-controlled MOSFET is also in series with the coil, so firmware can remove power but cannot restore it while the E-stop is pressed. K1 is off by default.
**Behaviour on a stop:** the worm drives and the spring are expected to hold the arm in place. This is to be verified.

### ADR-005 — Arca-Swiss + ¼"-20 end-effector standard
**Status:** Proposed
**Decision:** use an existing photography standard. V1 uses a printed Arca-compatible plate and clamp with a ¼"-20 bolt to save cost; a purchased metal clamp is V2.
**Why:** tool-free swaps and a large accessory ecosystem.

### ADR-020 — Accessibility-first physical controls
**Status:** Proposed
**Decision:** all V1 functions are reachable from a wired panel: a self-centring joystick (dead-man), two large buttons, a 3.5 mm two-switch jack, a large E-stop, and LED + tone feedback. Speed, deadzone and timing are configurable. There is no app.
**Why:** the project's hypothesis is about physical control ([accessibility.md](accessibility.md)). Whether it helps is unproven.

### ADR-023 — Payload and reach are design targets, not specifications
**Status:** Proposed
**Decision:** about 500 g at about 400–500 mm is always described as an unvalidated target. No document states it as a capability. If the measurements don't support it, the target is reduced; the safety factor is not.

### ADR-021 — Defer sensors and features V1 needs neither to work nor to be safe
**Status:** Proposed. **Supersedes** ADR-015 for V1.
**Decision:** V1 has no joint-angle sensors, no dedicated current sensor, no rotary encoder, no wireless and no telemetry. Control is by jog (velocity). Safety comes from the E-stop, limit switches, fuse, belt slip, dead-man input, stall timeout and watchdog.
**Cost of this choice:** no presets, and only approximate software soft limits. Angle sensing is the first V2 addition.
**Why:** budget, and a smaller system that is easier to make work and to review.

### ADR-024 — Request the warm-up maximum (US$100)
**Status:** Proposed. **Supersedes** ADR-017.
**Decision:** the mandatory V1 BOM is about ₹8,750 (≈ US$99, unverified). Request the warm-up maximum. Tier 1 (US$30) cannot fund a donor arm. Tier 2 (US$75) is a placeholder value and too small. ([bom.md](bom.md#funding-tier-fit))
**Risk:** there is no contingency.

### ADR-002 — ESP32-S3 controller
**Status:** Proposed
**Why:**
- Its LEDC peripheral provides hardware PWM for the H-bridges.
- Its ADC reads the joystick and the rail sense.
- FreeRTOS lets the safety task run separately.
- It has native USB.

A Raspberry Pi was rejected because a Linux safety loop is a poor fit and the SD card can be corrupted on power loss.

### ADR-003 — 12 V actuator rail, separately fused logic supply
**Status:** Proposed
**Decision:** a 12 V supply, provisionally 3 A, goes through fuse F1 and relay K1 to the drivers. A separately fused buck converter powers the logic. Final ratings depend on the motors chosen.

### ADR-004 — Wired panel; no wireless in V1
**Status:** Proposed
**Why:** a wired panel can't drop out and needs no pairing, and the E-stop loop stays hardwired. Wireless needs its own safety design, so it is V2.

### ADR-008 — PETG for printed parts
**Status:** Proposed
**Why:** PETG creeps less than PLA under sustained load and is easier to print safely in shared labs than ABS/ASA.

### ADR-010 — No PCA9685
**Status:** Proposed
**Why:** the ESP32-S3's built-in PWM channels are enough for V1.

### ADR-011 — No dedicated current sensor in V1
**Status:** Proposed
**Why:** the fuse, driver protection and stall timeout cover V1. A current sensor rated for the full stall current is V2. (See also ADR-021.)

---

## Superseded

| ADR | Was | Superseded by |
|---|---|---|
| ADR-001 | Hobby servos on a printed 4-DOF arm | ADR-013 |
| ADR-007 | Manual park procedure (servo design) | ADR-015 → ADR-021 |
| ADR-009 | 100 g at full reach (servo design) | ADR-023 |
| ADR-012 | Budget ≤ ₹9,300 (servo design) | ADR-017 → ADR-024 |
| ADR-015 | Absolute joint sensors in V1 | ADR-021 (moved to V2) |
| ADR-016 | Back-drivable vs self-locking (open) | ADR-022 |
| ADR-017 | Budget ≈ ₹14,000 | ADR-024 |

### Template
```
### ADR-NNN — Title
**Status:** Proposed | Open | Superseded by ADR-XXX
**Decision:**
**Alternatives:**
**Tradeoffs:**
**Revisit if:**
```

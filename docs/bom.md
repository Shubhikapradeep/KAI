# Preliminary Bill of Materials — V1

> **Nothing has been purchased.** Unless marked **[V]**, every price is a planning estimate marked **PRICE TO VERIFY**. No vendor stock or availability is claimed. Before ordering, each line must be checked against at least two vendors.
>
> **[V]** = seen on a vendor page on 2026-10-04 (still to be re-checked at purchase). Currency conversion assumes **₹88 = US$1 (rate to verify)**.

## Mandatory V1

V1 has 2 actuated joints (J1, J2), jog control and a hardware E-stop.

### Mechanical donor and retrofit

| # | Item | Qty | Est. total (₹) | Price status | Notes |
|---|---|---|---|---|---|
| M1 | Donor arm: NB North Bayou F80 (preferred) | 1 | 2,900 | PRICE TO VERIFY | Fallback: Green Soul 2–9 kg arm, ₹2,890 **[V]** ([donor-selection.md](donor-selection.md)) |
| M2 | PETG filament (~0.5 kg) for brackets, pulleys, strikers, panel box | 1 | 550 | PRICE TO VERIFY | Assumes department/makerspace printer access |
| M3 | GT2 belts + 20T motor pulleys (2 sets) | 2 | 350 | PRICE TO VERIFY | Joint-side pulleys printed |
| M4 | Fasteners, heat-set inserts, U-bolts/hose clamps | lot | 350 | PRICE TO VERIFY | No drilling of donor load paths |
| M5 | Ballast washers (only if D4 shows they're needed) | lot | 100 | PRICE TO VERIFY | Brings head mass to the spring's minimum load |
| | **Subtotal** | | **4,250** | | |

### Actuation

| # | Item | Qty | Est. total (₹) | Price status | Notes |
|---|---|---|---|---|---|
| A1 | 12 V worm-gear DC gearmotor, J2 | 1 | 650 | PRICE TO VERIFY | **Allocation.** Model chosen after D1–D11 ([actuator-selection.md](actuator-selection.md)) |
| A2 | 12 V worm-gear DC gearmotor, J1 | 1 | 650 | PRICE TO VERIFY | Allocation |
| A3 | Dual H-bridge driver module | 1 | 200 | PRICE TO VERIFY | Rating set by motor stall current |
| | **Subtotal** | | **1,500** | | |

### Controller, controls, power and safety

| # | Item | Qty | Est. total (₹) | Price status | Notes |
|---|---|---|---|---|---|
| E1 | ESP32-S3 dev board | 1 | 900 | PRICE TO VERIFY | |
| E2 | 2-axis analog joystick module (+ printed large handle) | 1 | 120 | PRICE TO VERIFY | |
| E3 | 30 mm arcade buttons (ARM/MODE, SLOW) | 2 | 160 | PRICE TO VERIFY | |
| E4 | 3.5 mm TRS jack (assistive switch input) | 1 | 40 | PRICE TO VERIFY | |
| E5 | Latching mushroom E-stop, NC contact | 1 | 300 | PRICE TO VERIFY | Must be latching |
| E6 | Lever microswitches (4 + 1 spare) | 5 | 150 | PRICE TO VERIFY | |
| E7 | Relay (contact ≥ F1 rating) + logic MOSFET + diode | 1 | 120 | PRICE TO VERIFY | Actuator power cut |
| E8 | 12 V supply (provisional 3 A) | 1 | 450 | PRICE TO VERIFY | Rating revised after motor choice |
| E9 | Buck converter 12 → 5 V | 1 | 80 | PRICE TO VERIFY | |
| E10 | Fuses + holders | lot | 80 | PRICE TO VERIFY | |
| E11 | Wire, connectors, perfboard, resistors, status LED, buzzer | lot | 350 | PRICE TO VERIFY | |
| | **Subtotal** | | **2,750** | | |

### End effector

| # | Item | Qty | Est. total (₹) | Price status | Notes |
|---|---|---|---|---|---|
| X1 | Printed Arca-compatible dovetail plate + clamp, ¼"-20 bolt | 1 | 50 | PRICE TO VERIFY | Printed from M2; bolt only. Purchased metal clamp is V2 |
| X2 | ¼"-20 phone clamp | 1 | 200 | PRICE TO VERIFY | First attachment |
| | **Subtotal** | | **250** | | |

### Mandatory V1 total

| Category | ₹ |
|---|---|
| Mechanical donor and retrofit | 4,250 |
| Actuation | 1,500 |
| Controller, controls, power, safety | 2,750 |
| End effector | 250 |
| **Total (no contingency)** | **8,750 ≈ US$99** |

The total has **no contingency.** One wrong motor or a donor price increase pushes it over US$100.

## Optional / V2 (not in the funding request)

| Item | Est. (₹) | Price status | Enables |
|---|---|---|---|
| J3 head-swivel actuator (servo) + bracket | 800 | PRICE TO VERIFY | 3rd actuated joint |
| Motorized head tilt | 800 | PRICE TO VERIFY | 4th actuated joint |
| Joint-angle sensors (AS5600-class, ×3) + magnets | 600 | PRICE TO VERIFY | Presets, closed loop, real soft limits |
| Rotary encoder + knob | 150 | PRICE TO VERIFY | Menu / fine control |
| Current-regulating drivers (DRV887x-class) | 600 | PRICE TO VERIFY | Better stall protection |
| Metal Arca quick-release clamp | 450 | PRICE TO VERIFY | Sturdier mount |
| Extra end effectors (tablet holder, camera mount) | 500 | PRICE TO VERIFY | More use cases |
| Wireless interface / telemetry | 0 hardware | — | Firmware only (ESP32-S3 has Wi-Fi/BLE); deferred for safety (ADR-004) |

## Funding-tier fit

Tier values come from Half Life's public source code (`lib/config/tiers.ts`, checked 2026-10-04). **Only Tier 1 is confirmed** there; Tier 2 and Tier 3 are marked as placeholders. The Half Life site states that warm-up projects can receive **up to $100**.

| Tier | Grant | Min. hours | ₹ (at ₹88/$) | Mandatory V1 (₹8,750) fits? |
|---|---|---|---|---|
| Tier 1 | $30 (confirmed) | 10 h | 2,640 | **No.** The donor arm alone costs more |
| Tier 2 | $75 (placeholder) | 20 h (placeholder) | 6,600 | **No.** Even a J2-only build (~₹7,865) exceeds it |
| Tier 3 | $150 (placeholder) | 35 h (placeholder) | 13,200 | Yes, with ~₹4,450 left for contingency or V2 items |
| Warm-up cap | up to $100 (site) | — | 8,800 | **Just.** ₹50 margin, no contingency |

### Recommendation
**Request the warm-up maximum (US$100)** for the 2-actuator V1. This is the smallest tier that fits the mandatory BOM.

- If the reviewer assigns less than ~US$90, the honest options are to self-fund part of the donor or to wait for a higher tier. A J2-only build (~₹7,865, ≈ US$89) doesn't fit US$75 either.
- If Tier 3 is confirmed at US$150, it adds a real contingency and could fund J3 or angle sensors.
- Tier 1 (US$30) cannot fund any version of KAI that includes a donor arm.

Sources: [Half Life site](https://halflife.hackclub.com/), [hackclub/half-life repository](https://github.com/hackclub/half-life).

## Not included
Tools, printer time, the force gauge, scale and test masses needed for characterization (to be borrowed), shipping, and taxes.

# Firmware Architecture — V1

> Status: **architecture only. No code has been written.** Planned location: `firmware/` (PlatformIO, Arduino-ESP32 core on FreeRTOS). Speeds and timings are placeholders.

## 1. V1 control model: jog control, no position sensing

V1 has no joint-angle sensors (ADR-021), so the firmware does **velocity (jog) control**. Joystick deflection sets motor speed and direction, and releasing the self-centring joystick stops the motor. Position presets need angle sensing and are **V2**.

Principles:
1. **Safe startup:** actuator relay K1 off at boot, reset and watchdog.
2. **Dead-man motion:** motors move only while an input is actively held.
3. **Safety task is separate**, highest priority, and the only code that drives K1.
4. **Slow:** speed caps (J2 ≤ 20°/s, J1 ≤ 30°/s, estimated via motor rpm × ratio) and acceleration ramps.
5. **No surprise motion:** arming, mode changes, fault clearing and E-stop release never move the arm.

## 2. State machine

```
 power-on / reset / watchdog
          │
          ▼
        BOOT ──self-test fail──► FAULT ──cause cleared + hold ARM 2 s──► SAFE
          │ ok
          ▼
        SAFE  (K1 off; actuators unpowered; worm drives hold position)
          │ hold ARM 2 s, joystick centred, no limit fault, E-stop released
          ▼
       ARMING (K1 on; rail sense must confirm power within 200 ms)
          │ rail present
          ▼
       ACTIVE (jog control) ──limit fault / rail lost / stall timeout / watchdog──► FAULT
          │ hold ARM 2 s, or 60 s idle
          ▼
        SAFE

 ANY state ── rail lost while K1 commanded on, or E-stop → ESTOP ── E-stop released ──► SAFE
```

| State | K1 / actuator power | Behaviour |
|---|---|---|
| BOOT | Off | Self-test: inputs readable, joystick near centre, limit switches closed, rail sense reads absent |
| SAFE | Off | Status LED slow white; config allowed over USB |
| ARMING | On | Confirms the rail is present; refuses if the joystick isn't centred |
| ACTIVE | On | Jog control; LED green (amber in SLOW) |
| FAULT | Off | LED flashes the cause code; manual clear only |
| ESTOP | Off (hardware) | LED solid red; on release → SAFE |

**Idle auto-disarm:** after 60 s without input in ACTIVE → SAFE. This limits time spent powered.

## 3. Software travel limits (without angle sensors)

- **Hard limits:** the physical limit switches (always enforced; a tripped limit blocks motion into it).
- **Soft limits (approximate):** the firmware integrates commanded speed over time to estimate each joint's position, **referenced to a limit switch**. After the user jogs a joint onto one of its switches, the estimate resets to that end. Near the estimated far end, speed is reduced to 25%. The estimate is labelled approximate in docs and on the CLI, since backlash and load variation make it drift. It only ever *slows* motion; the switches are the authority.

## 4. Input handling

- Joystick: centre calibration at boot, deadzone (default 15%, adjustable 10–35%), cubic expo, ~5 Hz low-pass filter. Each axis maps to one joint: X → J1, Y → J2.
- SLOW button toggles a 25% speed mode.
- **Switch-scan mode** (alt-input jack): switch A steps through *J1 left / J1 right / J2 up / J2 down*, indicated by LED colour and beeps. Holding switch B moves in the selected direction while held (dead-man).
- Long-press timing is configurable (default 2 s).

## 5. Fault detection

| Condition | Action |
|---|---|
| Limit switch open while moving toward it | Stop joint; if both ends of one joint read open → FAULT (wiring) |
| Rail lost while K1 commanded on | ESTOP (or a fault if E-stop is released) |
| Rail present while K1 commanded off | FAULT (possible welded relay) |
| Continuous drive > configurable time (e.g. 15 s) in one direction | FAULT "possible stall" (no position or current sensing, so a timeout is used instead) |
| Joystick reading out of range | FAULT |
| Task watchdog | Reset → K1 off → SAFE |

## 6. Tasks (FreeRTOS)

| Task | Priority | Rate | Role |
|---|---|---|---|
| `safety` | Highest | 200 Hz | Limits, rail sense, watchdog feeding, K1 ownership |
| `motion` | High | 100 Hz | Speed ramps, soft-limit slow zones, driver PWM |
| `input` | Medium | 100 Hz | Joystick, buttons, switch jack, long-press timing |
| `ui` | Low | 20 Hz | LED and buzzer |
| `comms` | Lowest | event | USB serial CLI and logs |

## 7. Module layout (planned)

```
firmware/
├── platformio.ini
├── include/config.h      # pins, speeds, timeouts, deadzone
└── src/
    ├── main.cpp
    ├── safety/           # relay, limits, rail_sense, supervisor
    ├── motion/           # jog, ramp, soft_limit_estimate
    ├── hal/              # hbridge, servo_out (optional J3)
    ├── input/            # joystick, buttons, switch_scan
    ├── state/            # state_machine
    ├── ui/               # led, buzzer
    └── comms/            # serial_cli
```

Hardware-free logic (state machine, ramps, input shaping, soft-limit estimate) will be unit-tested with PlatformIO's `native` environment + Unity once code exists.

## 8. Serial CLI (planned)

```
status            → state, limit states, rail present, estimated positions (approx.)
deadzone 20       → set joystick deadzone (SAFE only)
speed J2 15       → speed cap in deg/s (SAFE only)
stall_timeout 15
log on
```

## 9. V2 firmware
Joint-angle sensing → closed-loop position control, presets, true soft limits, ARMING from measured angles; encoder knob menus; telemetry.

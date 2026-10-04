# Accessibility & HCI — Design Exploration

> Status: **hypotheses and design rationale only.** KAI has not been built, and no one has used it. Nothing here claims that KAI improves accessibility. These are questions the project intends to explore, and they could turn out to be wrong.

## 1. Design hypothesis

> A counterbalanced arm moved by **large, configurable physical controls**, rather than by direct hand manipulation, may let some people position a phone, camera or small tablet on their desk with **less need for reach, grip strength and fine motor precision**.

KAI explores six specific questions:

| Theme | Question KAI explores |
|---|---|
| Physical interfaces for robotic movement | Is joystick/button/switch jogging an understandable way to move a desk arm? |
| Reduced need for precise manual manipulation | Can someone set a useful device position without gripping or pushing the arm itself? |
| Configurable controls | Do adjustable deadzone, speed and button timing make the controls usable by more people? |
| Assistive-switch compatibility | Is two-switch scanning through four jog directions practical, or too slow to be useful? |
| Physical feedback | Do LEDs, distinct tones and tactile buttons make the arm's state clear enough? |
| Adaptable end effectors | Does a standard quick-release mount make swapping between phone, camera and holder practical? |

## 2. Intended users and use cases (scenarios, not diagnoses)

| Possible user situation | Example use case |
|---|---|
| Limited reach or shoulder mobility | Bring a phone closer for reading, then push it back out of the way |
| Reduced grip strength or endurance | Avoid holding a phone or tablet up for long periods |
| Tremor | Make small adjustments that are filtered and slowed, instead of pushing the arm by hand |
| Difficulty using touchscreens or apps for control | Operate with physical controls only. No app, no pairing |
| Anyone with a crowded desk | Reposition a webcam or document camera during a call |

The team has no lived experience of these situations. Any real design direction has to come from the users themselves and from occupational therapists (§4).

## 3. Accessibility considerations in the V1 design

| Consideration | V1 design choice | Status |
|---|---|---|
| One-handed use | Joystick + 2 buttons; no simultaneous presses needed | Planned |
| Let go = stop | Self-centring joystick; motion only while input is held | Planned |
| Tolerance of unintended movement | Large adjustable deadzone, input filtering, slow speed caps, SLOW mode | Planned |
| Alternative input | 3.5 mm jack for two standard assistive switches; scanning mode | Planned |
| Large, distinguishable controls | 30 mm buttons with raised markers; oversized printed joystick handle with swappable tops | Planned |
| Clear state feedback | LED colour **and** pattern, plus distinct tones, so state isn't shown by colour alone | Planned |
| Control placement | Separate panel on a cable, placed where the user's hand rests | Planned |
| Emergency stop reachable | Large red latching E-stop on the panel, away from the arm | Planned |
| Adaptable end effector | Arca-compatible quick-release + ¼"-20 | Planned |

## 4. What must be evaluated with real users

None of these evaluations have happened.

| Question | Possible method |
|---|---|
| Can users understand jog control (X → swing, Y → raise/lower) without training? | Think-aloud task sessions |
| Is joystick or switch scanning fast enough to be worth using? | Task time for "bring phone to reading position" vs. the user's current method |
| Are deadzone and speed defaults sensible? | Adjust per participant; record the settings they choose |
| Do users feel safe with an arm of this size moving near them? | Post-session interview; perceived-safety rating |
| Is the E-stop actually reachable and operable for each participant? | Observed check before every session |
| Can users swap attachments independently, given the gas-spring rise hazard? | Observed task; likely needs a helper |
| What do OTs and AT users think is missing? | Expert review of this design before building |

Any session with participants would follow university ethics guidance and informed consent. Results, including negative ones, would be logged in `journal/`.

## 5. Limitations (known now)

- **No presets in V1.** Without position sensing, the user has to jog the arm to each position every time. That may be tiring, and it's a real accessibility cost of keeping V1 simple. Presets are V2.
- **Worm-gear actuators prevent moving the arm by hand** while fitted. That rules out a familiar, quick override.
- **Attachment swaps** are affected by gas-spring balance and the arm-rises hazard, and probably need a helper.
- **Size and energy:** a ~400–500 mm arm with a ~0.5 kg device carries more impact and pinch risk than a small desktop arm.
- **Head tilt is manual in V1**, which still requires hand use for that adjustment.
- **Small-n, informal evaluation** at best within this project's scope. Results won't generalize.

## 6. Safety scope

KAI is a prototype for repositioning a device on a desk. It is **not** intended for feeding or drinking, use near the face or eyes, unsupervised use by anyone who couldn't press the E-stop or move away, holding hot, sharp, heavy or liquid-filled items, or any medical or clinical use. It is not a medical device and makes no medical claims.

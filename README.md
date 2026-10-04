KAI - Kinetic Adaptive Interface
# KAI — Kinetic Adaptive Interface

> A programmable, accessibility-focused desktop robotic arm built by retrofitting a gas-spring monitor arm.

![KAI preliminary design](docs/img/kai-design.jpg)

## Overview

KAI (Kinetic Adaptive Interface) is a modular desktop robotic arm designed to explore more accessible ways of physically interacting with objects and devices on a desk.

Instead of designing a completely new arm from scratch, KAI retrofits an off-the-shelf gas-spring monitor/laptop arm. The existing gas spring provides passive counterbalance while the retrofit adds motorized control, an ESP32-S3 controller, physical accessibility-oriented controls, safety systems, and a modular end effector.

The project is currently in the **pre-build design stage**.

## V1 Design

The first version focuses on two controlled degrees of freedom:

- **J1 — Base rotation**
- **J2 — Spring-assisted arm movement**

The intended control path is:

```text
Joystick / physical controls
          │
          ▼
      ESP32-S3
          │
          ▼
    Motor drivers
          │
          ▼
      J1 / J2
          │
          ▼
 Counterbalanced arm
          │
          ▼
   Modular end effector

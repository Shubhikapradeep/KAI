#!/usr/bin/env python3
"""KAI J2 torque model.

ALL DEFAULT PARAMETER VALUES ARE ILLUSTRATIVE EXAMPLES, NOT MEASUREMENTS.
Replace them with donor measurements (docs/donor-measurements.md) before using
any output for actuator selection.

Usage:
    python3 tools/torque_model.py                 # example values -> docs/torque-model.csv + docs/img/torque-model.svg
    python3 tools/torque_model.py params.json     # your own parameters (same keys as EXAMPLE)

Sign convention: theta > 0 = arm above horizontal. Positive torque tends to
LOWER the arm (gravity direction). tau_res > 0 -> arm sinks if unpowered;
tau_res < 0 -> arm rises (spring wins).
"""
import csv, json, math, sys, pathlib

G = 9.81

EXAMPLE = {
    "_note": "EXAMPLE VALUES - NOT MEASURED",
    "m_payload_kg": 0.50,      # design target device
    "m_ee_kg": 0.08,           # end effector (clamp + plate) - example
    "m_head_kg": 0.35,         # donor VESA head - example
    "m_ballast_kg": 1.10,      # brings head to ~2 kg (donor min rated load) - example
    "m_link_kg": 0.90,         # moving parallelogram links - example
    "L_m": 0.40,               # J2 -> head pivot - estimate
    "e_m": 0.09,               # head pivot -> head CoM, horizontal - assumption
    "r_link_m": 0.20,          # link CoM distance from J2 - example
    "spring_a_m": 0.05,        # spring fixed end distance from J2 - example
    "spring_b_m": 0.16,        # spring moving end distance from J2 - example
    "spring_phi0_deg": 95.0,   # angle between A and B at theta = 0 - example
    "spring_force_N": None,    # None -> solved so the arm balances at theta=0 WITH payload (example only)
    "tau_friction_Nm": 0.30,   # break-away friction at J2 - example
    "alpha_rad_s2": 0.70,      # 20 deg/s reached in ~0.5 s
    "safety_factor": 2.0,
    "theta_min_deg": -30, "theta_max_deg": 30, "theta_step_deg": 5,
}


def head_mass(p, with_payload=True):
    return (p["m_payload_kg"] if with_payload else 0) + p["m_ee_kg"] + p["m_head_kg"] + p["m_ballast_kg"]


def tau_gravity(p, th, with_payload=True):
    c = math.cos(th)
    return G * (head_mass(p, with_payload) * (p["L_m"] * c + p["e_m"]) + p["m_link_kg"] * p["r_link_m"] * c)


def spring_arm(p, th):
    a, b = p["spring_a_m"], p["spring_b_m"]
    phi = math.radians(p["spring_phi0_deg"]) + th
    s = math.sqrt(a * a + b * b - 2 * a * b * math.cos(phi))
    return a * b * math.sin(phi) / s, s


def run(p):
    if p.get("spring_force_N") is None:
        d0, _ = spring_arm(p, 0.0)
        p["spring_force_N"] = tau_gravity(p, 0.0) / d0
        p["_spring_force_note"] = "solved to balance at theta=0 (example only)"
    I = head_mass(p) * (p["L_m"] + p["e_m"]) ** 2 + p["m_link_kg"] * p["r_link_m"] ** 2
    tau_dyn = I * p["alpha_rad_s2"]
    rows = []
    th = p["theta_min_deg"]
    while th <= p["theta_max_deg"] + 1e-9:
        r = math.radians(th)
        d, s = spring_arm(p, r)
        tg = tau_gravity(p, r, True)
        tg0 = tau_gravity(p, r, False)
        ts = p["spring_force_N"] * d
        rows.append({"theta_deg": th, "spring_len_mm": round(s * 1000, 1),
                     "tau_gravity_Nm": round(tg, 3), "tau_spring_Nm": round(ts, 3),
                     "tau_res_Nm": round(tg - ts, 3), "tau_res_no_payload_Nm": round(tg0 - ts, 3)})
        th += p["theta_step_deg"]
    worst = max(abs(x["tau_res_Nm"]) for x in rows)
    worst_np = max(abs(x["tau_res_no_payload_Nm"]) for x in rows)
    sf, tf = p["safety_factor"], p["tau_friction_Nm"]
    summary = {
        "I_J2_kgm2": round(I, 4), "tau_dyn_Nm": round(tau_dyn, 3),
        "max_abs_tau_res_Nm": round(worst, 3),
        "tau_req_Nm (with payload)": round(sf * (worst + tf + tau_dyn), 3),
        "max_abs_tau_res_no_payload_Nm": round(worst_np, 3),
        "tau_req_Nm (payload removed while armed)": round(sf * (worst_np + tf + tau_dyn), 3),
        "spring_force_N": round(p["spring_force_N"], 1),
    }
    return rows, summary


def write_csv(path, p, rows, summary):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["# KAI J2 torque model output - EXAMPLE VALUES, NOT MEASUREMENTS"])
        w.writerow(["# parameter", "value"])
        for k, v in p.items():
            if not k.startswith("_"):
                w.writerow([k, v])
        w.writerow([])
        w.writerow(["# summary", "value"])
        for k, v in summary.items():
            w.writerow([k, v])
        w.writerow([])
        w.writerow(list(rows[0].keys()))
        for r in rows:
            w.writerow(list(r.values()))


def write_svg(path, rows, summary):
    W, H, x0, y0, pw, ph = 1040, 560, 110, 110, 640, 340
    keys = [("tau_gravity_Nm", "#475569", "gravity τ_g", ""), ("tau_spring_Nm", "#0f766e", "spring τ_s", ""),
            ("tau_res_Nm", "#c2410c", "residual, with device", ""), ("tau_res_no_payload_Nm", "#dc2626", "residual, device removed", "6 4")]
    vals = [r[k] for r in rows for k, *_ in keys]
    lo, hi = min(vals + [0]), max(vals)
    lo, hi = math.floor(lo), math.ceil(hi)
    tmin, tmax = rows[0]["theta_deg"], rows[-1]["theta_deg"]
    X = lambda t: x0 + (t - tmin) / (tmax - tmin) * pw
    Y = lambda v: y0 + ph - (v - lo) / (hi - lo) * ph
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Helvetica, Arial, sans-serif">',
         f'<rect width="{W}" height="{H}" fill="#fff"/>',
         '<text x="40" y="44" font-size="22" font-weight="700" fill="#0f172a">J2 torque model — EXAMPLE output</text>',
         '<rect x="40" y="56" width="650" height="24" rx="4" fill="#fef2f2" stroke="#dc2626"/>',
         '<text x="50" y="73" font-size="12" font-weight="700" fill="#991b1b">ILLUSTRATIVE ONLY — example parameters, NOT measurements. Spring force solved to balance at θ = 0.</text>']
    for v in range(lo, hi + 1):
        o.append(f'<line x1="{x0}" y1="{Y(v):.1f}" x2="{x0+pw}" y2="{Y(v):.1f}" stroke="{"#94a3b8" if v == 0 else "#eef2f7"}"/>')
        o.append(f'<text x="{x0-10}" y="{Y(v)+4:.1f}" font-size="11" fill="#64748b" text-anchor="end">{v}</text>')
    for t in range(tmin, tmax + 1, 10):
        o.append(f'<text x="{X(t):.1f}" y="{y0+ph+20}" font-size="11" fill="#64748b" text-anchor="middle">{t}°</text>')
    o.append(f'<text x="{x0+pw/2}" y="{y0+ph+44}" font-size="12" fill="#334155" text-anchor="middle">J2 angle θ above horizontal</text>')
    o.append(f'<text x="40" y="{y0+ph/2}" font-size="12" fill="#334155" transform="rotate(-90 40 {y0+ph/2})" text-anchor="middle">torque about J2 (N·m)</text>')
    for k, col, lab, dash in keys:
        pts = " ".join(f"{X(r['theta_deg']):.1f},{Y(r[k]):.1f}" for r in rows)
        o.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2.5" stroke-dasharray="{dash}"/>')
    lx, ly = 780, 120
    for i, (k, col, lab, dash) in enumerate(keys):
        o.append(f'<line x1="{lx}" y1="{ly+i*24}" x2="{lx+30}" y2="{ly+i*24}" stroke="{col}" stroke-width="2.5" stroke-dasharray="{dash}"/>')
        o.append(f'<text x="{lx+38}" y="{ly+i*24+4}" font-size="12" fill="#334155">{lab}</text>')
    o.append(f'<text x="{lx}" y="{ly+120}" font-size="13" font-weight="700" fill="#0f172a">Example summary</text>')
    for i, (k, v) in enumerate(list(summary.items())[1:6]):
        o.append(f'<text x="{lx}" y="{ly+144+i*20}" font-size="11" fill="#334155">{k.replace("_Nm","").replace("_"," ")}: {v} N·m</text>')
    o.append(f'<text x="{lx}" y="{ly+260}" font-size="11" fill="#64748b">Positive = tends to lower the arm.</text>')
    o.append(f'<text x="{lx}" y="{ly+276}" font-size="11" fill="#64748b">Negative = spring wins (arm rises).</text>')
    o.append('</svg>')
    pathlib.Path(path).write_text("\n".join(o))


if __name__ == "__main__":
    p = dict(EXAMPLE)
    if len(sys.argv) > 1:
        p.update(json.loads(pathlib.Path(sys.argv[1]).read_text()))
    rows, summary = run(p)
    root = pathlib.Path(__file__).resolve().parent.parent
    write_csv(root / "docs/torque-model.csv", p, rows, summary)
    write_svg(root / "docs/img/torque-model.svg", rows, summary)
    for k, v in summary.items():
        print(f"{k}: {v}")

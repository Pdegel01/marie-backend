# polarimetric-calibration

Research project on **in-flight polarimetric calibration of multi-angle optical sensors** using ocean sunglint/glitter as a natural calibration target.

Instruments: **PARASOL/POLDER-3** (available) and **3MI/MetOp-SG** (not yet available).

---

## What exists

### Package — `src/polcal/`

| Module | Status | What it does |
|---|---|---|
| `config.py` | skeleton | Load and merge YAML configs |
| `ingestion/base.py` | skeleton | Abstract `InstrumentReader` + `Scene` dataclass |
| `ingestion/parasol.py` | skeleton | Concrete reader for PARASOL HDF5 L1B files |
| `ingestion/three_mi.py` | skeleton | Concrete reader for 3MI NetCDF4 L1B files |
| `modeling/geometry.py` | **implemented** | Scattering angle, Fresnel coefficients, Mueller matrices, rotations |
| `modeling/glitter.py` | **implemented** | Cox-Munk PDF, DoLP, full Stokes vector simulation |
| `modeling/atmosphere.py` | skeleton | Aerosol screening, Rayleigh OD, phase matrix |
| `calibration/pipeline.py` | skeleton | End-to-end pipeline: select → simulate → fit |
| `calibration/residuals.py` | skeleton | Residual statistics and outlier flagging |
| `visualization/plots.py` | **implemented** | Fresnel/Brewster curves, Cox-Munk distributions, 2D DoLP maps |

### Configuration — `config/`

- `default.yaml` — geometry thresholds, wind range, aerosol filters, calibration params
- `instruments/parasol.yaml` — PARASOL band table and file format
- `instruments/3mi.yaml` — 3MI band table and file format

### Notebooks — `notebooks/`

- `01_exploration.ipynb` — imports the package
- `02_simulation.ipynb` — Cox-Munk + Fresnel simulation and visualisation

---

## Key physics (implemented)

**Convention:** Δφ = 0° is the specular direction (same azimuth as the sun).

```
cos Θ = cos θ_s · cos θ_v − sin θ_s · sin θ_v · cos(Δφ)
θ_i   = Θ / 2
θ_B   = arctan(n) ≈ 53.2°  (Brewster angle — maximum DoLP)
σ²(W) = 0.003 + 0.00512·W  (Cox-Munk slope variance)
```

---

## Setup

```bash
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
jupyter lab notebooks/02_simulation.ipynb
```

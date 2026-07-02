"""Diagnostic plots for the polarimetric calibration project."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from polcal.modeling.geometry import brewster_angle, fresnel_coefficients
from polcal.modeling.glitter import cox_munk_slope_pdf, dolp_fresnel, glint_stokes


def plot_dolp_vs_incidence(n_water: float = 1.34, output: Path | None = None) -> plt.Figure:
    """Plot DoLP and Fresnel reflectances (Rs, Rp) vs incidence angle, marking the Brewster angle."""
    theta_i = np.linspace(0, np.pi / 2, 500)
    r_s, r_p = fresnel_coefficients(theta_i, n_water)
    dolp = dolp_fresnel(theta_i, n_water)
    theta_B = brewster_angle(n_water)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))

    ax = axes[0]
    ax.plot(np.degrees(theta_i), r_s**2, label=r"$R_s$", color="steelblue")
    ax.plot(np.degrees(theta_i), r_p**2, label=r"$R_p$", color="tomato")
    ax.axvline(np.degrees(theta_B), color="gray", linestyle="--", linewidth=0.8)
    ax.set_xlabel(r"$\theta_i$ (deg)")
    ax.set_ylabel("Fresnel reflectance")
    ax.set_title("Fresnel coefficients — seawater")
    ax.legend()
    ax.set_xlim(0, 90)
    ax.set_ylim(0, 1)

    ax = axes[1]
    ax.plot(np.degrees(theta_i), dolp, color="darkorange", linewidth=2)
    ax.axvline(np.degrees(theta_B), color="gray", linestyle="--", linewidth=0.8)
    ax.text(np.degrees(theta_B) + 1, 0.5, f"Brewster {np.degrees(theta_B):.1f}deg", color="gray", fontsize=9)
    ax.set_xlabel(r"$\theta_i$ (deg)")
    ax.set_ylabel("DoLP")
    ax.set_title("DoLP — Fresnel reflection of unpolarised light")
    ax.set_xlim(0, 90)
    ax.set_ylim(0, 1.05)

    fig.tight_layout()
    if output:
        fig.savefig(output, dpi=150)
    return fig


def plot_cox_munk(wind_speeds: list[float] | None = None, output: Path | None = None) -> plt.Figure:
    """Plot the Cox-Munk slope PDF for several wind speeds."""
    if wind_speeds is None:
        wind_speeds = [2.0, 4.0, 6.0, 8.0, 10.0]
    theta_n = np.linspace(0, np.radians(40), 400)
    fig, ax = plt.subplots(figsize=(7, 5))
    colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(wind_speeds)))
    for W, color in zip(wind_speeds, colors):
        ax.plot(np.degrees(theta_n), cox_munk_slope_pdf(theta_n, W), label=f"W = {W} m/s", color=color)
    ax.set_xlabel(r"$\theta_n$ (deg)")
    ax.set_ylabel(r"PDF (sr$^{-1}$)")
    ax.set_title("Cox-Munk slope distribution")
    ax.legend()
    ax.set_xlim(0, 40)
    ax.set_ylim(bottom=0)
    fig.tight_layout()
    if output:
        fig.savefig(output, dpi=150)
    return fig


def plot_glint_dolp_map(
    theta_s_deg: float = 40.0,
    wind_speed: float = 5.0,
    n_water: float = 1.34,
    output: Path | None = None,
) -> plt.Figure:
    """Plot 2-D maps of glint intensity and DoLP in (theta_v, delta_phi) space."""
    theta_v_deg = np.linspace(0, 70, 200)
    delta_phi_deg = np.linspace(0, 360, 360)
    TV, DP = np.meshgrid(np.radians(theta_v_deg), np.radians(delta_phi_deg))
    TS = np.full_like(TV, np.radians(theta_s_deg))
    S = glint_stokes(TS, TV, DP, wind_speed=wind_speed, n_water=n_water)
    I, Q = S[..., 0], S[..., 1]
    with np.errstate(invalid="ignore", divide="ignore"):
        dolp = np.where(I > 0, np.abs(Q) / I, np.nan)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    ax = axes[0]
    im0 = ax.pcolormesh(delta_phi_deg, theta_v_deg, I.T, cmap="hot_r", shading="auto")
    fig.colorbar(im0, ax=ax, label="Glint BRF [1/sr]")
    ax.set_xlabel("Delta_phi (deg)")
    ax.set_ylabel("theta_v (deg)")
    ax.set_title(f"Glint intensity — theta_s={theta_s_deg}deg, W={wind_speed}m/s")
    ax = axes[1]
    im1 = ax.pcolormesh(delta_phi_deg, theta_v_deg, dolp.T, cmap="plasma", shading="auto", vmin=0, vmax=0.15)
    fig.colorbar(im1, ax=ax, label="DoLP")
    ax.set_xlabel("Delta_phi (deg)")
    ax.set_ylabel("theta_v (deg)")
    ax.set_title(f"Glint DoLP — theta_s={theta_s_deg}deg, W={wind_speed}m/s")
    fig.tight_layout()
    if output:
        fig.savefig(output, dpi=150)
    return fig

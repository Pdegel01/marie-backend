"""Cox-Munk sunglint model: slope distribution, DoLP, and Stokes vector simulation."""

from __future__ import annotations

import numpy as np

from polcal.modeling.geometry import (
    facet_tilt_angle,
    fresnel_coefficients,
    fresnel_mueller_matrix,
    incidence_angle,
)


def cox_munk_variance(wind_speed: float | np.ndarray) -> float | np.ndarray:
    """Return Cox-Munk slope variance σ² = 0.003 + 0.00512·W (Cox & Munk 1954)."""
    return 0.003 + 0.00512 * wind_speed


def cox_munk_slope_pdf(
    theta_n: np.ndarray,
    wind_speed: float | np.ndarray,
) -> np.ndarray:
    """Return the Cox-Munk PDF of facet tilt angle θ_n.

    P(θ_n) = exp(−tan²θ_n / σ²) / (π · σ² · cos⁴θ_n)
    """
    sigma2 = cox_munk_variance(wind_speed)
    return np.exp(-(np.tan(theta_n) ** 2) / sigma2) / (np.pi * sigma2 * np.cos(theta_n) ** 4)


def dolp_fresnel(
    theta_i: np.ndarray,
    n_water: float = 1.34,
) -> np.ndarray:
    """Return DoLP = (Rs − Rp) / (Rs + Rp) for Fresnel reflection of unpolarised light."""
    r_s, r_p = fresnel_coefficients(theta_i, n_water)
    Rs, Rp = r_s**2, r_p**2
    total = Rs + Rp
    return np.where(total > 0, (Rs - Rp) / total, 0.0)


def glint_reflectance(
    theta_s: np.ndarray,
    theta_v: np.ndarray,
    delta_phi: np.ndarray,
    wind_speed: float = 5.0,
    n_water: float = 1.34,
) -> np.ndarray:
    """Return the glint BRF: π · P(θ_n) · (Rs+Rp)/2 / (4·cosθ_s·cosθ_v·cos⁴θ_n)."""
    theta_i = incidence_angle(theta_s, theta_v, delta_phi)
    theta_n = facet_tilt_angle(theta_s, theta_v, delta_phi)
    r_s, r_p = fresnel_coefficients(theta_i, n_water)
    pdf = cox_munk_slope_pdf(theta_n, wind_speed)
    denom = 4.0 * np.cos(theta_s) * np.cos(theta_v) * np.cos(theta_n) ** 4
    return np.pi * pdf * (r_s**2 + r_p**2) / 2.0 / np.where(np.abs(denom) > 1e-10, denom, np.nan)


def glint_stokes(
    theta_s: np.ndarray,
    theta_v: np.ndarray,
    delta_phi: np.ndarray,
    wind_speed: float = 5.0,
    n_water: float = 1.34,
    I0: float = 1.0,
) -> np.ndarray:
    """Return the Stokes vector [I, Q, U, V] of sunglint weighted by Cox-Munk PDF.

    Output shape: (..., 4). Δφ = 0° is the specular direction.
    """
    theta_i = incidence_angle(theta_s, theta_v, delta_phi)
    theta_n = facet_tilt_angle(theta_s, theta_v, delta_phi)
    M = fresnel_mueller_matrix(theta_i, n_water)
    pdf = cox_munk_slope_pdf(theta_n, wind_speed)
    sun = np.array([I0, 0.0, 0.0, 0.0])
    S = M @ sun
    denom = 4.0 * np.cos(theta_s) * np.cos(theta_v) * np.cos(theta_n) ** 4
    weight = np.pi * pdf / np.where(np.abs(denom) > 1e-10, denom, np.nan)
    return S * weight[..., np.newaxis]

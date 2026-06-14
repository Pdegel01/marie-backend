"""Geometric computations: angles, Fresnel coefficients, Mueller matrices."""

from __future__ import annotations

import numpy as np


def scattering_angle(
    theta_s: np.ndarray,
    theta_v: np.ndarray,
    delta_phi: np.ndarray,
) -> np.ndarray:
    """Return the scattering angle Θ (rad).

    cos Θ = cos θ_s · cos θ_v − sin θ_s · sin θ_v · cos(Δφ)
    Convention: Δφ = 0° is the specular direction (same azimuth as the sun).
    """
    return np.arccos(
        np.cos(theta_s) * np.cos(theta_v)
        - np.sin(theta_s) * np.sin(theta_v) * np.cos(delta_phi)
    )


def incidence_angle(
    theta_s: np.ndarray,
    theta_v: np.ndarray,
    delta_phi: np.ndarray,
) -> np.ndarray:
    """Return the local angle of incidence θ_i = Θ/2 on the specular facet."""
    return scattering_angle(theta_s, theta_v, delta_phi) / 2.0


def facet_tilt_angle(
    theta_s: np.ndarray,
    theta_v: np.ndarray,
    delta_phi: np.ndarray,
) -> np.ndarray:
    """Return the tilt angle θ_n of the specular facet from the vertical.

    cos θ_n = (cos θ_s + cos θ_v) / (2 · cos θ_i)
    """
    theta_i = incidence_angle(theta_s, theta_v, delta_phi)
    cos_n = (np.cos(theta_s) + np.cos(theta_v)) / (2.0 * np.cos(theta_i))
    return np.arccos(np.clip(cos_n, -1.0, 1.0))


def fresnel_coefficients(
    theta_i: np.ndarray,
    n_water: float = 1.34,
) -> tuple[np.ndarray, np.ndarray]:
    """Return Fresnel amplitude coefficients (r_s, r_p) via Snell's law."""
    sin_t = np.sin(theta_i) / n_water
    cos_t = np.sqrt(1.0 - sin_t**2)
    cos_i = np.cos(theta_i)
    r_s = (cos_i - n_water * cos_t) / (cos_i + n_water * cos_t)
    r_p = (n_water * cos_i - cos_t) / (n_water * cos_i + cos_t)
    return r_s, r_p


def fresnel_mueller_matrix(
    theta_i: np.ndarray,
    n_water: float = 1.34,
) -> np.ndarray:
    """Return the 4×4 Fresnel Mueller matrix in the s-p basis. Output shape: (..., 4, 4)."""
    r_s, r_p = fresnel_coefficients(theta_i, n_water)
    Rs, Rp, rsp = r_s**2, r_p**2, r_s * r_p
    shape = np.shape(theta_i)
    M = np.zeros(shape + (4, 4))
    M[..., 0, 0] = (Rs + Rp) / 2
    M[..., 0, 1] = (Rs - Rp) / 2
    M[..., 1, 0] = (Rs - Rp) / 2
    M[..., 1, 1] = (Rs + Rp) / 2
    M[..., 2, 2] = rsp
    M[..., 3, 3] = rsp
    return M


def rotation_mueller_matrix(alpha: np.ndarray) -> np.ndarray:
    """Return the 4×4 Mueller rotation matrix for a polarisation frame rotation by alpha (rad)."""
    shape = np.shape(alpha)
    R = np.zeros(shape + (4, 4))
    R[..., 0, 0] = 1.0
    R[..., 1, 1] = np.cos(2 * alpha)
    R[..., 1, 2] = np.sin(2 * alpha)
    R[..., 2, 1] = -np.sin(2 * alpha)
    R[..., 2, 2] = np.cos(2 * alpha)
    R[..., 3, 3] = 1.0
    return R


def brewster_angle(n_water: float = 1.34) -> float:
    """Return the Brewster angle (rad): θ_B = arctan(n)."""
    return np.arctan(n_water)

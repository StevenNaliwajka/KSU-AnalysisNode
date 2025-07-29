import math


def calculate_epsilon_fw(epsilon_w0, epsilon_w_inf, f, tau_w, sigma_eff, epsilon_0, rho_s, rho_b, m_v):
    """
    Calculate the free water permittivity (ε_fw).

    Parameters:
    epsilon_w0 (float): Static permittivity of water (ε_w0)
    epsilon_w_inf (float): High-frequency permittivity of water (ε_w∞)
    f (float): Frequency (Hz)
    tau_w (float): Relaxation time of water (s)
    sigma_eff (float): Effective conductivity (S/m)
    epsilon_0 (float): Vacuum permittivity (F/m)
    rho_s (float): Particle density (g/cm³ or kg/m³)
    rho_b (float): Bulk density (g/cm³ or kg/m³)
    m_v (float): Volumetric water content (decimal)

    Returns:
    float: Free water permittivity (ε_fw)
    """
    # First term (Debye-like)
    term1 = (epsilon_w0 - epsilon_w_inf) / (1 + (2 * math.pi * f * tau_w) ** 2)
    # Second term (conductivity-related)
    term2 = (sigma_eff / (2 * math.pi * f * epsilon_0)) * ((rho_s - rho_b) / (rho_s * m_v))

    return term1 - term2


# Example usage
epsilon_w0 = 87.134  # Static permittivity of water
epsilon_w_inf = 4.9  # High-frequency permittivity of water
f = 500e6  # Frequency (Hz)
tau_w = 1e-9  # Relaxation time (s)
sigma_eff = 0.01  # Effective conductivity (S/m)
epsilon_0 = 8.854e-12  # Vacuum permittivity (F/m)
rho_s = 2.66  # Particle density (g/cm³)
rho_b = 1.5  # Bulk density (g/cm³)
m_v = 0.25  # Volumetric water content

epsilon_fw = calculate_epsilon_fw(epsilon_w0, epsilon_w_inf, f, tau_w, sigma_eff, epsilon_0, rho_s, rho_b, m_v)
print(f"ε_fw: {epsilon_fw}")

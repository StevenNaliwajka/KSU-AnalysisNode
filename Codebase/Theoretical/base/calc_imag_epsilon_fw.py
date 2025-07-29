import math


def calculate_imag_epsilon_fw(epsilon_w0, epsilon_w_inf, f, tau_w, sigma_eff, epsilon_0, rho_s, rho_b, m_v):
    """
    Calculate the imaginary component of free water permittivity (Im(ε_fw)).

    Parameters:
    epsilon_w0 (float): Static permittivity of water (ε_w0)
    epsilon_w_inf (float): High-frequency permittivity of water (ε_w∞)
    f (float): Frequency (Hz)
    tau_w (float): Relaxation time of water (s)
    sigma_eff (float): Effective conductivity (S/m)
    epsilon_0 (float): Permittivity of free space (F/m)
    rho_s (float): Particle density (g/cm³)
    rho_b (float): Bulk density (g/cm³)
    m_v (float): Volumetric water content (decimal)

    Returns:
    float: Imaginary component of free water permittivity (Im(ε_fw))
    """
    term1 = ((epsilon_w0 - epsilon_w_inf) * (2 * math.pi * f * tau_w)) / (1 + (2 * math.pi * f * tau_w)**2)
    term2 = (sigma_eff / (2 * math.pi * f * epsilon_0)) * ((rho_s - rho_b) / (rho_s * m_v))
    return -(term1 + term2)

# Example usage
epsilon_w0 = 87.134
epsilon_w_inf = 4.9
f = 491e6
tau_w = 1e-9
sigma_eff = 1.645
epsilon_0 = 8.854e-12
rho_s = 2.66
rho_b = 1.08
m_v = 0.25

epsilon_fw_imag = calculate_imag_epsilon_fw(epsilon_w0, epsilon_w_inf, f, tau_w, sigma_eff, epsilon_0, rho_s, rho_b, m_v)
print(f"Im(ε_fw): {epsilon_fw_imag}")

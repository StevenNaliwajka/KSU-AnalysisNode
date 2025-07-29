import numpy as np

def calculate_real_epsilon_m(rho_b, rho_s, epsilon_s, m_v, beta, epsilon_fw_real, k):
    """
    Calculate the real component of mixed permittivity (Re(ε_m)) safely.

    Parameters:
    rho_b (float): Bulk density (g/cm³)
    rho_s (float): Particle density (g/cm³)
    epsilon_s (float): Permittivity of soil solids (ε_s)
    m_v (float): Volumetric water content (decimal, e.g., 0.2 for 20%)
    beta (float): Shape factor
    epsilon_fw_real (float): Real component of free water permittivity (Re(ε_fw))
    k (float): Exponent

    Returns:
    float: Real component of mixed permittivity (Re(ε_m))
    """

    # --- Clamp to safe ranges ---
    rho_b = np.clip(rho_b, 0.1, 3.0)
    rho_s = np.clip(rho_s, 0.1, 5.0)
    epsilon_s = np.clip(epsilon_s, 1.0, 100.0)
    m_v = np.clip(m_v, 1e-6, 1.0)
    epsilon_fw_real = np.clip(epsilon_fw_real, 1e-6, 1e6)
    k = np.clip(k, 1e-6, 10)

    # --- Use np.power for stability ---
    soil_term = np.power(epsilon_s, k, dtype=np.float64) - 1
    water_term = np.power(m_v, beta, dtype=np.float64) * np.power(epsilon_fw_real, k, dtype=np.float64)

    term = 1 + (rho_b / rho_s) * soil_term + water_term - m_v
    return np.power(term, 1.0 / k, dtype=np.float64)

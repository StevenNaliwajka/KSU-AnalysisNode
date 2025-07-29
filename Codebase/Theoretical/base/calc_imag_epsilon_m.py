import numpy as np

def calculate_imag_epsilon_m(m_v, beta, epsilon_fw_imag, k):
    """
    Calculate the imaginary component of mixed permittivity (Im(ε_m)) safely.

    Parameters:
    m_v (float): Volumetric water content (decimal, e.g., 0.2 for 20%)
    beta (float): Shape factor
    epsilon_fw_imag (float): Imaginary component of free water permittivity (Im(ε_fw))
    k (float): Exponent

    Returns:
    float: Imaginary component of mixed permittivity (Im(ε_m))
    """

    # --- Clamp to safe ranges ---
    m_v = np.clip(m_v, 1e-6, 1.0)                  # moisture between 0.000001 and 1
    epsilon_fw_imag = np.clip(epsilon_fw_imag, 1e-6, 1e6)  # avoid zero or absurdly large permittivity
    k = np.clip(k, 1e-6, 10)                       # prevent divide-by-zero or insane powers

    # --- Use np.power for stable exponentiation ---
    term = np.power(m_v, beta, dtype=np.float64) * np.power(epsilon_fw_imag, k, dtype=np.float64)
    return np.power(term, 1.0 / k, dtype=np.float64)

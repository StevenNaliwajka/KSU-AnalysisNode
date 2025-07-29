def calculate_epsilon_m(rho_b, rho_s, epsilon_s, m_v, beta, epsilon_fw, k):
    """
    Calculate the mixed permittivity ε_m^k.

    Parameters:
    rho_b (float): Bulk density (g/cm³ or kg/m³)
    rho_s (float): Particle density (g/cm³ or kg/m³)
    epsilon_s (float): Permittivity of soil solids (ε_s)
    m_v (float): Volumetric water content (decimal, e.g., 0.2 for 20%)
    beta (float): Shape factor (unitless)
    epsilon_fw (float): Permittivity of free water (ε_fw)
    k (float): Exponent applied to permittivity terms

    Returns:
    float: Mixed permittivity (ε_m^k)
    """
    return 1 + (rho_b / rho_s) * ((epsilon_s ** k) - 1) + (m_v ** beta) * (epsilon_fw ** k) - m_v

# Example usage
rho_b = 1.5        # Bulk density (g/cm³)
rho_s = 2.66       # Particle density (g/cm³)
epsilon_s = 4.7    # Permittivity of soil solids
m_v = 0.25         # Volumetric water content (25%)
beta = 0.65        # Shape factor
epsilon_fw = 80    # Permittivity of free water
k = 0.65           # Exponent

epsilon_m_k = calculate_epsilon_m_k(rho_b, rho_s, epsilon_s, m_v, beta, epsilon_fw, k)
print(f"ε_m^k: {epsilon_m_k}")

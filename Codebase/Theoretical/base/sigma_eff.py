def calculate_sigma_eff(rho_b, S, C):
    """
    Calculate the effective conductivity (σ_eff).

    Parameters:
    rho_b (float): Bulk density (g/cm³ or kg/m³)
    S (float): Sand percentage (%)
    C (float): Clay percentage (%)

    Returns:
    float: Effective conductivity (σ_eff) in S/m
    """
    return 1.645 + 1.939 * rho_b - 0.02013 * S + 0.01594 * C

# Example usage
rho_b = 1.5   # Bulk density (g/cm³)
S = 12.0      # Sand content (%)
C = 15.0      # Clay content (%)
sigma_eff = calculate_sigma_eff(rho_b, S, C)
print(f"σ_eff: {sigma_eff}")

def calculate_epsilon_s(rho_s):
    """
    Calculate the permittivity of soil solids (ε_s).

    Parameters:
    rho_s (float): Particle density (g/cm³ or kg/m³)

    Returns:
    float: Permittivity of soil solids (ε_s)
    """
    return (1.01 + 0.44 * rho_s)**2 - 0.062

# Example usage
rho_s = 2.66  # Particle density (g/cm³)
epsilon_s = calculate_epsilon_s(rho_s)
print(f"ε_s: {epsilon_s}")

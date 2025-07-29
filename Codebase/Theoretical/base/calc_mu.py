def calculate_mu(mu_r, mu_0=4*math.pi*1e-7):
    """
    Calculate magnetic permeability (μ).

    Parameters:
    mu_r (float): Relative permeability (dimensionless)
    mu_0 (float): Permeability of free space (H/m), default 4π×10⁻⁷

    Returns:
    float: Magnetic permeability (H/m)
    """
    return mu_r * mu_0

# Example usage
mu_r = 1.0  # Relative permeability (usually ~1 for soil)
mu = calculate_mu(mu_r)
print(f"μ: {mu} H/m")

def calculate_pl_soil(alpha, d_soil):
    """
    Calculate the path loss through soil (PL_soil).

    Parameters:
    alpha (float): Attenuation coefficient (Np/m)
    d_soil (float): Depth of soil path (m)

    Returns:
    float: Soil path loss (PL_soil) in dB
    """
    return 8.686 * alpha * d_soil

# Example usage
alpha = 0.5    # Attenuation coefficient (Np/m)
d_soil = 1.0   # Soil depth (m)
pl_soil = calculate_pl_soil(alpha, d_soil)
print(f"PL_soil: {pl_soil} dB")

def calculate_pl_total(PL_air, PL_soil):
    """
    Calculate total path loss as the sum of air and soil path loss.

    Parameters:
    PL_air (float): Path loss through air (dB)
    PL_soil (float): Path loss through soil (dB)

    Returns:
    float: Total path loss (dB)
    """
    return PL_air + PL_soil

# Example usage
PL_air = 60    # Path loss in air (dB)
PL_soil = 20   # Path loss in soil (dB)

PL_total = calculate_pl_total(PL_air, PL_soil)
print(f"PL_total: {PL_total} dB")

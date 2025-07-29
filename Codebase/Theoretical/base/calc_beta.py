def calculate_beta(S, C, epsilon_fw):
    """
    Calculate the shape factor (β).

    Parameters:
    S (float): Sand percentage (%)
    C (float): Clay percentage (%)
    epsilon_fw (float): Permittivity of free water (ε_fw)

    Returns:
    float: Shape factor (β)
    """
    numerator = 100 * S * epsilon_fw
    denominator = 1.33797 - 0.603 * S - 0.166 * C
    return numerator / denominator

# Example usage
S = 12.0       # Sand content (%)
C = 15.0       # Clay content (%)
epsilon_fw = 80  # Example free water permittivity
beta = calculate_beta(S, C, epsilon_fw)
print(f"β: {beta}")

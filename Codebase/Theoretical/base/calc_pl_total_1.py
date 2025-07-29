def calculate_pl_total1(P_t, G_t, G_r, RSSI):
    """
    Calculate total path loss (PL_total).

    Parameters:
    P_t (float): Transmit power (dBm)
    G_t (float): Transmitter antenna gain (dBi)
    G_r (float): Receiver antenna gain (dBi)
    RSSI (float): Received signal strength (dBm)

    Returns:
    float: Total path loss (PL_total) in dB
    """
    return P_t + G_t + G_r - RSSI

# Example usage
P_t = 10     # Transmit power (dBm)
G_t = 0      # Transmit gain (dBi)
G_r = 0      # Receive gain (dBi)
RSSI = -80   # Received signal strength (dBm)

PL_total = calculate_pl_total1(P_t, G_t, G_r, RSSI)
print(f"PL_total: {PL_total} dB")
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def fetch_sample_data(num_points: int) -> pd.DataFrame:
    """
    Generates a synthetic time series dataset simulating 15-minute intervals
    with a structural change (SR event).

    Args:
        num_points: The number of data points to generate.

    Returns:
        A pandas DataFrame with a DatetimeIndex and a 'Signal' column.
    """
    print(f"Generating {num_points} data points...")

    start_date = datetime(2025, 10, 1, 9, 0, 0)

    # Create a DatetimeIndex that increments by 15 minutes
    dates = [start_date + timedelta(minutes=i * 15) for i in range(num_points)]

    # 1. Generate normal noise
    np.random.seed(42)  # for reproducibility
    noise = np.random.normal(0, 0.5, num_points)

    # 2. Create a base signal
    base_signal = np.cumsum(noise) * 0.5

    # 3. Inject a structural shift (SR event) roughly in the middle
    shift_point = num_points // 2
    shift_magnitude = 15.0  # Large, sustained shift

    # Add the shift to the second half of the data
    base_signal[shift_point:] += shift_magnitude

    # Combine into a DataFrame
    data = pd.DataFrame({'Signal': base_signal}, index=dates)

    return data
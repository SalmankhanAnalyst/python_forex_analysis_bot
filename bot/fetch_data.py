import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def fetch_sample_data(num_points: int = 250) -> pd.DataFrame:
    """
    Generates mock time-series data representing a 'signal' with a synthetic
    structural change (SR event).

    This simulates fetching data from an external source (like an API or database).

    Args:
        num_points: The number of data points to generate.

    Returns:
        A pandas DataFrame with 'Timestamp' and 'Signal' columns.
    """
    print(f"Generating {num_points} data points...")

    # 1. Generate Timestamps
    start_date = datetime(2023, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(num_points)]

    # 2. Generate a base signal (random walk)
    np.random.seed(42)
    base_signal = np.cumsum(np.random.normal(0, 0.5, num_points))

    # 3. Introduce a 'Structural Shift' (the event we want to detect)
    shift_index = int(num_points * 0.65) # Introduce shift about 2/3rds of the way
    shift_magnitude = 15.0
    base_signal[shift_index:] += (shift_magnitude + np.cumsum(np.random.normal(0, 0.2, num_points - shift_index)))

    # 4. Add some noise
    signal = base_signal + np.random.normal(0, 1.0, num_points)

    # 5. Create the DataFrame
    df = pd.DataFrame({
        'Timestamp': dates,
        'Signal': signal
    })

    df.set_index('Timestamp', inplace=True)
    return df

# Example usage if run directly
if __name__ == '__main__':
    data_df = fetch_sample_data()
    print("\nSample Data Head:")
    print(data_df.head())
    print("\nSample Data Tail:")
    print(data_df.tail())
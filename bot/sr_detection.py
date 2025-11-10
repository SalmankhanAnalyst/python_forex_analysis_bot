import pandas as pd
import numpy as np

def detect_sr_events(df: pd.DataFrame, window: int = 30, z_score_threshold: float = 3.5) -> pd.DataFrame:
    """
    Detects 'Structural Rate' (SR) events based on sudden changes in the
    rolling mean relative to the rolling standard deviation (Z-score anomaly).

    Args:
        df: The input DataFrame containing a 'Signal' column (indexed by time).
        window: The rolling window size for calculating statistics.
        z_score_threshold: The Z-score cutoff for triggering an event.

    Returns:
        A DataFrame containing only the rows identified as SR events.
    """
    if 'Signal' not in df.columns:
        raise ValueError("DataFrame must contain a 'Signal' column.")

    print(f"Applying SR detection with window={window} and threshold={z_score_threshold}...")

    # 1. Calculate rolling statistics
    df['Rolling_Mean'] = df['Signal'].rolling(window=window).mean()
    df['Rolling_Std'] = df['Signal'].rolling(window=window).std()

    # 2. Calculate the difference from the rolling mean
    df['Difference'] = df['Signal'] - df['Rolling_Mean']

    # 3. Calculate Z-Score (Difference divided by Rolling Standard Deviation)
    # Adding a small epsilon to avoid division by zero
    epsilon = 1e-6
    df['Z_Score'] = df['Difference'] / (df['Rolling_Std'] + epsilon)

    # 4. Identify events where the absolute Z-Score exceeds the threshold
    df['Is_Event'] = (df['Z_Score'].abs() > z_score_threshold)

    # Filter for the detected events
    sr_events = df[df['Is_Event']].copy()
    print(f"Detected {len(sr_events)} potential SR events.")

    return sr_events[['Signal', 'Z_Score']]

# Example usage (requires mock data)
if __name__ == '__main__':
    # In a real setup, you would import and use fetch_sample_data
    # from the companion file, but for self-containment, we mock it here.
    data = {'Signal': np.random.randn(100) + np.concatenate([np.zeros(70), np.full(30, 8)])}
    mock_df = pd.DataFrame(data, index=pd.to_datetime(pd.date_range(start='2023-01-01', periods=100)))

    events = detect_sr_events(mock_df, window=10)
    print("\nDetected Events Head:")
    print(events.head())
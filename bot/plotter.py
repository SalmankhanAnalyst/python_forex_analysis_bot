import matplotlib.pyplot as plt
import pandas as pd
import os  # Import the os module for path manipulation


def plot_results(data_df: pd.DataFrame, sr_events_df: pd.DataFrame, output_filename: str = None):
    """
    Visualizes the main time series data and highlights the detected SR events.

    Args:
        data_df: The full time-series data DataFrame.
        sr_events_df: The DataFrame containing only the detected SR event points.
        output_filename: Optional filename (e.g., 'sr_analysis.png') to save the plot.
    """
    if data_df.empty:
        print("Error: Input data DataFrame is empty.")
        return

    print("Generating visualization...")

    # Check for the required column
    if 'Signal' not in data_df.columns:
        print("Error: 'Signal' column not found in data_df.")
        return

    # Initialize the plot
    plt.figure(figsize=(14, 7))
    # Using a common style that supports both display and saving
    plt.style.use('seaborn-v0_8-darkgrid')

    # 1. Plot the main signal
    plt.plot(data_df.index, data_df['Signal'], label='Original Signal', color='#3498db', linewidth=1.5)

    # 2. Highlight the detected SR events
    if not sr_events_df.empty:
        # Use the index of the events DataFrame for the x-axis (Timestamp)
        event_timestamps = sr_events_df.index
        event_signals = sr_events_df['Signal']

        plt.scatter(event_timestamps, event_signals,
                    color='#e74c3c',  # Red for high contrast
                    marker='o',
                    s=100,  # Size of the marker
                    zorder=5,  # Ensure markers are drawn on top
                    label='SR Event Detected')

    # 3. Add titles and labels
    plt.title('Time Series Data with Structural Rate (SR) Event Detection', fontsize=16, fontweight='bold')
    plt.xlabel('Timestamp', fontsize=12)
    plt.ylabel('Signal Value', fontsize=12)
    plt.legend(loc='upper left')
    plt.xticks(rotation=45)
    plt.tight_layout()  # Adjust plot to ensure everything fits

    # 4. Save the plot if a filename is provided
    if output_filename:
        # --- DEBUGGING STEP: Print the path before saving ---
        absolute_path = os.path.abspath(output_filename)
        print(f"Attempting to save chart to: {absolute_path}")

        try:
            # Save before showing the plot for better stability
            plt.savefig(output_filename, dpi=300)

            print(f"Chart successfully saved to: {absolute_path}")

        except Exception as e:
            # --- CRITICAL FIX: Print the full exception ---
            print(f"CRITICAL ERROR: Failed to save chart to disk.")
            print(f"Reason: {e}")
            print("Please check file permissions for the target folder.")

    # 5. Show the plot interactively (optional, but useful for debugging/immediate view)
    plt.show()


# Example workflow to demonstrate usage of all three files
if __name__ == '__main__':
    try:
        import sys
        import os

        # Ensure we can import components for the example
        # Adjust path dynamically for execution environment
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.append(current_dir)
        parent_dir = os.path.dirname(current_dir)
        if parent_dir not in sys.path:
            sys.path.append(parent_dir)

        # Assuming fetch_data is one level up relative to the current file (bot/plotter.py)
        # and sr_detection is a sibling in the 'bot' folder.
        from fetch_data import fetch_sample_data
        from sr_detection import detect_sr_events

        # 1. Fetch Data
        data = fetch_sample_data(num_points=300)

        # 2. Detect Events
        events = detect_sr_events(data, window=40, z_score_threshold=3.0)

        # 3. Plot Results
        plot_results(data, events, output_filename='example_sr_analysis.png')

    except ImportError as e:
        print(f"Could not complete full example workflow due to missing dependency or module import: {e}")
        print("Ensure 'fetch_data.py' and 'bot/sr_detection.py' are in the correct path structure.")
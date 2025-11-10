import sys
import os
import time
from datetime import datetime

# --- PATH FIX START ---
# Get the absolute path of the directory where this script is located (the root of the project).
script_dir = os.path.dirname(os.path.abspath(__file__))

# Add the script's directory to sys.path so Python can find sibling modules
# (if they existed) and packages (bot).
if script_dir not in sys.path:
    sys.path.append(script_dir)
# --- PATH FIX END ---

try:
    # Modules are imported from the 'bot' package
    from bot.fetch_data import fetch_sample_data
    from bot.sr_detection import detect_sr_events
    from bot.plotter import plot_results

except ImportError as e:
    print(f"Error importing modules even after path fix: {e}")
    print("Please double-check the file names and structure (bot/fetch_data.py, etc.).")
    sys.exit(1)


def main():
    """
    Orchestrates the data analysis pipeline:
    1. Fetches (generates) the sample time-series data.
    2. Detects Structural Rate (SR) events using Z-score anomaly detection.
    3. Plots the results, highlighting the detected events and saves the chart with a unique timestamped filename.
    """
    print("--- Starting SR Event Detection Pipeline ---")

    # --- Configuration ---
    NUM_POINTS = 300
    WINDOW_SIZE = 40
    Z_SCORE_THRESHOLD = 3.0

    # --- Generate Unique Filename ---
    # Creates a string like '20251110_205730'
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'sr_detection_{timestamp_str}.png'

    # Construct the absolute output path: This ensures the chart is saved
    # next to main.py regardless of the current working directory (CWD).
    CHART_OUTPUT_FILE = os.path.join(script_dir, filename)

    # 1. Fetch Data
    try:
        data_df = fetch_sample_data(num_points=NUM_POINTS)
        if data_df.empty:
            print("Pipeline aborted: Data fetching returned an empty DataFrame.")
            return
        print(f"Data ready (Shape: {data_df.shape}).")

        # 2. Detect Events
        events_df = detect_sr_events(
            df=data_df.copy(),
            window=WINDOW_SIZE,
            z_score_threshold=Z_SCORE_THRESHOLD
        )
        print(f"Detection complete. Found {len(events_df)} significant events.")

        # 3. Plot Results
        # Passing the absolute output filename to plotter.py
        plot_results(data_df, events_df, output_filename=CHART_OUTPUT_FILE)

        print("--- Pipeline Finished ---")

    except Exception as e:
        print(f"\nAn unexpected error occurred during execution: {e}")
        # Optionally, you could add more detailed traceback here for debugging


if __name__ == "__main__":
    main()
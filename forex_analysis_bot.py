import yfinance as yf
import pandas as pd
import numpy as np
import mplfinance as mpf
from scipy.signal import argrelextrema

# --- Configuration ---
TICKER = "AUDCAD=X"
INTERVAL = "15m"
PERIOD = "60d"  # Fetch last 60 days of data
ATR_PERIOD = 14  # Standard ATR period
ATR_MULTIPLIER = 1.0  # Multiplier for filtering noise near S/R levels


def fetch_data():
    """Fetches historical OHLCV data using yfinance."""
    print(f"Fetching {TICKER} {INTERVAL} data for the last {PERIOD}...")
    data = yf.download(TICKER, interval=INTERVAL, period=PERIOD)
    if data.empty:
        raise ValueError(f"Could not fetch data for {TICKER}. Check ticker and internet connection.")
    print(f"Data fetched (Rows: {len(data)}).")
    return data


def calculate_atr(data, period=ATR_PERIOD):
    """Calculates the Average True Range (ATR)."""
    # Calculate True Range (TR)
    data['High-Low'] = data['High'] - data['Low']
    data['High-PrevClose'] = abs(data['High'] - data['Close'].shift(1))
    data['Low-PrevClose'] = abs(data['Low'] - data['Close'].shift(1))
    data['TR'] = data[['High-Low', 'High-PrevClose', 'Low-PrevClose']].max(axis=1)

    # Calculate ATR (Exponential Moving Average of TR)
    data['ATR'] = data['TR'].ewm(span=period, adjust=False).mean()
    return data['ATR'].iloc[-1]  # Return the latest ATR value


def get_sr_levels(data, atr_multiplier=ATR_MULTIPLIER):
    """
    Identifies significant Support and Resistance levels using local extrema
    and filters them based on ATR for noise reduction.
    """
    levels = []

    # Identify local extrema (pivots)
    # 5-period lookback/lookforward to identify a pivot
    data['min'] = data.iloc[argrelextrema(data.Low.values, np.less_equal, order=5)[0]]['Low']
    data['max'] = data.iloc[argrelextrema(data.High.values, np.greater_equal, order=5)[0]]['High']

    # Get latest ATR
    latest_atr = calculate_atr(data)
    atr_filter = latest_atr * atr_multiplier

    # Combine all pivot values
    all_pivots = data['min'].dropna().tolist() + data['max'].dropna().tolist()
    all_pivots.sort()

    if not all_pivots:
        return levels

    # Cluster pivots into S/R levels using ATR as the tolerance
    current_level = all_pivots[0]
    levels.append(current_level)

    for pivot in all_pivots:
        # If the pivot is significantly far from the last level (outside ATR filter)
        if pivot > current_level + atr_filter:
            current_level = pivot
            levels.append(current_level)

    # Clean up and return unique levels
    return sorted(list(set(round(l, 5) for l in levels)))


def get_trendlines(data):
    """
    Identifies simple uptrend (support) and downtrend (resistance) lines
    by connecting major recent pivot points.
    """
    # Identify major swing high/low points (e.g., looking back 20 periods)
    pivot_order = 20

    data['Low_Pivot'] = data.iloc[argrelextrema(data.Low.values, np.less_equal, order=pivot_order)[0]]['Low']
    data['High_Pivot'] = data.iloc[argrelextrema(data.High.values, np.greater_equal, order=pivot_order)[0]]['High']

    # Get the last two major low pivots for uptrend support
    low_pivots = data['Low_Pivot'].dropna().tail(2)
    # Get the last two major high pivots for downtrend resistance
    high_pivots = data['High_Pivot'].dropna().tail(2)

    trendlines = []

    # 1. Uptrend Support Line (connecting last two major lows)
    if len(low_pivots) >= 2:
        # Use simple linear regression (line through two points)
        p1 = low_pivots.index[0], low_pivots.iloc[0]
        p2 = low_pivots.index[-1], low_pivots.iloc[-1]

        # Trendline is drawn from the first pivot to the end of the chart
        trendlines.append(
            dict(
                name='Uptrend Support',
                start=p1,
                end=p2,
                color='green',
                style='--',
                linewidth=1.5
            )
        )

    # 2. Downtrend Resistance Line (connecting last two major highs)
    if len(high_pivots) >= 2:
        p1 = high_pivots.index[0], high_pivots.iloc[0]
        p2 = high_pivots.index[-1], high_pivots.iloc[-1]

        trendlines.append(
            dict(
                name='Downtrend Resistance',
                start=p1,
                end=p2,
                color='red',
                style='--',
                linewidth=1.5
            )
        )

    return trendlines


def plot_analysis(data, sr_levels, trendlines):
    """Plots the candlestick chart with S/R levels and Trendlines overlaid."""

    apds = []

    # --- 1. S/R Horizontal Lines (A-Level Lines) ---
    print(f"Detected Support/Resistance Levels: {sr_levels}")

    hlines = dict(
        hlines=sr_levels,
        colors='grey',
        linestyle='-',
        linewidth=1,
        alpha=0.6,
        tline_use='low',
        tline_label_display='all'
    )

    apds.append(mpf.make_addplot(hlines, panel=0))

    # --- 2. Trendlines (Segments) ---
    line_segments = []
    for line in trendlines:
        line_segments.append([line['start'], line['end']])
        print(f"Detected Trendline: {line['name']} (From {line['start'][1]:.5f} to {line['end'][1]:.5f})")

    if line_segments:
        apds.append(mpf.make_addplot(line_segments, panel=0, type='line',
                                     color=[l['color'] for l in trendlines],
                                     linestyle=[l['style'] for l in trendlines],
                                     linewidth=[l['linewidth'] for l in trendlines]))

    # --- 3. Plotting ---
    file_name = f"{TICKER.replace('=', '_')}_analysis.png"

    mpf.plot(
        data,
        type='candle',
        style='yahoo',
        title=f'{TICKER} {INTERVAL} Chart Analysis',
        ylabel='Price (Close)',
        addplot=apds,
        figscale=1.5,
        savefig=file_name
    )
    print(f"\nAnalysis complete. Chart saved to: {file_name}")


def run_analysis():
    """Main execution function for the Forex Analysis Bot."""
    try:
        data = fetch_data()

        sr_levels = get_sr_levels(data.copy())
        trendlines = get_trendlines(data.copy())

        plot_analysis(data, sr_levels, trendlines)

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during analysis: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    run_analysis()
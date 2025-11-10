AUDCAD 15m Forex Analysis Bot

This project provides a Python-based analysis bot for the AUD/CAD Forex pair, focusing on identifying key Support/Resistance (S/R) levels and Trendlines on the 15-minute (15m) chart.

The core analysis logic is contained within forex_analysis_bot.py, which fetches live data using yfinance and applies dynamic, ATR-based clustering for S/R detection and linear regression for trendline analysis.

🚀 Setup and Installation

Prerequisites

You must have Python 3.13+ installed.

1. Clone the Repository

git clone <https://github.com/SalmankhanAnalyst/python_forex_analysis_bot>
cd audcad-trendline-bot-01



2. Create a Virtual Environment (Recommended)

# Create environment
python -m venv venv 

# Activate environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate



3. Install Dependencies

All required packages are listed in requirements.txt.

pip install -r requirements.txt



⚙️ How to Run the Bot

There are two main scripts:

A. Run the Forex Analysis Bot (Live Data)

This script downloads live 15-minute AUDCAD data and generates a full technical analysis chart.

python forex_analysis_bot.py



Output: The script will print the detected S/R levels and save the chart as audcad_analysis.png in the project root directory.

B. Run the Structural Change (SR) Detector (Synthetic Data)

This script runs a parameter sweep on mock time-series data to test the performance of the Structural Rate (SR) event detection logic across different sensitivity settings.

python main.py



Output: This script will generate multiple charts (e.g., sr_detection_20251110_210530.png) in the project root, allowing you to compare detection performance.




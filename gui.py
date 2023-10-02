# Stock Analysis - Graphical User Interface
# The GUI provides a link between the inference engine and knowledge base that the user can interact with
# The GUI is known as gui.py

# import necessary libraries and modules
import tkinter as tk
from tkinter import ttk
from tkinter import font
from knowledge_base import fetch_data
from inference_engine import (calculate_mean_daily_return,
                              calculate_annualized_return,
                              calculate_daily_volatility,
                              calculate_annualized_volatility,
                              calculate_sma,
                              calculate_ema,
                              calculate_beta,
                              calculate_macd,
                              calculate_rsi,
                              calculate_bollinger_bands,
                              calculate_stochastic_oscillator,
                              calculate_standard_deviation,
                              calculate_sharpe_ratio,
                              calculate_sortino_ratio,
                              )


# Define a function to download stock data and perform various calculations
def download_and_calculate():
    # Remove user manual label
    user_manual_label.grid_remove()

    # Get user input
    symbol = stock_symbol_entry.get()
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    market_symbol = market_symbol_entry.get()

    # Fetch data using user input
    data = fetch_data(symbol, start_date, end_date)
    if market_symbol:
        market_data = fetch_data(market_symbol, start_date, end_date)
    else:
        market_data = None

    # Perform calculations from Inference Engine from fetched data from the Knowledge Base
    mean_daily_return = calculate_mean_daily_return(data)
    annualized_return = calculate_annualized_return(mean_daily_return)
    daily_volatility = calculate_daily_volatility(data)
    annualized_volatility = calculate_annualized_volatility(daily_volatility)
    sma_50 = calculate_sma(data, 50)
    ema_50 = calculate_ema(data, 50)
    beta = calculate_beta(data, market_data)
    macd = calculate_macd(data)
    rsi_14 = calculate_rsi(data)
    bollinger_upper, bollinger_lower = calculate_bollinger_bands(data)
    stochastic_oscillator = calculate_stochastic_oscillator(data)
    standard_deviation = calculate_standard_deviation(data)
    sharpe_ratio = calculate_sharpe_ratio(mean_daily_return, daily_volatility)
    sortino_ratio = calculate_sortino_ratio(mean_daily_return, data)

    # Display calculation results in a grid
    results = {
        "Mean daily return": mean_daily_return,
        "Annualized return": annualized_return,
        "Daily volatility": daily_volatility,
        "Annualized volatility": annualized_volatility,
        "50-day SMA": sma_50.iloc[-1],
        "50-day EMA": ema_50.iloc[-1],
        "Beta": beta,
        "MACD": macd.iloc[-1],
        "14-day RSI": rsi_14.iloc[-1],
        "Bollinger Upper": bollinger_upper.iloc[-1],
        "Bollinger Lower": bollinger_lower.iloc[-1],
        "Stochastic Oscillator": stochastic_oscillator.iloc[-1],
        "Standard Deviation": standard_deviation,
        "Sharpe Ratio": sharpe_ratio,
        "Sortino Ratio": sortino_ratio
    }

    # Populate the grid with the calculated results
    for i, (key, value) in enumerate(results.items()):
        ttk.Label(calculation_results_frame, text=f"{key}: {value:.4f}").grid(row=i, column=0, sticky="w")

    # Add a daily return column to the data
    data['Daily Return'] = data['Adj Close'].pct_change()

    # Display fetched data from the Knowledge Base in a grid
    for i, col in enumerate(data.columns):
        ttk.Label(data_results_frame, text=col).grid(row=0, column=i)

    for row in range(data.shape[0]):
        for col in range(data.shape[1]):
            value = data.iloc[row, col]
            if col != data.columns.get_loc('Volume'):
                value = f"{value:.2f}"
            else:
                value = f"{int(value):,d}"
            ttk.Label(data_results_frame, text=value).grid(row=row + 1, column=col)


root = tk.Tk()
root.title("Finance Data Analysis")

# Set root window to full screen
root.geometry("1000x800")

# Create a frame to hold input fields and labels
input_fields_frame = ttk.Frame(root)
input_fields_frame.grid(row=0, column=0, padx=(10, 0), pady=(10, 0))

# Create input fields and labels
stock_symbol_label = ttk.Label(input_fields_frame, text="Stock Symbol:")
stock_symbol_entry = ttk.Entry(input_fields_frame)
start_date_label = ttk.Label(input_fields_frame, text="Start Date (YYYY-MM-DD):")
start_date_entry = ttk.Entry(input_fields_frame)
end_date_label = ttk.Label(input_fields_frame, text="End Date (YYYY-MM-DD):")
end_date_entry = ttk.Entry(input_fields_frame)
market_symbol_label = ttk.Label(input_fields_frame, text="Market Symbol:")
market_symbol_entry = ttk.Entry(input_fields_frame)
download_button = ttk.Button(input_fields_frame, text="Download and Calculate", command=download_and_calculate)

# Grid layout for input fields and labels (inside input_fields_frame)
stock_symbol_label.grid(row=0, column=0, padx=(10, 0), pady=(10, 0))
stock_symbol_entry.grid(row=0, column=1, padx=10, pady=(10, 0))
start_date_label.grid(row=1, column=0, padx=(10, 0), pady=10)
start_date_entry.grid(row=1, column=1, padx=10, pady=10)
end_date_label.grid(row=2, column=0, padx=(10, 0), pady=10)
end_date_entry.grid(row=2, column=1, padx=10, pady=10)
market_symbol_label.grid(row=3, column=0, padx=(10, 0), pady=10)
market_symbol_entry.grid(row=3, column=1, padx=10, pady=10)
download_button.grid(row=4, column=0, columnspan=2, pady=10)

# Configure rows and columns to center the widgets
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_columnconfigure(2, weight=1)

# Calculation results frame
calculation_results_frame = ttk.Frame(root)
calculation_results_frame.grid(row=0, column=1, rowspan=5, padx=(10, 0), pady=(10, 0))

# Data results frame
data_results_frame = ttk.Frame(root)
data_results_frame.grid(row=5, column=1, columnspan=3, padx=10, pady=(0, 10))

# Create a user manual label
user_manual_text = (
    "Welcome to the Finance Data Analysis App!\n\n"
    "To get started, please follow these steps:\n"
    "1. Enter the stock symbol in the 'Stock Symbol' field e.g. TSLA for Tesla Inc.\n"
    "2. Enter the start date in the 'Start Date' field.\n"
    "3. Enter the end date in the 'End Date' field.\n"
    "4. Enter a market symbol in the 'Market Symbol' field, this is to compare values against the market e.g ^NSD for "
    "Nasdaq.\n"
    "5. Click the 'Download and Calculate' button.\n\n"
    "The app will fetch the data and perform various financial calculations."
)

user_manual_label = tk.Label(input_fields_frame, text=user_manual_text, wraplength=300, justify=tk.LEFT)
user_manual_label.grid(row=5, column=0, columnspan=2, pady=10)

# Set a light theme
root.configure(bg="#f0f0f0")

style = ttk.Style()
style.theme_use("clam")
style.configure('TFrame', background='#f0f0f0')
style.configure('TButton', background='#e5e5e5', foreground='#000000', activebackground='#e5e5e5',
                activeforeground='#000000', bordercolor="#e5e5e5", lightcolor="#e5e5e5", darkcolor="#e5e5e5")
style.configure('TLabel', background='#f0f0f0', foreground='#000000')
style.configure('TEntry', fieldbackground='#ffffff', foreground='#000000', insertbackground='#000000',
                bordercolor="#e5e5e5", lightcolor="#e5e5e5", darkcolor="#e5e5e5")

# Set font for labels, buttons and entries
label_font = font.Font(family="Helvetica", size=10)
entry_font = font.Font(family="Helvetica", size=10)
button_font = font.Font(family="Helvetica", size=10)
manual_font = font.Font(family="Helvetica", size=10, weight="bold")

# Apply font to widgets
style.configure('TLabel', font=label_font)
style.configure('TEntry', font=entry_font)
style.configure('TButton', font=button_font)

user_manual_label.configure(font=manual_font)


root.mainloop()

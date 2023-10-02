# Stock Analysis - Inference Engine
# The inference engine performs the calculations on the data from the knowledge base
# The inference engine is known as inference_engine.py

# import necessary libraries
import numpy as np
import pandas as pd


# Function to calculate mean daily return of a stock
def calculate_mean_daily_return(data):
    data['Daily Return'] = data['Adj Close'].pct_change()
    mean_daily_return = data['Daily Return'].mean()
    return mean_daily_return


# Function to calculate annualized return of a stock
def calculate_annualized_return(mean_daily_return):
    return (1 + mean_daily_return) ** 252 - 1


# Function to calculate daily volatility of a stock
def calculate_daily_volatility(data):
    return data['Daily Return'].std()


# Function to calculate annualized volatility of a stock
def calculate_annualized_volatility(daily_volatility):
    return daily_volatility * np.sqrt(252)


# Function to calculate simple moving average (SMA) of a stock
def calculate_sma(data, window):
    return data['Adj Close'].rolling(window=window).mean()


# Function to calculate exponential moving average (EMA) of a stock
def calculate_ema(data, window):
    return data['Adj Close'].ewm(span=window, adjust=False).mean()


# Function to calculate beta of a stock compared to a market index
def calculate_beta(stock_data, market_data):
    if market_data is None:
        return None
    stock_returns = stock_data['Adj Close'].pct_change()
    market_returns = market_data['Adj Close'].pct_change()
    return stock_returns.cov(market_returns) / market_returns.var()


# Function to calculate moving average convergence/divergence (MACD) of a stock
def calculate_macd(data):
    ema_12 = calculate_ema(data, 12)
    ema_26 = calculate_ema(data, 26)
    return ema_12 - ema_26


# Function to calculate relative strength index (RSI) of a stock
def calculate_rsi(data, window=14):
    delta = data['Adj Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


# Function to calculate bollinger bands of a stock
def calculate_bollinger_bands(data, window=20):
    sma = calculate_sma(data, window)
    std = data['Adj Close'].rolling(window=window).std()
    upper_band = sma + (2 * std)
    lower_band = sma - (2 * std)
    return upper_band, lower_band


# Function to calculate stochastic oscillator of a stock
def calculate_stochastic_oscillator(data, window=14):
    low_min = data['Low'].rolling(window=window).min()
    high_max = data['High'].rolling(window=window).max()
    k = ((data['Close'] - low_min) / (high_max - low_min)) * 100
    return k


# Function to calculate standard deviation of a stock
def calculate_standard_deviation(data):
    return data['Adj Close'].std()


# Function to calculate sharpe ratio of a stock
def calculate_sharpe_ratio(mean_daily_return, daily_volatility, risk_free_rate=0.02):
    excess_return = mean_daily_return - (risk_free_rate / 252)
    return np.sqrt(252) * (excess_return / daily_volatility)


# Function to calculate sortino ratio of a stock
def calculate_sortino_ratio(mean_daily_return, data, risk_free_rate=0.02):
    excess_return = mean_daily_return - (risk_free_rate / 252)
    downside_volatility = data['Daily Return'].where(data['Daily Return'] < 0).std()
    return np.sqrt(252) * (excess_return / downside_volatility)


def calculate_alpha(data, market_data, beta, risk_free_rate=0.02):
    if market_data is None:
        return None

    market_return = calculate_annualized_return(market_data)
    stock_return = calculate_annualized_return(data)

    alpha = stock_return - (risk_free_rate + beta * (market_return - risk_free_rate))
    return alpha


def calculate_r_squared(data, market_data):
    if market_data is None:
        return None

    data_returns = data['Adj Close'].pct_change()[1:]
    market_returns = market_data['Adj Close'].pct_change()[1:]

    correlation_matrix = np.corrcoef(data_returns, market_returns)
    correlation = correlation_matrix[0, 1]

    r_squared = correlation ** 2
    return r_squared


def calculate_treynor_ratio(data, market_data, beta, risk_free_rate=0.02):
    if market_data is None:
        return None

    stock_return = calculate_annualized_return(data)
    market_return = calculate_annualized_return(market_data)

    excess_return = stock_return - risk_free_rate
    treynor_ratio = excess_return / beta

    return treynor_ratio


def calculate_maximum_drawdown(data):
    price_series = data['Adj Close']
    max_drawdown = 0
    peak = price_series[0]

    for price in price_series:
        if price > peak:
            peak = price
        drawdown = (peak - price) / peak
        max_drawdown = max(max_drawdown, drawdown)

    return max_drawdown

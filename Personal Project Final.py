# Your existing imports
import yfinance as yf
import webview
import plotly.graph_objects as go
from tkinter import Tk, Label, Button, Entry, messagebox, ttk

# Function to fetch stock data from Yahoo Finance
def fetch_stock_data(ticker, period='1y'):
    try:
        print(f"Fetching {ticker} stock data for the last {period}...")
        stock_data = yf.download(ticker, period=period)
        print("Data fetching complete!\n")

        if stock_data.empty:
            raise ValueError("No data found for the given ticker.")

        return stock_data
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data for {ticker}: {e}")
        return None


# Function to create a candlestick chart using Plotly
def create_candlestick_chart(data):
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                                         open=data['Open'],
                                         high=data['High'],
                                         low=data['Low'],
                                         close=data['Close'])])
    fig.update_layout(title="Candlestick Chart")
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

# Function to create a line chart for historical stock prices
def create_historical_price_chart(data):
    fig = go.Figure(data=go.Scatter(x=data.index, y=data['Adj Close'], mode='lines'))
    fig.update_layout(title="Historical Stock Prices")
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

# Function to create a line chart for daily returns
def create_daily_returns_chart(data):
    daily_returns = data['Adj Close'].pct_change()
    fig = go.Figure(data=go.Scatter(x=data.index, y=daily_returns, mode='lines'))
    fig.update_layout(title="Daily Returns")
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

# Function to create a line chart for stock price and its moving average
def create_moving_average_chart(data):
    moving_average = data['Adj Close'].rolling(window=50).mean()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Adj Close'], mode='lines', name='Stock Price'))
    fig.add_trace(go.Scatter(x=data.index, y=moving_average, mode='lines', name='50-Day Moving Average'))
    fig.update_layout(title="Stock Price with Moving Average")
    return fig.to_html(full_html=False, include_plotlyjs='cdn')
# Function to display the created chart in a webview window
def display_chart_in_webview(html_content):
    webview.create_window('Interactive Chart', html=html_content)
    webview.start()

# Function to handle fetching and displaying stock data based on user input
def fetch_and_display_data(ticker_entry, chart_type_var):
    ticker = ticker_entry.get()
    chart_type = chart_type_var.get()

    if not ticker:
        messagebox.showerror("Error", "Please enter a stock ticker.")
        return

    data = fetch_stock_data(ticker)
    if data is None:
        return

    try:
        if chart_type == 'Candlestick Chart':
            chart_html = create_candlestick_chart(data)
        elif chart_type == 'Historical Price':
            chart_html = create_historical_price_chart(data)
        elif chart_type == 'Daily Returns':
            chart_html = create_daily_returns_chart(data)
        elif chart_type == 'Moving Average':
            chart_html = create_moving_average_chart(data)
        else:
            messagebox.showerror("Error", "Please select a chart type.")
            return

        display_chart_in_webview(chart_html)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to compare two stocks
def compare_stocks(ticker1, ticker2, period='1y'):
    try:
        print(f"Comparing {ticker1} and {ticker2} for the last {period}...")
        stock_data1 = yf.download(ticker1, period=period)
        stock_data2 = yf.download(ticker2, period=period)

        if stock_data1.empty or stock_data2.empty:
            raise ValueError("No data found for one of the tickers.")

        stock_data1_normalized = stock_data1['Adj Close'] / stock_data1['Adj Close'].iloc[0]
        stock_data2_normalized = stock_data2['Adj Close'] / stock_data2['Adj Close'].iloc[0]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=stock_data1.index, y=stock_data1_normalized, mode='lines', name=ticker1))
        fig.add_trace(go.Scatter(x=stock_data2.index, y=stock_data2_normalized, mode='lines', name=ticker2))
        fig.update_layout(title=f"Stock Comparison: {ticker1} vs {ticker2}")

        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    except Exception as e:
        messagebox.showerror("Error", f"Failed to compare stocks: {e}")
        return None

# Function to handle fetching and displaying comparison data
def fetch_and_display_comparison_data(ticker_entry1, ticker_entry2):
    ticker1 = ticker_entry1.get()
    ticker2 = ticker_entry2.get()

    if not ticker1 or not ticker2:
        messagebox.showerror("Error", "Please enter two stock tickers.")
        return

    comparison_chart_html = compare_stocks(ticker1, ticker2)
    if comparison_chart_html is not None:
        display_chart_in_webview(comparison_chart_html)

# Initialize the main window for the application
root = Tk()
root.title("Stock Analysis Tool")

# GUI components for the first stock ticker
ticker_label = Label(root, text="Enter Stock Ticker:")
ticker_label.pack()
ticker_entry = Entry(root)
ticker_entry.pack()

# GUI components for the second stock ticker for comparison
ticker_label2 = Label(root, text="Enter Second Stock Ticker for Comparison:")
ticker_label2.pack()
ticker_entry2 = Entry(root)
ticker_entry2.pack()

# Combobox for selecting chart type
chart_type_var = ttk.Combobox(root, values=['Candlestick Chart', 'Historical Price', 'Daily Returns', 'Moving Average'])
chart_type_var.pack()
chart_type_var.set('Select Chart Type')

# Button for fetching and displaying data
fetch_data_button = Button(root, text="Fetch and Display Data", command=lambda: fetch_and_display_data(ticker_entry, chart_type_var))
fetch_data_button.pack()

# Button for fetching and displaying comparison data
compare_button = Button(root, text="Compare Stocks", command=lambda: fetch_and_display_comparison_data(ticker_entry, ticker_entry2))
compare_button.pack()

# Start the Tkinter event loop
root.mainloop()

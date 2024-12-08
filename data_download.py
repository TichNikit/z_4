import yfinance as yf


def fetch_stock_data(ticker, period='1mo'):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data


def add_moving_average(data, window_size=5):
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data


def calculate_and_display_average_price(data):
    average_price = data['Close'].mean()
    print(f"Средняя цена закрытия акций за данный период: {average_price:.2f} USD")


def notify_if_strong_fluctuations(data, threshold):
    if 'Close' in data:
        initial_price = data['Close'].min()
        final_price = data['Close'].max()

        if initial_price != 0:
            percentage_change = ((final_price - initial_price) / initial_price) * 100
            if abs(percentage_change) > threshold:
                print(
                    f"ЦЕНА СИЛЬНО ИЗМЕНИЛАСЬ!\n{percentage_change:.2f}% > {threshold}%")
            else:
                print(
                    f"ЦЕНА В ПРЕДЕЛАХ ОЖИДАНИЯ.{percentage_change:.2f}% < {threshold}%")
        else:
            print("С ценой что-то не так")
    else:
        print("Данные о закрытии отсутствуют.")

def export_data_to_csv(data, file_name):
    data.to_csv(file_name)

def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    data['RSI'] = rsi
    return data

def calculate_macd(data):
    short_ema = data['Close'].ewm(span=12, adjust=False).mean()
    long_ema = data['Close'].ewm(span=26, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=9, adjust=False).mean()
    data['MACD'] = macd
    data['MACD_Signal'] = signal
    return data
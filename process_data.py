import pandas
import json

with open('data.json', 'r') as f:
    df = pandas.read_json(f, orient='records')

va_data = df[['date', 'positive']][df.state=='VA']

# These WMA/HMA implementations are taken from finta, they don't apply yet, 
# but I'll fix them soon
def WMA(cls, ohlc: pandas.DataFrame, period: int = 9, column: str = "close") -> pandas.Series:
    """
    WMA stands for weighted moving average. It helps to smooth the price curve for better trend identification.
    It places even greater importance on recent data than the EMA does.
    :period: Specifies the number of Periods used for WMA calculation
    """

    d = (period * (period + 1)) / 2  # denominator
    _weights = pd.Series(np.arange(1, period + 1))
    weights = _weights.iloc[::-1]  # reverse the series

    def linear(w):
        def _compute(x):
            return (w * x).sum() / d
        return _compute

    close_ = ohlc["close"].rolling(period, min_periods=period)
    wma = close_.apply(linear(weights), raw=True)

    return pd.Series(wma, name="{0} period WMA.".format(period))

def HMA(cls, ohlc: pandas.DataFrame, period: int = 16) -> pandas.Series:
    """
    HMA indicator is a common abbreviation of Hull Moving Average.
    The average was developed by Allan Hull and is used mainly to identify the current market trend.
    Unlike SMA (simple moving average) the curve of Hull moving average is considerably smoother.
    Moreover, because its aim is to minimize the lag between HMA and price it does follow the price activity much closer.
    It is used especially for middle-term and long-term trading.
    :period: Specifies the number of Periods used for WMA calculation
    """

    import math

    half_length = int(period / 2)
    sqrt_length = int(math.sqrt(period))

    wmaf = cls.WMA(ohlc, period=half_length)
    wmas = cls.WMA(ohlc, period=period)
    ohlc['deltawma'] = 2 * wmaf - wmas
    hma = cls.WMA(ohlc, column="deltawma", period=sqrt_length)

    return pd.Series(hma, name="{0} period HMA.".format(period))

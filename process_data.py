import os
import math
import json
import numpy
import pandas

DIR = os.path.dirname(__file__)
def rel(*p): return os.path.normpath(os.path.join(DIR, *p))

def read_json(fpath):
    with open(fpath, 'r') as f:
        return json.load(f)

STATE_DATA = read_json(rel('static_data/state_data.json'))

def main():
    with open('data.json', 'r') as f:
        df = pandas.read_json(f, orient='records')
    df.sort_values(['date'], ascending=True, inplace=True)

    va_data = df[['date', 'positive']][df.state=='VA']
    va_data.set_index('date', inplace=True)
    va_data_orig = va_data.copy()
    va_data.rename(columns={'positive': '+'}, inplace=True)
    va_data['new +'] = va_data['+'].diff(periods=1)
    va_data['hma(+, 7)'] = HMA(va_data, 7, '+')
    va_data['hma(new +, 7)'] = HMA(va_data, 7, 'new +')
    va_data_ind = STATE_DATA['abbrev_ind']['VA']
    va_pop = STATE_DATA['data'][va_data_ind]['population']

    norm_cols = ['+', 'new +', 'hma(+, 7)', 'hma(new +, 7)']
    for c in norm_cols:
        norm_c = f'{c}/100k'
        va_data[norm_c] = va_data[c]/va_pop*100000

    print(va_data)
    va_json_str = va_data.to_json(orient='records', indent=1);
    # print(va_data)
    globals().update(locals())

# WMA/HMA implementations modified from finta
def WMA(df: pandas.DataFrame, period: int = 7, column: str = "positive") -> pandas.Series:
    """
    WMA stands for weighted moving average. It helps to smooth the price curve for better trend identification.
    It places even greater importance on recent data than the EMA does.
    :period: Specifies the number of Periods used for WMA calculation
    """

    d = (period * (period + 1)) / 2  # denominator
    weights = pandas.Series(numpy.arange(1, period + 1))
    # weights = _weights.iloc[::-1]  # reverse the series

    def linear(w):
        def _compute(x):
            # print(x)
            # print(w)
            # import pdb; pdb.set_trace()
            return (w * x).sum() / d
        return _compute

    print(weights)
    close_ = df[column].rolling(period, min_periods=period)
    print(close_)
    wma = close_.apply(linear(weights), raw=True)
    print(wma)

    return pandas.Series(wma, name="{0} period WMA.".format(period))

def HMA(df: pandas.DataFrame, period: int = 7, column: str = "positive") -> pandas.Series:
    """
    HMA indicator is a common abbreviation of Hull Moving Average.
    The average was developed by Allan Hull and is used mainly to identify the current market trend.
    Unlike SMA (simple moving average) the curve of Hull moving average is considerably smoother.
    Moreover, because its aim is to minimize the lag between HMA and price it does follow the price activity much closer.
    It is used especially for middle-term and long-term trading.
    :period: Specifies the number of Periods used for WMA calculation
    """

    half_length = int(period / 2)
    sqrt_length = int(math.sqrt(period))
    print(half_length, sqrt_length)

    
    delta_wma = pandas.DataFrame({'data': df[column]})
    wmaf = WMA(df, period=half_length, column=column)
    wmas = WMA(df, period=period, column=column)
    delta_wma[f'wma {half_length}'] = wmaf
    delta_wma[f'wma {period}'] = wmas
    delta_wma['dwma'] = 2 * wmaf - wmas
    hma = WMA(delta_wma, column="dwma", period=sqrt_length)
    delta_wma[f'hma {period}'] = hma

    return hma

if __name__ == '__main__':
    main()

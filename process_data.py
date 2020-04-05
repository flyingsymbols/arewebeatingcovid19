import os
import copy
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

OUT_JSON_PATH = rel('docs/data/state_data.js')

def main():
    with open('data.json', 'r') as f:
        df = pandas.read_json(f, orient='records')

    df.sort_values(['date'], ascending=True, inplace=True)

    state_calc_data = copy.deepcopy(STATE_DATA)

    for state_abbrev, data_row_i in sorted(state_calc_data['abbrev_ind'].items()):
        state_data = df[['date', 'positive']][df.state==state_abbrev]
        state_data.set_index('date', inplace=True)
        state_data.rename(columns={'positive': '+'}, inplace=True)
        state_data['new +'] = state_data['+'].diff(periods=1)
        state_data['hma(+, 7)'] = HMA(state_data, 7, '+')
        state_data['hma(new +, 7)'] = HMA(state_data, 7, 'new +')
        state_data_ind = STATE_DATA['abbrev_ind']['VA']
        state_pop = STATE_DATA['data'][state_data_ind]['population']

        norm_cols = ['+', 'new +', 'hma(+, 7)', 'hma(new +, 7)']
        for c in norm_cols:
            norm_c = f'{c}/100k'
            state_data[norm_c] = state_data[c]/state_pop*100000

        state_row = state_calc_data['data'][data_row_i]
        # This leaves off the index of the dataseries, which is the date,
        state_row['data'] = state_data.to_dict(orient='list')
        # so we want to add it back in again:
        state_dates = state_data.index.to_list()
        state_row['data']['date'] = state_dates
        # and we generate labels for the first and the last element
        state_labels = [None]*len(state_data.index)
        def to_label(date_int):
            '''
            converts a date int (YYYYMMDD) to a string SS M/DD,
            e.g. VA 4/05
            '''
            dd = date_int % 100
            mm = (date_int // 100) % 100
            return f'{state_abbrev} {dd}/{mm:02}'


        for label_ind in [0, -1]:
            state_labels[label_ind] = to_label(state_dates[label_ind])

        state_row['data']['labels'] = state_labels

    state_json_str = json.dumps(state_calc_data, indent=1)
    with open(OUT_JSON_PATH, 'w') as f:
        f.write(f'var STATE_DATA = {state_json_str};')

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

    close_ = df[column].rolling(period, min_periods=period)
    wma = close_.apply(linear(weights), raw=True)

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

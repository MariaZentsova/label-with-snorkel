import pandas as pd

def prepare_sum_stats(train_df, test_df):
    result = pd.concat([train_df, test_df])

    # get a year
    result['date'] = pd.to_datetime(result['date_gmt'],format='%Y%m%d %H:%M:%S')
    result['year'] = pd.DatetimeIndex( result['date']).year

    # rename labels
    result['label'] =  result['answer'].map({-1:'notcleantech', 1:'notcleantech', 0:'cleantech'})

    dff = result.groupby(['label', 'year']).size().reset_index()

    dff = dff.rename(columns= {0: 'count'})

    return dff
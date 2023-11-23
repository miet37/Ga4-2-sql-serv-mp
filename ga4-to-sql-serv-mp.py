# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import pandas as pd
import itertools

property_id = "xxxx"
starting_date = "8daysAgo"
ending_date = "yesterday"

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ga4-mp-xxx.json'


def query_data(api_response):
    dimension_headers = [header.name for header in api_response.dimension_headers]
    metric_headers = [header.name for header in api_response.metric_headers]
    dimensions = []
    metrics = []
    for i in range(len(dimension_headers)):
        dimensions.append([row.dimension_values[i].value for row in api_response.rows])
    dimensions
    for i in range(len(metric_headers)):
        metrics.append([row.metric_values[i].value for row in api_response.rows])
    headers = dimension_headers, metric_headers
    headers = list(itertools.chain.from_iterable(headers))   
    data = dimensions, metrics
    data = list(itertools.chain.from_iterable(data))
    df = pd.DataFrame(data)
    df = df.transpose()
    df.columns = headers
    return df
# end .....


from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)
client = BetaAnalyticsDataClient()


def request_api(dim_name="landingPagePlusQueryString",
                metrics_name="sessions"):
    request_api = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[ Dimension(name = dim_name) ],
        metrics=[ Metric(name = metrics_name) ],
        date_ranges=[DateRange(start_date=starting_date, end_date=ending_date)],
        )
    response = client.run_report(request_api)
    df_ga4_resp = query_data(response)
    return df_ga4_resp
# end .......    

df_ga4_resp = request_api(dim_name="landingPagePlusQueryString",
            metrics_name="sessions")   
 
df_ga4_resp.to_excel("ga4_resp_landingPagePlusQueryString.xlsx")

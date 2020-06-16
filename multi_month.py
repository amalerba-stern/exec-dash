# dashboard_generator.py

import pandas
import csv
import os
from os import listdir
import plotly
import plotly.graph_objs as go

def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    Param: my_price (int or float) like 4000.444444 
    Example: to_usd(4000.444444)
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}"

data_dir = "data/monthly-sales"

month_dict = [{"num":1, "name":"January"}, 
              {"num":2, "name":"February"}, 
              {"num":3, "name":"March"}, 
              {"num":4, "name":"April"}, 
              {"num":5, "name":"May"}, 
              {"num":6, "name":"June"}, 
              {"num":7, "name":"July"}, 
              {"num":8, "name":"August"}, 
              {"num":9, "name":"September"}, 
              {"num":10, "name":"October"}, 
              {"num":11, "name":"November"}, 
              {"num":12, "name":"December"}
              ]

sales_data = []

files = [file for file in listdir(data_dir)]

for file in files:
    date = file[6:12]
    date_filename = f"data/monthly-sales/sales-{date}.csv"
    data = pandas.read_csv(date_filename)
    sales = sum(data["sales price"])
    year = date[0:4]
    month = date[4:6]
    month_name = [m["name"] for m in month_dict if m["num"] == int(month)][0]
    sales_data.append(dict({"date":date, "sales":sales, "year":year, "month":month, "month_name":month_name}))

def num_sales(data):
    return data["sales"]

sales_data_2 = sorted(sales_data, key=num_sales)
# sorted from least to most sales

y = [data["sales"] for data in sales_data]
x = list(range(len(y)))
x = [data["month_name"]+" "+data["year"] for data in sales_data]
#y = [data["sales"] for data in sales_data]

line = go.Line(x = x, y = y)

layout = go.Layout(title = f"Sales by Month",
                   xaxis = dict({"title" : "Month"}),
                   yaxis = dict({"title" : "Product"}))

plotly.offline.plot({"data": line, 
                     "layout": layout},
                    filename = "monthly_sales_over_time.html",
                    auto_open=True)
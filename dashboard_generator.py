# dashboard_generator.py

import pandas
import csv
import os
from os import listdir
import plotly
import plotly.graph_objs as go

# create requirements.txt file

def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    Param: my_price (int or float) like 4000.444444 
    Example: to_usd(4000.444444)
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}"

# Prompt user for desired month of sales data
while True:
    date = input("Please enter the month you want sales data for as YYYYMM:")

    # Check validity of dates
    data_dir = "data/monthly-sales"
    files = [file[6:12] for file in listdir(data_dir)]

    if date not in files:
        print("This is not a valid input. Your input must be one of the following:", files)
    else:
        data_year = date[0:4]
        data_month = date[4:6]
        print(data_year, data_month)
        break

# open file
date_filename = f"data/monthly-sales/sales-{date}.csv"
data = pandas.read_csv(date_filename) 

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
              {"num":12, "name":"December"}]
month_name = [month["name"] for month in month_dict if month["num"] == int(data_month)][0]

print("-----------------------")
year_month = f"{month_name} {data_year}"
print(f"MONTH: {year_month}")

print("-----------------------")
print("CRUNCHING THE DATA...")

print("-----------------------")
sales = sum(data["sales price"])
print("TOTAL MONTHLY SALES:", to_usd(sales))

print("-----------------------")
print("TOP SELLING PRODUCTS:")
sales_by_product = data.groupby(["product"]).sum().sort_values(by=["sales price"], ascending=False)
num_products = sales_by_product.shape[0]

for row in range(num_products):
    rank = row + 1 # Python is zero based
    name = sales_by_product.index.values[row]
    sales = to_usd(sales_by_product["sales price"][row])
    print(f"  {rank}) {name}: {sales}")

print("-----------------------")
print("VISUALIZING THE DATA...")

# https://plotly.com/python/horizontal-bar-charts/

x = list(reversed(sales_by_product["sales price"].tolist()))
y = list(reversed(sales_by_product.index.values.tolist()))
# https://stackoverflow.com/questions/22341271/get-list-from-pandas-dataframe-column
# https://dbader.org/blog/python-reverse-list#:~:text=Every%20list%20in%20Python%20has,modifies%20the%20original%20list%20object.
# reverse order so that horizontal bar graph has top to bottom ordering

list_sales = []
for sale in x:
    list_sales.append(to_usd(sale))

bar = go.Bar(x = x, 
             y = y,
             text = list_sales, textposition = "auto",
             orientation = "h"
             )

layout = go.Layout(title = f"Top-Selling Products ({year_month})",
                   xaxis = dict({"title" : "Sales (USD)", 
                                 "tickformat":"$.2f"}),
                   yaxis = dict({"title" : "Product"}))

plotly.offline.plot({"data": bar, 
                     "layout": layout},
                    filename = "plot_top_selling_products.html",
                    auto_open=True)
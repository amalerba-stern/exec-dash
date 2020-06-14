# dashboard_generator.py

import pandas
import csv
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

data = pandas.read_csv("data/monthly-sales/sales-201803.csv") 
#need to make more dynamic

print("-----------------------")
year_month = "March 2018" # MAKE DYNAMIC
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
                                 "tickformat":"$"}),
                   yaxis = dict({"title" : "Product"}))

plotly.offline.plot({"data": bar, 
                     "layout": layout},
                    filename = "plot_top_selling_products.html",
                    auto_open=True)
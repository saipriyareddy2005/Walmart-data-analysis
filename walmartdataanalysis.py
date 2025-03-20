# -*- coding: utf-8 -*-
"""walmartdataAnalysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kj9sE4bHUUwKMHG4q2Y030jh1Lwj0xOf
"""

# Library
import pandas as pd
pd.set_option('display.max_columns', 1000)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.float_format', lambda x: f'{x:.3f}')
import numpy as np
import warnings
warnings.filterwarnings("ignore")

import seaborn as sns
import matplotlib.pyplot as plt

# Support Function to inspect data
def inspect_data(df, col=None, n_rows=5):
    # data shape check
    print(f'data shape: {df.shape}')

    # column definition
# Support Function to inspect data
def inspect_data(df, col=None, n_rows=5):
    # data shape check
    print(f'data shape: {df.shape}')

    # column definition
    if col is None:
        col = df.columns

    # head data check, use display function to display dataframe
    display(df[col].head(n_rows))

# Support function to check missing value
def check_missing(df, cut_off=0, sort=True):
    freq=df.isnull().sum()
    percent=df.isnull().sum()/df.shape[0]*100
    types=df.dtypes
    unique = df.apply(pd.unique).to_frame(name='Unique Values')['Unique Values']
    df_miss=pd.DataFrame({'missing_percentage':percent, 'missing_frequency':freq, 'types':types, 'unique_values':unique})
    if sort: df_miss.sort_values(by='missing_frequency',ascending= False, inplace=True)
    return df_miss[df_miss['missing_percentage'] >= cut_off]

# Support function to fill the missing value
def fillna_by_metric(df, column_name, metric='mean', custom_value=None):
    # Takes metric values as per input
    if metric == 'mean':
        metric_value = df[column_name].mean()
    elif metric == 'median':
        metric_value = df[column_name].median()
    elif metric == 'mode':
        metric_value = df[column_name].mode().iloc[0]
    elif metric == 'zero':
        metric_value = 0
    elif metric == 'custom':
        metric_value = custom_value
    else:
        raise ValueError("Invalid metric type")

    # Fill in the missing values in the column with the metric values that have been taken
    df[column_name].fillna(value=metric_value, inplace=True)

    return df

# Support function to check missing value
def check_missing(df, cut_off=0, sort=True):
    freq=df.isnull().sum()
    percent=df.isnull().sum()/df.shape[0]*100
    types=df.dtypes
    unique = df.apply(pd.unique).to_frame(name='Unique Values')['Unique Values']
    df_miss=pd.DataFrame({'missing_percentage':percent, 'missing_frequency':freq, 'types':types, 'unique_values':unique})
    if sort: df_miss.sort_values(by='missing_frequency',ascending= False, inplace=True)
    return df_miss[df_miss['missing_percentage'] >= cut_off]

# Support function to fill the missing value
def fillna_by_metric(df, column_name, metric='mean', custom_value=None):
    # Takes metric values as per input
    if metric == 'mean':
        metric_value = df[column_name].mean()
    elif metric == 'median':
        metric_value = df[column_name].median()
    elif metric == 'mode':
        metric_value = df[column_name].mode().iloc[0]
    elif metric == 'zero':
        metric_value = 0
    elif metric == 'custom':
        metric_value = custom_value
    else:
        raise ValueError("Invalid metric type")

    # Fill in the missing values in the column with the metric values that have been taken
    df[column_name].fillna(value=metric_value, inplace=True)

    return df

# Load Data and inspect the data shape
df = pd.read_csv("Walmart.csv")
inspect_data(df)

# Check misisng
check_missing(df)

df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
df.dtypes

descriptive = df['Weekly_Sales'].describe().reset_index()
descriptive

# Create subplots
f, (ax_box, ax_hist) = plt.subplots(2, sharex=True, gridspec_kw={"height_ratios": (.15, .85)})

# Create boxplot
sns.boxplot(x=df['Weekly_Sales'], ax=ax_box)
ax_box.set(xlabel='')  # Remove x-label from the box plot

# Create histogram
sns.histplot(x=df['Weekly_Sales'], bins=12, kde=True, stat='density', ax=ax_hist)

# Remove y-ticks from the box plot
ax_box.set(yticks=[])

# Despine the plots
sns.despine(ax=ax_hist)
sns.despine(ax=ax_box, left=True)

# Add title above the box plot
plt.suptitle('Weekly Sales Distribution', fontsize=20, y=1.05)  # Adjust the 'y' value to position the title

# Add label for X and Y to the histogram
ax_hist.set_xlabel('Weekly Sales', fontsize=14)
ax_hist.set_ylabel('Count', fontsize=14)

# Show the plot
plt.tight_layout()
plt.show()

# Create week_year and month_year column
df['month_year'] = df['Date'].dt.strftime('%m-%Y')
# Change month_year datatype from object to datetime
df['month_year'] = pd.to_datetime(df['month_year'], format='%m-%Y')

df.head()

sns.set_style('whitegrid')

# create plot
plt.figure(figsize=(15, 8))

# Plot lineplot
sns.lineplot(data=df, x='Date', y='Weekly_Sales', marker='o', color='b', linewidth=2.5)

# Add tittle
plt.title('Total Sales over Time Weekly from All Stores', fontsize=20)

# Add label for X and Y
plt.xlabel('Date', fontsize=14)
plt.ylabel('Amount', fontsize=14)

# Rotated the x label for 90 degree
plt.xticks(rotation=90)

# Show the plot
plt.tight_layout()
plt.show()

sns.set_style('whitegrid')

# create plot
plt.figure(figsize=(15, 8))

# Plot lineplot
sns.lineplot(data=df, x='month_year', y='Weekly_Sales', marker='o', color='b', linewidth=2.5)

# Add tittle
plt.title('Total Sales Monthly from All Stores', fontsize=20)

# Add label for X and Y
plt.xlabel('Month_Year', fontsize=14)
plt.ylabel('Amount', fontsize=14)

# Rotated the x label for 90 degree
plt.xticks(rotation=90)

# Show the plot
plt.tight_layout()
plt.show()

store_sales = df.groupby('Store')['Weekly_Sales'].sum().reset_index().sort_values(by='Weekly_Sales', ascending=False)
store_sales.rename(columns={'Weekly_Sales': 'Sales'}, inplace=True)
store_sales

# create plot
plt.figure(figsize=(15, 8))

# Create bar plot
ax = sns.barplot(data=store_sales, x='Store', y='Sales', order=store_sales['Store'])
ax.set_xticklabels(ax.get_xticklabels())
ax.grid(False) # remove x grid

# Set axis labels and titles
ax.set_xlabel('Store Number', fontsize=14)
ax.set_ylabel('Total Sales', fontsize=14)
ax.set_title('Total Sales by Each Store', fontsize=18)

# Remove spines
sns.despine()

avg_sales = df.groupby('Holiday_Flag')['Weekly_Sales'].mean().reset_index()
avg_sales.rename(columns={'Weekly_Sales': 'Average_Sales'}, inplace=True)

# Replace values in the Holiday_Flag column
avg_sales['Holiday_Flag'] = avg_sales['Holiday_Flag'].replace({0: 'Non-Holiday Week', 1: 'Special Holiday Week'})

avg_sales

# create plot
plt.figure(figsize=(6, 4))

# Create bar plot
ax = sns.barplot(data=avg_sales, x='Holiday_Flag', y='Average_Sales', width=0.4)
ax.set_xticklabels(ax.get_xticklabels())
ax.grid(False) # remove x grid

# Set axis labels and titles
ax.set_xlabel('Holiday Flag', fontsize=11)
ax.set_ylabel('Average Sales', fontsize=11)
ax.set_title('Average Sales between Holiday Flag', fontsize=14)

# Remove spines
sns.despine()

# Filter the dataframe only with Holiday_Flag > 0
condition = df['Holiday_Flag'] > 0
filtered_df = df[condition]

filtered_df = filtered_df.reset_index(drop=True)

print(filtered_df)

# List of the holiday_event
holiday_events = {
    'Super Bowl': ['2010-02-12', '2011-02-11', '2012-02-10', '2013-02-08'],
    'Labour Day': ['2010-09-10', '2011-09-09', '2012-09-07', '2013-09-06'],
    'Thanksgiving': ['2010-11-26', '2011-11-25', '2012-11-23', '2013-11-29'],
    'Christmas': ['2010-12-31', '2011-12-30', '2012-12-28', '2013-12-27']
}

# Convert the data type from string to date time
for event, dates in holiday_events.items():
    holiday_events[event] = pd.to_datetime(dates, format='%Y-%m-%d')

# Add a new column 'Holiday_Event' and initialize with 'None'
filtered_df['Holiday_Event'] = 'None'

# Update the 'Holiday_Event' column based on the date
for event, dates in holiday_events.items():
    filtered_df.loc[filtered_df['Date'].isin(dates), 'Holiday_Event'] = event

display(filtered_df)

# Aggregate the sum of sales by Holiday Event
holiday_sales = filtered_df.groupby('Holiday_Event')['Weekly_Sales'].sum().reset_index().sort_values(by='Weekly_Sales', ascending=False)
holiday_sales.rename(columns={'Weekly_Sales': 'Sales'}, inplace=True)
holiday_sales

# create plot
plt.figure(figsize=(8, 6))

# Create bar plot
ax = sns.barplot(data=holiday_sales, x='Holiday_Event', y='Sales', order=holiday_sales['Holiday_Event'], width=0.4)
ax.set_xticklabels(ax.get_xticklabels())
ax.grid(False) # remove x grid

# Set axis labels and titles
ax.set_xlabel('Holiday Event', fontsize=14)
ax.set_ylabel('Total Sales', fontsize=14)
ax.set_title('Total Sales by Holiday Event', fontsize=18)

# Remove spines
sns.despine()

# Create Scatterplot
sns.scatterplot(df, x="Weekly_Sales", y="Temperature")

# Extra Parameter
plt.title('Weekly Sales Correlation vs Temperature', fontsize=16)
plt.xlabel('Weekly Sales', fontsize=12)
plt.ylabel('Temperature', fontsize=12)

plt.show()

# Create Scatterplot
sns.scatterplot(df, x="Weekly_Sales", y="Unemployment")

# Extra Parameter
plt.title('Weekly Sales Correlation vs Unemployment', fontsize=16)
plt.xlabel('Weekly Sales', fontsize=12)
plt.ylabel('Unemployment', fontsize=12)

plt.show()

# Create Scatterplot
sns.scatterplot(df, x="Weekly_Sales", y="CPI")

# Extra Parameter
plt.title('Weekly Sales Correlation vs CPI', fontsize=16)
plt.xlabel('Weekly Sales', fontsize=12)
plt.ylabel('CPI', fontsize=12)

plt.show()

# Create Scatterplot
sns.scatterplot(df, x="Weekly_Sales", y="Fuel_Price")

# Extra Parameter
plt.title('Weekly Sales Correlation vs Fuel_Price', fontsize=16)
plt.xlabel('Weekly Sales', fontsize=12)
plt.ylabel('Fuel Price', fontsize=12)

plt.show()


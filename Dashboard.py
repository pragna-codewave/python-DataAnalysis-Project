import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.express as px

company_list = [
    'C:/Users/ASUS/Downloads/S&P_resources/individual_stocks_5yr\\AAPL_data.csv',
    'C:/Users/ASUS/Downloads/S&P_resources/individual_stocks_5yr\\AMZN_data.csv',
    'C:/Users/ASUS/Downloads/S&P_resources/individual_stocks_5yr\\GOOG_data.csv',
    'C:/Users/ASUS/Downloads/S&P_resources/individual_stocks_5yr\\MSFT_data.csv'
 ]
all_data = pd.DataFrame()
for file in company_list:
    current_file = pd.read_csv(file)
    all_data = pd.concat([current_file,all_data],ignore_index = True)

all_data['date'] = pd.to_datetime(all_data['date'])

tech_list = all_data['Name'].unique()



st.set_page_config(page_title = 'Stock Analysis Dashboard' , layout = 'wide')
st.title('Tech Stocks Analysis Dashboard')

st.sidebar.title('Choose a Company')
selected_company = st.sidebar.selectbox('Select a stock',tech_list)
company_df = all_data[all_data['Name']==selected_company]
company_df.sort_values('date',inplace=True)

## Plot1
st.subheader(f"Closing price of {selected_company} Over Time")
fig1 = px.line(company_df,x='date',y='close',title = selected_company + ' closing prices over time')
st.plotly_chart(fig1,use_container_width=True)

## Plot 2
st.subheader(f'Moving Averages of (10,20,50) days')

ma_day = [10,20,50]

for ma in ma_day:
    company_df['close_' + str(ma)] = company_df['close'].rolling(ma).mean()
    
fig2 = px.line(company_df,x='date',y=['close_10','close_20','close_50'],title=selected_company + 'closing')
st.plotly_chart(fig2,use_container_width=True)

##Plot 3
st.subheader('Daily returns for ' + selected_company)
company_df['Daily returns (in%)'] = company_df['close'].pct_change() * 100
fig3 = px.line(company_df,x='date',y='Daily returns (in%)',title = 'Daily returns (%)')
st.plotly_chart(fig3,use_container_width=True)

##Plot 4
st.subheader('Resampled closing price for (yearly/monthly/quaterly)')
company_df.set_index('date',inplace=True)
resample_option = st.radio('Select Resample frequency',['monthly','yearly','quaterly'])

if resample_option == 'monthly':
    fig4 = company_df['close'].resample('ME').mean()
elif resample_option == 'quaterly':
    fig4 = company_df['close'].resample("QE").mean()
else:
    fig4 = company_df['close'].resample("YE").mean()

fig5 = px.line(fig4,title = selected_company+" "+ resample_option + " Average closing price")
st.plotly_chart(fig5,use_container_width=True)

##Plot 5
st.subheader("Correlation between the companies")

apple = pd.read_csv(company_list[0])
amazon = pd.read_csv(company_list[1])
google = pd.read_csv(company_list[2])
microsoft = pd.read_csv(company_list[3])

closing_price = pd.DataFrame()

closing_price['apple_close'] = apple['close']
closing_price['amazon_close'] = amazon['close']
closing_price['goole_close'] = google['close']
closing_price['microsoft_close'] = microsoft['close']

fig6 ,ax = plt.subplots()
sns.heatmap(closing_price.corr(),annot=True,cmap = 'coolwarm')
st.pyplot(fig6)

st.markdown('---')
st.markdown('**Note:This heatmap provides basic technical details and analysis')

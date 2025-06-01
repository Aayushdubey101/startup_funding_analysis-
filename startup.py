import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import startup_enhancements as enh
import os
try:
    st.set_page_config(layout='wide', page_title='Startup Analysis')
except Exception as e:
    st.error(f"RELOAD ONCE AGAIN")
   
# Make CSV path configurable and relative to current file
csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app', 'ST1.csv'))

try:
    df = pd.read_csv(csv_path)
except FileNotFoundError:
    st.error(f"CSV file not found at path: {csv_path}")
    st.stop()
except pd.errors.ParserError:
    st.error(f"Error parsing CSV file at path: {csv_path}")
    st.stop()

st.sidebar.header('Startup Funding Analysis')
option = st.sidebar.selectbox('Select your option', ['Overall Analysis', 'Startup', 'Investor'])

df['Investors Name'].fillna("undisclosed", inplace=True)
df['startup'].fillna("undisclosed", inplace=True)
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['month_year'] = df['Date'].dt.to_period('M')

def general_analysis():
    st.subheader('Overall Analysis')
    c1, c2, c3, c4 = st.columns(4)
    # total investment in india
    with c1:
        total = round(df['amount'].sum(), 3)
        st.metric('Total in CR', total)
    # max funding get by startup
    with c2:
        max_funding = df.groupby('startup')['amount'].sum().max()
        st.metric('Maximun funding', max_funding)
    with c3:
        avg_funding = df.groupby('startup')['amount'].sum().mean()
        st.metric('Average Funding', avg_funding)
    # total funded startup
    with c4:
        num_startups = df['startup'].nunique()
        st.metric('Total funded startup', num_startups)
    op = st.selectbox('Select_Type', ['Total', 'Count'])
    # Month on month line chart of investing in startups
    if op == 'Total':
        st.subheader('Month-on-Month Investment Trend')
        monthly = df.groupby('month_year')['amount'].sum().sort_index()
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(monthly.index.astype(str), monthly.values, marker='o')
        ax.set_xlabel('Month-Year')
        ax.set_ylabel('Total Investment Amount')
        ax.set_title('Month-on-Month Investment in Startups')
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.subheader('Month-on-Month Investment Count Trend')
        monthly = df.groupby('month_year')['amount'].count().sort_index()
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(monthly.index.astype(str), monthly.values, marker='o')
        ax.set_xlabel('Month-Year')
        ax.set_ylabel('Number of Investments')
        ax.set_title('Month-on-Month Investment Count in Startups')
        plt.xticks(rotation=45)
        st.pyplot(fig)

    enh.overall_analysis_enhancements(df)

def inv_anlysis(invester):
    st.subheader(f"{invester} all investment")
    # Top 5 recent investments
    x = df[df['Investors Name'].str.contains(invester)][['startup', 'vertical', 'city', 'round', 'amount']].head()
    st.dataframe(x)
    # Top highest investment 
    st.subheader(f"{invester} highest investment")
    x1 = df[df['Investors Name'].str.contains(invester)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
    c1, c2 = st.columns(2)
    c3, c4 = st.columns(2)
    with c1:
        fig, ax = plt.subplots(figsize=(8, 8)) 
        ax.bar(x1.index, x1.values)
        ax.set_xlabel('Startup')
        ax.set_ylabel('Total Amount')
        ax.set_title(f'Top Investments by {invester}')
        ax.set_xticklabels(x1.index, rotation=45, ha='right')
        st.pyplot(fig)
    with c2:
        try:
            plotdata = df[df['Investors Name'].str.contains(invester)].groupby('vertical')['amount'].sum().sort_values(ascending=False)
            fig2, ax2 = plt.subplots(figsize=(8, 8))
            plotdata.head(10).plot(kind='pie', autopct='%1.1f%%', ax=ax2, title='Top 10 Verticals by Investment Amount')
            ax2.set_ylabel('')
            ax2.axis('equal')
            plt.tight_layout()
            st.pyplot(fig2)
        except ValueError:
            st.write('no data available')
        except Exception as e:
            st.write(f"An error occurred: {e}")
    with c3:
        try:
            plotdata = df[df['Investors Name'].str.contains(invester)].groupby('city')['amount'].sum().sort_values(ascending=False)
            fig3, ax3 = plt.subplots(figsize=(8, 8))
            plotdata.head(10).plot(kind='pie', autopct='%1.1f%%', ax=ax3, title='Top 10 Cities by Investment Amount')
            ax3.set_ylabel('')
            ax3.axis('equal')
            plt.tight_layout()
            st.pyplot(fig3)
        except ValueError:
            st.write('no data available')
        except Exception as e:
            st.write(f"An error occurred: {e}")
    with c4:
        try:
            plotdata = df[df['Investors Name'].str.contains(invester)].groupby('round')['amount'].sum().sort_values(ascending=False)
            fig4, ax4 = plt.subplots(figsize=(8, 8))
            plotdata.head(10).plot(kind='pie', autopct='%1.1f%%', ax=ax4, title='Top 10 Rounds by Investment Amount')
            ax4.set_ylabel('')
            ax4.axis('equal')
            plt.tight_layout()
            st.pyplot(fig4)
        except ValueError:
            st.write('no data available')
        except Exception as e:
            st.write(f"An error occurred: {e}")
    # Year-wise investment line chart
    try:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['year'] = df['Date'].dt.year
        yearly = df[df['Investors Name'].str.contains(invester)].groupby('year')['amount'].sum().sort_index()
        fig5, ax5 = plt.subplots(figsize=(8, 4))
        ax5.plot(yearly.index, yearly.values, marker='o')
        ax5.set_xlabel('Year')
        ax5.set_ylabel('Total Investment Amount')
        ax5.set_title(f'Year-wise Investment Trend for {invester}')
        st.pyplot(fig5)
    except Exception as e:
        st.write(f"Could not plot year-wise trend: {e}")

if option=='Overall Analysis':
    general_analysis()
elif option=='Startup':
    selected_startup = st.sidebar.selectbox('Select Startup', sorted(df['startup'].unique().tolist()))
    st.title('Startup Analysis')
    enh.startup_summary_metrics(df, selected_startup)
    enh.funding_rounds_breakdown(df, selected_startup)
    enh.top_investors_in_startup(df, selected_startup)
    enh.investment_frequency(df, selected_startup)
    enh.comparative_insights(df, selected_startup)
elif option=='Investor':
    i=st.sidebar.selectbox('Select Investor', sorted(set(df['Investors Name'].str.split(',').sum())))
    st.title('Investor Analysis')
    bt1=st.sidebar.button('Do Analysis on Investor')
    if bt1:
        inv_anlysis(i)
# st.dataframe(df)

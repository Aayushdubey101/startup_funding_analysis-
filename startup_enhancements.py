import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
c1,c2,c3=st.columns(3)

def startup_summary_metrics(df, startup_name):
    try:
        startup_df = df[df['startup'] == startup_name].copy()
        total_funding = startup_df['amount'].sum()
        num_rounds = startup_df.shape[0]
        first_funding = startup_df['Date'].min()
        latest_funding = startup_df['Date'].max()
        # Fix column name for unique investors
        unique_investors = startup_df['Investors Name'].nunique() if 'Investors Name' in startup_df.columns else startup_df['Investors_Name'].nunique()
        st.metric('Total Funding Amount', total_funding)
        st.metric('Number of Funding Rounds', num_rounds)
        st.metric('First Funding Date', first_funding.strftime('%Y-%m-%d') if pd.notnull(first_funding) else 'N/A')
        st.metric('Latest Funding Date', latest_funding.strftime('%Y-%m-%d') if pd.notnull(latest_funding) else 'N/A')
        st.metric('Unique Investors', unique_investors)
    except Exception as e:
        st.error(f"Error in startup_summary_metrics: {e}")

def funding_rounds_breakdown(df, startup_name):
    try:
        startup_df = df[df['startup'] == startup_name].copy()
        # Fix column name for round
        round_col = 'round' if 'round' in startup_df.columns else 'Round'
        rounds_count = startup_df[round_col].value_counts()
        fig, ax = plt.subplots(figsize=(8, 6))
        rounds_count.plot(kind='pie', autopct='%1.1f%%', ax=ax)
        ax.set_ylabel('')
        ax.set_title('Funding Rounds Breakdown')
        ax.axis('equal')
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error in funding_rounds_breakdown: {e}")

def top_investors_in_startup(df, startup_name):
    try:
        startup_df = df[df['startup'] == startup_name].copy()
        # Fix column name for Investors Name
        investors_col = 'Investors Name' if 'Investors Name' in startup_df.columns else 'Investors_Name'
        investors_sum = startup_df.groupby(investors_col)['amount'].sum().sort_values(ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(10, 6))
        investors_sum.plot(kind='bar', ax=ax)
        ax.set_xlabel('Investor')
        ax.set_ylabel('Total Investment Amount')
        ax.set_title('Top Investors in Startup')
        plt.xticks(rotation=45)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error in top_investors_in_startup: {e}")

def investment_frequency(df, startup_name):
    try:
        startup_df = df[df['startup'] == startup_name].copy()
        startup_df['month_year'] = startup_df['Date'].dt.to_period('M')
        freq = startup_df.groupby('month_year').size()
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(freq.index.astype(str), freq.values, marker='o')
        ax.set_xlabel('Month-Year')
        ax.set_ylabel('Number of Funding Rounds')
        ax.set_title('Investment Frequency Over Time')
        plt.xticks(rotation=45)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error in investment_frequency: {e}")

def comparative_insights(df, startup_name):
    try:
        startup_df = df[df['startup'] == startup_name].copy()
        if startup_df.empty:
            st.write("No data available for this startup.")
            return
        vertical = startup_df['vertical'].mode()[0] if not startup_df['vertical'].mode().empty else None
        city = startup_df['city'].mode()[0] if not startup_df['city'].mode().empty else None
        startup_total = startup_df['amount'].sum()
        avg_vertical = df[df['vertical'] == vertical]['amount'].mean() if vertical else None
        avg_city = df[df['city'] == city]['amount'].mean() if city else None
        st.write(f"Comparative Insights for {startup_name}:")
        st.write(f"- Total Raised Capital: {startup_total}")
        st.write(f"- Average Funding in Vertical ({vertical}): {avg_vertical if avg_vertical is not None else 'N/A'}")
        st.write(f"- Average Funding in City ({city}): {avg_city if avg_city is not None else 'N/A'}")
    except Exception as e:
        st.error(f"Error in comparative_insights: {e}")

def overall_analysis_enhancements(df):
    try:
        st.subheader('Top 10 Startups by Total Funding')
        top10 = df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(10)
        fig6, ax6 = plt.subplots(figsize=(12, 6))
        ax6.bar(top10.index, top10.values)
        ax6.set_xlabel('Startup')
        ax6.set_ylabel('Total Funding Amount')
        ax6.set_title('Top 10 Startups by Total Funding')
        plt.xticks(rotation=45)
        st.pyplot(fig6)

        st.subheader('Top Sectors by Total Investment')
        top_sectors = df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head(10)
        fig7, ax7 = plt.subplots(figsize=(8, 8))
        top_sectors.plot(kind='pie', autopct='%1.1f%%', ax=ax7)
        ax7.set_ylabel('')
        ax7.axis('equal')
        st.pyplot(fig7)

        st.subheader('Funding Round Trends Over Time')
        df['year'] = df['Date'].dt.year
        round_trends = df.groupby(['year', 'round'])['amount'].sum().unstack().fillna(0)
        fig8, ax8 = plt.subplots(figsize=(12, 6))
        round_trends.plot(kind='line', ax=ax8)
        ax8.set_xlabel('Year')
        ax8.set_ylabel('Total Funding Amount')
        ax8.set_title('Funding Round Trends Over Time')
        st.pyplot(fig8)

        st.subheader('Yearly Funding Amount with Peaks and Drops')
        yearly = df.groupby('year')['amount'].sum()
        fig9, ax9 = plt.subplots(figsize=(12, 6))
        ax9.plot(yearly.index, yearly.values, marker='o')
        peak_year = yearly.idxmax()
        drop_year = yearly.idxmin()
        ax9.annotate('Peak', xy=(peak_year, yearly.max()), xytext=(peak_year, yearly.max()*1.1),
                     arrowprops=dict(facecolor='green', shrink=0.05))
        ax9.annotate('Drop', xy=(drop_year, yearly.min()), xytext=(drop_year, yearly.min()*0.9),
                     arrowprops=dict(facecolor='red', shrink=0.05))
        ax9.set_xlabel('Year')
        ax9.set_ylabel('Total Funding Amount')
        ax9.set_title('Yearly Funding Amount with Peaks and Drops')
        st.pyplot(fig9)

        st.subheader('Outlier Detection: Top 1% Funding Rounds')
        threshold = df['amount'].quantile(0.99)
        outliers = df[df['amount'] >= threshold][['startup', 'amount', 'round', 'Investors Name']]
        st.dataframe(outliers)
    except Exception as e:
        st.error(f"Error in overall_analysis_enhancements: {e}")

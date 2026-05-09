import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Setup (Makes it look wide and professional)
st.set_page_config(page_title="Shrinkflation Tracker", layout="wide")
st.title("🛒 Pakistani Snacks Shrinkflation Tracker")
st.markdown("Tracking the **Price per Gram** of 50 targeted grocery items at Greenvalley RWP to detect hidden inflation (Shrinkflation).")

# 2. Load the Data
# The @st.cache_data makes the app run super fast by remembering the data
@st.cache_data
def load_data():
    df = pd.read_csv('greenvalley_snacks_may_2026.csv')
    df = df.dropna(subset=['Price_Per_Gram']) # Remove broken rows
    return df

df = load_data()

# 3. High-Level Metrics (The "Recruiter Hook")
st.subheader("Current Market Snapshot (May 2026)")
col1, col2, col3 = st.columns(3)
col1.metric("Target Products Tracked", len(df))
col2.metric("Highest Price per Gram", f"Rs. {df['Price_Per_Gram'].max():.2f}")
col3.metric("Lowest Price per Gram", f"Rs. {df['Price_Per_Gram'].min():.2f}")

st.divider()

# 4. Interactive Search Bar
st.subheader("🔍 Search for a Specific Snack")
search_query = st.text_input("Type a brand (e.g., Cheetos, Doritos, Lays):")

# Filter the table based on search
if search_query:
    filtered_df = df[df['Product Name'].str.contains(search_query, case=False, na=False)]
else:
    filtered_df = df

# Display the clean table
st.dataframe(
    filtered_df[['Product Name', 'Price (PKR)', 'Weight_Grams', 'Price_Per_Gram']].style.format({
        'Price (PKR)': 'Rs. {:.0f}',
        'Weight_Grams': '{:.1f}g',
        'Price_Per_Gram': 'Rs. {:.2f}'
    }), 
    width='stretch'
)

# 5. Interactive Bar Chart
st.subheader("📊 Price per Gram Comparison")
st.markdown("Hover over the bars to see exact data. Notice the massive premium on imported goods.")

# Sort data so the most expensive is on the left
chart_data = filtered_df.sort_values('Price_Per_Gram', ascending=False).head(20)

fig = px.bar(
    chart_data, 
    x='Product Name', 
    y='Price_Per_Gram', 
    color='Price_Per_Gram',
    color_continuous_scale='Reds', # Visually highlights the most expensive ones in dark red
    labels={'Price_Per_Gram': 'Price per Gram (PKR)'}
)

# Make the chart look clean
fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig, width='stretch')
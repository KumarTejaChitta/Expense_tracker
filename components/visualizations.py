"""
Visualization components for expense tracker
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from database import db_manager

def render_summary_section():
    """
    Render the summary section with all visualizations
    """
    # Get data from database
    total_expense = db_manager.get_total_expense()
    category_df = db_manager.get_expenses_by_category()
    trend_df = db_manager.get_expense_trend()
    highest_lowest = db_manager.get_highest_lowest_category()
    
    # Create two rows with two columns each
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)
    
    # Column 1: Total Expense
    with row1_col1:
        render_total_expense(total_expense)
    
    # Column 2: Pie Chart
    with row1_col2:
        render_category_pie_chart(category_df)
    
    # Column 3: Highest and Lowest
    with row2_col1:
        render_highest_lowest(highest_lowest)
    
    # Column 4: Line Chart
    with row2_col2:
        render_trend_line_chart(trend_df)
    
def render_total_expense(total: float):
    """Render total expense metric"""
    st.markdown("#### 💰 Total Expense")
    st.metric(
        label="Total",
        value=f"${total:,.2f}",
        label_visibility="hidden",
        delta=None
    )
    st.info(f"Total spending across all categories")

def render_category_pie_chart(df):
    """Render pie chart for expenses by category"""
    st.markdown("#### 📊 Expense by Category")
    
    if df.empty:
        st.info("No expense data available yet")
    else:
        fig = px.pie(
            df, 
            values='Total', 
            names='Category',
            color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', 
                                    '#96CEB4', '#FFEAA7', '#DDA0DD']
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=300, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

def render_highest_lowest(data):
    """Render highest and lowest spending categories"""
    st.markdown("#### 📈 Spending Summary")
    
    if data['highest']['category'] != 'N/A':
        st.success(f"**Highest:** {data['highest']['category']} - ${data['highest']['amount']:,.2f}")
    else:
        st.info("No spending data yet")
    
    if data['lowest']['category'] != 'N/A':
        st.warning(f"**Lowest:** {data['lowest']['category']} - ${data['lowest']['amount']:,.2f}")
    else:
        st.info("Add expenses to see lowest category")

def render_trend_line_chart(df):
    """Render line chart for expense trends"""
    st.markdown("#### 📈 Expense Trend")
    
    if df.empty:
        st.info("No trend data available yet")
    else:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['Total'],
            mode='lines+markers',
            name='Daily Expense',
            line=dict(color='#4ECDC4', width=2),
            marker=dict(size=8)
        ))
        fig.update_layout(
            height=300,
            margin=dict(t=0, b=0, l=0, r=0),
            xaxis_title="Date",
            yaxis_title="Amount ($)",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

"""
Simple Expense Tracker Application
A Streamlit-based expense tracking application with PostgreSQL backend
"""
import streamlit as st
from config import PAGE_TITLE, PAGE_ICON, LAYOUT
from components.data_entry import render_data_entry_form
from components.visualizations import render_summary_section

# Page configuration
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT
)

def main():
    """Main application function"""
    
    # Title
    st.markdown("<h1 style='text-align: center;'>💰 Simple Expense Tracker</h1>", 
                unsafe_allow_html=True)
    
    # Add some spacing
    st.markdown("---")
    
    # Data Entry Section
    render_data_entry_form()
    
    # Add separator
    st.markdown("---")
    
    # Summary Button and Section
    if st.button("📊 Show Summary", type="secondary", width='stretch'):
        st.markdown("---")
        render_summary_section()

if __name__ == "__main__":
    main()
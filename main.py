import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Streamlit app configuration
st.set_page_config(page_title='Data Visualiser', layout="centered", page_icon="📊")
st.title("📊 Data Visualiser")

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('shining-reality-431616-d5-6035b47230cb.json', scope)
client = gspread.authorize(creds)

# Fetch list of Google Sheets
sheet_list = client.openall()
sheet_names = [sheet.title for sheet in sheet_list]

selected_sheet = st.selectbox("Select a Google Sheet", sheet_names, index=None)

if selected_sheet:
    # Open the selected Google Sheet
    spreadsheet = client.open(selected_sheet)

    # Fetch list of worksheets (sheets) within the Google Sheet
    worksheet_list = spreadsheet.worksheets()
    worksheet_names = [worksheet.title for worksheet in worksheet_list]

    selected_worksheet = st.selectbox("Select a Worksheet", worksheet_names, index=None)

    if selected_worksheet:
        # Open the selected worksheet
        worksheet = spreadsheet.worksheet(selected_worksheet)
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)

        # Ensure 'Date' column is in datetime format
        df['Date'] = pd.to_datetime(df['Date'])

        # Filter data based on selected date
        unique_dates = df['Date'].dt.date.unique()
        selected_date = st.selectbox("Select a Date", unique_dates, index=None)

        if selected_date:
            filtered_df = df[df['Date'].dt.date == selected_date]

            col1, col2 = st.columns(2)
            columns = filtered_df.columns.tolist()
            columns.remove('Time')  # Remove 'Time' from parameter selection as it will be used for x-axis

            with col1:
                st.write(" ")
                st.write(filtered_df.head())

            with col2:
                y_axis = st.selectbox("Select the Parameter", options=columns + ["None"])
                plot_list = ["Line Plot", "Bar Chart", "Scatter Plot", "Distribution Plot", "Count Plot"]
                selected_plot = st.selectbox("Select a Plot", plot_list, index=None)

            if st.button("Generate Plot"):
                fig, ax = plt.subplots(figsize=(10, 8))
                if selected_plot == "Line Plot":
                    sns.lineplot(x=filtered_df['Time'], y=filtered_df[y_axis], ax=ax)
                elif selected_plot == "Bar Chart":
                    sns.barplot(x=filtered_df['Time'], y=filtered_df[y_axis], ax=ax)
                elif selected_plot == "Distribution Plot":
                    sns.histplot(filtered_df[y_axis], kde=True, ax=ax)
                elif selected_plot == "Scatter Plot":
                    sns.scatterplot(x=filtered_df['Time'], y=filtered_df[y_axis], ax=ax)
                elif selected_plot == "Count Plot":
                    sns.countplot(x=filtered_df['Time'], ax=ax)

                plt.title(f"{selected_worksheet} on {selected_date}: {y_axis} vs Time")
                plt.xlabel('Time')
                plt.ylabel(y_axis)

                # Rotate x-axis labels and set font size
                plt.xticks(rotation=45, ha='right', fontsize=10)
                plt.tight_layout()  # Adjust layout to make room for x-axis labels

                st.pyplot(fig)

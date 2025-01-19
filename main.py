import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# Streamlit app configuration
st.set_page_config(page_title="Solar Dryer Data", layout="wide", page_icon=":sun_with_face:")

# Define app pages
PAGES = {
    "Overview": "overview",
    "Visualize Data": "visualize"
}

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", list(PAGES.keys()))

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Google Service Account Credentials (Directly included in the code)
credentials = {
    "type": "service_account",
    "project_id": "shining-reality-431616-d5",
    "private_key_id": "6035b47230cbab372662000ba24db269b38eba58",
    "private_key": """-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDcdgT1OJnbZO0O
RB8orkTpqerTvXP5VzSA9jmhYbx+bg50k9nRe0gysUr7X2XQKqgOQW3aHgrnvf8k
wNjD6RvX5zmchuZi0FgaFMNl/InHR8aQvIAwyippZ8rD1wgk0TAi8A80OY2VJJjT
6/k2JV3vHE9Y7XL/DrtbMPIJZQs8VwIsrvdE4ZL83S1pXYQlqzNIEMVMgr5b1bMV
Qf8uOFHNCh9kQZCKrIFVdBTz3TglyC1JzPndpR4lVXmuusdX62Aw1S76OU568TbR
qcJwPjgi6HY3t/8ReVXWRPsgLLLvPbwTY9eyX1NZq78yYh4IYI7F6tjl71YhAM2k
q/7SIK9XAgMBAAECggEAKTkeQzZCur37/6toQiSX+TNPGCm4Slruk+C2tQEADIoK
xOyykZOiU+xH74oOkSawxv2gC2WLt3qU/2vZ/IQVs0DmymiFItv/ZV0Vjnfy0WMP
85dzxuu+k3gXd5g5Sx0ciaPmy+apHUa7FwFsV54UGvZpteCsnJnGGc6kq3IL8Euh
0UUpEv2IQ4ThnB6CV63bOLe9O+zbj/CXEUnYhFc3JEff7DzEHr0GMy/ugjgwhs0C
O5XGkiMYgUGL+VuBppCCmJO+6MP3W238mI+7phByOXcCEeagSLT7K4Se8bye2wiR
dwr4Tfizk2U+pJRNxSseQ9c0FA1RBz7NevTQkJ/T3QKBgQD2xmKInmGivfTSrCYr
OXUjY3BJfVsX3YYgN+ERaW4jlW/LmJrYR6886q9/4SZdkxtV2M/dcTqNy1uT1uAd
pxCLXIFllonfdBPw71atWPqF1KdzNC6GFAog3ANMqcOLXntG4pDGaf5TvbrRkemy
kVi4uKSWqXT/82CEyiwkb7/2rQKBgQDks8/7SoSCFGnseu3Ic7Y8i2UVRrfwmHD/
fIByItfqkGg3vM4Ecs3eVQ9lk2z1sFFXZyDZ3m6VELkqGqwRIKqtCBYWZrTfgJW5
JS1RnUC0ApWgjKLG/28wSaeLFnsw/oTM1WZGKu8VL9EXM8IqZxqmNBmGHSe0FCoV
J7QpceFykwKBgQCC4PiFSKqzq1dbHF4p8pFDsYtuDoPvhleKYtiFaYs2aB0gt9D4
ABzajAWEJx835btLrm+gHFtXtJDfOcknMOG/Z9Jg1JRO5LtmvykTSuujawNcQEKk
baBpiQZe9HJ3SibLk4IBGVn/g9K/L0nooNmTLqpsFXet/6AjDS6YLIR9CQKBgQDD
+e2sOVPJH/MQqNpf3f/4a77H95yheA/EboymwYLiRrJ3qLulhjcxYRRbh3RkKJ3b
Vs0IxRlfdUAme0qdNq/qrDY5JfOyXj5utBPcjvMmDdzoAftuqO4/o64FetM/zapA
2FDWqe3L6viyeDDXIxjr+VMx4IPoRSs2i5pPtX1qLwKBgBsC5Z/LnBb3bbqylN5u
D84mBVZ2zw2RgKIV4upBH515fC+vJOjip9G8BY8fsDD4b0PA014c/gkdPC6+38Vf
FO7LfglYrm26GcsKaME87QfDF2uTWamQGEZPKmNWdQLaF28uzXepTMGJwtDWXYMk
fmvKCgD4ht3vFYE1ohD8Zl+u
-----END PRIVATE KEY-----""",
    "client_email": "solar-dryer@shining-reality-431616-d5.iam.gserviceaccount.com",
    "client_id": "114008855893744940682",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/solar-dryer%40shining-reality-431616-d5.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}
# Convert credentials into a dictionary and authorize
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
client = gspread.authorize(creds)

# Define the Google Sheet name directly
spreadsheet_name = "Solar Dryer Comparative Study"
spreadsheet = client.open(spreadsheet_name)

sheet_list = spreadsheet.worksheets()

if page == "Overview":
    st.title("📈 Solar Dryer Data Overview")

    # Define the Solar Dryer sheet names
    dryer_sheets = ["Solar Dryer 1", "Solar Dryer 2", "Solar Dryer 3"]

    # Iterate over the dryer sheets and display the data
    for dryer in dryer_sheets:
        worksheet = spreadsheet.worksheet(dryer)
        headers = worksheet.row_values(1)
        data = worksheet.get_all_records(expected_headers=headers)
        df = pd.DataFrame(data)

        # Ensure Date is in datetime format
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        # Drop rows with invalid dates
        df = df.dropna(subset=['Date'])

        # Get the latest date
        latest_date = df['Date'].max()

        # Filter data for the latest date
        latest_date_data = df[df['Date'] == latest_date]

        # Columns for temperature and humidity
        temperature_columns = [col for col in df.columns if "Temperature" in col]
        humidity_columns = [col for col in df.columns if "Humidity" in col]

        # Calculate averages, ignoring NaN values
        avg_temperature = latest_date_data[temperature_columns].mean().mean(skipna=True)
        avg_humidity = latest_date_data[humidity_columns].mean().mean(skipna=True)

        # Display data
        st.write(
            f"### {dryer}\n"
            f"- **Latest Date**: {latest_date.date()}\n"
            f"- **Average Temperature**: {avg_temperature:.2f}°C\n"
            f"- **Average Humidity**: {avg_humidity:.2f}%\n"
        )


elif page == "Visualize Data":
    st.title("📊 Data Visualizer")

    sheet_names = [sheet.title for sheet in sheet_list]

    selected_sheet = st.selectbox("Select a Sheet", sheet_names, index=None)

    if selected_sheet:
        # Open the selected sheet
        worksheet = spreadsheet.worksheet(selected_sheet)
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)

        # Ensure 'Date' column is in datetime format
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        # Drop rows with invalid dates
        df = df.dropna(subset=['Date'])

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
                # Plotting section
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

                plt.title(f"{selected_sheet} on {selected_date}: {y_axis} vs Time")
                plt.xlabel('Time')
                plt.ylabel(y_axis)

                # Rotate x-axis labels and set font size
                plt.xticks(rotation=45, ha='right', fontsize=10)
                plt.tight_layout()  # Adjust layout to make room for x-axis labels

                st.pyplot(fig)

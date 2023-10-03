import sys
sys.path.append("C:\\Users\\kundu\\PycharmProjects\\task\\venv\\Lib\\site-packages")
import streamlit as st
import os
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import PowerTransformer
from sklearn.preprocessing import QuantileTransformer
from sklearn.preprocessing import MaxAbsScaler
from sklearn.impute import SimpleImputer
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def preprocess_data(df,columndrop,fillna_strategy,columns_to_not_transfrom,scalerchoice,encoderchoice):
    # Fill null values with mean for numerical columns
    # Drop selected columns
    df = df.drop(columndrop, axis=1)
    df=df.drop_duplicates()
    df1=df[columns_to_not_transfrom]
    df = df.drop(columns_to_not_transfrom,axis=1)
    numerical_cols = df.select_dtypes(include='number').columns
    ncols = numerical_cols.tolist()
    if ncols:
        if fillna_strategy == "mean":
            imputer = SimpleImputer(strategy='mean')
            df[numerical_cols] = imputer.fit_transform(df[numerical_cols])
        elif fillna_strategy == "median":
            imputer = SimpleImputer(strategy='median')
            df[numerical_cols] = imputer.fit_transform(df[numerical_cols])
        elif fillna_strategy == "most_frequent":
            imputer = SimpleImputer(strategy='most_frequent')
            df[numerical_cols] = imputer.fit_transform(df[numerical_cols])
        else:
            pass


        # Scale numerical columns
        if scalerchoice=='Standard':
            scaler = StandardScaler()
            df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
        elif scalerchoice=='MinMax':
            scaler=MinMaxScaler()
            df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
        elif scalerchoice=='MaxAbs':
            scaler=MaxAbsScaler()
            df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
        elif scalerchoice=='PowerTransformer':
            scaler=PowerTransformer()
            df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
        elif scalerchoice=='Quantile':
            rng = np.random.RandomState(0)
            scaler = QuantileTransformer(n_quantiles=10, random_state=0)
            df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
        elif scalerchoice=='Robust':
            scaler=RobustScaler()
            df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
        else:
            pass


    # Encode categorical columns
    categorical_cols = df.select_dtypes(include='object').columns
    ccols = categorical_cols.tolist()
    if ccols:
        if(encoderchoice=="Label"):
          encoder = LabelEncoder()
          df[categorical_cols] = df[categorical_cols].apply(encoder.fit_transform)
        elif(encoderchoice=="None"):
            encoder = LabelEncoder()
        elif(encoderchoice=="OneHot"):
            encoder=OneHotEncoder()
            enc_data = pd.DataFrame(encoder.fit_transform(df[categorical_cols]).toarray())
            # Merge with main
            df=df.join(enc_data)
    for i in df1.columns:
        extracted_col = df1[i]
        df = df.join(extracted_col)
    return df
def main():
    st.set_page_config(page_title="StackIt 🚀", page_icon=":magic_wand:", layout="wide")

    st.title("CSV File Preprocessor and uploader")
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file is not None:
        # Read uploaded file
        df = pd.read_csv(uploaded_file)
        columns_to_drop = st.multiselect("Select columns to drop", df.columns)
        columns_to_not_transfrom = st.multiselect("Select columns not to transfrom", df.columns)
        fillna_strategy = st.selectbox("Select fillna strategy", ["None","mean", "median", "most_frequent"])
        scalerchoice = st.selectbox("Select the type of scaler",
                                    ["None","MinMax", "Standard", "Robust", "PowerTransformer", "MaxAbs", "Quantile"])
        encoderchoice = st.selectbox("Select the type of Encoder", ["None","Label", "OneHot"])
        # Perform preprocessing
        preprocessed_df = preprocess_data(df, columns_to_drop, fillna_strategy, columns_to_not_transfrom, scalerchoice,
                                          encoderchoice)

        # Display preprocessed data

        st.write("Preprocessed Data")
        st.dataframe(preprocessed_df)

    text_input = st.text_input("Enter the google sheet id 👇", )

    spreadsheet_id = text_input
    # Authentication process
    credentials = None
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            credentials = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(credentials.to_json())
    try:
        service = build("sheets", "v4", credentials=credentials)
        sheets = service.spreadsheets()
        result = sheets.values().get(spreadsheetId=spreadsheet_id, range="Sheet1").execute()
        values = result.get("values", [])
        # Clear existing data in the Google Sheet


        df=preprocessed_df.copy()
        sheets.values().clear(
            spreadsheetId=spreadsheet_id,
            range="Sheet1"
        ).execute()
        # Add column names as the first row in the DataFrame
        values_to_update = [df.columns.tolist()] + df.values.tolist()

        # Specify the range where you want to update the values
        range_to_update = "Sheet1!A1"  # Update this with the desired range

        # Update the values in the Google Sheet
        sheets.values().update(
            spreadsheetId=spreadsheet_id,
            range=range_to_update,
            valueInputOption="USER_ENTERED",
            body={"values": values_to_update}
        ).execute()
        st.write("Data updated succesfully")

    except HttpError as error:
        print(error)

if __name__ == "__main__":
    main()

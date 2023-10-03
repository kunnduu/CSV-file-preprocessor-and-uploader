# CSV File Preprocessor and Uploader
I made this web app as part of a hiring task for a company 
# Here is a demo video of the working web app
- Link : https://drive.google.com/file/d/1Q2ghdXd6lCMHKFXaLhjZT4ofsEv0JFid/view?usp=sharing
This Python script provides a web-based interface for uploading CSV files, performing data preprocessing, and updating a Google Sheet with the preprocessed data. It utilizes the Streamlit library for creating the web app and various data preprocessing techniques from scikit-learn.

## Libraries Used

- `sys`: Access system-specific parameters and functions.
- `streamlit`: Create the web application.
- `os`: Interact with the operating system.
- `sklearn.preprocessing`: Perform data preprocessing tasks.
- `google.auth.transport.requests`: Handle authentication requests.
- `google.oauth2.credentials.Credentials`: Manage Google OAuth2 credentials.
- `google_auth_oauthlib.flow.InstalledAppFlow`: Perform OAuth2 flow for installed applications.
- `googleapiclient.discovery.build`: Create a Google Sheets service client.
- `googleapiclient.errors.HttpError`: Handle HTTP errors.
- `pandas`: Manipulate and read CSV data.
- `numpy`: Perform numerical operations.

## `preprocess_data` Function

This function takes an input DataFrame, processes it based on user-defined parameters, and returns a preprocessed DataFrame. Key steps:

1. Drop specified columns from the DataFrame.
2. Remove duplicate rows.
3. Split the DataFrame into two parts: columns not to be transformed and columns to be transformed.
4. Fill missing values in numerical columns based on the chosen strategy.
5. Scale numerical columns based on the selected scaling method.
6. Encode categorical columns based on the chosen encoding method.
7. Re-add the columns that were not transformed back into the preprocessed DataFrame.

## `main` Function

This function sets up the Streamlit web application and handles the main workflow:

1. Create a file uploader widget in the web app, allowing the user to upload a CSV file.
2. Create a text input field for the user to enter a Google Sheet ID.
3. Create interactive widgets for the user to select columns to drop, columns to not transform, fillna strategy, scaler choice, and encoder choice.
4. Handle Google Sheets authentication. Check if there's a token file, and if not, initiate the OAuth2 flow to obtain credentials. The credentials are stored in a token file for future use.
5. Build a Google Sheets API service client and attempt to fetch values from the specified Google Sheet.
6. Clear the existing data to upload the new data.
7. Update the Google Sheet with the preprocessed data and display a success message.

## How to Use

1. Run the script using the command: `streamlit run name_of_file.py`.
2. Upload a CSV file.
3. Select preprocessing options.
4. View the preprocessed data in the web app.
5. Enter the Google Sheet ID and update the Google Sheet with the processed data.
6. Finally, after this, you can see your preprocessed file uploaded to the Google sheet.

This script provides an efficient way to preprocess and upload CSV data to Google Sheets for further analysis.

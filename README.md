# CSV-file-preprocessor-and-uploader
This Python script provides a web-based interface for uploading CSV files, performing data preprocessing, and updating a Google Sheet with the preprocessed data. It utilizes the Streamlit library for creating the web app and various data preprocessing techniques from scikit-learn.

# Libraries Used
sys: Access system-specific parameters and functions.
streamlit: Create the web application.
os: Interact with the operating system.
sklearn.preprocessing: Perform data preprocessing tasks.
google.auth.transport.requests: Handle authentication requests.
google.oauth2.credentials.Credentials: Manage Google OAuth2 credentials.
google_auth_oauthlib.flow.InstalledAppFlow: Perform OAuth2 flow for installed applications.
googleapiclient.discovery.build: Create a Google Sheets service client.
googleapiclient.errors.HttpError: Handle HTTP errors.
pandas: Manipulate and read CSV data.
numpy: Perform numerical operations.
# preprocess_data Function
This function takes an input DataFrame, processes it based on user-defined parameters, and returns a preprocessed DataFrame. Key steps:

Drop specified columns from the DataFrame.
Remove duplicate rows.
Split the DataFrame into two parts: columns not to be transformed and columns to be transformed.
Fill missing values in numerical columns based on the chosen strategy.
Scale numerical columns based on the selected scaling method.
Encode categorical columns based on the chosen encoding method.
Re-add the columns that were not transformed back into the preprocessed DataFrame.

# main Function
This function sets up the Streamlit web application and handles the main workflow:

We first create a file uploader widget in the web app, allowing the user to upload a CSV file.
Then we create a text input field for the user to enter a Google Sheet ID
Then the next few lines create interactive widgets for the user to select columns to drop, columns to not transform, fillna strategy, scaler choice, and encoder choice
The next section handles Google Sheets authentication. It checks if there's a token file and if not, it initiates the OAuth2 flow to obtain credentials. The credentials are stored in a token file for future use.
The next lines build a Google Sheets API service client and attempt to fetch values from the specified Google Sheet.
Then we clear the existing data to upload the new data
Then we update the Google Sheet with the preprocessed data and display a success message.
How to Use
Run the script using the cmd by typing streamlit run name_of_file.py.
Upload a CSV file.
Select preprocessing options.
View the preprocessed data in the web app.
Enter the Google Sheet ID and update the Google Sheet with the processed data.
Finally after this you can see your preprocessed file uploaded to the Google sheet
This script provides an efficient way to preprocess and upload CSV data to Google Sheets for further analysis.

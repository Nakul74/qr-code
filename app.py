import streamlit as st
import json
from google.cloud import storage
import os

def upload_with_expiration(creds_path, local_file_path, bucket_name, folder_name, expiration_seconds):
    client = storage.Client.from_service_account_json(creds_path)
    source_blob_name = os.path.basename(local_file_path)
    destination_blob_name = os.path.join(folder_name, source_blob_name)
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(local_file_path)

with open('codes.json', 'r') as fp:
    codes_dict = json.load(fp)
    
creds_path = "credentials.json"
bucket_name = "xerorx-project-bucket"
folder_name = "sample3"
expiration_seconds = 120 

st.title("Zerox Business model")
st.write("Enter the information and click the Upload button")

xerox_uid = st.selectbox(label='select the xerox center', options = list(codes_dict.values()), index=0)
name = st.text_input("Enter your name")
upload_file = st.file_uploader("Upload File")
expiry_time = st.number_input("Set expiry Time in minutes", min_value=1)

if st.button("Upload"):
    if xerox_uid and name and upload_file:
        with open(upload_file.name, 'wb') as f:
            f.write(upload_file.getbuffer())
        local_file_path = upload_file.name
        folder_name = xerox_uid
        expiration_seconds = expiry_time*60
        upload_with_expiration(creds_path, local_file_path, bucket_name, folder_name, expiration_seconds)
        os.remove(upload_file.name)
        st.success('Files uploaded to bucket')
    else:
        st.error('Some fileds are missing')
    

# verify-excel

A small webtool made for Kirk Lab members to check column output for Mass Spectometry spreadsheets. This app is hosted on streamlit community cloud to allow for easy access. The user should copy and paste the column headers of the specific sheet into each respective textbox, then press ctrl + enter to check whether the sheet contains the correct columns. 

The output will appear under the textbox, and indicate any missing columns for each protein or peptide sheet. Additionally, warnings might appear for any non-column related issues, such as the number of raw abundances and the number of normalized abundances being different. 
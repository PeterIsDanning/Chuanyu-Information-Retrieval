# Chuanyu Information Retrieval
Focus on the integration and indexing of financial and social information resources in Sichuan and Chongqing. Information includes financial indexes in the secondary market, fundamental information of companies in the primary market, and Q&amp;A information from the directors' secretaries of listed companies.

This project automates the extraction and summarization of key information from EasyMoney's latest news and Q&A sessions related to Sichuan's companies in the primary market. It generates structured data (CSV files) and comprehensive reports (DOCX files) for further analysis.

* **main.py:** Python script demonstrating how to use the code.
* **tutorial.ipynb:** Jupyter Notebook demonstrating how to use the code, including:
    1. Extracting yesterday's EastMoney news for Sichuan's companies and saving the data to a CSV file.
    2. Generating a summary report (DOCX) from the extracted news data.
    3. Extracting Q&A data between investors and company secretaries and saving it to a CSV file.
    4. Generating a summary report (DOCX) from the Q&A data.
* **data/:** Stores all the data used in the project (company lists, CSV files, etc.).
* **report/:** Contains the generated DOCX reports:
    * **eastmoney/:** Reports based on EastMoney news.
    * **dongmi/:** Reports based on Q&A data.
* **utils/:** Contains Python scripts for file and data processing tasks.
* **src/:** Houses the supporting scripts.


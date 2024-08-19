# Chuanyu Information Retrieval
Focus on the integration and indexing of financial and social information resources in Sichuan and Chongqing. Information includes financial indexes in the secondary market, fundamental information of companies in the primary market, and Q&amp;A information from the directors' secretaries of listed companies.

* **tutorial.ipynb:** Jupyter Notebook demonstrating how to use the code, including:
    1. Extracting yesterday's EasyMoney news for Sichuan's companies and saving the data to a CSV file.
    2. Generating a summary report (DOCX) from the extracted news data.
    3. Extracting Q&A data between investors and company secretaries and saving it to a CSV file.
    4. Generating a summary report (DOCX) from the Q&A data.
* **data/:** Stores all the data used in the project (company lists, CSV files, etc.).
* **report/:** Contains the generated DOCX reports:
    * **easymoney/:** Reports based on EasyMoney news.
    * **dongmi/:** Reports based on Q&A data.
* **script/:** Contains Python scripts for file and data processing tasks.
* **src/:** Houses the main Python script and any supporting scripts.

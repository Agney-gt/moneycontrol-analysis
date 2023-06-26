# moneycontrol-analysis
This project is a web scraper built using Python and Selenium to extract financial data from the website moneycontrol.com. The scraper automates the process of collecting data for multiple companies listed on the website and saves the data in a structured format for further analysis.

The scraper utilizes various functionalities provided by Selenium, such as browser automation, locating elements by XPath, interacting with elements, and handling exceptions. It also incorporates other libraries like Pandas, BeautifulSoup, and NumPy for data manipulation and analysis.

The main features of this scraper include:

Scraping financial data: The code navigates to the company pages on moneycontrol.com and extracts various financial metrics such as beta, volume, sector PE, book value, price, PE ratio, EPS growth, promoter share, foreign institutional investor share, revenue, and market depth buy/sell ratio.

Scraping financial ratios: The code also visits the ratio-specific pages for each company and extracts relevant financial ratios. The ratios are then stored in a separate CSV file for each company.

Data preprocessing: After scraping the data, the code performs necessary data preprocessing tasks, such as removing commas from numeric values, filling missing values with zeros, and saving the data into a CSV file.

Linear regression analysis: The code further processes the data by preparing it for linear regression analysis. It organizes the data into separate arrays for each metric over a five-year period. It then applies linear regression models to each metric and stores the resulting trends in a new DataFrame.

Output and visualization: Finally, the code combines the original data with the linear regression trends and saves the final analysis in a CSV file. The output can be further utilized for visualizations or other statistical analysis.

https://app.noteable.io/published/ab6fdb9e-0abb-4b78-b2db-7623e78a9c8c/Moneycontrol-June-2023

The project provides a comprehensive solution for extracting and analyzing financial data from moneycontrol.com, enabling users to gain insights and perform trend analysis on various metrics. It can be used for research, investment analysis, or any application that requires financial data from the website.

import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import InvalidArgumentException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import pickle
import os
import glob
from bs4 import BeautifulSoup
from tqdm import tqdm
import numpy as np
def calc_trend(rev_list,y,strs):
    if rev_list[0]==rev_list[-1]:
        df.at[y,"5Year Overall "+strs]=-1
    elif rev_list[0]<rev_list[-1]:
        df.at[y,"5Year Overall "+strs]=0
    else:
        df.at[y,"5Year Overall "+strs]=1
    x = np.arange(len(rev_list))
    m, _ = np.polyfit(x, rev_list, 1)
    df.at[y,strs]=m
y=0
chrome_options = Options()
Options.binary_location = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'
#chrome_options.add_argument("--headless") #For AWS/GCP 
driver=webdriver.Chrome(options=chrome_options, executable_path='D:/Downloads/chromedriver.exe')
driver.delete_all_cookies()
driver.maximize_window()
action = ActionChains(driver)
df=pd.read_csv('companies.csv')
urls=df['Company Link'].to_list()
rurls=df['RatioURL'].to_list()
count=0
for url in urls[y:]:
    try:

        driver.get(url)
        time.sleep(5)
        try:
            driver.find_element(By.XPATH,"//button[@class='No thanks']").click()
        except Exception as e:
            pass
        beta=driver.find_element(By.XPATH,"//div[@class='nsebeta']").text
        df.at[y,"Beta"]=beta
        DVol=driver.find_element(By.XPATH,"//td[contains(@class,'nsev20a')]").text
        df.at[y,"20DVol"]=DVol
        SectorPE=driver.find_element(By.XPATH,"//td[contains(@class,'nsesc')]").text
        df.at[y,"SectorPE"]=SectorPE
        bvps=driver.find_element(By.XPATH,"//td[contains(@class,'nsebv')]").text
        df.at[y,"BVPS"]=bvps
        price=driver.find_element(By.XPATH,"//td[contains(@class,'nseopn')]").text
        df.at[y,"Price"]=price
        PE=driver.find_element(By.XPATH,"//span[contains(@class,'nsepe')]").text
        df.at[y,"PE"]=PE
        try:
        #bvps=driver.find_element(By.XPATH,"//td[contains(@class,'nsebv')]").text
            eps_growth=driver.find_element(By.XPATH,"//span[contains(@id,'ttm_eps')]").text
            df.at[y,"EPS-Growth"]=eps_growth
        except Exception as e:
            pass
        try:
            promoters=driver.find_elements(By.XPATH,"//div[@id='Promoter']//*[local-name()='g']//*[local-name()='text']//*[local-name()='tspan'][@class]")
            ptrend_list=[]
            pc=1
            for promoter in promoters[:5]:
                ptrend_list.append(float(promoter.text))
                df.at[y,'PromoterShare_'+str(2024-pc)]=float(promoter.text)
                pc=pc+1
                
            
        except Exception as e:
            print("Promoter Error")
            pass
        #df.at[y,"PromotersShares"]=", ".join([str(x) for x in ptrend_list])
        try:
            fii_button=driver.find_element(By.XPATH,"//li[@id='li_fii']")
            action.move_to_element(fii_button).perform()
            fii_button.click()
            time.sleep(2)
            fiis=driver.find_elements(By.XPATH,"//div[@id='FII']//*[local-name()='g']//*[local-name()='text']//*[local-name()='tspan'][@class]")
            fii_list=[]
            pc=1
            for fii in fiis[:5]:
                fii_list.append(float(fii.text))
                df.at[y,'ForeignInstitutionalInvestor_'+str(2024-pc)]=float(fii.text)
                pc=pc+1
            print(fii_list)
            
        except Exception as e:
            pass
        try:
            #df.at[y,"FIISharehoding"]=", ".join([str(x) for x in fii_list])
            revs=driver.find_elements(By.XPATH,"//div[contains(@id,'revenue')]//*[local-name()='g']//*[local-name()='text']//*[local-name()='tspan'][@class]")
            rev_list=[]
            pc=1
            for rev in revs[:5]:
                rev_list.append(float(rev.text))
                df.at[y,'Revenue_'+str(2024-pc)]=float(rev.text)
                pc=pc+1
            print(rev_list)
           
        except Exception as e:
            pass
        #df.at[y,"Revenues"]=", ".join([str(x) for x in rev_list])
        mdepth=driver.find_elements(By.XPATH,"//div[contains(@class,'ic_infoh')]")
        action.move_to_element(mdepth[0]).perform()
        action.move_to_element(mdepth[1]).perform()
        print("Moved to spread")
        time.sleep(2)
        mdepth_table=driver.find_element(By.XPATH,"//table[@id='best_5_box_table']//tbody")
        soup=BeautifulSoup(mdepth_table.get_attribute('outerHTML'),'lxml')
        Totals=soup.find_all('strong',class_="market_depth_total")
        print(Totals[0].text)
        print(Totals[1].text)
        try:
            bsell=float(Totals[0].text)/float(Totals[1].text)
            df.at[y,'Market_Depth_Buy/Sell']=bsell
        except Exception as e:
            df.at[y,'Market_Depth_Buy/Sell']="Div By 0"
            pass
    except Exception as e:
        print(e)
        pass
    driver.get(rurls[y])
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    a=driver.find_elements(By.XPATH,"//table[@class='mctable1']//tbody//tr[not(contains(@class,'bg'))]")
    
    for ele in a:
        try:
            ratios=ele.find_elements(By.XPATH,'.//td')
            rc=1
            for ratio in ratios[:-2]:
                df.at[y,ratios[0].text+"_"+str(2024-rc)]=ratios[rc].text
                rc=rc+1
        except Exception as e:
            pass
    
            
    df.to_csv('test-full.csv')
    y=y+1

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
df=pd.read_csv('test-full.csv')
df = df.replace(',', '', regex=True)
df.to_csv('strings.csv')
# Prepare the data for linear regression
years = np.array([2019, 2020, 2021, 2022, 2023]).reshape((-1, 1))
# Create a list to store all the variables
metrics_list = []
# Create a list to store all the metrics (column names)
metric_names = [
    'PromoterShare', 'ForeignInstitutionalInvestor', 'Revenue',
    'Basic EPS (Rs.)', 'Diluted EPS (Rs.)', 'Cash EPS (Rs.)',
    'Book Value [ExclRevalReserve]/Share (Rs.)', 'Book Value [InclRevalReserve]/Share (Rs.)',
    'Dividend / Share(Rs.)', 'Revenue from Operations/Share (Rs.)',
    'PBDIT/Share (Rs.)', 'PBIT/Share (Rs.)', 'PBT/Share (Rs.)',
    'Net Profit/Share (Rs.)', 'PBDIT Margin (%)', 'PBIT Margin (%)', 'PBT Margin (%)',
    'Net Profit Margin (%)', 'Return on Networth / Equity (%)',
    'Return on Capital Employed (%)', 'Return on Assets (%)', 'Total Debt/Equity (X)',
    'Asset Turnover Ratio (%)', 'Current Ratio (X)', 'Quick Ratio (X)',
    'Inventory Turnover Ratio (X)', 'Dividend Payout Ratio (NP) (%)',
    'Dividend Payout Ratio (CP) (%)', 'Earnings Retention Ratio (%)',
    'Cash Earnings Retention Ratio (%)', 'Enterprise Value (Cr.)',
    'EV/Net Operating Revenue (X)', 'EV/EBITDA (X)', 'MarketCap/Net Operating Revenue (X)',
    'Retention Ratios (%)', 'Price/BV (X)', 'Price/Net Operating Revenue',
    'Earnings Yield'
]

# Create a list to store all the variables
metrics_list = []

# Promoter Share
promoter_share = df.fillna(0)[['PromoterShare_2019', 'PromoterShare_2020', 'PromoterShare_2021', 'PromoterShare_2022', 'PromoterShare_2023']].values
metrics_list.append(promoter_share)

# Foreign Institutional Investor
fii = df.fillna(0)[['ForeignInstitutionalInvestor_2019', 'ForeignInstitutionalInvestor_2020', 'ForeignInstitutionalInvestor_2021', 'ForeignInstitutionalInvestor_2022', 'ForeignInstitutionalInvestor_2023']].values
metrics_list.append(fii)

# Revenue
revenues = df.fillna(0)[['Revenue_2019', 'Revenue_2020', 'Revenue_2021', 'Revenue_2022', 'Revenue_2023']].values
metrics_list.append(revenues)

# Market Depth Buy/Sell
#market_depth = df.fillna(0)[['Market_Depth_Buy/Sell']].values
#metrics_list.append(market_depth)

# Basic EPS (Rs.)
basic_eps = df.fillna(0)[['Basic EPS (Rs.)_2023', 'Basic EPS (Rs.)_2022', 'Basic EPS (Rs.)_2021', 'Basic EPS (Rs.)_2020', 'Basic EPS (Rs.)_2019']].values
metrics_list.append(basic_eps)

# Diluted EPS (Rs.)
diluted_eps = df.fillna(0)[['Diluted EPS (Rs.)_2023', 'Diluted EPS (Rs.)_2022', 'Diluted EPS (Rs.)_2021', 'Diluted EPS (Rs.)_2020', 'Diluted EPS (Rs.)_2019']].values
metrics_list.append(diluted_eps)

# Cash EPS (Rs.)
cash_eps = df.fillna(0)[['Cash EPS (Rs.)_2023', 'Cash EPS (Rs.)_2022', 'Cash EPS (Rs.)_2021', 'Cash EPS (Rs.)_2020', 'Cash EPS (Rs.)_2019']].values
metrics_list.append(cash_eps)

# Book Value [ExclRevalReserve]/Share (Rs.)
book_value_excl = df.fillna(0)[['Book Value [ExclRevalReserve]/Share (Rs.)_2023', 'Book Value [ExclRevalReserve]/Share (Rs.)_2022', 'Book Value [ExclRevalReserve]/Share (Rs.)_2021', 'Book Value [ExclRevalReserve]/Share (Rs.)_2020', 'Book Value [ExclRevalReserve]/Share (Rs.)_2019']].values
metrics_list.append(book_value_excl)

# Book Value [InclRevalReserve]/Share (Rs.)
book_value_incl = df.fillna(0)[['Book Value [InclRevalReserve]/Share (Rs.)_2023', 'Book Value [InclRevalReserve]/Share (Rs.)_2022', 'Book Value [InclRevalReserve]/Share (Rs.)_2021', 'Book Value [InclRevalReserve]/Share (Rs.)_2020', 'Book Value [InclRevalReserve]/Share (Rs.)_2019']].values
metrics_list.append(book_value_incl)

# Dividend / Share(Rs.)
dividend = df.fillna(0)[['Dividend / Share(Rs.)_2023', 'Dividend / Share(Rs.)_2022', 'Dividend / Share(Rs.)_2021', 'Dividend / Share(Rs.)_2020', 'Dividend / Share(Rs.)_2019']].values
metrics_list.append(dividend)

# Revenue from Operations/Share (Rs.)
revenue_operations = df.fillna(0)[['Revenue from Operations/Share (Rs.)_2023', 'Revenue from Operations/Share (Rs.)_2022', 'Revenue from Operations/Share (Rs.)_2021', 'Revenue from Operations/Share (Rs.)_2020', 'Revenue from Operations/Share (Rs.)_2019']].values
metrics_list.append(revenue_operations)

# PBDIT/Share (Rs.)
pbdit = df.fillna(0)[['PBDIT/Share (Rs.)_2023', 'PBDIT/Share (Rs.)_2022', 'PBDIT/Share (Rs.)_2021', 'PBDIT/Share (Rs.)_2020', 'PBDIT/Share (Rs.)_2019']].values
metrics_list.append(pbdit)

# PBIT/Share (Rs.)
pbit = df.fillna(0)[['PBIT/Share (Rs.)_2023', 'PBIT/Share (Rs.)_2022', 'PBIT/Share (Rs.)_2021', 'PBIT/Share (Rs.)_2020', 'PBIT/Share (Rs.)_2019']].values
metrics_list.append(pbit)

# PBT/Share (Rs.)
pbt = df.fillna(0)[['PBT/Share (Rs.)_2023', 'PBT/Share (Rs.)_2022', 'PBT/Share (Rs.)_2021', 'PBT/Share (Rs.)_2020', 'PBT/Share (Rs.)_2019']].values
metrics_list.append(pbt)

# Net Profit/Share (Rs.)
net_profit = df.fillna(0)[['Net Profit/Share (Rs.)_2023', 'Net Profit/Share (Rs.)_2022', 'Net Profit/Share (Rs.)_2021', 'Net Profit/Share (Rs.)_2020', 'Net Profit/Share (Rs.)_2019']].values
metrics_list.append(net_profit)

# PBDIT Margin (%)
pbdit_margin = df.fillna(0)[['PBDIT Margin (%)_2023', 'PBDIT Margin (%)_2022', 'PBDIT Margin (%)_2021', 'PBDIT Margin (%)_2020', 'PBDIT Margin (%)_2019']].values
metrics_list.append(pbdit_margin)

# PBIT Margin (%)
pbit_margin = df.fillna(0)[['PBIT Margin (%)_2023', 'PBIT Margin (%)_2022', 'PBIT Margin (%)_2021', 'PBIT Margin (%)_2020', 'PBIT Margin (%)_2019']].values
metrics_list.append(pbit_margin)

# PBT Margin (%)
pbt_margin = df.fillna(0)[['PBT Margin (%)_2023', 'PBT Margin (%)_2022', 'PBT Margin (%)_2021', 'PBT Margin (%)_2020', 'PBT Margin (%)_2019']].values
metrics_list.append(pbt_margin)

# Net Profit Margin (%)
net_profit_margin = df.fillna(0)[['Net Profit Margin (%)_2023', 'Net Profit Margin (%)_2022', 'Net Profit Margin (%)_2021', 'Net Profit Margin (%)_2020', 'Net Profit Margin (%)_2019']].values
metrics_list.append(net_profit_margin)

# Return on Networth / Equity (%)
return_on_networth = df.fillna(0)[['Return on Networth / Equity (%)_2023', 'Return on Networth / Equity (%)_2022', 'Return on Networth / Equity (%)_2021', 'Return on Networth / Equity (%)_2020', 'Return on Networth / Equity (%)_2019']].values
metrics_list.append(return_on_networth)

# Return on Capital Employed (%)
return_on_capital_employed = df.fillna(0)[['Return on Capital Employed (%)_2023', 'Return on Capital Employed (%)_2022', 'Return on Capital Employed (%)_2021', 'Return on Capital Employed (%)_2020', 'Return on Capital Employed (%)_2019']].values
metrics_list.append(return_on_capital_employed)

# Return on Assets (%)
return_on_assets = df.fillna(0)[['Return on Assets (%)_2023', 'Return on Assets (%)_2022', 'Return on Assets (%)_2021', 'Return on Assets (%)_2020', 'Return on Assets (%)_2019']].values
metrics_list.append(return_on_assets)

# Total Debt/Equity (X)
debt_equity = df.fillna(0)[['Total Debt/Equity (X)_2023', 'Total Debt/Equity (X)_2022', 'Total Debt/Equity (X)_2021', 'Total Debt/Equity (X)_2020', 'Total Debt/Equity (X)_2019']].values
metrics_list.append(debt_equity)

# Asset Turnover Ratio (%)
asset_turnover = df.fillna(0)[['Asset Turnover Ratio (%)_2023', 'Asset Turnover Ratio (%)_2022', 'Asset Turnover Ratio (%)_2021', 'Asset Turnover Ratio (%)_2020', 'Asset Turnover Ratio (%)_2019']].values
metrics_list.append(asset_turnover)

# Current Ratio (X)
current_ratio = df.fillna(0)[['Current Ratio (X)_2023', 'Current Ratio (X)_2022', 'Current Ratio (X)_2021', 'Current Ratio (X)_2020', 'Current Ratio (X)_2019']].values
metrics_list.append(current_ratio)

# Quick Ratio (X)
quick_ratio = df.fillna(0)[['Quick Ratio (X)_2023', 'Quick Ratio (X)_2022', 'Quick Ratio (X)_2021', 'Quick Ratio (X)_2020', 'Quick Ratio (X)_2019']].values
metrics_list.append(quick_ratio)

# Inventory Turnover Ratio (X)
inventory_turnover = df.fillna(0)[['Inventory Turnover Ratio (X)_2023', 'Inventory Turnover Ratio (X)_2022', 'Inventory Turnover Ratio (X)_2021', 'Inventory Turnover Ratio (X)_2020', 'Inventory Turnover Ratio (X)_2019']].values
metrics_list.append(inventory_turnover)

# Dividend Payout Ratio (NP) (%)
dividend_payout_np = df.fillna(0)[['Dividend Payout Ratio (NP) (%)_2023', 'Dividend Payout Ratio (NP) (%)_2022', 'Dividend Payout Ratio (NP) (%)_2021', 'Dividend Payout Ratio (NP) (%)_2020', 'Dividend Payout Ratio (NP) (%)_2019']].values
metrics_list.append(dividend_payout_np)

# Dividend Payout Ratio (CP) (%)
dividend_payout_cp = df.fillna(0)[['Dividend Payout Ratio (CP) (%)_2023', 'Dividend Payout Ratio (CP) (%)_2022', 'Dividend Payout Ratio (CP) (%)_2021', 'Dividend Payout Ratio (CP) (%)_2020', 'Dividend Payout Ratio (CP) (%)_2019']].values
metrics_list.append(dividend_payout_cp)

# Earnings Retention Ratio (%)
earnings_retention = df.fillna(0)[['Earnings Retention Ratio (%)_2023', 'Earnings Retention Ratio (%)_2022', 'Earnings Retention Ratio (%)_2021', 'Earnings Retention Ratio (%)_2020', 'Earnings Retention Ratio (%)_2019']].values
metrics_list.append(earnings_retention)

# Cash Earnings Retention Ratio (%)
cash_earnings_retention = df.fillna(0)[['Cash Earnings Retention Ratio (%)_2023', 'Cash Earnings Retention Ratio (%)_2022', 'Cash Earnings Retention Ratio (%)_2021', 'Cash Earnings Retention Ratio (%)_2020', 'Cash Earnings Retention Ratio (%)_2019']].values
metrics_list.append(cash_earnings_retention)

# Enterprise Value (Cr.)
enterprise_value = df.fillna(0)[['Enterprise Value (Cr.)_2023', 'Enterprise Value (Cr.)_2022', 'Enterprise Value (Cr.)_2021', 'Enterprise Value (Cr.)_2020', 'Enterprise Value (Cr.)_2019']].values
metrics_list.append(enterprise_value)

# EV/Net Operating Revenue (X)
ev_net_operating_revenue = df.fillna(0)[['EV/Net Operating Revenue (X)_2023', 'EV/Net Operating Revenue (X)_2022', 'EV/Net Operating Revenue (X)_2021', 'EV/Net Operating Revenue (X)_2020', 'EV/Net Operating Revenue (X)_2019']].values
metrics_list.append(ev_net_operating_revenue)

# EV/EBITDA (X)
ev_ebitda = df.fillna(0)[['EV/EBITDA (X)_2023', 'EV/EBITDA (X)_2022', 'EV/EBITDA (X)_2021', 'EV/EBITDA (X)_2020', 'EV/EBITDA (X)_2019']].values
metrics_list.append(ev_ebitda)

# MarketCap/Net Operating Revenue (X)
marketcap_net_operating_revenue = df.fillna(0)[['MarketCap/Net Operating Revenue (X)_2023', 'MarketCap/Net Operating Revenue (X)_2022', 'MarketCap/Net Operating Revenue (X)_2021', 'MarketCap/Net Operating Revenue (X)_2020', 'MarketCap/Net Operating Revenue (X)_2019']].values
metrics_list.append(marketcap_net_operating_revenue)

# Retention Ratios (%)
retention_ratios = df.fillna(0)[['Retention Ratios (%)_2023', 'Retention Ratios (%)_2022', 'Retention Ratios (%)_2021', 'Retention Ratios (%)_2020', 'Retention Ratios (%)_2019']].values
metrics_list.append(retention_ratios)

# Price/BV (X)
price_bv = df.fillna(0)[['Price/BV (X)_2023', 'Price/BV (X)_2022', 'Price/BV (X)_2021', 'Price/BV (X)_2020', 'Price/BV (X)_2019']].values
metrics_list.append(price_bv)

# Price/Net Operating Revenue
price_net_operating_revenue = df.fillna(0)[['Price/Net Operating Revenue_2023', 'Price/Net Operating Revenue_2022', 'Price/Net Operating Revenue_2021', 'Price/Net Operating Revenue_2020', 'Price/Net Operating Revenue_2019']].values
metrics_list.append(price_net_operating_revenue)

# Earnings Yield
earnings_yield = df.fillna(0)[['Earnings Yield_2023', 'Earnings Yield_2022', 'Earnings Yield_2021', 'Earnings Yield_2020', 'Earnings Yield_2019']].values
metrics_list.append(earnings_yield)

# Create a new DataFrame to store the results
result_df = pd.DataFrame()
count=0
# Iterate through metrics_list
for metric_name, metrics_data in zip(df.columns, metrics_list):
    # Iterate through rows of data
    trends=[]
    for i, row in enumerate(metrics_data):
        try:# Create feature matrix X and target variable y
            X = years
            y = row
            
            # Create and fit the linear regression model
            model = LinearRegression()
            model.fit(X, y)
            
            trends.append(model.coef_[0])
        except Exception as e:
            print(X,y,e)
    # Create a new column name for the result
    column_name = f'{metric_names[count]}_Linear_Regression'
    print(column_name)
        # Add the predicted values to the result DataFrame
    result_df[column_name] = trends
    count=count+1

    # Concatenate the result DataFrame with the original DataFrame
    output_df = pd.concat([df, result_df], axis=1)
    output_df.to_csv('test-analysis.csv')

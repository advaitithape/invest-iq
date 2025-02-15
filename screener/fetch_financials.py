from fastapi import FastAPI, HTTPException
import yfinance as yf
import pandas as pd

app = FastAPI()


def stock_info(stock):

    info = stock.info

    return {
        "Company Name": info.get("longName", "NA"),
        "About": info.get("longBusinessSummary", "NA"),
        "Current Price": info.get("currentPrice", "NA"),
        "Market Cap": info.get("marketCap", "NA"),
        "Stock PE": info.get("trailingPE", "NA"),
        "ROCE": round((info.get("returnOnEquity", 0) / info.get("debtToEquity", 1)) * 100, 2) if "returnOnEquity" in info else "N/A",
        "Book Value": info.get("bookValue", "NA"),
        "High": info.get("fiftyTwoWeekHigh", "NA"),
        "Low": info.get("fiftyTwoWeekLow", "NA"),
        "Face Value": info.get("faceValue", "NA"),
        "Sector": info.get("sector", "NA")
    }


def fetch_balance_sheet(stock):
    
    balance_sheet = stock.balance_sheet.fillna(0).astype(float)
    balance_sheet_1 = balance_sheet.drop(columns=["2020-03-31"])

    required_rows = [
        "Common Stock", "Capital Stock", "Retained Earnings", "Long Term Debt", "Current Debt", 
        "Long Term Capital Lease Obligation", "Current Capital Lease Obligation", 
        "Other Non Current Liabilities", "Minority Interest", "Accounts Payable",
        "Total Debt", "Land And Improvements", "Buildings And Improvements", 
        "Machinery Furniture Equipment", "Other Intangible Assets", "Other Properties",
        "Construction In Progress", "Investmentin Financial Assets", "Available For Sale Securities", 
        "Long Term Equity Investment", "Investmentsin Joint Venturesat Cost", "Investmentsin Associatesat Cost",
        "Inventory", "Accounts Receivable", "Cash And Cash Equivalents", "Other Current Assets", "Total Assets"
    ]

    required_balance_sheet = balance_sheet_1[balance_sheet_1.index.isin(required_rows)]
    return required_balance_sheet


def fetch_cash_flow(stock):
    
    cash_flow = stock.cashflow.fillna(0).astype(float)
    cash_flow_1 = cash_flow.drop(columns=["2020-03-31"])

    required_rows = [
        "Operating Cash Flow", "Change In Receivables", "Change In Inventory", "Change In Payable",
        "Change In Working Capital", "Taxes Refund Paid", "Other Non Cash Items", "Capital Expenditure",
        "Sale Of PPE", "Purchase Of Investment", "Sale Of Investment", "Interest Received Cfi",
        "Dividends Received Cfi", "Net Investment Purchase And Sale", "Net Other Investing Changes",
        "Common Stock Issuance", "Net Common Stock Issuance", "Issuance Of Debt","Long Term Debt Issuance",
        "Repayment Of Debt", "Long Term Debt Payments", "Interest Paid Cff", "Cash Dividends Paid",
        "Net Other Financing Changes", "Other Cash Adjustment Outside Changein Cash", "Investing Cash Flow",
        "Financing Cash Flow", "Changes In Cash" 
    ]

    required_cash_flow = cash_flow_1[cash_flow_1.index.isin(required_rows)]
    return required_cash_flow

def fetch_income_statements(stock):

    income_statements = stock.financials.fillna(0).astype(float)
    income_statements_1 = income_statements.drop(columns=["2020-03-31"])

    required_rows = [
        "Total Revenue", "Cost Of Revenue", "Gross Profit", "Operating Income",
        "Selling General And Administration", "Other Non Operating Income Expenses",
        "Interest Expense", "Reconciled Depreciation", "Pretax Income", "Tax Provision",
        "Net Income","Diluted EPS", "Basic EPS" 
    ]

    required_income_statements = income_statements_1[income_statements_1.index.isin(required_rows)]
    return required_income_statements

def fetch_quarterly_results(stock):
    
    quarterly_results = stock.quarterly_financials.fillna(0).astype(float)

    required_rows = [
        "Total Revenue", "Cost Of Revenue", "Operating Income", "Other Non Operating Income Expenses",
        "Interest Expense", "Reconciled Depreciation", "Pretax Income", "Tax Provision", "Net Income",
        "Minority Interests", "Diluted EPS", "Basic EPS"
    ]

    required_quarterly_results = quarterly_results[quarterly_results.index.isin(required_rows)]
    return required_quarterly_results


@app.get("/stock/{symbol}")
def fetch_data(symbol: str):
    
    stock = yf.Ticker(symbol + ".NS")

    company_balance_sheet = fetch_balance_sheet(stock)
    json_balance_sheet = company_balance_sheet.to_json(indent=4)

    company_cash_flow = fetch_cash_flow(stock)
    json_cash_flow = company_cash_flow.to_json(indent=4)

    company_income_statements = fetch_income_statements(stock)
    json_income_statements = company_income_statements.to_json(indent=4)

    company_quarterly_results = fetch_quarterly_results(stock)
    json_quarterly_results = company_quarterly_results.to_json(indent=4)

    return{
        "Company info": stock_info(stock),
        "Balance Sheet": json_balance_sheet,
        "Cash Flow": json_cash_flow,
        "Income Statement": json_income_statements,
        "Quarterly Results": json_quarterly_results
    }
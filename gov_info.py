import requests

headers = {
    'Content-Type': 'application/json',
}
payload = {"award_levels":["prime_awards"],"filters":{"award_types":["contracts","direct_payments","grants","idvs","loans","other_financial_assistance"],"agency":"United States Mint","date_type":"action_date","date_range":{"start_date":"2019-01-01","end_date":"2019-01-31"}},"columns":[],"file_format":"csv"}
data = {"award_levels":["prime_awards"],"filters":{"award_types":["contracts","direct_payments","grants","idvs","loans","other_financial_assistance"],"agency":"all","date_type":"action_date","date_range":{"start_date":"2019-01-01","end_date":"2019-01-31"}},"columns":[],"file_format":"csv"}

response = requests.get('https://transparency.treasury.gov/services/api/fiscal_service//v1/accounting/dts/dts_table_1')
print(response.text)
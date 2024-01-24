import pprint as pp

import pandas as pd
import requests


def fetch_scopus_paper(api_key, query):
    url = "https://api.elsevier.com/content/search/scopus"
    headers = {"X-ELS-APIKey": api_key, "Accept": "application/json"}

    # Initial request to get the total count
    initial_params = {"query": query, "count": 1}
    initial_response = requests.get(url, headers=headers, params=initial_params)

    if initial_response.status_code != 200:
        return f"Initial request error: {initial_response.status_code}"

    total_count = (
        initial_response.json()
        .get("search-results", {})
        .get("opensearch:totalResults", 0)
    )
    total_count = int(total_count)

    # Fetch data in batches due to API limits
    entries = []
    batch_size = 25  # Adjust batch size as per API limits and your requirements
    for start in range(0, total_count, batch_size):
        params = {"query": query, "count": batch_size, "start": start}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            batch_entries = response.json().get("search-results", {}).get("entry", [])
            entries.extend(batch_entries)
        else:
            print(f"Error fetching data: {response.status_code}")

    return entries


def parse_papers_to_df(entries):
    df = pd.DataFrame(entries)
    return df


def save_to_csv(df, file_name):
    df.to_csv(file_name, index=False)
    print(f"Data saved to {file_name}")


import json

# 打开JSON文件
with open("./AJGlist.json", "r") as file:
    # 读取文件并将JSON转化为Python列表
    data = json.load(file)

# 显示数据
print(data)


api_key = "014f542e11b109cfb82972c66479341a"
# 现在你可以像使用普通列表一样使用data变量
for journal in data:
    query = f"SRCTITLE({journal}) AND ABS((DEA OR data envelopment) AND (chinese bank))"
    # file_name = "scopus_papers_DEA_Chinese_Banks"  # Name of the CSV file to save

    # Fetching papers
    entries = fetch_scopus_paper(api_key, query)

    # Replace 'YOUR_API_KEY' and 'YOUR_SEARCH_QUERY' with your actual API key and search query

    # query = "SRCTITLE(European Journal of Operational Research) AND SUBJAREA(BUSI) AND ABS(DEA OR data envelopment analysis) AND TITLE-ABS-KEY(DEA OR efficiency AND (chinese AND bank OR banking OR banks))"

    if isinstance(entries, list):
        papers_df = parse_papers_to_df(entries)
        if papers_df.shape[0] > 0:
            print(f"we get {papers_df.shape[0]} results containing keywords {journal}!")
            save_to_csv(papers_df, f"DEA_CHN_banks_{journal}.csv")
    else:
        print(entries)

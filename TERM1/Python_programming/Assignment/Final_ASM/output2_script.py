import requests

import pandas as pd

import gender_guesser.detector as gender
import plotly.express as px

def call_api_with(url_extension):
    your_company_house_api_key = "9ca44c28-e54d-4c26-9bf7-6c766c53c054"

    login_headers = {"Authorization": your_company_house_api_key}
    url = f"https://api.companieshouse.gov.uk/{url_extension}"
    # above: could be eg. https://api.companieshouse.gov.uk/search/companies?q=shop&items_per_page=1
    print(f"requesting: {url}")
    # above, optional: printing, so that you see visually how many calls you are making
    res = requests.get(url, headers=login_headers)  # , verify=False)
    return res.json()


def all_officers_in_company(company_number):
    url = f"company/{company_number}/officers"

    return call_api_with(url).get("items", [])

top10FintechCompanies = pd.read_csv(
    "https://raw.githubusercontent.com/REDhawC/EDI_BUSANA/master/Python_programming/Assignment/Final_ASM/TOP10_Fintech_Companies.csv"
)

top10FintechCompanies = top10FintechCompanies.drop(columns=["Unnamed: 3"])
# Convert 'company_number' to string and pad with '0' to a length of 8
top10FintechCompanies['company_number'] = top10FintechCompanies['company_number'].astype(str).str.zfill(8)

# Display the first few rows of the DataFrame
top10FintechCompanies

# Initialize an empty list to store the officers' information
officers_info = []

# Iterate over each company number in the DataFrame
for companyNum in top10FintechCompanies["company_number"]:
    # Get the officers for the current company
    officers = all_officers_in_company(companyNum)

    # Initialize an empty list to store the current company's officers' information
    current_officers_info = []

    # Iterate over each officer
    for officer in officers:
        # Extract the required information and add it to the list
        current_officers_info.append(
            {
                "name": officer.get("name"),
                "identification": officer.get("identification"),
                "nationality": officer.get("nationality"),
            }
        )

    # Add the current company's officers' information to the list
    officers_info.append(current_officers_info)

# Add the officers' information to the 'officers_info' column of the DataFrame
top10FintechCompanies["officers_info"] = pd.Series(officers_info)

# Display the first few rows of the DataFrame
top10FintechCompanies.head()

top10FintechCompanies

top10FintechCompanies["officers_info"] = top10FintechCompanies["officers_info"].apply(
    lambda officers: [
        officer for officer in officers if officer["identification"] is None
    ]
)

top10FintechCompanies["officers_info"][0]

top10FintechCompanies["officers_info"][1]

# 提取高管姓名的函数
def extract_names(officers_list):
    return [officer["name"] for officer in officers_list if "name" in officer]


top10FintechCompanies["officer_names"] = top10FintechCompanies["officers_info"].apply(
    extract_names
)

detector = gender.Detector(case_sensitive=False)


def guess_gender(names):
    male_count = 0
    female_count = 0
    for name in names:
        if len(name.split(", ")) > 1:
            first_name = name.split(", ")[1].split()[0]  # 假设名字是逗号后的第一个词
            guessed_gender = detector.get_gender(first_name)
            if guessed_gender in ["male", "mostly_male"]:
                male_count += 1
            elif guessed_gender in ["female", "mostly_female"]:
                female_count += 1
    return male_count, female_count


(
    top10FintechCompanies["Male Officers Number"],
    top10FintechCompanies["Female Officers Number"],
) = zip(*top10FintechCompanies["officer_names"].apply(guess_gender))

# Sort companies by total_funding and assign rankings
top10FintechCompanies = top10FintechCompanies.sort_values(
    by="total_funding", ascending=False
)
top10FintechCompanies["Rank"] = range(1, len(top10FintechCompanies) + 1)

# Adjust Funding based on the ranking
multipliers = {rank: 20 - 2 * (rank - 1) for rank in top10FintechCompanies["Rank"]}
top10FintechCompanies["Adjusted Funding"] = (
    top10FintechCompanies["Rank"].map(multipliers)
    * top10FintechCompanies["total_funding"]
)

# Calculate the officer percentages
top10FintechCompanies["Male Officer Percentage"] = (
    top10FintechCompanies["Male Officers Number"]
    / (
        top10FintechCompanies["Male Officers Number"]
        + top10FintechCompanies["Female Officers Number"]
    )
    * 100
)
top10FintechCompanies["Female Officer Percentage"] = (
    top10FintechCompanies["Female Officers Number"]
    / (
        top10FintechCompanies["Male Officers Number"]
        + top10FintechCompanies["Female Officers Number"]
    )
    * 100
)

# Recalculate Funding per officer based on the adjusted funding
top10FintechCompanies["Funding per Officer"] = top10FintechCompanies[
    "Adjusted Funding"
] / (
    top10FintechCompanies["Male Officers Number"]
    + top10FintechCompanies["Female Officers Number"]
)

# Create separate data for male and female officers
male_data = top10FintechCompanies[
    ["company_name", "Male Officers Number", "Funding per Officer"]
].copy()
male_data["Funding"] = (
    male_data["Male Officers Number"] * male_data["Funding per Officer"]
)
male_data["Gender"] = "Male"
male_data["Percentage"] = top10FintechCompanies["Male Officer Percentage"]

female_data = top10FintechCompanies[
    ["company_name", "Female Officers Number", "Funding per Officer"]
].copy()
female_data["Funding"] = (
    female_data["Female Officers Number"] * female_data["Funding per Officer"]
)
female_data["Gender"] = "Female"
female_data["Percentage"] = top10FintechCompanies["Female Officer Percentage"]

# Combine male and female data
nested_data = pd.concat([male_data, female_data], ignore_index=True)

# You can now use nested_data to create a treemap
# ... [Treemap creation code] ...

# 创建嵌套树状图，并定义颜色映射
fig = px.treemap(
    nested_data,
    path=["company_name", "Gender"],
    values="Funding",
    color="Gender",
    custom_data=["Percentage"],  # 添加自定义数据
    color_discrete_map={"Male": "#4169E1", "Female": "#FF1493"},  # 为Male和Female指定颜色
)

# 设置文本模板，显示自定义数据
fig.update_traces(
    texttemplate="%{label}<br>%{customdata[0]:.2f}%", textposition="middle center"
)

# 设置图表标题
fig.update_layout(
    title="Treemap of UK's Top 10 Fintech Companies: Comparison Between <br>Funding and Gender Percentage of Officers",
    autosize=False,
    width=800,
    height=500,
)

# 显示图表
fig.show()
fig.write_image("treemap.png", scale=2)


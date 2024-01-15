import pandas as pd
import requests


def advanced_company_search(**kwargs):
    api_key = "9ca44c28-e54d-4c26-9bf7-6c766c53c054"
    url = "https://api.company-information.service.gov.uk/advanced-search/companies"
    headers = {"Authorization": api_key}
    response = requests.get(url, headers=headers, params=kwargs)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Request failed", "status_code": response.status_code}


# 示例用法
search_params = {
    "sic_codes": "64191",
    "incorporated_from": "2015-01-01",
    "incorporated_to": "2023-01-01",
    "size": 5000,
    "start_index": 0,
}
results_original = advanced_company_search(**search_params)

results = results_original["items"]

print(len(results))

locations = []

# Convert the list to a DataFrame
df = pd.DataFrame(results)


# Expand the 'registered_office_address' column into separate columns
address_df = df["registered_office_address"].apply(pd.Series)

# Join the new columns with the original DataFrame
df = pd.concat([df.drop(["registered_office_address"], axis=1), address_df], axis=1)

# Convert 'date_of_cessation' and 'date_of_creation' to datetime and get the year
df["year_of_cessation"] = pd.to_datetime(df["date_of_cessation"]).dt.year
df["year_of_creation"] = pd.to_datetime(df["date_of_creation"]).dt.year
df["year_of_cessation"] = df["year_of_cessation"].astype("Int64")

# Display the first few rows of the DataFrame
df.head()

# Select rows where 'locality' is 'Birmingham' and 'year_of_creation' is 2015
selected_rows = df[(df["locality"] == "Bradford") & (df["year_of_creation"] == 2017)]

# Count the number of such rows
num_companies = len(selected_rows)

# Display the result
num_companies


def calculate_cessation_rate(df):
    # 初始化一个新的DataFrame来存储结果
    years = range(2015, 2023)
    columns = (
        ["locality"]
        + [f"{year}_created" for year in years]
        + [f"{year}_ceased" for year in years]
        + [f"{year}_cessation_rate" for year in years]
    )
    summary_df = pd.DataFrame(columns=columns)
    summary_df["locality"] = df["locality"].unique()

    # 遍历每年进行计算
    for year in years:
        # 计算每个城市在特定年份创建的公司数量
        created = (
            df[df["year_of_creation"] == year]
            .groupby("locality")["company_number"]
            .count()
        )
        # 计算每个城市在特定年份停业的公司数量
        ceased = (
            df[df["year_of_cessation"] == year]
            .groupby("locality")["company_number"]
            .count()
        )

        summary_df[f"{year}_created"] = summary_df["locality"].map(created)
        summary_df[f"{year}_ceased"] = summary_df["locality"].map(ceased)
        summary_df[f"{year}_cessation_rate"] = (
            summary_df[f"{year}_ceased"] / summary_df[f"{year}_created"]
        )

    # 处理NaN值
    summary_df.fillna(0, inplace=True)

    return summary_df


# 使用函数计算并生成新的DataFrame
new_df = calculate_cessation_rate(df)
new_df.head()  # 展示前几行以检查结果

new_df.loc[new_df["locality"] == "Cardiff", "2015_ceased"]

# 计算每个城市的公司数量
counts = df["locality"].value_counts()

# 获取公司数量大于30的城市列表
counts_greater_than30 = counts[counts > 30]
cities_to_keep = counts_greater_than30.index.tolist()

# 过滤数据框以保留这些城市的数据
filtered_df = new_df[new_df["locality"].isin(cities_to_keep)]

filtered_df

import pandas as pd
from geopy.geocoders import Nominatim

# 确保您已加载了DataFrame 'filtered_df'
# 如果还没有加载，可以使用类似下面的代码加载它：
# filtered_df = pd.read_csv('path_to_your_csv_file.csv')  # 替换为您的CSV文件路径

# 初始化地理编码器
geolocator = Nominatim(user_agent="geoapiExercises")


# 函数：根据城市名获取纬度和经度
def get_lat_long(city):
    try:
        location = geolocator.geocode(city + ", UK")  # 假设所有城市都在英国
        return location.latitude, location.longitude
    except:
        return None, None


# 为数据集中的每个城市添加经纬度
for city in filtered_df["locality"].unique():
    lat, lon = get_lat_long(city)
    filtered_df.loc[filtered_df["locality"] == city, "latitude"] = lat
    filtered_df.loc[filtered_df["locality"] == city, "longitude"] = lon

# 检查添加了坐标的数据集
filtered_df.head()
# 可以选择保存更新后的数据


import pandas as pd
import plotly.express as px

# 假设您已经加载了带有经纬度的filtered_df
# filtered_df = pd.read_csv('path_to_your_updated_csv_file.csv')

# 准备数据，将年份数据合并到一列
data = []
for year in range(2016, 2023):
    temp_df = filtered_df[
        [
            "locality",
            "latitude",
            "longitude",
            f"{year}_created",
            f"{year}_cessation_rate",
        ]
    ]
    temp_df["year"] = year
    temp_df = temp_df.rename(
        columns={
            f"{year}_created": "Bank Created",
            f"{year}_cessation_rate": "Cessation Rate",
        }
    )
    data.append(temp_df)
map_data = pd.concat(data)

# 确定cessation_rate的最小值和最大值
min_cessation_rate = map_data["Cessation Rate"].min()
max_cessation_rate = map_data["Cessation Rate"].max()

custom_color_scale = [[0, "yellow"], [1, "red"]]  # 浅黄色  # 深红色

# 创建气泡图
fig = px.scatter_mapbox(
    map_data,
    lat="latitude",
    lon="longitude",
    hover_name="locality",
    hover_data=["Bank Created", "Cessation Rate"],
    color="Cessation Rate",
    size="Bank Created",
    animation_frame="year",
    color_continuous_scale=custom_color_scale,
    range_color=[min_cessation_rate, max_cessation_rate],  # 设置颜色比例尺范围
    size_max=100,
    zoom=4.9,
    height=600,
)

# 设置地图样式
fig.update_layout(
    mapbox_style="open-street-map",
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    title="Visualisation of New Bank Creation and Bank Cessation Rate<br> in the UK from 2016 to 2022",
)

fig.update_traces(marker=dict(opacity=0.80))
# 添加注释
fig.add_annotation(
    text="The larger the bubble size, the more banks are established in the area;<br> the darker the color, the higher the bank closure rate (= number of closed banks / number of new banks) in the area.",
    align="left",
    showarrow=False,
    xref="paper",
    yref="paper",
    x=0,
    y=-0.1,
    bgcolor="white",
    font=dict(size=12, color="black"),  # 调整为您希望的大小
)


# 显示图表
fig.show()

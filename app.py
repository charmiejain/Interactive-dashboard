# TO RUN : python -m streamlit run C:/Users/charm/OneDrive/Desktop/app.py
#TO RUN THIS CODE : streamlit run d:/OneDrive/Desktop/app.py

# import pandas lib as pd
import pandas as pd
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit


st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")
# read by default 1st sheet of an excel file
df = pd.read_excel(r'C:/Users/charm/OneDrive/Desktop/Datasets/Sample - Superstore.xls')


#print(df)

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
City = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

Country = st.sidebar.multiselect(
    "Select the Country:",
    options=df["Country"].unique(),
    default=df["Country"].unique(),
)

State = st.sidebar.multiselect(
    "Select the State:",
    options=df["State"].unique(),
    default=df["State"].unique()
)

df_selection = df.query(
    "City == @City & Country ==@Country & State == @State"
)

#st.dataframe(df_selection)



# ---- MAINPAGE ----
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# TOP KPI's
total_sales = int(df_selection["Sales"].sum())
average_quantity = round(df_selection["Quantity"].mean(), 1)
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
#average_profit =  int(round(average_profit, 0))
average_sale_by_transaction = round(df_selection["Sales"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("""---""")

# SALES BY CATEGORY [BAR CHART]
sales_by_category = df_selection.groupby(by=["Category"])[["Sales"]].sum().sort_values(by="Sales")
fig_product_sales = px.bar(
    sales_by_category,
    x="Sales",
    y=sales_by_category.index,
    orientation="h",
    title="<b>Sales by Category</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_category),
    template="plotly_white",
)



fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

#st.plotly_chart(fig_product_sales)

# SALES BY Region [BAR CHART]
sales_by_region = df_selection.groupby(by=["Region"])[["Sales"]].sum()
fig_region_sales = px.bar(
    sales_by_region,
    x=sales_by_region.index,
    y="Sales",
    title="<b>Sales by Region</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_region),
    template="plotly_white",
)
fig_region_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

#st.plotly_chart(fig_region_sales)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_region_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
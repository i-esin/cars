import streamlit as st
import pandas as pd

st.set_page_config("Home", layout="wide")

# Home and layout
st.header("Home")

# Ingest
filename = "1.csv"
df = pd.read_csv(f"Data/{filename}", sep=",")

# cleaning

# transformations
df["Verwachte kms"] = pd.to_numeric(df["Verwachte kms"].str.split(" ").str[0])


with st.sidebar:
    st.header("Filters")
    input_makes = st.multiselect("Make", options=df["Make"].unique())
    
    # Checkbox for each unique transmission value
    input_versnellingen = list(df["Versnellingen"].unique())

    for versnelling in input_versnellingen:
        st.checkbox(versnelling)

    # Filter by Price range
    input_price_range = st.slider(
        "Price range", 
        min_value=0,
        max_value=20_000,
        value=(0, 20000),
        step=1000
    )
    
    # Filter by Kilometerstand
    input_kilometerstand = st.slider(
        "Kilometerstand",
        min_value=0,
        max_value=int(df["Verwachte kms"].max()),
        value=(0, int(df["Verwachte kms"].max())),
        step=1000
    )

# Filter the DataFrame based on the selected makes
if input_makes:
    df = df[df["Make"].isin(input_makes)]

# Filter the DataFrame based on the selected transmission values
if input_versnellingen:
    df = df[df["Versnellingen"].isin(input_versnellingen)]

# df = df[(df["Price"] >= input_price_range[0]) & (df["Price"] <= input_price_range[1])]
df = df[(df["Verwachte kms"] >= input_kilometerstand[0]) & (df["Verwachte kms"] <= input_kilometerstand[1])]


# Display car info
tab_cars, tab_raw_table = st.tabs(["Overview", "Raw table"])

with tab_cars:
    df["fotos"] = df["fotos"].str.split(" , ")
    for _, row in df.iterrows():
        with st.container():
            st.header(f"""{row["Make"]} - {row["Model"]}""")
            st.write(f"""**Offerte**: {row["Offerte"]}""")
            st.write(f"""**Type**: {row["Type"]}""")
            st.write(f"""**Versnellingen**: {row["Versnellingen"]}""")
            # with st.expander("foto's"):
            st.image(row["fotos"], width=250)
            st.write("---")


with tab_raw_table:
    st.dataframe(
        df,
        use_container_width=True
    )

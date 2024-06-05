import streamlit as st
import pandas as pd

st.set_page_config("Home", layout="wide")

# Ingest
filename = "1.csv"
df = pd.read_csv(f"Data/{filename}", sep=",")

# cleaning

# transformations
df["Verwachte kms"] = pd.to_numeric(df["Verwachte kms"].str.split(" ").str[0])
df["Eerste Inschrijving Year"] = df["Eerste Inschrijving"].astype("datetime64[ns]").dt.year
df["fotos"] = df["fotos"].str.split(" , ")

with st.sidebar:
    st.header("Filters")

    # Filter make (merk)
    input_makes = st.selectbox("Merk", options=sorted(df["Make"].unique()), index=None)
    if input_makes:
        df = df[df["Make"] == input_makes]
        
        # Filter model
        input_model = st.selectbox("Model", options=df["Model"].unique(), index=None)
        if input_model:
            df = df[df["Model"] == input_model]
    
    # Filter versnellingen
    input_versnellingen = st.multiselect("Versnellingsbak", options=df["Versnellingen"].unique())
    if input_versnellingen:
        df = df[df["Versnellingen"].isin(input_versnellingen)]
    
    # Filter inschrijving
    input_inschrijving = st.selectbox(
        "Eerste registratie",
        options=sorted(
            df["Eerste Inschrijving Year"].unique(),
            reverse=True),
        index=None
    )
    if input_inschrijving:
        df = df[df["Eerste Inschrijving Year"] >= input_inschrijving]

    # Filter brandstof
    input_brandstof = st.multiselect(
        "Type brandstof",
        options=df["Brandstof"].unique()
    )
    if input_brandstof:
        df = df[df["Brandstof"].isin(input_brandstof)]

    # Filter price
    input_price_range = st.slider(
        "Prijs (€)", 
        min_value=0,
        max_value=20_000,
        value=(0, 20000),
        step=1000
    )
    # TODO: filter df by price
    
    # Filter kilometerstand
    input_kilometerstand = st.slider(
        "Kilometerstand",
        min_value=0,
        max_value=int(df["Verwachte kms"].max()),
        value=(0, int(df["Verwachte kms"].max())),
        step=1000
    )
    df = df[(df["Verwachte kms"] >= input_kilometerstand[0]) & (df["Verwachte kms"] <= input_kilometerstand[1])]


# Display simple stats
st.write(f"""**{str(len(df))} Resultaten** voor uw keuze""")

# Display tabs
tab_cars, tab_raw_table = st.tabs(["Overview", "Raw table"])

with tab_cars:
    for _, row in df.iterrows():
        with st.container():
            col_description, col_images = st.columns(2)
            col_description.header(f"""{row["Make"]} {row["Model"]} :grey[{row["Type"]}]""")
            col_description_1, col_description_2 = col_description.columns(2)
            col_description_1.write(f"""**Offerte**:\n{row["Offerte"]}""")
            col_description_1.write(f"""**Type**: {row["Type"]}""")
            col_description_1.write(f"""**Versnellingen**: {row["Versnellingen"]}""")
            col_description_1.write(f"""**Eerste Inschrijving**: {row["Eerste Inschrijving"]}""")
            col_description_1.write(f"""**Brandstof**: {row["Brandstof"]}""")
            col_description_1.write(f"""**Verwachte kms**: {row["Verwachte kms"]}""")
            col_description_2.write(f"""**Verwachte levertermijn**: {row["Verwachte levertermijn"]}""")
            col_description_2.write(f"""**Kleur (exterieur)**: {row["Kleur"]}""")
            col_description_2.write(f"""**Interieur**: {row["Interieur"]}""")
            col_description_2.write(f"""**VIN**: {row["VIN"]}""")
            col_description.write(f"""**Schades**: {row["Schades"]}""")
            
            with st.expander("Meer info"):
                col1, col2 = st.columns(2)
                col1.write(f"""**Vermogen**: {row["Vermogen"]}""")
                col1.write(f"""**CC**: {row["CC"]}""")
                col1.write(f"""**BTW**: {row["BTW"]}""")
                col1.write(f"""**Dealer**: {row["Dealer"]}""")
                col1.write(f"""**Straat**: {row["Straat"]}""")
                col2.write(f"""**Plaats**: {row["Plaats"]}""")
                col2.write(f"""**Postcode**: {row["Postcode"]}""")
                col2.write(f"""**Tel**: {row["Tel"]}""")
                col2.write(f"""**Mobile**: {row["Mobile"]}""")

            col_images.image(row["fotos"], width=100)
            st.write("---")


with tab_raw_table:
    st.dataframe(
        df,
        use_container_width=True
    )

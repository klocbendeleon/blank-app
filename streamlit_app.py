import streamlit as st
import pandas as pd

# Flavor profile presets
profiles = {
    "Bright & Sweet": {"mg_conc": 5.0, "ca_conc": 1.0, "note": "Fruity, high clarity, sparkling acidity"},
    "Balanced": {"mg_conc": 4.3, "ca_conc": 2.5, "note": "Sweet, clear, medium body"},
    "Rich & Heavy": {"mg_conc": 3.0, "ca_conc": 4.0, "note": "Chocolatey, full-bodied, low acidity"},
    "Clean & Crisp": {"mg_conc": 5.5, "ca_conc": 0.8, "note": "Tea-like, bright, delicate body"}
}

st.title("Water Profile Calculator with GH & KH")
st.markdown("""
Customize your coffee brewing water by selecting target KH and a flavor profile. The app calculates Le Minerale and distilled water mix, total TDS, and estimated GH in ppm.
""")

with st.expander("What do KH and GH control in flavor?"):
    st.markdown("""
    **KH (Carbonate Hardness / Alkalinity)**
    - Controls **acidity and brightness** in your coffee.
    - Low KH → brighter, more vibrant cups (can be sour if too low).
    - High KH → duller, flatter cups, but more stable.

    **GH (General Hardness / Calcium + Magnesium)**
    - Controls **extraction strength and body**.
    - Magnesium → boosts sweetness and clarity.
    - Calcium → enhances body and roundness.

    | Parameter | Affects           | Too Low                  | Too High                   |
    |-----------|-------------------|--------------------------|----------------------------|
    | KH        | Acidity balance   | Sour, unstable flavor     | Flat, muted, dull cup      |
    | GH        | Extraction & body | Weak, under-extracted     | Chalky, muddy, heavy body  |

    Recommended: KH ~40–70 ppm, GH ~50–150 ppm with more magnesium for clarity.
    """)

num_batches = st.number_input("How many batches would you like to compare?", min_value=1, value=1, step=1)

for i in range(num_batches):
    st.subheader(f"Batch {i+1}")

    selected_profile = st.selectbox(f"Flavor Profile for Batch {i+1}", list(profiles.keys()), key=f"profile_{i}")
    profile = profiles[selected_profile]
    st.markdown(f"_Flavor Note: **{profile['note']}**_")

    batch_size = st.number_input(f"Batch Size (L) for Batch {i+1}", min_value=0.1, value=1.0, step=0.1, key=f"batch_size_{i}")
    target_kh = st.number_input(f"Target KH (ppm) for Batch {i+1}", min_value=1.0, value=45.0, step=1.0, key=f"target_kh_{i}")

    mg_conc = profile['mg_conc']
    ca_conc = profile['ca_conc']
    dose_per_liter = 10.0  # Fixed dose in mL per L

    calculate = st.button(f"Calculate Batch {i+1}", key=f"calc_{i}")

    if calculate:
        try:
            dilution_factor = 133 / target_kh
            le_minerale_ratio = 1 / dilution_factor

            le_minerale = le_minerale_ratio * batch_size
            distilled = (1 - le_minerale_ratio) * batch_size
            concentrate = dose_per_liter * batch_size

            mg_total = mg_conc * batch_size  # grams of MgSO4 to use
            ca_total = ca_conc * batch_size  # grams of CaCl2 to use

            mg_ppm = mg_conc * dose_per_liter
            ca_ppm = ca_conc * dose_per_liter

            gh_ppm = mg_ppm + ca_ppm
            estimated_tds = (le_minerale_ratio * 255.5) + gh_ppm

            st.success(f"""
            **Results for Batch {i+1}:**

            - Le Minerale: {le_minerale:.2f} L
            - Distilled Water: {distilled:.2f} L
            - Concentrate: {concentrate:.0f} mL

            - KH: {target_kh:.0f} ppm
            - GH: {gh_ppm:.0f} ppm

            - Estimated TDS: {estimated_tds:.0f} ppm

            - Magnesium Sulfate: {mg_total:.2f} g
            - Calcium Chloride: {ca_total:.2f} g

            **Instructions:**
            Mix {mg_total:.2f} g of Magnesium Sulfate and {ca_total:.2f} g of Calcium Chloride into {concentrate:.0f} mL of concentrate. Then combine with {le_minerale:.2f} L of Le Minerale and {distilled:.2f} L of Distilled Water.
            """)

        except Exception as e:
            st.error(f"Error: {e}")

if st.button("Reset All"):
    st.experimental_rerun()
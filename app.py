import json
import streamlit as st

# Load JSON
with open("data/food.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Page config
st.set_page_config(page_title="Food Sensitivity Report", layout="wide")

st.title("🧬 Food Sensitivity Report")

# Global DAO value
if "globalLR" in data["data"]:
    for global_entry in data["data"]["globalLR"]:
        st.metric(label=f"{global_entry['name']} ({global_entry['shortName']})", value=global_entry["value"])

st.markdown("---")

# Prepare categorized lists
verträglich_text = []
unverträglich_text = []

for category in data["data"]["categories"]:
    verträglich_foods = []
    unverträglich_foods = []

    for food in category.get("foods", []):
        degree = int(food.get("reactionDegree", 0))
        if degree == 0:
            verträglich_foods.append(f"- {food['name']}")
        elif degree >= 1:
            unverträglich_foods.append(f"- {food['name']}")

    if verträglich_foods:
        verträglich_text.append(f"{category['name']}\n" + "\n".join(verträglich_foods) + "\n")
    if unverträglich_foods:
        unverträglich_text.append(f"{category['name']}\n" + "\n".join(unverträglich_foods) + "\n")

verträglich_output = "\n".join(verträglich_text).strip()
unverträglich_output = "\n".join(unverträglich_text).strip()

# Download buttons
colA, colB = st.columns(2)
with colA:
    st.download_button(
        label="⬇️ Verträgliche Lebensmittel herunterladen",
        data=verträglich_output,
        file_name="vertraegliche_lebensmittel.txt",
        mime="text/plain"
    )
with colB:
    st.download_button(
        label="⬇️ Unverträgliche Lebensmittel herunterladen",
        data=unverträglich_output,
        file_name="unvertraegliche_lebensmittel.txt",
        mime="text/plain"
    )

st.markdown("---")

# Filter Option
filter_option = st.radio(
    "Filter anzeigen:",
    options=["Alle", "Nur verträglich (Grad 0)", "Nur unverträglich (Grad ≥ 1)"],
    horizontal=True
)

# Category Loop
for category in data["data"]["categories"]:
    foods = category.get("foods", [])

    # Filter logic
    if filter_option == "Nur verträglich (Grad 0)":
        foods = [f for f in foods if int(f.get("reactionDegree", 0)) == 0]
    elif filter_option == "Nur unverträglich (Grad ≥ 1)":
        foods = [f for f in foods if int(f.get("reactionDegree", 0)) >= 1]

    if not foods:
        continue

    st.header(category["name"])

    for food in foods:
        col1, col2, col3 = st.columns([3, 2, 2])
        with col1:
            st.markdown(f"**{food['name']}**")
        with col2:
            st.markdown(f"Lab Result: `{food['labResult']}`")
        with col3:
            degree = int(food.get("reactionDegree", 0))
            color = food.get("labelColor", "#9cdb9b")
            st.markdown(
                f'<div style="padding: 0.3em; background-color: {color}; border-radius: 5px; text-align: center;">'
                f'Reaction Degree: {degree}</div>',
                unsafe_allow_html=True,
            )
    st.markdown("---")

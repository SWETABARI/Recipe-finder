
import re
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Smart Ingredient-Based Recipe Finder",
    page_icon="🥗",
    layout="wide"
)

st.title("🥗 Smart Ingredient-Based Recipe Finder")
st.write(
    "Enter the ingredients available in your kitchen. "
    "The system ranks recipes using ingredient overlap and prioritizes "
    "recipes that require fewer additional ingredients."
)

@st.cache_data
def load_data(path):
    data = pd.read_csv(path)
    required = {"title", "ingredients", "instructions"}
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"Dataset is missing columns: {', '.join(sorted(missing))}")
    data["ingredients"] = data["ingredients"].fillna("")
    data["title"] = data["title"].fillna("")
    data["instructions"] = data["instructions"].fillna("")
    return data

def normalize(text):
    text = str(text).lower()
    # Keep words/numbers and remove quantities/punctuation.
    text = re.sub(r"\([^)]*\)", " ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    tokens = text.split()
    # Common quantity/unit words are ignored.
    stop = {
        "cup", "cups", "tbsp", "tsp", "tablespoon", "tablespoons",
        "teaspoon", "teaspoons", "oz", "ounce", "ounces", "lb", "lbs",
        "pound", "pounds", "gram", "grams", "kg", "ml", "liter", "liters",
        "clove", "cloves", "piece", "pieces", "large", "small", "medium",
        "fresh", "chopped", "diced", "minced", "sliced", "ground"
    }
    return {t for t in tokens if t not in stop and not t.isdigit() and len(t) > 1}

def ingredient_score(user_items, recipe_items):
    matched = user_items & recipe_items
    missing = recipe_items - user_items
    # Main IR-style overlap score: Jaccard similarity.
    union = user_items | recipe_items
    jaccard = len(matched) / len(union) if union else 0
    coverage = len(matched) / len(user_items) if user_items else 0
    # Bonus for using more of the user's ingredients and penalty for extras.
    score = 0.65 * coverage + 0.35 * jaccard
    return score, matched, missing

try:
    data = load_data("recipes_sample.csv")
except Exception as e:
    st.error(str(e))
    st.stop()

with st.sidebar:
    st.header("Search Settings")
    top_n = st.slider("Number of results", 1, 10, 5)
    min_score = st.slider("Minimum match score", 0.0, 1.0, 0.05, 0.01)
    st.caption("Replace recipes_sample.csv with your Kaggle dataset if desired.")

ingredients_text = st.text_input(
    "🥕 Your ingredients",
    placeholder="Example: chicken, broccoli, garlic"
)

if ingredients_text.strip():
    user_items = normalize(ingredients_text)

    if not user_items:
        st.warning("Please enter valid ingredient names.")
        st.stop()

    results = []
    for _, row in data.iterrows():
        recipe_items = normalize(row["ingredients"])
        score, matched, missing = ingredient_score(user_items, recipe_items)
        if score >= min_score:
            results.append({
                "title": row["title"],
                "ingredients": row["ingredients"],
                "instructions": row["instructions"],
                "score": score,
                "matched": matched,
                "missing": missing
            })

    results.sort(
        key=lambda x: (x["score"], len(x["matched"]), -len(x["missing"])),
        reverse=True
    )
    results = results[:top_n]

    st.subheader(f"Top {len(results)} Recipe Matches")

    if not results:
        st.info("No recipes matched. Try fewer or more general ingredients.")
    else:
        for i, r in enumerate(results, start=1):
            with st.container(border=True):
                st.markdown(f"### {i}. {r['title']}")
                st.progress(min(r["score"], 1.0), text=f"Match score: {r['score']:.1%}")

                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**Ingredients you have**")
                    st.write(", ".join(sorted(r["matched"])) if r["matched"] else "None")
                with c2:
                    st.markdown("**Additional ingredients needed**")
                    st.write(", ".join(sorted(r["missing"])) if r["missing"] else "None")

                with st.expander("View full recipe"):
                    st.markdown("**Ingredients:**")
                    st.write(r["ingredients"])
                    st.markdown("**Instructions:**")
                    st.write(r["instructions"])
else:
    st.info("Enter ingredients above to find and rank recipes.")

st.divider()
st.caption("IR concepts demonstrated: preprocessing, keyword matching, set-based similarity, ranking and retrieval.")

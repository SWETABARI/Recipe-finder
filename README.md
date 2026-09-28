# Smart Ingredient-Based Recipe Finder

A mini Information Retrieval project for finding recipes from the ingredients available to a user.

## IR Concepts
- Text preprocessing and normalization
- Keyword/ingredient matching
- Set representation
- Jaccard similarity
- Ingredient coverage
- Ranking and top-k retrieval

## Project Structure

```
smart_ingredient_recipe_finder/
├── app.py
├── recipes_sample.csv
├── requirements.txt
└── README.md
```

## Run Locally

1. Install Python 3.9+.
2. Open a terminal in this folder.
3. Run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Create a GitHub repository.
2. Upload `app.py`, `recipes_sample.csv`, `requirements.txt`, and `README.md`.
3. Open Streamlit Community Cloud.
4. Select the GitHub repository.
5. Set the main file to `app.py`.
6. Deploy.

No API key is required.

## Using a Kaggle Recipe Dataset

The included CSV is a small sample dataset so the project works immediately.

For a larger Kaggle dataset, replace `recipes_sample.csv` with your dataset and make sure it contains these columns:

- `title`
- `ingredients`
- `instructions`

If the column names differ, rename them in the CSV or modify the corresponding column names in `app.py`.

## Example Query

Input:

`chicken, broccoli, garlic`

The system:
1. Normalizes the input.
2. Converts each recipe's ingredients into a set of terms.
3. Calculates ingredient overlap.
4. Calculates a Jaccard-based similarity/coverage score.
5. Ranks recipes from the strongest match to the weakest.
6. Shows matched and additional ingredients.

## Suggested Report Title

**Smart Ingredient-Based Recipe Finder Using Information Retrieval**

## Possible Future Improvements

- TF-IDF based ranking
- Ingredient synonym handling (e.g., coriander/cilantro)
- Fuzzy matching for spelling mistakes
- Nutrition and dietary filters
- Recipe images
- Larger Kaggle dataset
- Elasticsearch backend
- User feedback-based ranking

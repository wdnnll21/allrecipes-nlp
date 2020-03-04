# allrecipes-nlp
Parses and transforms recipes from AllRecipes.com

How to Use:
- Install all requirements from requirements.txt (or spacy, spacy's en_core_web_sm language model, beautifulsoup4 by hand)
- Run recipe_api.py. The UI will provide instructions

Features:
Recipe Parsing: Ingredients (+ Quantities, Measurements, Descriptors, and Preparations), Steps, Tools, Primary Method.

Recipe Transformations: Take any recipe and convert it To and From Vegetarian, To and From "Healthy", To Indian Cuisine, To Thai Cuisine, Double/Half It, or convert it to an Analogous Cooking Method. You can also ask it to Sandwich a recipe. Beware of the To American Cuisine and Lethal transformations, also included.

from RecipeGrabber import GrabFromRemote
from RecipeX import Recipe
import spacy
from copy import copy

nlp = spacy.load('en_core_web_sm')

rec = GrabFromRemote("https://www.allrecipes.com/recipe/269595")

""" def CompoundSentenceSeperator(recipe):
  steps = []
  for step in recipe.directions:
    sentences = []
    for sentence in step:
      for word in sentence:
        if word.pos_ == "CCONJ":
          for wordb in sentence:
            if wordb.pos_ in ["CCONJ"]:
              break
            if wordb.pos_ == "VERB" """
          

def basicActions(recipe):
  replRecipe = copy(recipe)
  steps = []
  for step in recipe.directions:
    sentences = []
    for sentence in step:
      a = nlp(sentence)
      for word in a:
        if word.dep_ == "ROOT":
          if word.pos_ == "VERB":
            print(word.text)
          else:
            reclaimSentence(sentence)
            break
        elif word.dep_ == "conj" and word.pos_ == "VERB":
          print(word.text)

def reclaimSentence(sentence):
  sentence = "I " + sentence
  a = nlp(sentence)
  for word in a:
    if word.dep_ == "ROOT" and word.pos_ == "VERB":
      print(word.text)

basicActions(rec)

def ingredientSeparation(recipe):
  ingrs = []
  for ingredient in recipe.ingredients:
    doc = nlp(ingredient)
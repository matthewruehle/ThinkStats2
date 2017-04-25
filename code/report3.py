"""
Data Science project by Matt Ruehle, working with a recipes dataset from Kaggle/Yummly
https://www.kaggle.com/c/whats-cooking/data
"""

import pandas as pd
import numpy as np
import string
import sys
import operator
from scipy.stats import gmean
import itertools

import thinkstats2
import thinkplot



def get_frequency_dict(df):
	"""
	Counts the ingredients for the dataframe.
	"""
	counts_dict = {}
	for index, row in df.iterrows():
		for i in row.ingredients:
			if i in counts_dict:
				counts_dict[i] += 1
			else:
				counts_dict[i] = 1
	return counts_dict


def sorted_list_from_dict(d):
	"""
	gets a list of all elements sorted, by reverse.
	"""
	s_l = sorted(d.keys(), key=lambda x: d[x], reverse=True)
	return s_l


def cutoff_at_frequency(d, frequency=100):
	"""
	takes a frequency dict; returns a list of all elements with 
	corresponding value above frequency.
	"""
	return [i for i in d.keys() if d[i] >= frequency]


def frequency_cdf(d):
	"""
	Shows how the vast majority of ingredients are relatively uncommon, but a few are 
	nearly universal.
	Generates a figure.
	"""
	all_counts = [d[i] for i in d.keys()]
	cdf = thinkstats2.Cdf(all_counts, label='recipe counts')
	thinkplot.Cdf(cdf)
	thinkplot.Config(xscale="log", xlabel="Number of recipes with an ingredient", ylabel="CDF")
	thinkplot.Show()


def recipes_with_ingredient_dict(df):
	"""
	Takes a dataframe, and returns a dictionary matching an ingredient 
	to all of the recipes with it.
	"""
	pairings_dict = {}
	for index, row in df.iterrows():
		for i in row.ingredients:
			if i in pairings_dict:
				pairings_dict[i].append([j for j in row.ingredients if j != i])
			else:
				pairings_dict[i] = [[j for j in row.ingredients if j != 1]]
	return pairings_dict


def recipes_for(df, ing_list):
	"""
	Takes as an input a list of ingredients, e.g. from cutoff_at_frequency()
	Returns the recipes associated with at least two of them.
	"""
	relevants = set(ing_list) # set conversion for quicker membership checks
	res = {}
	for index, row in df.iterrows():
		for i in row.ingredients:
			if i not in relevants:
				pass
			elif i in res:
				r = [j for j in row.ingredients if j != i and j in relevants]
				if len(r) > 0:
					res[i].append(r)
			else:
				r = [j for j in row.ingredients if j != i and j in relevants]
				if len(r) > 0:
					res[i] = [r]
	return res



pct_memo = {}
def percent_containing(d, term1, term2):
	"""
	Gets the percentage of recipes containing term1 which also contain term2, 
	out of those in d.
	Should definitely memoize this in the future. Right now, this will frequently get 
	called more than once for the same ingredient pairs, directed.
	"""
	if (term1, term2) in pct_memo:
		return pct_memo[(term1, term2)]
	all_recipes = d[term1]
	contains = 0
	for recipe in all_recipes:
		if term2 in recipe:
			contains += 1
	res = float(contains)/len(all_recipes)
	pct_memo[(term1, term2)] = res
	return res


def all_pairings(d, term1):
	"""
	Gets all of the pairings, sorted by frequency.
	"""
	all_recipes = d[term1]
	counts_dict = {}
	for recipe in all_recipes:
		for ingredient in recipe:
			if ingredient in counts_dict:
				counts_dict[ingredient] += 1
			else:
				counts_dict[ingredient] = 1
	vals = [(i, float(counts_dict[i]) / len(all_recipes)) for i in counts_dict.keys()]
	return sorted(vals, key=lambda x: x[1], reverse=True)


def get_sorted_pairings(d):
	"""
	Takes a recipes dictionary as an input. Suggestion: use the one from 
	common_ingredient_pairings().

	Returns two lists - one, of all of the "directed" pairings, and the other,
	of all of the reciprocal pairings, sorted.

	To clarify: directed means that Potatoes have a high rating for Salt, since
	most Potato recipes have Salt in them.

	Reciprocal means that Potatoes and Salt have a low rating as a pair, since
	although potato has a lot of salt recipes, most salt recipes do *not* have
	potatoes in them.

	Of course, low for both is a particularly low pairing. Using the geometric
	mean right now.
	"""
	directed_pairings = []
	reciprocal_pairings = []
	for ingredient_1 in d.keys():
		for ingredient_2 in d.keys():
			pct = percent_containing(d, ingredient_1, ingredient_2)
			tup = (ingredient_1, ingredient_2, pct)
			directed_pairings.append(tup)
	for i1, i2 in itertools.combinations(d.keys(), 2):
		pct_12 = percent_containing(d, i1, i2)
		pct_21 = percent_containing(d, i2, i1)
		tup = (i1, i2, gmean([pct_12, pct_21]))
		reciprocal_pairings.append(tup)
	directed_sorted = sorted(directed_pairings, key=lambda x: x[2], reverse=True)
	reciprocal_sorted = sorted(reciprocal_pairings, key=lambda x: x[2], reverse=True)
	return directed_sorted, reciprocal_sorted


def most_likely_next_ingredient(d, ing_list):
	"""
	Finds out what ingredient is most likely to get paired with ing_list - so,
	which ingredient in d as the best gmean for their directed pairing frequency.
	Recurring runs of this will take a while, but can "autocomplete" recipes!
	"""
	other_ingredients = [i for i in d.keys() if i not in ing_list]
	best_so_far = None
	best_gmean = 0
	for ingredient in other_ingredients:
		all_pcts = [percent_containing(d, i, ingredient) for i in ing_list]
		this_gmean = gmean(all_pcts)
		if this_gmean > best_gmean:
			best_gmean = this_gmean
			best_so_far = ingredient
	return (best_so_far, best_gmean)


def identify_n_sets(d, n=3):
	"""
	Identifies the most common sets of n ingredients, based on the gmean
	of their reciprocal pairings.
	With n = 2, this is essentially get_sorted_pairings().
	With n=3, this identifies "trinities".
	Of course, this takes progressively longer to run the greater the n - there wind up being
	more and more combinations. Especially at low numbers, this essentially grows in exponential
	time.
	"""

	groupings_dict = {}

	def add_to_groupings(ingredients_list, recipes_dict):
		l = len(ingredients_list) # should be n.
		if ingredients_list in groupings_dict: # no need to duplicate this work.
			# although, itertools.combinations should take care of this.
			return
		else:
			vals = []
			for i in ingredients_list:
				for j in ingredients_list:
					if j != i:
						vals.append(percent_containing(recipes_dict, i, j))
			groupings_dict[ingredients_list] = gmean(vals)
			return

	for n_set in itertools.combinations(d.keys(), n):
		add_to_groupings(n_set, d)

	all_n_sets = sorted([(i, groupings_dict[i]) for i in groupings_dict.keys()], key=lambda x: x[1], reverse=True)
	return all_n_sets


if __name__ == "__main__":
	df = pd.read_json("train.json")
	freq_d = get_frequency_dict(df)
	common_ingredients = cutoff_at_frequency(freq_d, frequency=125)
	recs = recipes_for(df, common_ingredients)

	# Generate a plot of frequencies:
	# frequency_cdf(freq_d)

	# Print out the most common pairings for a given food - here, celery
	# celery_pairings = all_pairings(recs, "celery")
	# print celery_pairings[:10]

	# Print out the most common reciprocal pairings of all.
	# _, reciprocals = get_sorted_pairings(recs)
	# print reciprocals[:10]

	# "Fill in" the next ingredients for a recipe:
	# these_ingredients = ["onions","salt","celery"]
	# for i in range(10): # autocomplete the next three ingredients.
	# 	next_ing = most_likely_next_ingredient(recs, these_ingredients)
	# 	print next_ing[0]
	# 	these_ingredients.append(next_ing[0])	


	# # Identify "trinities." Note - running this will take a considerable while.
	# trinities = identify_n_sets(recs)
	# print trinities[:50]
	# 
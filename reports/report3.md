## Food Trinities and Recipe Completion

Matt Ruehle
Data Science, Spring 2017

![hook image](images/dsr_head)
*Figure 1 - an example of a classified "trinity."*

#### Overview

Cooking is, at its core, the art of combining a (relatively) small number of ingredients in nearly-innumerable different ways. However, some ingredient combinations are more common than others. Different types of cuisine, and different regional palates, promote certain pairings while avoiding others. For example, consider the French [mirepoix](https://en.wikipedia.org/wiki/Mirepoix_(cuisine)) - the quintessential combination of onion, carrot, celery, and an oil which form the basis for numerous dishes from western Europe. 


This specific combination - just one of the thousands of ways to group vegetables French cuisine - is an example of a "trinity" - a combination of three aromatics which give a character to an entire cuisine. Other such examples include the Cajun ["Holy Trinity"](http://www.cookinglouisiana.com/Cooking/The_Trinity.htm) and the Spanish [sofrito](https://en.wikipedia.org/wiki/Sofrito). 

However, identifying these groupings is typically a subjective task - that is to say, what flavor profiles are and aren't tied varies between regions, cuisines, and even individual chefs. We aim to identify ingredient groupings without a "gut check" towards domain knowledge. To this end, we use a [database of recipes provided by Yumly and Kaggle](https://www.kaggle.com/c/whats-cooking/data), although the tools which we use could be adapted to different cuisines or recipe sources.


#### Trinity identification

After trying several different algorithms for the grouping of foods, we find that the optimal method of grouping foods, or of finding pairs (e.g. salt and pepper) which are frequently used together, is to examine ingredient combinations, looking for which ones are most likely to be contained with each other; more specifically, our analysis finds the proportion of recipes containing A which also contain B, and looks for "reciprocal" combinations - ones in which both A is likely to include B, and B is likely to include A. This reciprocity helps avoid alimentary "false positives", although it also disadvantages ingredients which appear in multiple regions' cuisines.

Sample results for searching for trinities, among the 554 most common ingredients in the dataset, yields responses which seem, at least subjectively, reasonable. The output from displaying the fifty most internally-correlated trios, out of the ~28 million such groupings which exist, can be found [here](trinities_results.md); the top fifty includes almost entirely combinations which feature prominently in a type of cooking. For example, the combination of "buttermilk, baking powder, and baking soda" is - while perhaps not a *palate* in the traditional sense - nonetheless recognizeable to western bakers; "garlic, sesame oil, and soy sauce" is found in both Chinese and Japanese cuisine as a sauce or marinade. 



Ingredient        | Ingredient           | Ingredient 
 --- 			  | --- 				 | ---
buttermilk 			| baking powder 		| baking soda
sesame oil 			| rice vinegar 		| soy sauce
garam masala 		| ground turmeric 	| coriander powder
green onions 		| sesame oil 			| soy sauce
red chili powder 	| garlic paste 		| coriander powder
onions 				| salt 				| ground black pepper
sake 				| mirin 				| dashi
garlic 				| salt 				| ground black pepper
dry yeast 			| bread flour 		| warm water
onions 				| salt 				| tomatoes
garlic paste 		| ground turmeric 	| coriander powder
garlic 				| sesame oil 			| soy sauce
onions 				| garlic 				| pepper
clove 				| cardamom pods 		| cinnamon sticks
sake 				| mirin 				| soy sauce

Table 1: a partial set of the top 50 pairings



As for less intuitive results - or, at least, ones less intuitive based on our personal familiarity with foods - we have the trio of "garam masala, cumin seed, and ground turmeric" - which, as it turns out, are some of the [prototypical spices in many Indian curries](https://en.wikipedia.org/wiki/Curry). Furthermore, although "clove, cardamom pods, cinnamon sticks" is not - at least, to our understanding of domain knowledge - considered an aromatic "trinity," its appearance in many recipes and high reciprocal correlations suggests that it may merit such a status, perhaps even above the aforementioned mirepoix.

On a procedural note - the association between "dry yeast, bread flour, and warm water" likely reflects a bias in the source data - with delineations between varieties of yeast, and between "bread" and "all-purpose" flour - but nonetheless also comprises the basic recipe (*sans salt*) for bread.


#### Recipe completion

A small variation on the techniques used to identify mutual groupings has another potential application - one of predictive recipe generation, analogous to a food version of cell phone "autocomplete."

Rather than searching for reciprocal connections, an ingredient - or list of ingredients - can instead be used to find ingredients which are likely to be "next" in the recipe. Repeated application of this technique, adding the previous result to the recipe list, can in turn function similarly to a Markov generator, save for being more internally checked, and order-agnostic.

As an example, feeding in the ingredients "onions, salt, celery" as the beginning of a recipe in turn suggests the following ingredients, in order: *garlic, water, pepper, ground black pepper, garlic cloves, carrots, butter, sugar, all-purpose flour, vegetable oil*.

Once duplicates - an artifact of the source dataset - are disregarded, we add garlic - and, only then, do we complete the mirepoix with carrots and butter; from there, we expand with sugar, oil, and flour into a [*roux*](https://en.wikipedia.org/wiki/Roux). This suggests that, perhaps, garlic "belongs" with onions and celery more than carrots do - although, this could also reflect the fact that many combinations are regional, and this analysis does not subdivide the dataset based on the source culture.

As an addendum - we further considered inverse-frequency approaches to this complmmetion, akin to that used in the generation of trinities; however, this leads to a reduction in the usefulness of the overall predictions - in particular, it over-weights ingredients which are unlikely to be in *any* recipe, but are more likely for a given ingredient set than others.



#### Source notebook, script

The full code used for this report can be found here: [notebook](report3.ipynb), [script](report3.py); however, as an addendum, we would like to add that the script version runs better, as the length of some outputs can cause the Jupyter interface to freeze.
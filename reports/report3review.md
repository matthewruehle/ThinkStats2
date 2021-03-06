Review of "Should you Follow the Food Groups for Dietary Advice?" (Kaitlyn Keil and Kevin Zhang)

This report looks to be motivated mainly by looking for statistical evidence towards (or against) the "Food Groups" advocated by the USDA, food pyramid, departments of education, &c.

In pursuing this, they use the UK Nutrient Databank, created by a UK government department; this database provides the macronutrient and micronutrient breakdowns of common foods. 

The analysis emphasizes nutrient similarity - arguing that foods in a given group will "belong" if they share a similar nutritional role to other elements in the group; they use K-Means Clustering to do so, searching for six natural "clusters" in the overall database and seeing if they map effectively with the published guidelines.

Although some amount of the classification is naturally subjective (e.g., whether to include pulses with meats; where to delineate between fruits and vegetables), I find the overall argument compelling - with some caveats. I especially appreciate the Meats analysis, and buy into your contention that protein content gives the group a strong identifying factor. 

I'm somewhat more hesitant about the ill-fitting Fruits cluster, though - principally due to existing domain knowledge that fruits are remarkably similar, in terms of macronutrient breakdowns, to snack foods like packaged cookies or candies (varying chiefly in sub-divisions of simple v. complex carbohydrates and micronutrients, neither of which look to be accounted for in the model - for example, a macronutrient breakdown of a pear shows 100 calories having 24 g. carbohydrates and ~2g protein, virtually the same ratio as that in Haribo gummi bears). That said, adding in micronutrients, especially with a dataset of ~3000 entries, would certainly risk over-fitting, and the decision to emphasize the macronutrient content is a justifiable one.

I like seeing a confusion matrix, and find it quite telling that there seems to be an accurate predictor for meats and vegetables; it might also bear mentioning that fruits are most commonly confused with vegetables. I'm also somewhat surprised by how frequently dairy is confused with a vegetable - a surprise chiefly because most dairy products are thought of as providing a source of oil and protein. This might be an interesting avenue to explore, if y'all have the time and inclination.

Overall, I found the report quite readable, and also managed to follow along with the methods. There were a few points when the report went a bit more "basic" than I would like (e.g., "Correct predictions lie on the main diagonal, and any other square is an incorrect prediction. Thus, a perfect prediction from our K-Means algorithm would be seen if the main diagonal of the matrix was black squares," - arguably not a necessary clarification), but erring on the side of assuming less prior knowledge is quite defensible.

As an aside - and I'm not quite certain whether this would mesh with your vision of your project and report - there's a short but interesting reading in [this paper](https://www.ncbi.nlm.nih.gov/pubmed/8375951) and [this Time article](http://time.com/4130043/lobbying-politics-dietary-guidelines/). This might be some relevant policy context for the data you're working with!


Edit - one last note, it looks like your figures are all in italics - except for figure 3, which is instead bolded. This is probably just a formatting typo, but might be worth fixing!
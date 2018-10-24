# This script will parse a recipe from allRecipies.com, 
# and output it in dokuwiki format to stdout.

## Reqirements: Beautiful soup, requests
# pip3 install beautifulsoup4
# pip3 install requests

## Usage:
# python3 parseBudgetBytes.py [url of recipe]
# python3 parseBudgetBytes.py https://www.allrecipes.com/recipe/233613/best-damn-chili/?internalSource=streams&referringId=14729&referringContentType=Recipe%20Hub&clickId=st_recipes_mades

import re
import sys
import requests
from bs4 import BeautifulSoup

## Print the title of the recipe
def printTitle(soup, url):
	## Grabbing the recipe name
	recipeName = soup.find("h1", id='recipe-main-content')

	# Making sure we found the recipe name
	if not recipeName:
		print("Error: Didn't find the recipe title.")
		sys.exit(2)

	# Bulding the link in the wiki
	wikiLink = recipeName.getText().replace(" ", "").lower()


	## Grabbing the serving size, cook time, and prep time
	statsContainer = soup.findAll("li", "prepTime__item")
	if not statsContainer:
		print("Error: Wasn't able to find the prep time, cook time, or service size.")
		sys.exit(2)
	if len(statsContainer) is not 4:
		print("Error: Prep time, cook time, or service size is missing.")
		sys.exit(2)

	# Time spent preparing
	prepTimeContainer = statsContainer[1]
	prepTime = prepTimeContainer.text.replace("\n", "").replace("Prep", "")


	# Time spent cooking
	cookTimeContainer = statsContainer[2]
	cookTime = cookTimeContainer.text.replace("\n", "").replace("Cook", "")


	# Number of servings is dynamically calculated client side
	# based on what proportion of ingredients are added.
	# No valid information here (maybe)

	# No difficulty listed on this site.
	difficulty = ""


	# Getting the rating, as provided by the users
	ratingContainer = soup.find("div", "rating-stars")
	if not ratingContainer:
		print("Error: Wasn't able to find the rating on the site.")
		sys.exit(2)
	else:
		# Stripping info from the container.
		rating = ratingContainer.find("img").get("alt")


	## Printing wiki page name
	print("")
	print("====={0}=====".format(recipeName.getText()))

	## Printing table entry for this recipe
	print("^Name^Meat^Serves^Difficulty^Prep time^Cook time^Tried it?^Rating^Source rating^Calories^Protein^Source^")

	# URL
	print("|[[.:{0}|{1}]]|".format(wikiLink, recipeName.getText()), end='')

	# Meat type, serving size, prep time, cook time
	print("||{}|{}|{}|".format(difficulty, prepTime, cookTime), end='')

	# Tried myself, rating, source rating, calories, protein
	print("No|{}||||".format(rating), end='')

	# Source
	print("[[{0}|Budget Bytes]]|".format(url))



## Print the ingredients section
def printIngredients(soup):
	print("")
	print("====Ingredients====")

	# Grabbing all ingredients and their proportions
	ingredientsList = soup.findAll("span", "recipe-ingred_txt")
	if not ingredientsList:
		print("Error: Didn't find any ingredients.")
		sys.exit(2)

	# Printing ingredients/proportions
	# Culling the last 3 elements of the list (garbage data)
	for i in ingredientsList[:-3]:
		print("  * {0}".format(i.text))

def printInstructions(soup):
	instructionsList = soup.find_all("span", "recipe-directions__list--item")
	if(len(instructionsList)  < 1):
		print("Error: Wasn't able to find instructions")
		sys.exit(2)

	# Printing to dokuwiki format
	print("")
	print("====Instructions====")
	for i in instructionsList[:-1]:
		print("  - {}".format(i.text))



##################################################
#
## Entry Point
#
##################################################
# Getting command line args
if(len(sys.argv) != 2):
	exampleURL = "https://www.allrecipes.com/recipe/233613/best-damn-chili/?internalSource=streams&referringId=14729&referringContentType=Recipe%20Hub&clickId=st_recipes_mades"
	print("Usage: python3 {0} [url of a recipe from allrecipies.com]".format(sys.argv[0]))
	print("Example: python3 {0} {1}".format(sys.argv[0], exampleURL))
	sys.exit(0)

# Getting the website
#print("Making HTTP request...")
page = requests.get(sys.argv[1])
if(page.status_code != 200):
	print("Error: Couldn't resolve the HTTP request (Status code: {0})".format(page.status_code));
	sys.exit(1)
#print("Done. Building wiki entry...")
#print()

# Building a nice ol' bowl of soup
soup = BeautifulSoup(page.content, 'html.parser');

# Printing the title, and the info of the recipe
# This info includes...
#	- Recipe name
#	- Serving size
#	- Prep time
#	- Cook time
#	- Source link
printTitle(soup, sys.argv[1])
printIngredients(soup)
printInstructions(soup)

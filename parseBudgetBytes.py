# This script will parse a recipe from budgetBytes.com, 
# and output it in dokuwiki format to stdout.

## Reqirements: Beautiful soup, requests
# pip3 install beautifulsoup4
# pip3 install requests

## Usage:
# python3 parseBudgetBytes.py [url of recipe]
# python3 parseBudgetBytes.py https://www.budgetbytes.com/pork-peanut-dragon-noodles/

import re
import sys
import requests
from bs4 import BeautifulSoup

## Print the title of the recipe
def printTitle(soup, url):
	## Grabbing the recipe name
	recipeName = soup.find("h2", 'wprm-recipe-name')

	# Making sure we found the recipe name
	if not recipeName:
		print("Error: Didn't find the recipe title.")
		sys.exit(2)

	# Bulding the link in the wiki
	wikiLink = recipeName.getText().replace(" ", "").lower()


	## Grabbing the serving size, cook time, and prep time
	# Time spent preparing
	prepTimeContainer = soup.find("div", "wprm-recipe-prep-time-container")
	if not prepTimeContainer:
		print("Error: Wasn't able to find the prep time.")
		sys.exit(2)
	else:
		# Stripping info from the container.
		# We're parsing the container rather than the spans in the div 
		#	because the time elapsed and the unit of time are in different spans.
		prepTime = prepTimeContainer.getText()
		prepTime = prepTime.replace("\n Prep Time ", "")


	# Time spent cooking
	cookTimeContainer = soup.find("div", "wprm-recipe-cook-time-container")
	if not cookTimeContainer:
		print("Error: Wasn't able to find the cook time.")
		sys.exit(2)
	else:
		# Stripping info from the container.
		# We're parsing the container rather than the spans in the div 
		#	because the time elapsed and the unit of time are in different spans.
		cookTime = cookTimeContainer.getText()
		cookTime = cookTime.replace("\n Cook Time ", "")


	# Number of servings
	numServingsContainer = soup.find("span", "wprm-recipe-servings")
	if not numServingsContainer:
		print("Error: Wasn't able to find the number of servings.")
		sys.exit(2)
	else:
		# Stripping info from the container.
		servingSize = numServingsContainer.getText()

	# No difficulty listed on this site.
	difficulty = ""


	## Printing wiki page name
	print("")
	print("====={0}=====".format(recipeName.getText()))

	## Printing table entry for this recipe
	print("^Name^Meat^Serves^Difficulty^Prep time^Cook time^Tried it?^Rating^Source rating^Calories^Protein^Source^")

	# URL
	print("|[[.:{0}|{1}]]|".format(wikiLink, recipeName.getText()), end='')

	# Meat type, serving size, prep time, cook time
	print("|{0}|{1}|{2}|{3}|".format(servingSize, difficulty, prepTime, cookTime), end='')

	# Tried myself, rating, source rating, calories, protein
	print("No|||||", end='')

	# Source
	print("[[{0}|Budget Bytes]]|".format(url))



## Print the ingredients section
def printIngredients(soup):
	print("")
	print("====Ingredients====")

	# Grabbing ingredients and their proportions
	ingredientsList = soup.find_all("li", "wprm-recipe-ingredient")
	if not ingredientsList:
		print("Error: Didn't find any ingredients.")
		sys.exit(2)

	# Printing ingredients/proportions
	for i in ingredientsList:
		# Getting the amount
		# Not every ingredient has an amount (eg: pepper to taste). 
		# Don't throw a fit if it's not there
		tmp = i.find("span", "wprm-recipe-ingredient-amount")
		if tmp:
			amount = tmp.getText()

		# Getting the unit of measurement
		# Not every ingredient has a unit of measurement (eg: 1 apple). 
		# Don't throw a fit if it's not there
		tmp = i.find("span", "wprm-recipe-ingredient-unit")
		if tmp:
			unit = tmp.getText()

		# Getting the name of the item
		tmp = i.find("span", "wprm-recipe-ingredient-name")
		if not tmp:
			print("Error: Didn't find the name for one of the ingredients.")
			sys.exit(2)
		else:
			name = tmp.getText()


		## Printing the ingredient 
		# Sometimes there is no unit of measurement (Eg: 3 apples, 1 green pepper)
		# There is also sometimes no amount (Eg: Pepper to taste)
		# Make sure we don't heck up
		if not unit and not amount:
			print("  * {0}".format(name))
		if not unit:
			print("  * {0} {1}".format(amount, name))
		else:
			print("  * {0} {1} {2}".format(amount, unit, name))

def printInstructions(soup):
	instructionsList = soup.find_all("div", "wprm-recipe-instruction-text")
	if(len(instructionsList)  < 1):
		print("Error: Wasn't able to find instructions")
		sys.exit(2)

	# Printing to dokuwiki format
	print("")
	print("====Instructions====")
	for i in instructionsList:
		print("  - {}".format(i.getText()))



##################################################
#
## Entry Point
#
##################################################
# Getting command line args
if(len(sys.argv) != 2):
	print("Usage: python3 {0} [url of a recipe from budgetbytes.com]".format(sys.argv[0]))
	print("Example: python3 {0} https://www.budgetbytes.com/pork-peanut-dragon-noodles/".format(sys.argv[0]))
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

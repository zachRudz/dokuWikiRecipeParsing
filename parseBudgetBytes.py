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
		print("Error: Didn't find the recipe title. Found:")
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

	# The webpage has 2 sections of ingredients
	# Grab the first one
	panel = soup.find_all("div", "panel-body")
	if(len(panel) < 1):
		print("Error: Wasn't able to find ingredients section")
		sys.exit(2)

	ingredientSection = panel[0].find_all("ul", "list-ingredients")[0]

	# Grabbing ingredients and their proportions
	proportions = ingredientSection.find_all("span", itemprop="amount")
	item = ingredientSection.find_all("span", itemprop="name")

	# Printing ingredients/proportions
	i = 0
	for p in proportions:
		# Some recipies don't have proportions for their ingredients.
		# Eg: "Sliced tomato", "Salt and pepper to taste"
		# This check is to help our formatting so that we don't get a leading space
		#	in our ingredients list when this happens
		if(p.getText().strip() == ""):
			print("  * {0}".format(item[i].getText().strip()))
		else:
			print("  * {0} {1}".format(p.getText().strip(), item[i].getText().strip()))

		i = i + 1


def printInstructions(soup):
	# The webpage has 4 sections of instructions: [Header / Instruction body] * 2
	# Grab the first instruction body 
	instructionSections = soup.find_all("div", id=re.compile("recipe-instructions*"))
	if(len(instructionSections)  < 2):
		print("Error: Wasn't able to find instructions section")
		sys.exit(2)

	# Isolating panel of instructions
	instructionPanel = instructionSections[1].find_all("div", "panel-body")
	if(len(instructionPanel) < 1):
		print("Error: Wasn't able to find instructions section")
		sys.exit(2)

	# Formatting
	instructions = instructionPanel[0].getText()
	instructions = instructions.replace("\n", "")
	instructions = instructions.replace("\t", "")

	# Printing to dokuwiki format
	print("")
	print("====Instructions====")
	print(instructions)



##################################################
#
## Entry Point
#
##################################################
# Getting command line args
if(len(sys.argv) != 2):
	print("Usage: python3 {0} [url of a recipe from thePioneerWoman.com]".format(sys.argv[0]))
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
#printIngredients(soup)
#printInstructions(soup)


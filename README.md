# Dokuwiki Recipe Parsing

A set of scripts that can be used to parse and format various online recipes into a neat dokuwiki format for archival.

Currently, recipies can be parsed from...
* http://thepioneerwoman.com
* https://www.budgetbytes.com/

## Getting Started

Fetch the git repo
```
$ git clone git@github.com:zachRudz/dokuWikiRecipeParsing.git
```

### Prerequisites

This project requires python3, beautifulsoup4, and requests.

### Installing

Install pip3. It should be already installed, but if not:

```
$ sudo apt install python3-pip
```

Install beautifulsoup, and requests via pip:
```
$ pip3 install beautifulsoup4
$ pip3 install requests

```

Example usage:
```
$ python3 parseBudgetBytes.py https://www.budgetbytes.com/slow-cooker-chicken-dumplings/

=====Slow Cooker Chicken & Dumplings=====
^Name^Meat^Serves^Difficulty^Prep time^Cook time^Tried it?^Rating^Source rating^Calories^Protein^Source^
|[[.:slowcookerchicken&dumplings|Slow Cooker Chicken & Dumplings]]||6||30 minutes |4 hours 20 minutes |No|||||[[https://www.budgetbytes.com/slow-cooker-chicken-dumplings/|Budget Bytes]]|

====Ingredients====
  * 2 cloves garlic
  * 1 cloves medium yellow onion
  * 3 ribs celery
  * 1/2 lb 3-4 carrots
  * 1 lb large (3/4 lb) chicken breast*
  * 1 lb whole bay leaf
  * 1 tsp dried basil
  * 1 tsp dried thyme
  * 1 tsp freshly cracked pepper
  * 4 cups water
  * 1 tsp salt plus more to taste
  * 1 1/2 cups all-purpose flour
  * 1 1/2 tsp baking powder
  * 1/2 tsp salt
  * 1/2 Tbsp dried parsley
  * 6 Tbsp cold butter
  * 3/4 tsp sugar
  * 2/3 cup milk

====Instructions====
  - Mince the garlic, dice the onion, and slice the carrots and celery into small pieces. Add the garlic, onion, carrot, celery, bay leaf, basil, thyme, chicken breast, water, and some freshly cracked pepper to a slow cooker. Stir to combine and then cook on high for four hours or low for eight hours.
  - After cooking for four hours on high or eight hours on low, remove the chicken from the broth and place it on a cutting board (if you cooked on low heat, turn it to high now). Use two forks to shred the chicken. Return the chicken to the pot and stir in 1 tsp of salt to the soup. Keep the slow cooker covered as much as possible during this process to retain heat and maintain the temperature.
  - Allow the soup to continue to cook on high while you mix the dumpling batter. In a medium bowl combine the flour, baking powder, salt, parsley, and sugar. Mix well. Add butter in small chunks and cut it in or work it in with your hands until the mixture resembles damp sand. Add the milk and stir until a very soft paste-like mixture forms.
  - Remove the lid from the slow cooker and drop the dumpling batter into the soup by the heaping spoonful. Return the lid to the slow cooker and allow the dumplings to steam for 20 minutes. After 20 minutes they should have fluffed and expanded from the heat. Although they may look moist on the outside, they will be light and fluffy on the inside. Serve hot.
```

From this point, the parsed recipe can be copy/pasted into a new page on your wiki:

![Screenshot](https://i.imgur.com/2y6A0BU.png)

## Built With

* [Requests](http://docs.python-requests.org/en/master/) - For fetching webpages
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - For parsing webpages
* [Dokuwiki](https://www.dokuwiki.org/dokuwiki) - For hosting the parsed recipies

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Big thanks to all of the chefs hosting their recipies
* Thanks to PurpleBooth for the github [README template](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)

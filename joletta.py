from bs4 import BeautifulSoup
import urllib
import nltk

temp = urllib.urlopen("http://allrecipes.com/recipe/26317/chicken-pot-pie-ix/").read()
soup = BeautifulSoup(temp, 'html.parser')

# Recipe Name
# title = soup.find('h1', class_='recipe-summary__h1')
# print title.text.strip()


ingredients = soup.find_all('span', class_='recipe-ingred_txt added')
for ingredient in ingredients:
    ingredient_name = ingredient.text.strip()

    tokens = nltk.word_tokenize(ingredient_name)
    tags = nltk.pos_tag(tokens)

    filtered_tags = list()
    for tag in tags:
        if 'NN' in tag[1]:
            filtered_tags.append(tag[0])

    prefixes = ['cup', 'teaspoon', 'pound', 'inch', 'tablespoon']

    ingredient_name = ' '.join(filtered_tags)

    for p in prefixes:
        if p + 's' in ingredient_name:
            ingredient_name = ingredient_name.replace(p+'s', '')
        elif p in ingredient_name:
            ingredient_name = ingredient_name.replace(p, '')

    print ingredient_name.strip()

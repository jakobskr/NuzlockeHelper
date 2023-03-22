import time
import os
from urllib import response
import re
from bs4 import BeautifulSoup
import requests

# import HTMLSession from requests_html
from requests_html import HTMLSession


SITE = "https://pokemondb.net/pokedex/national"
VERBOSE = False



def gen1():
	NotImplementedError


def gen2():
	NotImplementedError


def gen3():
	NotImplementedError


def gen4():
	lastMon = 493
	baseSpritePath = "https://img.pokemondb.net/sprites/diamond-pearl/normal/"
	
	if not os.path.exists("assets/gen4"):
		os.mkdir("assets/gen4")

	dirpath = "assets/gen4"

	res = []
	pokemons = {}
	session = HTMLSession()
	resp = session.get(SITE)
	resp.html.render()

	#res = resp.html.document.getElementsByClassName("infoCard")
	soup = BeautifulSoup(resp.html.html, "lxml")

	res = soup.find_all("div", class_="infocard")
	#print(soup)
	#print(res[0].prettify())


	for r in res:
		#print(type(r))
		#print(r.find_all("small", class_="")[0].string)
		id = int(r.find_all("small", class_="")[0].string[1:])
		name = r.find("a", class_="ent-name").string
		pokemons[id] = name
		#print(id, name)

	nationalDex = dict( filter( lambda x : x[0] <= lastMon, pokemons.items()))
	for name in nationalDex.values():

		parsedName = name.lower()

		# handle mime jr.
		if parsedName == "mime jr.":
			parsedName = "mime-jr"
		# if the name contains an apostrophe (such as in
		# Farfetch'd, just simply remove it)
		parsedName = parsedName.replace("'", "")
		# if the name contains a period followed by a space
		# (as is the case with Mr. Mime), then replace it
		# with a dash
		parsedName = parsedName.replace(". ", "-")
		# handle the case for Nidoran (female)
		if name.find(u'\u2640') != -1:
			parsedName = "nidoran-f"
		# and handle the case for Nidoran (male)
		elif name.find(u'\u2642') != -1:
			parsedName = "nidoran-m"


		url = baseSpritePath + parsedName.lower() + ".png"
		r = requests.get(url)

		if r.status_code != 200:
			print("error for downloading %s" % (parsedName)) 
			continue
	
		f = open("%s/%s.png" % (dirpath, parsedName.lower() ), "wb")
		f.write(r.content)
		r.close()
		
	print("finished downloading sprites for gen4")

if __name__ == "__main__":

	# TODO: add usage commands.

	if os.path.exists("assets"):
		print("assets exists")
	else:
		os.mkdir("assets")
		
	gen4()

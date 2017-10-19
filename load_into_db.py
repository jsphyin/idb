import glob
from lxml import etree

def load_items(file_list):
	item_nodes = []
	for fname in file_list:
		with open(fname) as f:
			root = etree.parse(f).getroot()
			item_nodes.extend(root.xpath("item"))

	return item_nodes

item_nodes = load_items(glob.glob("scrapefiles/*.xml")[:10])
for item in item_nodes:
	item_id = item.xpath("@id")
	item_type = item.xpath("@type")
	# assert item_type in ("boardgame", "boardgameexpansion")

	primary_name = item.xpath("name[@type='primary']/@value")
	alt_names = item.xpath("name[@type='alternate']/@value")
	
	image = item.xpath("image/text()")

	description = item.xpath("description/text()")

	family = item.xpath("link[@type='boardgamefamily']/@value")

	genre = item.xpath("link[@type='boardgamecategory']/@value")

	year = item.xpath("yearpublished/@value")

	publishers = item.xpath("link[@type='boardgamepublisher']/@value")

	artists = item.xpath("link[@type='boardgameartist']/@value")

	developers = item.xpath("link[@type='boardgamedesigner']/@value")

	mechanics = item.xpath("link[@type='boardgamemechanic']/@value")

	min_players = item.xpath("minplayers/@value")
	max_players = item.xpath("maxplayers/@value")

	rating = item.xpath("statistics/ratings/average/@value")

	print(item_id, item_type, primary_name, alt_names, image, description, family, genre, year, publishers, artists, developers, mechanics, rating, end="\n\n")
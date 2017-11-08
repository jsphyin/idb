from datetime import datetime
import glob
import itertools
import json
from lxml import etree
import re

import models

HTML_TAG_REGEX = re.compile('<[^>]*>')
def strip_html(s):
    return HTML_TAG_REGEX.sub('', s)

def load_items(file_list):
    xml_root = etree.Element('items')
    for fname in file_list:
        with open(fname) as f:
            file_root = etree.parse(f).getroot()
            xml_root.extend(file_root.xpath('item'))

    return xml_root

def load_json(json_fname):
    with open(json_fname) as f:
        data = json.load(f)
        return data

def xml_link_type_to_json(xml_root, link_type):
    link_type_json = {}
    for elem in xml_root.xpath('//link[@type="{}"]'.format(link_type)):
        link_type_json[elem.get('id')] = {
            'name': elem.get('value')
        }

    return link_type_json

def augment_raw_desc(json_objects):
    for info in json_objects.values():
        if 'desc' in info:
            info['raw_desc'] = strip_html(info['desc']) if info['desc'] else None

    return json_objects

def json_to_db_objects(json_objects, db_type):
    for object_id, info in json_objects.items():
        db_object = db_type()

        db_object.id = int(object_id)
        for attr, value in info.items():
            setattr(db_object, attr, value)

        yield db_object

def add_and_commit(db_objects):
    for db_object in db_objects:
        models.db.session.add(db_object)

    models.db.session.commit()

def get_all_ids(db_type):
    return set(next(zip(*models.db.session.query(db_type.id).all())))

def populate_games(xml_root):
    game_family_pairs = set()
    game_genre_pairs = set()
    game_publisher_pairs = set()
    game_artist_pairs = set()
    game_developer_pairs = set()
    game_mechanic_pairs = set()

    json_games = {}

    valid_family_ids = get_all_ids(models.Family)
    valid_genre_ids = get_all_ids(models.Genre)
    valid_publisher_ids = get_all_ids(models.Publisher)
    valid_artist_ids = get_all_ids(models.Artist)
    valid_developer_ids = get_all_ids(models.Developer)
    valid_mechanic_ids = get_all_ids(models.Mechanic)

    for item in xml_root.xpath('item'):
        game_id = item.xpath('@id')
        game_type = item.xpath('@type')
        primary_name = item.xpath('name[@type="primary"]/@value')
        alt_names = item.xpath('name[@type="alternate"]/@value')
        image = item.xpath('image/text()')
        description = item.xpath('description/text()')
        year = item.xpath('yearpublished/@value')
        min_players = item.xpath('minplayers/@value')
        max_players = item.xpath('maxplayers/@value')
        rating = item.xpath('statistics/ratings/average/@value')

        families = item.xpath('link[@type="boardgamefamily"]/@id')
        genres = item.xpath('link[@type="boardgamecategory"]/@id')
        publishers = item.xpath('link[@type="boardgamepublisher"]/@id')
        artists = item.xpath('link[@type="boardgameartist"]/@id')
        developers = item.xpath('link[@type="boardgamedesigner"]/@id')
        mechanics = item.xpath('link[@type="boardgamemechanic"]/@id')

        game_id = int(game_id[0])
        json_games[game_id] = {
            'is_expansion': game_type[0] == 'boardgameexpansion',
            'primary_name': primary_name[0],
            'alt_names': ','.join(alt_names) if alt_names else None,
            'image': image[0] if image else None,
            'desc': description[0] if description else None,
            'year': int(year[0]) if year and year[0] else None,
            'min_players': int(min_players[0]) if min_players and min_players[0] else None,
            'max_players': int(max_players[0]) if max_players and max_players[0] else None,
            'rating': float(rating[0]) if rating and rating[0] else None,
        }

        game_family_pairs.update(itertools.product((game_id,), set(map(int, families)) & valid_family_ids))
        game_genre_pairs.update(itertools.product((game_id,), set(map(int, genres)) & valid_genre_ids))
        game_publisher_pairs.update(itertools.product((game_id,), set(map(int, publishers)) & valid_publisher_ids))
        game_artist_pairs.update(itertools.product((game_id,), set(map(int, artists)) & valid_artist_ids))
        game_developer_pairs.update(itertools.product((game_id,), set(map(int, developers)) & valid_developer_ids))
        game_mechanic_pairs.update(itertools.product((game_id,), set(map(int, mechanics)) & valid_mechanic_ids))

    add_and_commit(json_to_db_objects(augment_raw_desc(json_games), models.Game))
    print('added games')

    models.db.session.execute(models.game_family_assoc.insert().values(list(game_family_pairs)))
    models.db.session.execute(models.game_genre_assoc.insert().values(list(game_genre_pairs)))
    models.db.session.execute(models.game_publisher_assoc.insert().values(list(game_publisher_pairs)))
    models.db.session.execute(models.game_artist_assoc.insert().values(list(game_artist_pairs)))
    models.db.session.execute(models.game_developer_assoc.insert().values(list(game_developer_pairs)))
    models.db.session.execute(models.game_mechanic_assoc.insert().values(list(game_mechanic_pairs)))

    models.db.session.commit()
    print('added game assocs')

def populate_events(event_list):
    event_game_pairs = set()
    event_genre_pairs = set()

    json_events = {}
    event_id = 1

    valid_game_ids = get_all_ids(models.Game)
    valid_genre_ids = get_all_ids(models.Genre)

    for event in event_list:
        location = event['group']['localized_location']
        if 'venue' in event:
            location = '{}, {}'.format(event['venue']['city'], event['venue']['state'])

        json_events[event_id] = {
            'name': event['name'],
            'desc': event.get('description'),
            'location': location,
            'link': event['link'],
            'time': datetime.fromtimestamp(event['time'] / 1000),
        }

        event_game_pairs.update(itertools.product((event_id,), set(event.get('game_ids', [])) & valid_game_ids))
        event_genre_pairs.update(itertools.product((event_id,), set(event.get('genre_ids', [])) & valid_genre_ids))

        event_id += 1

    add_and_commit(json_to_db_objects(augment_raw_desc(json_events), models.Event))
    print('added events')

    models.db.session.execute(models.event_game_assoc.insert().values(list(event_game_pairs)))
    models.db.session.execute(models.event_genre_assoc.insert().values(list(event_genre_pairs)))

    models.db.session.commit()
    print('added event assocs')

def create_indexes():
    models.db.session.execute('CREATE FULLTEXT INDEX ix_ft_game ON game ({})'.format(models.Game.__ftcolumns__))
    models.db.session.execute('CREATE FULLTEXT INDEX ix_ft_genre ON genre ({})'.format(models.Genre.__ftcolumns__))
    models.db.session.execute('CREATE FULLTEXT INDEX ix_ft_developer ON developer ({})'.format(models.Developer.__ftcolumns__))
    models.db.session.execute('CREATE FULLTEXT INDEX ix_ft_event ON event ({})'.format(models.Event.__ftcolumns__))
    print('created indexes')

def populate_db():
    models.db.drop_all()
    models.db.create_all()

    xml_root = load_items(glob.glob('../idb_scrapefiles/*.xml')[:1000])
    print('loaded xml')

    add_and_commit(json_to_db_objects(augment_raw_desc(load_json('../idb_scrapefiles/categories.json')), models.Genre))
    print('added genres')

    add_and_commit(json_to_db_objects(augment_raw_desc(load_json('../idb_scrapefiles/designers.json')), models.Developer))
    print('added developers')

    add_and_commit(json_to_db_objects(augment_raw_desc(xml_link_type_to_json(xml_root, 'boardgamefamily')), models.Family))
    print('added families')

    add_and_commit(json_to_db_objects(augment_raw_desc(xml_link_type_to_json(xml_root, 'boardgamepublisher')), models.Publisher))
    print('added publishers')

    add_and_commit(json_to_db_objects(augment_raw_desc(xml_link_type_to_json(xml_root, 'boardgameartist')), models.Artist))
    print('added artists')

    add_and_commit(json_to_db_objects(augment_raw_desc(xml_link_type_to_json(xml_root, 'boardgamemechanic')), models.Mechanic))
    print('added mechanics')

    populate_games(xml_root)

    populate_events(
        load_json('../idb_scrapefiles/austin.json') + \
        load_json('../idb_scrapefiles/newyorkcity.json') + \
        load_json('../idb_scrapefiles/sanfrancisco.json')
    )

    create_indexes()

populate_db()

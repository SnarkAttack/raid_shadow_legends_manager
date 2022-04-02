from abc import ABC, abstractmethod
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import re

class RSLParser(ABC):

	def __init__(self, base_url):
		self.base_url = base_url
		self.champions_url = urljoin(self.base_url, 'champions/')

	def normalize_champion_name(self, name):
		return name.replace(' ', '-').lower()

	def generate_champion_url(self, name):
		norm_name = self.normalize_champion_name(name)
		full_champ_url = urljoin(self.champions_url, norm_name+'/')
		return full_champ_url

	def parse_champion(self, name):
		full_champ_url = self.generate_champion_url(name)
		r = requests.get(full_champ_url)
		soup = BeautifulSoup(r.content, 'html.parser')
		rating = self.get_champion_rating(soup)
		location_ratings = self.get_champion_location_ratings(soup)

		return rating, location_ratings

	def get_site_name(self):
		return self.__class__.__name__

	@abstractmethod
	def get_champion_rating(self, soup):
		raise NotImplementedError()

	@abstractmethod
	def get_champion_location_ratings(self, soup):
		raise NotImplementedError()

class RaidCodexParser(RSLParser):

	def __init__(self):
		super().__init__("https://raid-codex.com/")

	def get_stars(self, star_soup):

		return len(star_soup.find_all(class_='fas'))

	def get_champion_rating(self, soup):

		champ_view = soup.find(class_='champion-view')
		champ_rating = champ_view.find(class_='champion-rating')
		rating = self.get_stars(champ_rating)

		return rating

	def get_champion_location_ratings(self, soup):

		champ_rating_table = soup.find(class_='table-champion-ratings').find('tbody')
		rating_trs = champ_rating_table.find_all('tr')

		location_ratings = []

		for rating_tr in rating_trs:
			name_td, rating_td = rating_tr.find_all('td')[:2]
			name = name_td.renderContents().decode()
			rating_spans = rating_td.find_all('span')
			if len(rating_spans) == 1:
				rating_stars_span = rating_spans[0]
				rating = self.get_stars(rating_stars_span)
				location_ratings.append((name, rating))
			else:
				for rating_span in rating_spans:
					sub_name_nav_str = rating_span.previousSibling
					# [:-1] removes colon from the end
					sub_name = str(sub_name_nav_str).strip()[:-1]
					rating = self.get_stars(rating_span)
					location_ratings.append((f"{name} ({sub_name})", rating))

		return location_ratings

class AyumiLoveParser(RSLParser):

	def __init__(self):
		super().__init__("https://ayumilove.net")
		self.champions_url = self.base_url

	def get_stars(self, star_str):
		return star_str.count('★')

	def generate_champion_url(self, name):
		norm_name = self.normalize_champion_name(name)
		full_champ_url = urljoin(self.champions_url, f'raid-shadow-legends-{norm_name}-skill-mastery-equip-guide/')
		return full_champ_url

	def get_champion_rating(self, soup):
		loc_ratings = self.get_champion_location_ratings(soup)
		rating_sum = sum([loc_rating[1] for loc_rating in loc_ratings])
		# Cutoffs found at https://ayumilove.net/raid-shadow-legends-list-of-champions-by-ranking/
		# All .5 values determined by me by just grabbing the halfway points between two tiers, with
		# the exception of 1.5, because the halfway point is still 14 stars which meants there would
		# almost never be a pure 1 star. 22 is the halfway between 29 and 14. 
		if rating_sum >= 63:
			return 5
		elif rating_sum >= 59:
			return 4.5
		elif rating_sum >= 53:
			return 4
		elif rating_sum >= 49:
			return 3.5
		elif rating_sum >= 43:
			return 3
		elif rating_sum >= 36:
			return 2.5
		elif rating_sum >= 29:
			return 2
		elif rating_sum >= 22:
			return 1.5
		else:
			return 1

	def get_champion_location_ratings(self, soup):

		champ_rating_table = soup.find(text=re.compile('Grinding')).parent.parent

		champ_rating_sections = champ_rating_table.find_all('p')

		location_ratings = []

		for champ_ratings in champ_rating_sections[:4]:
			champ_ratings_ind = champ_ratings.renderContents().decode('utf-8').split('<br/>')
			for champ_loc_rating in champ_ratings_ind:
				star_str, loc_name = champ_loc_rating.strip().split(' ', 1)
				location_ratings.append((loc_name, self.get_stars(star_str)))

		return location_ratings


class HellHadesParser(RSLParser):

	def __init__(self):
		super().__init__("https://hellhades.com/")

	def get_champion_rating(self, soup):

		champ_rating_box = soup.find(text=re.compile('Champion Overall Rating:')).parent

		# Manually check for .5, its the only value where hellhades.com does not have an
		# integer in front of the decimal point
		rating = champ_rating_box.find(text=re.compile('^\d((\.\d)?)|\.5'))

		return float(str(rating))

	def get_champion_location_ratings(self, soup):

		location_ratings = []

		location_types = ['Key Areas', 'Dungeons']

		for location_type in location_types:

			location_ratings_box = soup.find(text=re.compile(location_type)).parent.parent

			table_rows = location_ratings_box.find_all('tr')

			for table_row in table_rows:
				area_name_td, area_stars_td = table_row.find_all('td')

				area_name = area_name_td.text[:-1]
				area_stars = float(area_stars_td.text)/2

				location_ratings.append((area_name, area_stars))

		# Have to grab Doom Tower separately because its contents are nested deeper and because
		# 'Doom Tower' appears as its own section on the site
		
		doom_tower_ratings_box = soup.find(text=re.compile('Magma Dragon')).find_parent(class_='fusion-builder-row')

		tables_rows = doom_tower_ratings_box.find_all('tr')

		for table_row in tables_rows:
			area_name_td, area_stars_td = table_row.find_all('td')

			area_name = area_name_td.text[:-1]
			area_stars = float(area_stars_td.text)/2

			location_ratings.append((area_name, area_stars))

		return location_ratings


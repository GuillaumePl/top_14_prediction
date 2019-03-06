from scraping.scraping_parameters import ScrapingParameters

import pandas as pd
from bs4 import BeautifulSoup as b
import requests


class ScrapWeb:
    """
    Class used as base to scrap data from LNR website.
    The constructor takes as an input the path to the configuration file (.yml).
    The default file (usage recommended) is "scrapping_parameters.yml".
    The scraping is performed successively on the pages reachable with the PATHS defined
    in the "saison_wiki" field of the configuration file.

    The 'debug' parameter launches the scraping on the last PATH only

    The scraped data is loaded in the '.results' attribute
    """
    def __init__(self, scraping_parameters_path='scraping/scraping_parameters.yml', debug=False):

        print('Creating a ScrapWeb instance with debug = {}'.format(debug))

        # Initialization of the attributes
        #       Loading the data from the configuration file
        self.scraping_parameters_path = scraping_parameters_path
        self.scraping_parameters = ScrapingParameters(self.scraping_parameters_path)

        #       Creating an empty DataFrame to concatenate the data
        self.results = pd.DataFrame(columns=self.scraping_parameters.saison_cols)

        if debug:
            # We keep only the last PATH of the configuration file (ie the last season)
            self.scraping_parameters.saison_wiki = [self.scraping_parameters.saison_wiki[-1]]

        print('The scraping will be performed over {} seasons'
              .format(len(self.scraping_parameters.saison_wiki)))

        # For each PATH of the configuration file (ie each season)
        for season_url in self.scraping_parameters.saison_wiki:

            # Create an instance of the Season class using the corresponding url
            # For each season, the data are loaded in the .season_results attribute as a DataFrame
            current_season = Season(self.scraping_parameters.fixe + season_url,
                                    self.scraping_parameters_path)

            # Append the data of the current season to main DataFrame
            self.results = self.results.append(current_season.season_results)

            print('Season {} loaded in the DataFrame'.format(current_season.season_id))

        print('Initialisation of the ScrapWeb object completed')
        print('The matchs DataFrame concatenates {} games'.format(self.results.shape[0]))


class Season:
    """

    """
    def __init__(self, url, scraping_parameters_path='scraping/scraping_parameters.yml'):
        self.scraping_parameters_path = scraping_parameters_path
        self.scraping_parameters = ScrapingParameters(self.scraping_parameters_path)
        self.season_results = pd.DataFrame(columns=self.scraping_parameters.saison_cols)
        self.days = {}
        self.season_id = None

        # Access the current season data, using current season url
        season_http_request = requests.get(url)
        season_page = season_http_request.content
        self.season_soup = b(season_page, 'html.parser')

        # Get the urls to the different Days of the current season (stored in a dictionary) \
        # and the identification of the current season.
        self.season_id, self.days = self.get_days_url()

        for day in self.days:

            current_day = Day(self.scraping_parameters.fixe + self.days[day],
                              self.season_id,
                              day,
                              self.scraping_parameters_path,
                              )

            self.season_results = self.season_results.append(current_day.day_results)

    def get_days_url(self):
        season = None
        days = {}

        html_calendar_filters = self.season_soup.select(
            'section.block.block-lnr-custom.block-lnr-custom-calendar-results-filter'
        )[0]
        html_field_content = html_calendar_filters.select(
            'span.field-content'
        )

        for day_filter in html_field_content:
            # Remove general data ('all' days in the season)
            if "all" not in day_filter.a['href']:

                day_url_temp = day_filter.a['href']
                day_temp = day_filter.a['data-title'].split(' - ')[-1].split('è')[0]

                days[day_temp] = day_url_temp

                if season is None:
                    # Populate season information
                    season = day_filter.a['data-title'].split(' - ')[0].split()[-1]

        return season, days


class Day:
    def __init__(self, day_url, season_id,
                 current_day, scraping_parameters_path='scraping/scraping_parameters.yml'):
        self.season_id = season_id
        self.current_day = current_day
        self.scraping_parameters_path = scraping_parameters_path
        self.scraping_parameters = ScrapingParameters(self.scraping_parameters_path)
        self.day_results_list = []

        # Access the current day data, using current day url
        day_http_request = requests.get(day_url)
        day_page = day_http_request.content
        day_soup = b(day_page, 'html.parser')
        day_container = day_soup.select('div.day-results-table')

        for html_match_info in day_container[0].select('tr.info-line.after'):
            current_match = Match(html_match_info, self.season_id, self.current_day)
            self.day_results_list.append(current_match.match_results)

        # for match_info in day_container[0].select('tr.info-line.after.table-hr'):
        #     current_match = Match(match_info, season_id, current_day)
        #     self.day_results.append(current_match.match_results)

        self.day_results = pd.DataFrame(self.day_results_list,
                                        columns=self.scraping_parameters.saison_cols)


class Match:
    def __init__(self, html_match_info, season_id, current_day):

        self.match = html_match_info
        self.match_results = []
        self.season_id = season_id
        self.current_day = current_day
        self.date = (self.match.select("span.format-full"))[0].text
        self.team_dom = (self.match.select("span.format-full"))[1].text
        self.team_ext = (self.match.select("span.format-full"))[2].text
        self.score_dom = self.match.select("td.cell-score")[0].text.strip().split("-")[0]
        self.score_ext = self.match.select("td.cell-score")[0].text.strip().split("-")[1]
        self.bonus_dom = self.match.select("td.cell-bonus-a")[0].text.strip("\n")
        self.bonus_ext = self.match.select("td.cell-bonus-b")[0].text.strip("\n")

        self.match_results = [
            self.season_id,
            self.current_day,
            self.date,
            self.team_dom,
            self.team_ext,
            self.score_dom,
            self.score_ext,
            self.bonus_dom,
            self.bonus_ext
        ]


def main(debug=False):

    print("Creating an instance of ScrapWeb Class")
    scraping = ScrapWeb(debug=debug)

    print(scraping.results.head(5))

    if not debug:
        scraping.results.to_csv('data/matchs_results.csv',
                                sep='|',
                                encoding='utf-8',
                                index=False)


if __name__ == "__main__":

    main(debug=True)

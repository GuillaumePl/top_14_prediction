import yaml


class ScrapingParameters:

    def __init__(self, scraping_parameters_path='scraping_parameters.yml'):
        self.scraping_parameters_path = scraping_parameters_path
        self.scraping_parameters_dict = self.load_parameters()
        self.fixe = self.scraping_parameters_dict['fixe']
        self.saison_wiki = self.scraping_parameters_dict['saison_wiki']
        self.saison_cols = self.scraping_parameters_dict['saison_cols']

    def load_parameters(self):
        """
        Load parameters needed to scrap the Web into a Dictionary
        Parameters are defined in a .yml file
        """
        with open(self.scraping_parameters_path) as f:
            parameters = yaml.safe_load(f)
        return parameters

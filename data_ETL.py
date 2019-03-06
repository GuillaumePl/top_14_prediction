"""
Class to Extract - Transform - Load Data

    Extraction :
        - Scraping from LNR website

    Transformation :
        - TBD

    Loading :
        - Save data as .CSV file in the 'data/' folder

"""

from scraping.scraping import *
import pandas as pd


class ETL:
    def __init__(self, debug=False):
        self.debug = debug
        self.data = pd.DataFrame()
        self.loaded = False

    def extract(self, scraping_parameters_path='scraping/scraping_parameters.yml'):

        if self.debug:

            pass

        else:

            pass

        return None

    def transform(self):

        return None

    def load(self, custom_path='loaded_data'):

        if self.data.shape[0] == 0:
            raise Exception('Tried to load DataFrame with 0 line')

        if self.data.shape[1] == 0:
            raise Exception('Tried to load DataFrame with 0 column')

        self.data.to_csv('data/{}.csv'.format(custom_path),
                         sep='|',
                         encoding='utf-8',
                         index=False)

        print('Data loaded at {}'.format('data/{}.csv'.format(custom_path)))


def main(debug=False)

    return None


if __name__ == '__main__':
    main()



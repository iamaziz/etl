import sqlite3
import pandas as pd


class Pipeline(object):
    def __init__(self):
        self.population = None
        self.unemployment = None

    def extract(self):
        """
        Data source (based on data from data.gov)
        description:
            table1: https://www2.census.gov/programs-surveys/popest/technical-documentation/file-layouts/2010-2017/cbsa-est2017-alldata.pdf
            table2: https://www.ers.usda.gov/data-products/county-level-data-sets/download-data
        """
        url_popul_est = 'https://www2.census.gov/programs-surveys/popest/datasets/2010-2017/metro/totals/cbsa-est2017-alldata.csv'
        url_unemployment = 'https://www.ers.usda.gov/webdocs/DataFiles/48747/Unemployment.xls'

        self.population = pd.read_csv(url_popul_est, encoding='ISO-8859-1')
        self.unemployment = pd.read_excel(url_unemployment, skiprows=7)

    def transform(self):
        # formatting Population dataset

        # keep the relevant columns only i.e. the columns that contain year-population-estimate and index names
        pop_idx = ['CBSA', 'MDIV', 'STCOU', 'NAME', 'LSAD']
        pop_cols = [c for c in self.population.columns if c.startswith('POPEST')]
        population = self.population[pop_idx + pop_cols].copy()

        # melt, "unpivot" the yearly rate values (from wide format 'columns' to long format 'rows')
        self.population = population.melt(id_vars=pop_idx,
                                          value_vars=pop_cols,
                                          var_name='YEAR',
                                          value_name='POPULATION_EST')

        # fix columns values
        self.population['YEAR'] = self.population['YEAR'].apply(
            lambda x: x[-4:])  # e.g. POPESTIMATE2010 -> 2010

        # formatting Unemployment dataset

        # keep the relevant columns only i.e. unemployment-rate-year and names
        unemp_idx = ['FIPStxt', 'State', 'Area_name']
        unemp_cols = [c for c in self.unemployment.columns if c.startswith('Unemployment_rate')]
        unemployment = self.unemployment[unemp_idx + unemp_cols].copy()

        # melt, "unpivot" the yearly rate values (from wide format 'columns' to long format 'rows')
        self.unemployment = unemployment.melt(id_vars=unemp_idx,
                                              value_vars=unemp_cols,
                                              var_name='Year',
                                              value_name='Unemployment_rate')

        # fix columns values
        self.unemployment = self.unemployment.round(1)  # set precision to .1
        self.unemployment['Year'] = self.unemployment['Year'].apply(
            lambda x: x[-4:])  # remove prefix i.e. 'Unemployment_rate_XXXX'

    def load(self):
        db = DB()
        self.population.to_sql('population', db.conn, if_exists='append', index=False)
        self.unemployment.to_sql('unemployment', db.conn, if_exists='append', index=False)


class DB(object):

    def __init__(self, db_file='db.sqlite'):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self.__init_db()

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def __init_db(self):
        table1 = f"""CREATE TABLE IF NOT EXISTS population(
              CBSA INTEGER,
              MDIV REAL,
              STCOU INTEGER,
              NAME TEXT,
              LSAD TEXT,
              YEAR INTEGER,
              POPULATION_EST INTEGER
                );"""

        table2 = f"""CREATE TABLE IF NOT EXISTS unemployment(
            FIPStxt INTEGER,
            State TEXT,
            Area_name TEXT,
            Year INTEGER,
            unemployment_rate REAL
            );"""

        self.cur.execute(table1)
        self.cur.execute(table2)


if __name__ == '__main__':
    pipeline = Pipeline()
    print('Data Pipeline created')
    print('\t extracting data from source .... ')
    pipeline.extract()
    print('\t formatting and transforming data ... ')
    pipeline.transform()
    print('\t loading into database ... ')
    pipeline.load()

    print('\nDone. See: result in "db.sqlite"')

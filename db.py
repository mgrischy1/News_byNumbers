import mysql.connector
# 123@Weezer
import requests
from mysql.connector import errorcode


class AwsRds:
    def create_table(self):
        create_awarding_agency_table = (
            "CREATE TABLE `awarding_agency` ("
            "  `name` varchar(60) NOT NULL,"
            "  `amount` DECIMAL(60,2) NOT NULL,"
            "  PRIMARY KEY (`name`)"
            ") ENGINE=InnoDB")

        cnx = mysql.connector.connect(user='admin', password='123Weezer',
                                      host='database-1.c9vvzuo2osva.us-east-2.rds.amazonaws.com',
                                      database='news_by_numbers')
        cursor = cnx.cursor()
        cursor.execute(create_awarding_agency_table)

    def create_database(self):
        try:
            cnx = mysql.connector.connect(user='admin', password='123Weezer',
                                          host='database-1.c9vvzuo2osva.us-east-2.rds.amazonaws.com')
            crs = cnx.cursor()
            # crs.execute("CREATE DATABASE news_by_numbers")
            crs.execute("show databases")
            for d in crs:
                print(d)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            cnx.close()

df = AwsRds()
df.create_database()

class SpendingByCategory:
    """|POST| Returns data that is grouped in preset units to support the Spending by Awarding Agency data
       visualizations on USAspending.gov's Advanced Search page |
    """
    awarding_agency_url = '/awarding_agency/'

    """|POST| Returns data that is grouped in preset units to support the Spending by Awarding Subgency data
     visualizations on USAspending.gov's Advanced Search page |
    """
    awarding_subagency_url = '/awarding_subagency/'

    """POST| Returns data that is grouped in preset units to support the Spending by CFDA data
     visualizations on USAspending.gov's Advanced Search page |
    """
    cfda_url = '/cfda/'

    """|POST| Returns data that is grouped in preset units to support the Spending by Country data visualizations
     on USAspending.gov's Recipient Profile page |
    """
    country_url = '/country/'

    """|POST| Returns data that is grouped in preset units to support the Spending by County data visualizations 
      on USAspending.gov's State Profile page |
    """
    county_url = '/county/'

    """|POST| Returns data that is grouped in preset units to support the Spending by Congressional District data
     visualizations on USAspending.gov's State Profile page |
    """
    district_url = '/district/'

    """|POST| Returns data that is grouped in preset units to support the Spending by Recipient DUNS data
     visualizations on USAspending.gov's Advanced Search page |
    """
    recipient_duns_url = '/recipient_duns/'

    """|POST| Returns data that is grouped in preset units to support the Spending by Federal Account data 
    visualizations on USAspending.gov's Recipient Profile page |
    """
    federal_account = '/federal_account/'

    """POST| Returns data that is grouped in preset units to support the Spending by Funding Agency data visualizations
     on USAspending.gov's Advanced Search page |
    """
    funding_agency = '/funding_agency/'

    """|POST| Returns data that is grouped in preset units to support the Spending by Funding Subgency data
     visualizations on USAspending.gov's Advanced Search page |
    """
    funding_subagency = '/funding_subagency/'

    """POST| Returns data that is grouped in preset units to support the Spending by NAICS data visualizations
     on USAspending.gov's Advanced Search page |
    """
    naics = '/naics/'

    """|POST| Returns data that is grouped in preset units to support the Spending by PSC data visualizations
     on USAspending.gov's Advanced Search page |
    """
    psc = '/psc/'

    """|POST| Returns data that is grouped in preset units to support the Spending by State Territory data 
    visualizations on USAspending.gov's Recipient Profile page |
    """
    state_territory = '/state_territory/'

    def __init__(self):
        self.base_url = 'https://api.usaspending.gov/api/v2/search/spending_by_category/'
        self.headers = {'Content-Type': 'application/json'}

    def request(self, end_point):
        url = f'{self.base_url}{end_point}'
        response = requests.post(url,
                                 headers=self.headers).json()
        try:
            i = 0
            dep_spendings = {}
            path_to_info = response['results']
            length = len(path_to_info)
            while i < length:
                # print(path_to_info['name'][])
                name = path_to_info[i]['name']
                amount = path_to_info[i]['amount']
                # print(name, amount)
                insert_name_amnt = f"INSERT INTO awarding_agency (name, amount) VALUES('%s', '%s')" % (name, amount)
                cnx = mysql.connector.connect(user='admin', password='123Weezer',
                                      host='database-1.c9vvzuo2osva.us-east-2.rds.amazonaws.com',
                                      database='news_by_numbers')
                cursor = cnx.cursor()
                cursor.execute(insert_name_amnt)
                cnx.commit()
                dep_spendings[path_to_info[i]['name']] = path_to_info[i]['amount']
                i += 1
            # print(dep_spendings)
        except Exception as e:
            print('errored: ', e)

        # print(response['results'])

    def select(self):
        s = 'SELECT * FROM awarding_agency;'
        cnx = mysql.connector.connect(user='admin', password='123Weezer',
                                      host='database-1.c9vvzuo2osva.us-east-2.rds.amazonaws.com',
                                      database='news_by_numbers')
        cursor = cnx.cursor()
        cursor.execute(s)
        print( cursor.fetchall())

    def delete(self):
        Delete_all_rows = """truncate table awarding_agency """
        cnx = mysql.connector.connect(user='admin', password='123Weezer',
                                      host='database-1.c9vvzuo2osva.us-east-2.rds.amazonaws.com',
                                      database='news_by_numbers')
        cursor = cnx.cursor()
        cursor.execute(Delete_all_rows)

db = SpendingByCategory()
db.select()
# db.request(db.awarding_agency_url)
#
# DB_NAME = 'SPENDDINGS'
#
# TABLES = {}
# TABLES['SPENDDINGS'] = (
#     "CREATE TABLE `awarding_agency` ("
#     "  `name` varchar(16) NOT NULL AUTO_INCREMENT,"
#     "  `amount` DECIMAL(4,2) NOT NULL,"
#     "  PRIMARY KEY (`name`)"
#     ") ENGINE=InnoDB")
# cnx = mysql.connector.connect(user='root', password='123@Weezer')
# cursor = cnx.cursor()
#
#
# def create_database(cursor):
#     try:
#         cursor.execute(
#             "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
#     except mysql.connector.Error as err:
#         print("Failed creating database: {}".format(err))
#         exit(1)
#
#     try:
#         cursor.execute("USE {}".format(DB_NAME))
#     except mysql.connector.Error as err:
#         print("Database {} does not exists.".format(DB_NAME))
#         if err.errno == errorcode.ER_BAD_DB_ERROR:
#             create_database(cursor)
#             print("Database {} created successfully.".format(DB_NAME))
#             cnx.database = DB_NAME
#         else:
#             print(err)
#             exit(1)
#
#
# create_database(cursor)

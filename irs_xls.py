import mysql.connector
# 123@Weezer
import requests
from mysql.connector import errorcode
import pandas as pd


class AwsRds:
    #  class variables that start with tbl are database tables
    tbl_adjusted_gross_income_less_deficit = 'Adjusted gross income less deficit'
    tbl_alternative_minimum_tax_amount = 'Alternative minimum tax Amount'
    tbl_alternative_minimum_tax_number_of_returns = 'Alternative minimum tax Number of returns'
    tbl_ITAC_APAG_income_less_deficit = 'ITAC APAG income less deficit'
    tbl_ITAC_APM_taxable_income_one = 'ITAC APM taxable income [1]'
    tbl_income_tax_after_credits_total = 'Income tax after credits Total'
    tbl_modified_taxable_income_one_At_all_rates = 'Modified taxable income [1] At all rates'
    tbl_modified_taxable_income_one_at_marginal_rate = 'Modified taxable income [1] At marginal rate'
    tbl_net_investment_income_tax_amount = 'Net investment income tax Amount'
    tbl_net_investment_income_tax_number_of_returns = 'Net investment income tax Number of returns'
    tbl_number_of_returns = 'Number of returns'
    tbl_tax_generated_at_all_rates = 'Tax generated At all rates'
    tbl_tax_generated_at_marginal_rate = 'Tax generated At marginal rate'
    tbl_awarding_agency = 'awarding_agency'

    def __init__(self):
        name: str
        value: list
        res: dict
        results: int

    def create_table(self):
        r = self.show_tables()
        file = r'xls_files/tax_brackets.xls'
        df = pd.read_excel(file).columns
        for i in df:
            name = i.replace('\n', ' ')
            results_list = [item[0] for item in r]
            if name not in results_list:
                create_awarding_agency_table = (
                    f"CREATE TABLE `{name}` ("
                    "  `Header` varchar(60) NOT NULL,"
                    "  `value` DECIMAL(60,2) NOT NULL,"
                    "  PRIMARY KEY (`header`)"
                    ") ENGINE=InnoDB")

                cnx = mysql.connector.connect(user='admin', password='123Weezer',
                                              host='database-1.c9vvzuo2osva.us-east-2.rds.amazonaws.com',
                                              database='news_by_numbers')
                cursor = cnx.cursor()
                cursor.execute(create_awarding_agency_table)

    def show_databeses(self):
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

    def show_tables(self):
        cnx = mysql.connector.connect(user='admin', password='123Weezer',
                                      host='database-1.c9vvzuo2osva.us-east-2.rds.amazonaws.com',
                                      database='news_by_numbers')
        crs = cnx.cursor()
        # crs.execute("CREATE DATABASE news_by_numbers")
        crs.execute("show tables")
        return crs.fetchall()

    def insert(self):
        try:
            file = r'xls_files/tax_brackets.xls'
            df = pd.read_excel(file).columns
            df2 = pd.read_excel(file)
            for i in df:
                if i != df[0]:
                    self.name = i.replace('\n', ' ')
                    self.value = list(df2[i])
                    rows = list(df2[df[0]])
                    self.res = dict(zip(rows, self.value))
                    print(self.name, 'is ', self.res)
                    for k, v in self.res.items():
                        print(k, v)
                        insert_name_amnt = f"INSERT INTO `{self.name}` (header, value) VALUES('%s', '%s')" % (k, v)
                        cnx = mysql.connector.connect(user='admin', password='123Weezer',
                                                      host='database-1.c9vvzuo2osva.us-east-2.rds.amazonaws.com',
                                                      database='news_by_numbers')
                        cursor = cnx.cursor()
                        cursor.execute(insert_name_amnt)
                        cnx.commit()

        except Exception as e:
            print('errored: ', e)

    def select_all_tables_and_data(self):
        file = r'xls_files/tax_brackets.xls'
        df = pd.read_excel(file).columns
        for i in df:
            if i != df[0]:
                self.name = i.replace('\n', ' ')
                s = f'SELECT * FROM `{self.name}`;'
                cnx = mysql.connector.connect(user='admin', password='123Weezer',
                                              host='database-1.c9vvzuo2osva.us-east-2.rds.amazonaws.com',
                                              database='news_by_numbers')
                cursor = cnx.cursor()
                cursor.execute(s)
                print(self.name, cursor.fetchall())

    def delete_data(self):
        Delete_all_rows = """truncate table awarding_agency """
        cnx = mysql.connector.connect(user='admin', password='123Weezer',
                                      host='database-1.c9vvzuo2osva.us-east-2.rds.amazonaws.com',
                                      database='news_by_numbers')
        cursor = cnx.cursor()
        cursor.execute(Delete_all_rows)

    def delete_table(self):
        file = r'xls_files/tax_brackets.xls'
        df = pd.read_excel(file)
        d = df.to_dict(orient='records')
        for i in d:
            print(list(i.items())[0][-1])
            delte_table = f'DROP TABLE `{list(i.items())[0][-1]}`;'
            cnx = mysql.connector.connect(user='admin', password='123Weezer',
                                          host='database-1.c9vvzuo2osva.us-east-2.rds.amazonaws.com',
                                          database='news_by_numbers')
            cursor = cnx.cursor()
            cursor.execute(delte_table)

    def alert_table(self):
        file = r'xls_files/tax_brackets.xls'
        df = pd.read_excel(file)
        d = df.to_dict(orient='records')
        for i in d:
            table_name = (list(i.items())[0][-1])
            altr = f"ALTER TABLE `{table_name}` ALTER COLUMN value FLOAT(60,2);"
            cnx = mysql.connector.connect(user='admin', password='123Weezer',
                                          host='database-1.c9vvzuo2osva.us-east-2.rds.amazonaws.com',
                                          database='news_by_numbers')
            cursor = cnx.cursor()
            cursor.execute(altr)

    # def number_of_return(self):
    #     main_list = []
    #     vj = []
    #     l = []
    #     s = f'SELECT * FROM `Number of returns`;'
    #     cnx = mysql.connector.connect(user='admin', password='123Weezer',
    #                                   host='database-1.c9vvzuo2osva.us-east-2.rds.amazonaws.com',
    #                                   database='news_by_numbers')
    #     cursor = cnx.cursor()
    #     cursor.execute(s)
    #     for i in cursor.fetchall():
    #         # print(i)
    #         (k, v) = i
    #
    #         vj.append(k)
    #         l.append(str(v))
    #     # print(l)
    #     main_list.append(vj)
    #     main_list.append(l)
    #     return main_list
    #
    # def tax_generated_at_marginal_rate(self):
    #     main_list = []
    #     vj = []
    #     l = []
    #     s = f'SELECT * FROM `Tax generated At marginal rate`;'
    #     cnx = mysql.connector.connect(user='admin', password='123Weezer',
    #                                   host='database-1.c9vvzuo2osva.us-east-2.rds.amazonaws.com',
    #                                   database='news_by_numbers')
    #     cursor = cnx.cursor()
    #     cursor.execute(s)
    #     for i in cursor.fetchall():
    #         # print(i)
    #         (k, v) = i
    #
    #         vj.append(k)
    #         l.append(str(v))
    #     # print(l)
    #     main_list.append(vj)
    #     main_list.append(l)
    #     return main_list
    #
    # def awarding_agency(self):
    #     main_list = []
    #     vj = []
    #     l = []
    #     s = f'SELECT * FROM `awarding_agency`;'
    #     cnx = mysql.connector.connect(user='admin', password='123Weezer',
    #                                   host='database-1.c9vvzuo2osva.us-east-2.rds.amazonaws.com',
    #                                   database='news_by_numbers')
    #     cursor = cnx.cursor()
    #     cursor.execute(s)
    #     for i in cursor.fetchall():
    #         # print(i)
    #         (k, v) = i
    #
    #         vj.append(k)
    #         l.append(str(v))
    #     # print(l)
    #     main_list.append(vj)
    #     main_list.append(l)
    #     return main_list

    def irs_data(self, table_name: str):
        main_list = []
        vj = []
        l = []
        s = f'SELECT * FROM `{table_name}`;'
        cnx = mysql.connector.connect(user='admin', password='123Weezer',
                                      host='database-1.c9vvzuo2osva.us-east-2.rds.amazonaws.com',
                                      database='news_by_numbers')
        cursor = cnx.cursor()
        cursor.execute(s)
        for i in cursor.fetchall():
            # print(i)
            (k, v) = i

            vj.append(k)
            l.append(str(v))
        # print(l)
        main_list.append(vj)
        main_list.append(l)
        return main_list


# df = AwsRds()
# df.number_of_return()
# df.create_table()
# df.delete_table()
# print(df.show_tables())
# df.alert_table()
# df.insert()
# df.select()
# print(df.awarding_agency())

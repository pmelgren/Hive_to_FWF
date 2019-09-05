import pandas as pd
import numpy as np
import sqlalchemy as sa
from tabulate import tabulate
import datetime

##########################################################
# Functions that can be easily updated based on user needs
##########################################################

# Manipulate a few columns of the 
def restructure(df):
    df['DATE'] = df['Date'].apply(lambda x: x[0:10].replace('-', ''))  
    df['ACCOUNTNO'] = df['AccountNo'].apply(lambda x: '{:0>10.0f}'.format(float(x)))


    # Specify the order of the columns using this list
    # make sure any columns created above appear in col_order
    col_order = ['DATE','ACCOUNTNO', 'Item', 'Amount', 'Bonus']

    return df.loc[:, col_order]


pd.DataFrame.restructure = restructure


# Function to store the text of the Hive query.
def get_query_text():
    query = """
    SELECT 
         AccountNo 
         ,Amount  
         ,Bonus 
         ,Item
         ,Date   
    FROM
        dbo.sample_data
    LIMIT
        150
    """
    return query


########################
# ETL Functions
########################

def hive_to_dataframe(user, pwd='', host='localhost', db='sample_data'):
    """Hive to DataFrame.

    Function takes Hive connection information and returns the entire
    contents of the specified table as a pandas dataframe.

    The query text for this function is pulled from the get_query_text()
    function which is stored in hive_xml_to_ascii_inputs.py

    Args:
        user (str): Username
        pwd (str): Password
        host (str): host
        db (str): database name

    Returns:
        pandas.dataFrame: a DataFrame of the table specified
    """

    # different string formatting depending on if there is a pwd
    if pwd != '':
        pwd = ':' + pwd

    # create SQLalchemy engine from connection information
    engine = sa.engine.create_engine('hive://' + user + pwd + '@' + host + ':10000/' + db)

    # fetch query text from the inputs module
    query_txt = get_query_text()

    # return the specified table as a data frame
    df = pd.read_sql(query_txt, engine)
    return df

def to_fwf(df, fname, datestr):
    """To Fixed Width File

    Writes the provided DataFrame as a Fixed Width File in the provided 
        filepath:

    Args:
        df (pandas.DataFrame): a pandas dataframe to write
        fname (str): a string of the file location to save the output file

    Returns:
        None
    """
    #Format Today's Date as a String
    datestr = str(datetime.datetime.today().strftime('%Y%m%d'))
    
    # open and truncate (or create) the file and write the header
    file = open(fname, "w", encoding="ascii")
    file.write('SALESINFO_'+ datestr + '\n')

    # format the data frame as fixed width characters and write to file
    df = df.replace(np.nan, '', regex=True)
    content = tabulate(df.values.tolist()  # ,headers = list(df.columns)
                       , tablefmt="plain", stralign="left", numalign="left")
    file.write(content)

    # write the footer and close the file
    file.write('\n3' + str(len(df)))
    file.close()
    
# specify the to_fwf function to be used as a method for pandas DataFrames
pd.DataFrame.to_fwf = to_fwf


########################
# Main Script
########################
    
# read in data
df = hive_to_dataframe('fake_user','','0.00.0.000') #final version
#df = pd.read_csv("./sample_data.csv", sep=',')  # read test data

# write dataframe to fixed width file
df.restructure().to_fwf("./test_fwf_2019.txt", '20190829')

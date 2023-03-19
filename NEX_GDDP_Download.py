# NEX GDDP CMIP6 data download tool
# References: (i) https://www.nasa.gov/nex/gddp and (ii) https://www.nccs.nasa.gov/services/data-collections/land-based-products/nex-gddp-cmip6

# Uses a CSV file to get data URL from.

# Libraries
import csv
import pandas as pd
from tqdm import tqdm

# Methods
def Read_URL_Address(user_input):
    """
    Objective:
    Input:
    Output:

    """

    iFlagServer = int(user_input)
    if iFlagServer == 0:
        # NASA Server
        URLfile = 'gddp-cmip6-thredds-fileserver.csv'
        # Original file address: r'https://ds.nccs.nasa.gov/thredds2/fileServer/listing/gddp-cmip6-thredds-fileserver.csv'
        # Backup in case it get lost: https://github.com/EcoNumerica/EN_Data_Pipeline/blob/a2eef14f612c6e89e7db7c421922eb3414a59942/gddp-cmip6-thredds-fileserver.csv
    elif iFlagServer == 1:
        # AWS Server
        URLfile = 'gddp-cmip6-files.csv'
        # Original file address: r'https://nex-gddp-cmip6.s3-us-west-2.amazonaws.com/gddp-cmip6-files.csv'
        # Backup in case it get lost: https://github.com/EcoNumerica/EN_Data_Pipeline/blob/6f62381f5c5a5ec59a1e212d99c9e6d90388cb18/gddp-cmip6-files.csv
    else:
        print('\n')
        print('------------------------------')
        print('Check for server option.')
        print('Server option 0 = NASA Server.')
        print('Server option 1 = AWS Server.')
        print('Other options are not available')
        print('------------------------------')
        quit()

    # ----
    # Read file and save URL address in a list
    URL = []
    with open(URLfile) as index:
        fobjects = csv.reader(index)
        next(fobjects)
        for objs in fobjects:
            md5, uri = [o.strip() for o in objs]
            URL.append(uri)
        # ---

    return URL
# -----


def Generate_GCM_DataFrame(iFlagServer, URLAddress, SaveOption=0):
    """
    Objetive:
    Input:
    Output:

    """

    # ---
    # Check list for conditions
    # Type of data:
    # hurs      -> Near-Surface Relative Humidity -> percentage (%)
    # huss      -> Near-Surface Specific Humidity -> dimensionless ratio (kg.kg-1)
    # pr        -> Precipitation (mean of the daily precipitation rate) -> kg.m-2.s-1
    # rlds      -> Surface Downwelling Longwave Radiation -> W.m-2
    # rsds      -> Surface Downwelling Shortwave Radiation -> W.m-2
    # sfcWind   -> Daily-Mean Near-Surface Wind Speed -> m.s-1
    # tas       -> Daily Near-Surface Air Temperature -> Degrees Kelvin (K)
    # tasmax    -> Daily Maximum Near-Surface Air Temperature -> Degrees Kelvin (K)
    # tasmin    -> Daily Minimum Near-Surface Air Temperature -> Degrees Kelvin (K)

    # URL breakdown
    # NASA Server: https://ds.nccs.nasa.gov/thredds2/fileServer/AMES/NEX/GDDP-CMIP6/UKESM1-0-LL/ssp370/r1i1p1f2/tas/tas_day_UKESM1-0-LL_ssp370_r1i1p1f2_gn_2098.nc
    # AWS Server: https://nex-gddp-cmip6.s3.us-west-2.amazonaws.com/NEX-GDDP-CMIP6/ACCESS-CM2/historical/r1i1p1f1/hurs/hurs_day_ACCESS-CM2_historical_r1i1p1f1_gn_1950.nc

    # Server adress: https://nex-gddp-cmip6.s3.us-west-2.amazonaws.com/NEX-GDDP-CMIP6/
    # Model index: ACCESS-CM2/historical/r1i1p1f1/hurs/hurs_day_ACCESS-CM2_historical_r1i1p1f1_gn_1950.nc
    # Scenario index: historical/r1i1p1f1/hurs/hurs_day_ACCESS-CM2_historical_r1i1p1f1_gn_1950.nc
    # Variant index: r1i1p1f1/hurs/hurs_day_ACCESS-CM2_historical_r1i1p1f1_gn_1950.nc
    # Variable index: hurs/hurs_day_ACCESS-CM2_historical_r1i1p1f1_gn_1950.nc
    # Data and Year index: hurs_day_ACCESS-CM2_historical_r1i1p1f1_gn_1950.nc

    # Dimensions:
    # 1. Models
    # 2. Projection Scenario
    # 3. Climate Variable
    # 4. Years

    GCM_DB = pd.DataFrame(
        columns=['Link', 'Model', 'Scenario', 'Variable', 'Years'])
    # Muito demorado!
    cont = 0
    for ilines in URLAddress:
        Aux = ilines.split('/')
        if iFlagServer == 0:
            GCM_DB.loc[len(GCM_DB)] = [ilines, Aux[8],
                                       Aux[9], Aux[11], Aux[12][-7:-3]]
        else:
            GCM_DB.loc[len(GCM_DB)] = [ilines, Aux[4],
                                       Aux[5], Aux[7], Aux[8][-7:-3]]
        # -----
        cont += 1
        # screen = str(cont) + '/' + str(len(URL))
        # print(screen)
    if SaveOption == 0:
        pass
    else:
        if iFlagServer == 0:
            GCM_DB.to_pickle('GCM_DB_NEX.pkl')
        else:
            GCM_DB.to_pickle('GCM_DB_AWS.pkl')
        # -----
    # -----

    return GCM_DB
# -----


def Read_GCM_DataFrame(iFlagServer):
    """

    """
    if iFlagServer == 0:
        DF = pd.read_pickle('GCM_DB_NEX.pkl')
    else:
        DF = pd.read_pickle('GCM_DB_AWS.pkl')
    # -----

    return DF
# -----


# 1. Parse the CSV file
user_input = 0
# print('Choose the dowload server.')
# print('Server option 0 = NASA Server.')
# print('Server option 1 = AWS Server.')
# input_message = 'Pick an option (0 or 1):'
# user_input = input(input_message)
# ----

# print('Reading URL Address from Server...')
# URL = Read_URL_Address(user_input)
# print(URL)

# print('Saving URL Address as DataFrame...')
# save_file = 0
# GCM_DF = Generate_GCM_DataFrame(user_input,URL,save_file)

print('Reading GCM DataFrame...')
GCM_DF = Read_GCM_DataFrame(user_input)
print(GCM_DF)


# Get unique values from each column
UniqueModel = GCM_DF.Model.unique()
UniqueScen = GCM_DF.Scenario.unique()
UniqueVar = GCM_DF.Variable.unique()
UniqueYear = GCM_DF.Years.unique()

print(UniqueModel[0])
print(UniqueScen)
print(UniqueVar)
print(UniqueYear)

# Aqui eu tenho um DataFrame separado com as dimensões que preciso no banco de dados.
# Começar as perguntas e iniciar o dowload

# Ex. Perguntas:
# 1. QUais modelos possuem todos os cenários?
# 2. Quais modelos possuem todos os anos?
# 3. Quais modelos possuem todas as variáveis?
# 4. Quais variáveis possuem todos os cenários?
# 5. Quais variáveis possuem todos os anos?
# -----
# 6. Quero todos os modelos disponíveis com o ano 2100 em três cenários (A, B e C) para Precipitação;
# Retorna uma lista para download

# FILTRAR DATAFRAME DO GCM POR CONDIÇÃO E INICAR DOWNLOAD
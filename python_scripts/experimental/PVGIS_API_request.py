# script for calling the PVGIS API with a get request for getting the irradiation/insolation data
# for any location by logitude and latitude

import requests


# minimum:
# https://re.jrc.ec.europa.eu/api/MRcalc?lat=45&lon=8&horirrad=1

def get_pvgis_data():
    
    full_url = 'https://re.jrc.ec.europa.eu/api/MRcalc?lat=56.855&lon=12.691&raddatabase=PVGIS-SARAH&horirrad=1'
    # raddatabase=PVGIS-SARAH ger oss bara data fram till 2016
    # raddatabase=PVGIS-SARAH2 är databasen som innehåller data fram till 2020 men det verkar inte som att vi kan
    # nå den från API?

    response = requests.get(full_url)
    csv_data = response.text
    return csv_data


if __name__=="__main__":
    print(get_pvgis_data())
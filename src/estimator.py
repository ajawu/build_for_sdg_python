def estimator(data):
    """
    function to determine impact and severe impact of covid-19 on a country
    :param data:
    :return:
    """
    # Challenge 1
    # calculate currentlyInfected based on reportedCases
    print(data)
    try:
        if isinstance(data['reportedCases'], int):
            impact = {'currentlyInfected': data['reportedCases'] * 10}
            severeImpact = {'currentlyInfected': data['reportedCases'] * 50}
        else:
            return 'Key "reportedCases" has to be of type "int"'
    except KeyError:
        return 'Key "reportedCases" not found'

    # normalize timeToElapse to days
    days = 0
    try:
        if isinstance(data['timeToElapse'], int):
            if data['periodType'].lower() == 'months':
                days = data['timeToElapse'] * 30
            elif data['periodType'].lower() == 'weeks':
                days = data['timeToElapse'] * 7
            elif data['periodType'].lower() == 'days':
                days = data['timeToElapse']
            else:
                return 'Key "periodType" has to be one of the following: weeks, months or days'
        else:
            return 'Key "timeToElapse" has to be of type "int"'
    except AttributeError:
        return 'Key "periodType" has to be of type "str"'

    # Calculate currentlyInfected based on elapsed day sets
    impact['infectionsByRequestedTime'] = int(impact['currentlyInfected'] * (2 ** (days // 3)))
    severeImpact['infectionsByRequestedTime'] = int(severeImpact['currentlyInfected'] *
                                                    (2 ** (days // 3)))

    # Challenge 2
    # calculate severe cases and available beds
    impact['severeCasesByRequestedTime'] = int(impact['infectionsByRequestedTime'] * 0.15)
    severeImpact['severeCasesByRequestedTime'] = int(severeImpact['infectionsByRequestedTime'] *
                                                     0.15)

    if isinstance(data['totalHospitalBeds'], int):
        available_beds = round(data['totalHospitalBeds'] * 0.35, 0)
        impact['hospitalBedsByRequestedTime'] = available_beds - \
            impact['severeCasesByRequestedTime']
        severeImpact['hospitalBedsByRequestedTime'] = available_beds - \
            severeImpact['severeCasesByRequestedTime']
    else:
        return 'Key "totalHospitalBeds" must be of type int'

    # Challenge 3
    impact['casesForICUByRequestedTime'] = int(impact['infectionsByRequestedTime'] * 0.05)
    severeImpact['casesForICUByRequestedTime'] = int(severeImpact['infectionsByRequestedTime'] *
                                                     0.05)

    impact['casesForVentilatorsByRequestedTime'] = int(impact['infectionsByRequestedTime'] * 0.02)
    severeImpact['casesForVentilatorsByRequestedTime'] = int(severeImpact
                                                             ['infectionsByRequestedTime'] * 0.02)

    impact['dollarsInFlight'] = round(impact['infectionsByRequestedTime'] *
                                      data['region']['avgDailyIncomePopulation'] *
                                      data['region']['avgDailyIncomeInUSD'] * days, 2)
    severeImpact['dollarsInFlight'] = round(severeImpact['infectionsByRequestedTime'] *
                                            data['region']['avgDailyIncomePopulation'] *
                                            data['region']['avgDailyIncomeInUSD'] * days, 2)

    return {'data': data, 'impact': impact, 'severeImpact': severeImpact}

#
# print(estimator({
#     "region": {
#         "name": "Africa",
#         "avgAge": 19.7,
#         "avgDailyIncomeInUSD": 4,
#         "avgDailyIncomePopulation": 0.73
#     },
#     "periodType": "days",
#     "timeToElapse": 38,
#     "reportedCases": 2747,
#     "population": 92931687,
#     "totalHospitalBeds": 678874
# }))

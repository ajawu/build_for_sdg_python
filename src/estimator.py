def estimator(data):
    """
    function to determine impact and severe impact of covid-19 on a country
    :param data:
    :return:
    """
    # Challenge 1
    # calculate currentlyInfected based on reportedCases
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
    impact['severeCasesByRequestedTime'] = round(impact['infectionsByRequestedTime'] * 0.15, 0)
    severeImpact['severeCasesByRequestedTime'] = round(severeImpact['infectionsByRequestedTime'] *
                                                     0.15, 0)

    if isinstance(data['totalHospitalBeds'], int):
        available_beds = round(data['totalHospitalBeds'] * 0.35, 0)
        impact['hospitalBedsByRequestedTime'] = round(available_beds -
                                                      impact['severeCasesByRequestedTime'], 0)
        severeImpact['hospitalBedsByRequestedTime'] = round(available_beds -
                                                            severeImpact
                                                            ['severeCasesByRequestedTime'],
                                                            0)
    else:
        return 'Key "totalHospitalBeds" must be of type int'

    # Challenge 3
    impact['casesForICUByRequestedTime'] = round(impact['infectionsByRequestedTime'] * 0.05, 0)
    severeImpact['casesForICUByRequestedTime'] = round(severeImpact['infectionsByRequestedTime'] *
                                                       0.05, 0)

    impact['casesForVentilatorsByRequestedTime'] = round(impact['infectionsByRequestedTime'] * 0.02,
                                                         0)
    severeImpact['casesForVentilatorsByRequestedTime'] = round(severeImpact
                                                               ['infectionsByRequestedTime'] * 0.02,
                                                               0)

    impact['dollarsInFlight'] = round(impact['infectionsByRequestedTime'] *
                                      data['region']['avgDailyIncomePopulation'] *
                                      data['region']['avgDailyIncomeInUSD'] * days, 2)
    severeImpact['dollarsInFlight'] = round(severeImpact['infectionsByRequestedTime'] *
                                            data['region']['avgDailyIncomePopulation'] *
                                            data['region']['avgDailyIncomeInUSD'] * days, 2)

    return {'data': data, 'impact': impact, 'severeImpact': severeImpact}

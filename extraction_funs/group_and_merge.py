

def combineResources(resourcesToCombine, onlyFirstValue = [], deleteMultiples = True):
    """
    Merges resources together. Given a list of resources, this functions returns
    a single resource containing the information of the given resources. 

    If a key appears in several resources, the returned resource will contain the
    respective values in a list with that key.
    
    Parameters
    ----------
    resourcesToCombine : the resources (i.e. dictionaries) we want to merge together
    onlyFirstValue : list with strings. For the named keys here, no list will
        be created if they appear several times, instead only the first appearing 
        value will be used.
        The default is [].
    deleteMultiples : Boolean. If True and field contains multiple values, the
        multiple values will be removed. The default is True.

    Returns
    -------
    result : Dictionary. Contains the union of the fields/keys of the given resources.

    """
    result = {}
    listsKeys = [] # make those fields unique later
    for resource in resourcesToCombine:
        currentKeys = result.keys()
        for key in resource.keys():
            if key not in currentKeys:
                result[key] = resource[key]
            else:
                if key in onlyFirstValue:
                    continue
                if key not in listsKeys:
                    listsKeys.append(key)
                if (type(result[key]) == list) and (type(resource[key]) == list):
                    result[key] += resource[key]
                elif (type(result[key]) == list) and (type(resource[key]) != list):
                    result[key].append(resource[key])
                elif (type(result[key]) != list) and (type(resource[key]) == list):
                    result[key] = resource[key].append(result[key])
                else:
                    result[key] = [result[key],resource[key]]
    if deleteMultiples:
        for key in listsKeys:
            values = list(set(result[key]))
            if len(values) == 1:
                values = values[0]
            result[key] = values
    return result
    
def groupResources(resources, groupBy):
    """
    Given a list of resources, they will be grouped together such that resources
    which share a common property and up in the same group.

    Parameters
    ----------
    resources : List of resources (i.e. dictionaries) to be grouped.
    groupBy : Property of a resource, i.e. a key (as string) or function which
        extracts a value out of the resource that is ordered.

    Returns
    -------
    resourcesGrouped : list of the grouped resources, i.e. each element of the
        list is itself a list which contains the resources. All resources in one 
        group have the same specified property (groupBy).

    """
    if type(groupBy) == str:
        key = groupBy
        groupBy = lambda x: x[key]
    resources.sort(key = groupBy)
    resourcesGrouped = []
    prevKey = None
    currentGroup = None
    for res in resources:
        currentKey = groupBy(res)
        if prevKey != currentKey:
            if currentGroup is not None:
                resourcesGrouped.append(currentGroup)
            currentGroup = []
            currentGroup.append(res)
        else:
            currentGroup.append(res)
        prevKey = currentKey
    resourcesGrouped.append(currentGroup)
    return resourcesGrouped
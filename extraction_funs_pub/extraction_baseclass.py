def tryPath(resource,fields,condition = None):
    res = resource
    n = 0
    for field in fields:
        n += 1
        if (type(field) == str) and (type(res) == dict):
            if field in res.keys():
                res = res[field]
            else:
                #print('Field not found 1')
                return None
        elif (type(field) == int) and (type(res) == list) and (field < len(res)):
            res = res[field]
        elif (field == '*') and (type(res) == list):
            remainingFields = fields[n:]
            moreStars = '*' in remainingFields
            if moreStars:
                res = [tryPath(x, remainingFields, condition) for x in res]
            elif condition is None:
                res = [tryPath(x, remainingFields) for x in res]
            else: 
                res = [tryPath(x, remainingFields) for x in res if condition(x)]
                res = [x for x in res if x is not None]
            if len(res) > 0:
                if len(res) == 1:
                    res = res[0]
                #print('res',res)    
                return res
            else:
                #print('Field not found 2')
                return None
        else:
            #print('Field not found 3')
            return None
    if condition is None:
        #print('res',res) 
        return res
    if condition(resource):
        #print('res',res) 
        return res
    #print('Field not found 4')
    return None

class extractor:
    
    def __init__(self, name, resourceType = None):
        self.name = name
        self.resourceType = resourceType
        self.fields = []
        self.conditions = []
    
    def addField(self, name, addfun, necessary, fill = "skip"):
        self.fields.append((name, addfun, necessary, fill))
     
    def addFieldsByPaths(self, fields, fill = 'skip'):
        fun_xy = lambda x: lambda y: tryPath(y, x)
        self.fields += [(fieldName,
                         fun_xy(fieldPath),
                         False,
                         fill) for fieldName, fieldPath in fields.items()]
    
    def addCondition(self, condfun):
        self.conditions.append(condfun)
    
    def addFieldsFromList(self, fieldPath, names2conditions, fill = "skip"):
        fun_xy = lambda x: lambda y : tryPath(y, fieldPath, x)
        self.fields += [(fieldName,
                         fun_xy(condition),
                         False,
                         fill) for fieldName, condition in names2conditions.items()]
    
    def extract(self, jsons):
        res = []
        for resource in jsons:
            
            # check resourceType
            if 'resource' in resource.keys():
                resource = resource['resource']
            if resource['resourceType'] not in self.resourceType:
                continue
            
            # check additional conditions
            allTrue = True
            for condfun in self.conditions:
                if not condfun(resource):
                    allTrue = False
                    continue
            if not allTrue:
                continue
            
            # fill fields
            lres = {}
            allNecessaries = True
            for name, addfun, necessary, fill in self.fields:
                value = addfun(resource)
                isNone = value is None
                if isNone and necessary:
                    allNecessaries = False
                    continue
                if isNone and (fill != "skip"):
                    value = fill
                if (value is not None) or (fill != "skip"):
                    lres[name] = value
            if len(lres) > 0:
                res.append(lres)
            else:
                print('hohohoh')
        return res

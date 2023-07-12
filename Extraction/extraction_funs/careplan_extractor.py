from extraction_baseclass import extractor, tryPath

def getCareplan(json_pat):

    # With this we extract the primary diagnosis
    # Create the instance of the base class
    careplan_ex = extractor(name="PatientCarePlan", resourceType="care plan")

    # Note: when you add condition you are already under this so you start path from here
    careplan_ex.addCondition(lambda x: tryPath(x, ['identifier',0,'system']) == 'https://hospital.org/TumorDocumentation/TherapyPlanning')

    # We add the patient id first and it is necessary
    careplan_ex.addField('patid', lambda x: x['subject']['reference'], True)
    careplan_ex.addField('time_of_careplan', lambda x: x['period']['start'], True)

    conds = [{'careplan_name':lambda x: tryPath(x, ['category',0,'coding',0,'system']) == 'https://hospital.org/TumorDocumentation/TherapyPlanning/therapy'},
             {'careplan_intention':lambda x: tryPath(x, ['category',1,'coding',0,'system']) == 'https://hospital.org/TumorDocumentation/TherapyPlanning/therapy target'},
             {'careplan_type':lambda x: tryPath(x, ['category',2,'coding',0,'system']) == 'https://hospital.org/TumorDocumentation/TherapyPlanning/therapy art'} ]

    careplan_ex.addFieldsFromList(['category',0,'coding',0,'display'], conds[0])
    careplan_ex.addFieldsFromList(['category',1,'coding',0,'display'], conds[1])
    careplan_ex.addFieldsFromList(['category',2,'coding',0,'display'], conds[2])

    careplan_simp = careplan_ex.extract(json_pat['entry'])


    return careplan_simp # return format is a list
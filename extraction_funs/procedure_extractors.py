from extraction_baseclass import extractor, tryPath

def getRadioTherapy():
    ex = extractor(name = "RadioTherapy", resourceType = "Procedure")
    
    ex.addCondition(lambda x: tryPath(x, ['identifier',0,'system']) == 'https://uk-essen.de/HIS/Cerner/Medico/TumorDocumentation/RadiationTherapy/nNGM')
    
    ex.addField('patid', lambda x: x['subject']['reference'], True)

    ex.addFieldsByPaths({
        'dt_start': ['performedPeriod','start'],
        'dt_end': ['performedPeriod','end'],
        'cat_intention': ['reasonCode','*','coding',0,'code'],
        'cat_status': ['status'],
        'cat_reason_end': ['statusReason',0,'coding',0,'code'],
    })
    ex.addField('cat_type_radiation1', lambda x: tryPath(x, ['code','coding','*','display'],
                                                         lambda x: tryPath(x,['code']) != '33195004'), False)
    ex.addField('cat_type_radiation2', lambda x: tryPath(x, ['code','extension',0,'valueCoding','code']), False)
    
    return ex

def getOperation():
    ex = extractor(name = "Operatioon", resourceType = "Procedure")
    ex.addCondition(lambda x: tryPath(x, ['identifier',0,'system']) == 'https://uk-essen.de/HIS/Cerner/Medico/TumorDocumentation/Operation/nNGM')
    
    ex.addField('patid', lambda x: x['subject']['reference'], True)  
    ex.addFieldsByPaths({
        'dt_record': ['performedDateTime'],
        'cat_intention': ['reasonCode',0,'coding',0,'code'],
        'cat_status': ['status'],
        'cat_bodysite': ['bodySite',0,'coding',0,'display']
    })
    
    def getResectionStatus(x):
        statusCode = tryPath(x, ['code','extension','*','extension','*','valueCodeableConcept','coding',0,'code'],
                            lambda x: tryPath(x, ['url']) == 'resektionsstatus')
        statusLabel = None # label from loinc.org
        if statusCode == 'LA26542-3':
            statusLabel = 'R0'
        elif statusCode == 'LA26543-1':
            statusLabel = 'R1'
        elif statusCode == 'LA26544-9':
            statusLabel = 'R2'
        return statusLabel
    
    ex.addField('cat_resection_type', lambda x: tryPath(x, 
                                                        ['code','extension','*','extension','*','valueCodeableConcept','coding',0,'code'],
                                                        lambda x: tryPath(x, ['url']) == 'resektionsart'),
                False)
    ex.addField('cat_resection_status', getResectionStatus, False)
    ex.addField('cat_ops_code', lambda x: tryPath(x, ['code','coding','*','code'],
                                                 lambda x: tryPath(x, ['system']) == 'https://uk-essen.de/HIS/Cerner/Medico/TumorDocumentation/Operation/OPS'), False)
    
    return ex

def getExaminations():
    ex = extractor(name = "Operation", resourceType = "Procedure")
    ex.addCondition(lambda x: tryPath(x, ['identifier',0,'system']) == 'https://uk-essen.de/HIS/Cerner/Medico/TumorDocumentation/ExaminationPerformed')
    
    ex.addField('patid', lambda x: x['subject']['reference'], True)
    ex.addField('dt_record', lambda x: tryPath(x, ['performedDateTime']), False)
    ex.addField('cat_examination_type', lambda x: tryPath(resource = x, 
                                                          fields = ['code','coding','*','display'],
                                                          condition = lambda x: tryPath(x, ['system']) == 'http://ncimeta.nci.nih.gov'),
                False)
    ex.addField('cat_reasons', lambda x: tryPath(resource = x, 
                                                 fields = ['reasonCode','*','coding','*','display'],
                                                 condition = lambda x: tryPath(x, ['system']) == 'http://ncimeta.nci.nih.gov'),
                False)
    return ex
                
                
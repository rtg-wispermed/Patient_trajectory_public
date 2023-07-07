from extraction_baseclass import extractor, tryPath

def getMedicationAdministration():
    ex = extractor(name = "TumorMedication", resourceType = "MedicationAdministration")
    
    ex.addCondition(lambda x: tryPath(x, ['identifier',0,'system']) == 'https://uk-essen.de/HIS/Cerner/Medico/TumorDocumentation/SystemicTherapy')
    
    ex.addField('patid', lambda x: x['subject']['reference'], True)

    # medtype: take text if code is error
    def getmed(x):
        medi = tryPath(x, ['medicationCodeableConcept','coding',0,'code'])
        if (medi is None) or (medi == 'error'):
            medi = tryPath(x, ['medicationCodeableConcept','text'])
        return medi
    ex.addField('cat_drugtype', getmed, False, 'Unknown')

    ex.addFieldsByPaths({
        'dt_start': ['effectivePeriod','start'],
        'dt_end': ['effectivePeriod','end'],
        'cat_intention': ['reasonCode','*','coding',0,'code'],
        'cat_status': ['status'],
        'cat_reason_end': ['statusReason',0,'coding',0,'code'],
        'ref_supporting_information': ['supportingInformation','reference'],
        'num_quantity': ['dosage','rateQuantity','value']
    })
    
    ex.addField('ref_episode', lambda x: tryPath(x, ['extension','*','valueReference','reference'], 
                                                lambda x: tryPath(x, ['url']) == 'https://uk-essen.de/HIS/Cerner/Medico/TumorDocumentation/EpisodeOfCareExtension'), False)
    ex.addField('flg_offlabel', lambda x: tryPath(x, ['extension','*','valueBoolean'], 
                                                 lambda x: tryPath(x, ['url']) == 'http://uk-koeln.de/fhir/StructureDefinition/Extension/nNGM/OffLabelTherapie'), False)
    ex.addField('flg_studytherapy_url', lambda x: tryPath(x, ['extension','*','extension',0,'url'], 
                                                          lambda x: tryPath(x,['url']) == 'http://uk-koeln.de/fhir/StructureDefinition/Extension/cancer-base/studientherapie'), False)
    ex.addField('flg_studytherapy', lambda x: tryPath(x, ['extension','*','extension',0,'valueBoolean'], 
                                                          lambda x: tryPath(x,['url']) == 'http://uk-koeln.de/fhir/StructureDefinition/Extension/cancer-base/studientherapie'), False)
    
    return ex
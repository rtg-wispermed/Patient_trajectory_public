from extraction_baseclass import extractor, tryPath

def getExtractorPTNM():
    tnm_extract = extractor(name = 'ptnm', resourceType = "Observation")
    tnm_extract.addCondition(lambda x: tryPath(x, ['identifier',0,'system']) == 'https://uk-essen.de/HIS/Cerner/Medico/TumorDocumentation/pTNM')
    tnm_extract.addField('patid', lambda x: x['subject']['reference'], True)
    tnm_extract.addField('dt_record', lambda x: tryPath(x, ['effectiveDateTime']), False)
    tnm_extract.addField('cat_version', lambda x: tryPath(x, ['valueCodeableConcept','coding',0,'version']), False, None)
    tnm_extract.addField('tnm_stage', lambda x: tryPath(x, ['valueCodeableConcept','coding',0,'display']), False)

    # t stage n stage m stage, residualstatus
    conds = {'tstage' : lambda x: tryPath(x, ['code','coding',0,'display']) == 'Primary tumor.pathology',
             'nstage' : lambda x: tryPath(x, ['code','coding',0,'display']) == 'Regional lymph nodes.pathology',
             'mstage' : lambda x: tryPath(x, ['code','coding',0,'display']) == 'Distant metastases.pathology',
             'residual_state' : lambda x: tryPath(x, ['code','coding',0,'display']) == 'Residual tumor^postoperative'}
    tnm_extract.addFieldsFromList(['component','*','valueCodeableConcept','coding',0,'code'], conds)

    # number of affected nodes
    conds = {'snodes_postive': lambda x: tryPath(x, ['code','coding',0,'display']) == 'Anzahl SN-LK befallen',
             'snodes_examined': lambda x: tryPath(x, ['code','coding',0,'display']) == 'Sentinel lymph nodes examined',
             'rnodes_positive': lambda x: tryPath(x, ['code','coding',0,'display']) == 'Regional lymph nodes positive', 
             'rnodes_examined': lambda x: tryPath(x, ['code','coding',0,'display']) == 'Regional lymph nodes examined'}
    tnm_extract.addFieldsFromList(['component','*','valueQuantity','value'], conds)
    return tnm_extract

def getExtractorCTNM():
    tnm_extract = extractor(name = 'ctnm', resourceType = "Observation")
    tnm_extract.addCondition(lambda x: tryPath(x, ['identifier',0,'system']) == 'https://uk-essen.de/HIS/Cerner/Medico/TumorDocumentation/cTNM')
    tnm_extract.addField('patid', lambda x: x['subject']['reference'], True)
    tnm_extract.addField('dt_record', lambda x: tryPath(x, ['effectiveDateTime']), False)
    tnm_extract.addField('tnm_stage', lambda x: tryPath(x, ['valueCodeableConcept','coding',0,'display']), False)
    tnm_extract.addField('cat_version', lambda x: tryPath(x, ['valueCodeableConcept','coding',0,'version']), False, None)

    # t stage n stage m stage
    conds = {'tstage' : lambda x: tryPath(x, ['valueCodeableConcept','coding',0,'system']) == 'http://dktk.dkfz.de/fhir/onco/core/ValueSet/TNMTVS',
             'nstage' : lambda x: tryPath(x, ['valueCodeableConcept','coding',0,'system']) == 'http://dktk.dkfz.de/fhir/onco/core/ValueSet/TNMNVS',
             'mstage' : lambda x: tryPath(x, ['valueCodeableConcept','coding',0,'system']) == 'http://dktk.dkfz.de/fhir/onco/core/ValueSet/TNMMVS'}
    tnm_extract.addFieldsFromList(['component','*','valueCodeableConcept','coding',0,'code'], conds)
    
    return tnm_extract

def getExtractorPropertiesPrimary():
    # general stuff
    ex = extractor(name = 'PropertiesPrimary', resourceType = 'Observation')
    ex.addCondition(lambda x: tryPath(x, ['identifier',0,'system']) == 'https://uk-essen.de/HIS/Cerner/Medico/TumorDocumentation/DCP08/PathologyReport/TumorProperties')
    ex.addField('patid', lambda x: x['subject']['reference'], True)
    ex.addField('dt_record', lambda x: tryPath(x, ['effectiveDateTime']), False)
    
    # boolean infos
    conds = {'flg_ulcerated': lambda x: tryPath(x, ['code','coding',0,'display']) == 'Ulzeration',
             'flg_transcapsular': lambda x: tryPath(x, ['code','coding',0,'display']) == 'Kapseldurchbruch',
             'flg_reexcision': lambda x: tryPath(x, ['code','coding',0,'display']) == 'Nachexzision',
             'flg_regression': lambda x: tryPath(x, ['code','coding',0,'display']) == 'Regression'}
    ex.addFieldsFromList(['valueBoolean'], conds)
    
    # quantity infos
    conds = {'no_mitotic_rate': lambda x: tryPath(x, ['code','coding',0,'display']) == 'Anzahl Mitosen pro mm^2',
             'no_tumor_thickness': lambda x: tryPath(x, ['code','coding',0,'display']) == 'Tumordicke in mm'}
    ex.addFieldsFromList(['valueQuantity','value'], conds)
    
    return ex

def getExtractorPropertiesMetastases():
    ex = extractor(name = 'PropertiesMetastases', resourceType = 'Observation')
    ex.addCondition(lambda x: tryPath(x, ['identifier',0,'system']) == 'https://uk-essen.de/HIS/Cerner/Medico/TumorDocumentation/DistantMetastases')
    ex.addField('patid', lambda x: x['subject']['reference'], True)
    ex.addField('dt_record', lambda x: tryPath(x, ['effectiveDateTime']), False)
    
    # certainty of diagnosis
    ex.addField('cat_certainty',
                lambda x: tryPath(x, ['category','*','coding',0,'display'],
                                 lambda x: tryPath(x, ['coding',0,'system']) == 'https://uk-essen.de/HIS/Cerner/Medico/TumorDocumentation/DistantMetastases/Auspraegung'),
                False)
    
    ex.addField('cat_prooftype',
                lambda x: tryPath(x, ['category','*','coding',0,'code'], 
                                  lambda x: tryPath(x, ['coding',0,'system']) == 'http://terminology.hl7.org/CodeSystem/observation-category'),
               False)
    
    ex.addField('cat_bodysite', lambda x: tryPath(x, ['bodySite','coding',0,'display']), False)
    
    return ex

def getExtractorOncogenes():
    # basically two in one:
    # 1) The results for individual genes
    # 2) The overall resource linking to the individual ones.
    # -> Throw overall resource away? at the moment I don't see any use for it
    
    ex = extractor(name = "Oncogenes", resourceType = "Observation")
    ex.addCondition(lambda x: tryPath(x, ['identifier',0,'system']) == 'https://uk-essen.de/HIS/Cerner/Medico/TumorDocumentation/DCP08/PathologyReport/MutationStatus')
    ex.addCondition(lambda x: tryPath(x, ['code','coding',0,'system']) == 'https://uk-essen.de/HIS/Cerner/Medico/TumorDocumentation/DCP08/PathologyReport/MutationStatus/Oncogene')
    
    ex.addField('patid', lambda x: x['subject']['reference'], True)
    ex.addField('dt_record', lambda x: tryPath(x, ['effectiveDateTime']), False)
    
    ex.addField('cat_gene', lambda x: tryPath(x, ['code','coding',0,'display']), False)
    ex.addField('cat_variant', lambda x: tryPath(x, ['valueCodeableConcept','text']), False)
    
    def isGeneticFinding(x):
        res = tryPath(x, ['valueCodeableConcept','coding',0,'display'])
        if res is None:
            return None
        return res == 'Genetic Finding'
                                                 
    ex.addField('flg_mutated', isGeneticFinding, False)
    ex.addField('num_frequency', lambda x: tryPath(x, ['component',0,'valueInteger']), False)
    
    return ex
                
def getExtractorProgress():
    ex = extractor(name = "Progress", resourceType = "Observation")
    
    relsys = ['https://uk-essen.de/HIS/Cerner/Medico/TumorDocumentation/TumorStatusOverall',
              'https://uk-essen.de/HIS/Cerner/Medico/TumorDocumentation/TumorStatusLymphNodes',
              'https://uk-essen.de/HIS/Cerner/Medico/TumorDocumentation/TumorStatusMetastases',
              'https://uk-essen.de/HIS/Cerner/Medico/TumorDocumentation/Progress']
    ex.addCondition(lambda x: tryPath(x, ['identifier',0,'system']) in relsys)
    
    ex.addField('patid', lambda x: x['subject']['reference'], True)
    ex.addField('dt_record', lambda x: tryPath(x, ['effectiveDateTime']), False)
    
    conds = {'cat_progress_overall': lambda x: x['identifier'][0]['system'] == 'https://uk-essen.de/HIS/Cerner/Medico/TumorDocumentation/TumorStatusOverall',
            'cat_progress_primary': lambda x: x['identifier'][0]['system'] == 'https://uk-essen.de/HIS/Cerner/Medico/TumorDocumentation/Progress',
            'cat_progress_nodes': lambda x: x['identifier'][0]['system'] == 'https://uk-essen.de/HIS/Cerner/Medico/TumorDocumentation/TumorStatusLymphNodes',
            'cat_progress_metastases': lambda x: x['identifier'][0]['system'] == 'https://uk-essen.de/HIS/Cerner/Medico/TumorDocumentation/TumorStatusMetastases'}
    
    ex.addFieldsFromList(['valueCodeableConcept','coding',0,'display'], conds)
    
    return ex

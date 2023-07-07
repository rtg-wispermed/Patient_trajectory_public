from extraction_baseclass import extractor, tryPath
from tnm_extractors import *
from group_and_merge import groupResources

def getPrimaryTumor(json_pat):
    # With this we extract the primary diagnosis
    # Create the instance of the base class
    cond_ex = extractor(name="PatientCondition", resourceType="condition")

    # Since we want first Primary Diagnosis we add this condition
    # Note: when you add condition you are already under this so you start path from here
    cond_ex.addCondition(lambda x: tryPath(x, ['identifier',0,'system']) == 'https://hospital.org/TumorDocumentation/PrimaryTumorDiagnosis')


    # We add the patient id first and it is necessary
    cond_ex.addField('patid', lambda x: x['subject']['reference'], True)

    # We add the cancer code and display
    conds = [{'ICD10_2019_cancer_code' : lambda x: tryPath(x, ['code','coding',0,'system']) == 'http://fhir.de/CodeSystem/dimdi/icd-10-gm'},
             {'Code_display' : lambda x: tryPath(x, ['code','coding',0,'system']) == 'http://fhir.de/CodeSystem/dimdi/icd-10-gm'},
             {'Location_Eng' : lambda x: tryPath(x, ['bodySite',0,'coding',0,'system']) == 'http://snomed.info/sct'},
             {'Location_specific' : lambda x: tryPath(x, ['bodySite',1,'coding',0,'system']) == 'http://snomed.info/sct'},
             {'Other_skin_disorders_code' : lambda x: tryPath(x, ['bodySite',2,'coding',0,'system']) == "http://terminology.hl7.org/CodeSystem/icd-o-3"},
             {'Other_skin_disorders_loc' : lambda x: tryPath(x, ['bodySite',2,'coding',0,'system']) == "http://terminology.hl7.org/CodeSystem/icd-o-3"},
             {'Starting_stage' : lambda x: tryPath(x, ['stage',0,'type','coding',0,'system']) == "http://snomed.info/sct"},
             ]
    cond_ex.addFieldsFromList(['code','coding',0,'code'], conds[0])
    cond_ex.addFieldsFromList(['code','coding',0,'display'], conds[1])
    cond_ex.addFieldsFromList(['bodySite',0,'coding',0,'display'], conds[2])
    cond_ex.addFieldsFromList(['bodySite',1,'coding',0,'display'], conds[3])
    cond_ex.addFieldsFromList(['bodySite',2,'coding',0,'code'], conds[4])
    cond_ex.addFieldsFromList(['bodySite',2,'coding',0,'display'], conds[5])
    cond_ex.addFieldsFromList(['stage',0,'type','coding',0,'display'], conds[6])

    # We add the date of the primary diagnosis
    cond_ex.addField('Date', lambda x: x['onsetDateTime'], True)

    cond_simp = cond_ex.extract(json_pat['entry']) # these are moment
    
    # Lets use the TNM extractors to add references
    ctnm = getExtractorCTNM().extract(json_pat['entry'])
    ptnm = getExtractorPTNM().extract(json_pat['entry'])

    ctnm = groupResources(ctnm,'dt_record')
    ptnm = groupResources(ptnm,'dt_record')

    
    cond_simp.append([ptnm]) # We take only ptnm as stated in PDF from Meijie
    
    return cond_simp

def getComorbitidies():
    pass
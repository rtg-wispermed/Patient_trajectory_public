## Patient trajectory visualization for FHIR healthcare data: A use case on melanoma patients
Fast Healthcare Interoperability Resources (FHIR) is gaining popularity as a standard framework for
the exchange of electronic health record (EHR) data. Despite the advantages of FHIR, it is difficult
for clinicians to understand the data in EHR. To support clinicians in accessing data about a patient,
we created a pipeline that extracts, transforms, and visualizes patient data from FHIR. We employ a
web-bases timeline visualization that shows clinical data recorded for the patient over their disease
trajectory. This can help clinicians to use the patient data more efficiently and to get a clear picture of
the patient’s disease progress and physical condition more quickly, which could help them to develop the
best treatment plan for their patients. 

## Approach
Our pipeline consists of four steps (cf. Figure 1): i) patient selection, ii) relevance judgement of
attributes by domain experts, iii) extraction of relevant attributes and iv) visualisation.


<img width="613" alt="Pipeline" src="https://github.com/rtg-wispermed/Patient_trajectory_public/assets/52000882/9f1c499d-4ee7-4fab-87c3-dec731f1cbab">

## For fake patient building

1. Transfer all German words to English use  "deep_translator" API
2. Modify the links include "uk-essen.de", "https://uk-essen.de/HIS/Cerner/Medico/TumorDocumentation/.." to "https://hospital.org/TumorDocumentation/.."
3. Add random noise for the data infromaton within 10 days without change the order of the elements.
4. Manually change the patient 'id', 'birthdate' and 'deceasedDateTime'
5. Manually add some fake information 

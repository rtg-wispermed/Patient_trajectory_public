# patient-history
Building patient trajectory from FHIR data

# For extaction_funcs_pub

# For fake patient building

1. Transfer all German words to English use  "deep_translator" API
2. Modify the links include "uk-essen.de", "https://uk-essen.de/HIS/Cerner/Medico/TumorDocumentation/.." to "https://hospital.org/TumorDocumentation/.."
3. Add random noise for the data infromaton within 10 days without change the order of the elements.
4. Manually change the patient 'id', 'birthdate' and 'deceasedDateTime'
5. Manually add some fake information 

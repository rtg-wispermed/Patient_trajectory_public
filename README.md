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

## Example
This example is based on a synthetic, but realistic patient.
### 1.Selection criteria:
Melanoma patients: Condition.category = |C0677930 (Primary Neoplasm) AND Condition.code = C43.*.
### 2.FHIR 
  under "Example_patient" folder,"patient_01.json"
### 3.Relevance judgement of attributes
  under relevance judgment
### 4.Simple JSON output
  under "Visualisation" folder,"patient_01_simple.json"
### 5.Visualisation
Example with all selected attributes from "Relevance judgement of attributes" step.(cropped due to space constraints, get it by running "trajectory_zoom.html" under "Visualization" folder):
<img width="1291" alt="github_all" src="https://github.com/rtg-wispermed/Patient_trajectory_public/assets/52000882/88e249fe-0033-45e7-8a20-fae0e95ef81f">

Example with filter function, only show the progress information(cropped due to space constraints, get it by running "trajectory_filter.html" under "Visualization" folder):
<img width="1282" alt="github_progress" src="https://github.com/rtg-wispermed/Patient_trajectory_public/assets/52000882/0f8fa01d-fa8a-4d1d-a44d-d6d0b7929763">


## Patient trajectory visualization for FHIR healthcare data: A use case on melanoma patients
This repository is the official implementation of the paper https://ceur-ws.org/Vol-3630/LWDA2023-paper14.pdf

## Abstract
Fast Healthcare Interoperability Resources (FHIR) is gaining popularity as a standard framework for
the exchange of electronic health record (EHR) data. Despite the advantages of FHIR, it is difficult
for clinicians to understand the data in EHR. To support clinicians in accessing data about a patient,
we created a pipeline that extracts, transforms, and visualizes patient data from FHIR. We employ a
web-bases timeline visualization that shows clinical data recorded for the patient over their disease
trajectory. This can help clinicians to use the patient data more efficiently and to get a clear picture of
the patient’s disease progress and physical condition more quickly, which could help them to develop the
best treatment plan for their patients. 

## Approach
Our pipeline consists of four steps (cf. Figure 1): i) patient selection, ii) relevance judgment of
attributes by domain experts, iii) extraction of relevant attributes, and iv) visualization.


<img width="613" alt="Pipeline" src="https://github.com/rtg-wispermed/Patient_trajectory_public/assets/52000882/9f1c499d-4ee7-4fab-87c3-dec731f1cbab">


## Example
This example is based on a synthetic, but realistic patient.
### 1.Selection criteria:
  In our use case, the selection criteria is melanoma patients: Condition.category = |C0677930 (Primary Neoplasm) AND Condition.code = C43.*.
### 2.FHIR 
  Under "Example_patient" folder,"patient_01.json", which is a synthetic, but realistic patient. 
### 3.Relevance judgement of attributes
  Under "Relevance_judgment" folder. We selected the attributes which at least one clinician rated as very important for inclusion in the patient trajectory visualisation.
### 4.Simple JSON outputs
  Under "Visualisation" folder,"patient_01_simple.json".
### 5.Visualisation
For visulisation, we utilize the publicly available, web-based charting framework AnyChart(https://github.com/AnyChart). An example with all selected attributes from "Relevance judgement of attributes" step.(cropped due to space constraints, get it by running "trajectory_zoom.html" under "Visualization" folder):
![Alt text](https://github.com/rtg-wispermed/Patient_trajectory_public/blob/main/Images/new_all.png)
<!--<img width="1514" alt="Screenshot 2023-07-20 at 14 04 31" src="/Users/meijie/Desktop/Patient_trajectory_public-main/new_all.png">-->

An example with filter function, only show the progress information(cropped due to space constraints, get it by running "trajectory_filter.html" under "Visualization" folder):
<img width="1282" alt="github_progress" src="https://github.com/rtg-wispermed/Patient_trajectory_public/assets/52000882/0f8fa01d-fa8a-4d1d-a44d-d6d0b7929763">


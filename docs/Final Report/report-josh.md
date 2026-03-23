Joshua – Data Retrieval 
1. Plant Data Structure

(Explain how plant data and ideal environmental ranges were stored in the system.)

We will have a single entity list, stored by UUID. It will contain data from both PFAF and the USDA PLANTS database merged into a single table. If the data was supplied by the USDA PLANTS database we will have `moisture_use`, `drought_tolerance`, `precipitation_min` and `precipitation_max` values for moisture, and `moisture_code` from the PFAF database. For lighting we have `shade_tolerance` from the USDA, and `shade_code`, as well as `hardiness_zone` from PFAF. Temperature is given as `min_temp_f` from the USDA and `hardiness_zone` from PFAF. Anything from PFAF will also have `care_requirements`, as well as some other data about `habitats`, `cultivation`, `edible_uses`, and `medicinal_uses`. `attributions` should always be provided.

2. Data Retrieval Process

(Describe how plant data was retrieved using the plant name as input.)

Data can be returned from the database using either the common plant name (`common_name_primary`), or the scientific name (`scientific_name_primpary`). If we have a match for the user, we can return the moisture, lighting, and temperature data to the LLM for processing.

3. Role in the System

Explain how this data supports the system’s decision  making process and how it is used in the system workflow.


4. Example Data

(Provide a table showing plant profiles and their ideal ranges)

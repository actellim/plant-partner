Joshua – Data Retrieval 

*Needs to be discussed with the team to verify their implementations.*

1. Plant Data Structure

(Explain how plant data and ideal environmental ranges were stored in the system.)

We will have a single table for plant data, stored by UUID. It will contain data from both PFAF and the USDA PLANTS database merged into a single table. If the data was supplied by the USDA PLANTS database we will have `moisture_use`, `precipitation_min` values for moisture, and `moisture_code` from the PFAF database. For lighting we have `shade_tolerance` from the USDA, and `shade_code`. Temperature is given as `min_temp_f` from the USDA and `hardiness_zone` from PFAF. Anything from PFAF will also have `care_requirements`, as well as some other data about `habitats`, `cultivation`, `edible_uses`, and `medicinal_uses`. `attributions` should always be provided.

*speculative, needs discussion:*

We should also have a table for sensor data. Sensor data should be associated with a specific plant species chosen by the user at startup; and each of the users plants should have a specific UUID for matching associated sensor data.

2. Data Retrieval Process

(Describe how plant data was retrieved using the plant name as input.)

Data can be returned from the database using either the common plant name (`common_name_primary`), or the scientific name (`scientific_name_primpary`). If we have a match for the user, we can return the moisture, lighting, and temperature data to the LLM for processing.

The past month of sensor data and the plant species UUID will be returned to the back-end for a given plant UUID when an automated query is conducted. This will then be compared to the plant data via species UUID lookup from our database. 

3. Role in the System

(Explain how this data supports the system’s decision  making process and how it is used in the system workflow.)

Once the user verifies that we have a match for their plant, we provide the LLM with a recommendation, with a summary of the associated sensor data and plant care data. The LLM then produces a response, which we log for debugging/verification/testing purposes. Responses will be stored with a response UUID, the species and plant UUIDs, the time, the programs input data and recommendation, and the model's output. The output is then presented to the user.


4. Example Data

(Provide a table showing plant profiles and their ideal ranges)

## Retrieval-Augmented Generation (RAG)

### Introduction

Part of the reason that Large Multimodal Models (LMMs) have proven to be so robustly useful is their ability to think creatively. This has also, unfortunately, been one of their major pain points for integration. Largely documented as the hallucination problem, if a model doesn't know an answer it will often make one up[citation needed]. Fairly early in the Large Language Model (LLM) era (the era preceeding the current LMM reasoning era), the technique of Retreival Augmented Generation (RAG) was purposed to address this failure case. As RAG techniques have improved, models have become more reliable and useful at tasks that can be clearly defined in documentation. 

### RAG in Prior Research

Researchers have developed numerous techniqes to ground models. The original technique was purposed shortly after "The ChatGPT Moment" in 2022, and there have been several advancements in the field as model architectures have matured (as there will be many more!). This was originally achieved by giving models access to documents directly in their context window[original facebook research], however more modern methods involve the use of databases[microsoft research] and tools[mit paper] that either automatically retrieve relevant information or allow the model to retrieve it on their own through the use of command line tools. This has increased model accuracy and reduced hallucinations in the current generation of models, improving their reliability in low-stakes production environments. 

### Data Sources for Retrieval

For our project we chose to use the database approach, as there were existing plant databases that gave us the atomic information we would need for various species of plant. By giving our model endpoint specific data on the light, moisture, temperature, and humidity requirements of a plant, and the sensor data from another database that we plan to store the sensor data in, we expect to be able to host a small model locally that will provide actionable feedback to users. We have elected to use a pre-existing database from perenual and pass that data along with our sensor database data to our model.

### Proposed RAG Pipeline for This Project

#### Input

- Plant species
- Environmental sensor data
- Query from user application

#### Retrieval Step

The model will be given sensor data for the last 24 hours from our database, and grounding data from the perenual database, the plant species.

#### Generation Step

The model will then be asked to interpret this data and provide a response for users to better care for their plants or encourage them to keep taking excellent care of their plants.

### Citation and Traceability Strategy

If deemed necessary we could ask the model to cite sensor data in its user response. We should also keep a log in our database of data sent to model and the model response for potential debugging later. 

### Evaluation Strategy

We will run test cases by giving the model stubbed sensor data, having it compare to the perenual data for a few given species, and capturing/logging/monitoring the output. 

### Barriers and Risks

- Incomplete datasets
- Retrieval errors
- Data quality issues
- Incomplete sensor data

### Summary

RAG will take our project from "uses AI" to "integrates AI in a reliable way." By incorporating sensor data, known optimal plant conditions, and long term monitoring with LLMs, we can create an engaging user experience that will make interacting with houseplants more fufilling and engaging. Our project aims to give plants a voice that we can direct to a users phone, increasing plant integration into daily life. 

### References

[List peer-reviewed references in IEEE format]


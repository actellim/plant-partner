## Retrieval-Augmented Generation (RAG)

### Introduction

Part of the reason that Large Multimodal Models (LMMs) have proven to be so robustly useful is their ability to generate novel and contextually complex content. This has also, unfortunately, been one of the major challenges for integration. Largely documented as the hallucination problem, if a model doesn't know an answer it will often fabricate plausible but ultimately incorrect information[1]. In 2020 the initial technique of Retrieval Augmented Generation (RAG) was proposed to address this failure case[2]. As RAG techniques have improved, models have become more reliable and useful at tasks that can be clearly defined in documentation. 

### RAG in Prior Research

Researchers have developed numerous techniques to ground models. The original technique was proposed before the public release of large-scale generative models in late 2022, and there have been several advancements in the field as model architectures have matured. This was originally achieved by giving models access to documents directly in their context window[2] by using embeddings to search across documents, however more modern methods evolved the use of databases[3], and environments[4] that allow autonomous retrieval through the use of tools and recursive tool use, respectively. This has increased model accuracy and reduced hallucinations in the current generation of models, improving their reliability in low-stakes production environments. 

### Data Sources for Retrieval

For our project we chose to use the database approach, as there were existing plant databases that gave us the granular data we would need for various species of plant. By giving our model endpoint specific data on the light, moisture, temperature, and humidity requirements of a plant, and the sensor data from another database that we plan to store the sensor data in, we expect to be able to host a small model locally that will provide actionable feedback to users. 

For our grounding data, we will not be using vector search, instead we utilize symbolic retrieval[3] allowing for direct numerical comparison specified by SQL queries, a task not well suited for vector search. We utilize a pre-existing relational database from Perenual to serve as our symbolic truth[3]. By passing that data, along with our sensor telemetry database data, to our model we perform a validation check[1] to ensure the model's generation is grounded in the current physical state.

### Proposed RAG Pipeline for This Project

#### Input

- Plant species
- Environmental sensor data
- Query from user application

#### Retrieval Step

Our model, a Reasoning Large Language Model, will be given data that is programmatically retrieved via SQL lookup using Symbolic Retrieval[3] from the Perenual database, as well as the plant species.

#### Generation Step

The model will then be asked to cross-reference the data provided by the sensors with the gold-standard plant condition from the Perenual database to identify any deltas. The model then provides a response for users, in the context of the deltas, to optimize their plant care routines, or reinforce existing healthy maintenance protocols.

#### Conversational Step

The RLLM Agent will be given a tool to use for future conversational turns that will allow it access to lookup arbitrary information in the sensor database. This will further enhance its usefulness and ability to diagnose, troubleshoot, and respond to user queries.

### Citation and Traceability Strategy

If deemed necessary we could ask the model to cite sensor data in its user response. We will also keep a log in the database of data sent to model and the model's response for potential debugging and auditing in the future. 

### Evaluation Strategy

We will run test cases by giving the model stubbed sensor data, having it compare to the Perenual data for a few given species, and capturing/logging/monitoring the output. This output will then be evaluated against the data provided for optimal, sub-optimal, and detrimental plant care cases and evaluated primarily for semantic accuracy (i.e. did the model provide a valid recommendation for plant care). 

### Barriers and Risks

- Incomplete datasets
- Retrieval errors
- Data quality issues
- Incomplete sensor data
- Latency due to model inference times
- Context Window Management
- State Maintance

### Summary

The integration of RAG with LLMs elevates this into a robust, context-aware conversational plant system. By incorporating sensor data, known optimal plant conditions, and long term monitoring with LLMs, we can create an novel user experience that will make interacting with houseplants more fulfilling and interactive. Ultimately the project aims to develop a bio-digital interface that gives plants a 'voice' that can be directed to a users mobile device.

### References

[1] E. Collini, F. I. Kurniadi, P. Nesi, and G. Pantaleo, "Context-Aware Retrieval Augmented Generation Using Similarity Validation to Handle Context Inconsistencies in Large Language Models," *IEEE Access*, vol. 13, pp. 170065-170080, 2025. doi: 10.1109/ACCESS.2025.11180037.

[2] P. Lewis *et al.*, "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," in *Advances in Neural Information Processing Systems*, vol. 33, 2020, pp. 9459–9474. [Online]. Available: https://proceedings.neurips.cc/paper/2020/file/6b493230205f780e1bc26945df7481e5-Paper.pdf

[3] C. Hu *et al.*, "ChatDB: Augmenting LLMs with Databases as Their Symbolic Memory," *arXiv preprint arXiv:2306.03901*, 2023. [Online]. Available: https://arxiv.org/abs/2306.03901

[4] A. L. Zhang, T. Kraska, and O. Khattab, "Recursive Language Models," *arXiv preprint arXiv:2512.24601*, 2025. [Online]. Available: https://arxiv.org/abs/2512.24601

# Joshua – Data Retrieval and Backend Logic

## Introduction
A significant challenge in integrating Large Language Models (LLMs) into specialized domains like horticulture is the "hallucination" problem, where models fabricate plausible but incorrect information[1]. To mitigate this, our research focused on Retrieval-Augmented Generation (RAG). While early RAG research focused on vector-based search[2], more recent advancements have proven the efficacy of "Symbolic Retrieval," where models are augmented with relational databases to serve as a structured, deterministic memory[3]. 

For this project, we implemented a symbolic retrieval architecture that grounds the LLM in real-world sensor telemetry and established botanical thresholds. By providing the model with a "gold-standard" care profile retrieved via SQL, we perform a validation check[1] that ensures the model's care recommendations are physically grounded. Furthermore, we integrated a multi-user awareness layer, allowing the system to adjust its conversational complexity based on the user's self-identified "audience level" (e.g., beginner vs. expert).

## Work Done
The core of the retrieval system involved merging disparate datasets from the USDA PLANTS and Plants For A Future (PFAF) databases into a unified SQLite repository. This unified plant table contains consolidated data indexed by UUID, merging USDA fields like `moisture_use`, `precipitation_min`, and `shade_tolerance` with PFAF data such as `moisture_code`, `shade_code`, and `hardiness_zone`. Records sourced from the PFAF database also include qualitative care data, including `care_requirements`, `habitats`, `cultivation` details, and `edible_uses`, ensuring each entry contains mandatory source attributions and comprehensive physiological thresholds.

Beyond species data, the schema includes a relational structure to support time-series environmental telemetry and user management. Sensor data is associated with specific plant species selected by the user, with each individual plant instance assigned a unique UUID to link it to its historical readings. I also implemented an `App_User` table to store experience levels and a dedicated logging table for LLM interactions. This logging table captures the precise payloads sent to the model—including sensor states, alerts, and history—alongside the generated response to ensure a complete audit trail for system verification.

The data retrieval process I developed allows the system to query the database using either the plant's common name or its primary scientific name. Once a match is identified, the backend retrieves the relevant moisture, lighting, and temperature thresholds. During an automated monitoring cycle, the system fetches the historical sensor data for a given plant UUID and performs a direct numerical comparison against the corresponding species data using a species UUID lookup. This comparison allows our deterministic software engineering safeguards to identify alerts before the LLM is even invoked.

Once a species match and sensor status are verified, the system compiles a structured RAG payload to provide the LLM with a grounded recommendation context. The LLM then produces a response, which is logged with a unique response UUID, the associated identifiers, the original input data, and the model's final output. This ensures that the advice presented to the user is verified against our deterministic thresholds and that the LLM's output is logged for later validation.

## References
[1] E. Collini, F. I. Kurniadi, P. Nesi, and G. Pantaleo, "Context-Aware Retrieval Augmented Generation Using Similarity Validation to Handle Context Inconsistencies in Large Language Models," *IEEE Access*, vol. 13, 2025.

[2] P. Lewis *et al.*, "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," in *Advances in Neural Information Processing Systems*, vol. 33, 2020.

[3] C. Hu *et al.*, "ChatDB: Augmenting LLMs with Databases as Their Symbolic Memory," *arXiv preprint arXiv:2306.03901*, 2023.
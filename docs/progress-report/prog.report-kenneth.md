# Large Language Models (LLMs) in the Proposed System

## 1. Introduction
This section explores the role of Large Language Models (LLMs) in the proposed system and their potential use in generating explanations and recommendations for plant care.

Large Language Models (LLMs) are AI systems that can generate human like text from structured input. In the proposed plant care system, the LLM does not collect sensor data or decide whether a plant needs water or environmental changes. All analysis and decision making happen in the backend system. The LLM is only used after those decisions are made. Its purpose is to turn structured results into clear explanations so users understand why a recommendation was given.

LLMs are usually deployed as external services that are accessed through APIs instead of being built directly into the main system logic [1]. This keeps the system organized and easier to manage. By separating the decision logic from the explanation component, the plant care system stays reliable while still providing easy to understand responses.


## 2. Use of LLMs in Prior Research
Overview of how LLMs have been used in:
- Decision support systems
- Recommendation systems
- Knowledge-based applications

LLMs are often used in systems that help users make decisions or understand recommendations. In large systems, models are handled through structured request systems that manage incoming requests, processing steps, and system resources [1]. It allows the AI component to scale properly without affecting the rest of the application.

In IoT systems, RESTful APIs are commonly used to connect sensors, databases, and other services [2]. These systems are built in layers. First, data is collected. Then it is processed. Finally, results are shared through APIs. The SEMAR IoT platform follows this approach by receiving sensor data, processing it internally, and exposing results through REST services [3].

In both cases, intelligent components are added after structured processing is complete. They support the system by explaining or interpreting results, but they do not replace core logic. This same approach is used in the plant care system.



## 3. Risks and Challenges of LLMs
- Hallucinations
- Overconfidence in generated responses
- Lack of grounding in factual data
- Privacy and data concerns

Using LLMs brings some risks. One common issue is hallucination. The model might generate information that sounds correct but is not fully supported by the actual data.

Another concern is overconfidence. The model may produce explanations that sound very certain, even when the measured values are close to decision limits.

Grounding is also important. If the LLM is not given clear and structured input, it might rely on general plant knowledge instead of the specific sensor readings stored in the system. That could create mismatches between calculated results and explanations.

There are also a system level concerns. Since the LLM is accessed through an external API [1], explanation generation depends on network connection and service availability. If the service is slow or temporarily unavailable, response time may increase.


## 4. Mitigation Strategies from Literature
- Grounding responses using external data
- Rule-based constraints
- Output validation
- Handling uncertainty

To reduce these risks, the system must control how the LLM is used. In IoT platforms like SEMAR, sensor data is validated and processed before being shared with other services [3]. The plant care system follows the same idea. All recommendations are calculated first, using rule based comparisons between sensor readings and plant specific ideal ranges.

The LLM only receives a structured summary that already contains the final decision. It does not calculate thresholds or determine plant health. This keeps the decision logic safe and predictable.

The system can also check whether the explanation matches the structured data. If there is a mismatch, a simple predefined explanation can be used instead.

Handling uncertainty clearly is also important. If values are close to limits, the explanation can reflect that instead of making absolute statements. RESTful API frameworks emphasize proper validation and structured communication for reliability [2], and this principle also applies here.


## 5. Proposed Role of LLMs in This Project
- Generating natural-language explanations
- Supporting user understanding
- Avoiding use as a primary data source

In this project, the LLM is used only to generate explanations. The backend system collects sensor readings, retrieves plant profile data, and compares measured values with ideal ranges. Based on this comparison, it decides whether watering or environmental adjustment is needed.

After that decision is made, the system creates a structured summary containing the plant name, measured values, ideal ranges, and recommended action. This summary is sent to the LLM through an API request. The LLM then generates a clear explanation to help the user understand the recommendation.

The LLM does not access the database directly, change decisions, or serve as the main knowledge source. It simply translates structured results into understandable language.


## 6. Barriers and Integration Risks
- Reliability concerns
- Evaluation challenges
- Dependency on external models

Even with careful design, some challenges remain. Because the LLM is accessed as an external service [1], explanation generation depends on network reliability and system availability. Delays may occur if the service experiences heavy load.

Testing explanation quality is also harder than testing numeric calculations. Backend logic can be checked using fixed rules, but natural language responses must be reviewed to ensure they match the structured input.

Dependency on external services adds operational risk. RESTful IoT systems highlight the importance of secure and well managed API communication [2]. To reduce risk, the plant care system should include fallback responses. If the LLM is unavailable, a simple template based explanation can be returned without affecting the main functionality.

Keeping the LLM separate from the core logic, can make these risks manageable.


## 7. Summary
Summary of why LLMs are used in a limited and controlled manner in this project.

LLMs can improve user experience by generating clear explanations in recommendation systems. However, they introduce risks such as hallucination, overconfidence, grounding issues, and service dependency.

Research on scalable LLM services and layered IoT architectures shows that intelligent components should be integrated through structured APIs and modular design [1]–[3]. The proposed plant care system follows this approach. All decisions are made using deterministic backend logic, and the LLM is used only to explain the results.

This controlled integration keeps the system reliable while improving clarity for users.


## References
[List peer-reviewed references in IEEE format]

[1] J. Hu, J. Xu, Z. Liu, Y. He, Y. Chen, H. Xu, J. Liu, J. Meng, B. Zhang, S. Wan, G. Dan, Z. Dong, Z. Ren, C. Liu, T. Xie, D. Lin, Q. Zhang, Y. Yu, H. Feng, X. Chen, and Y. Shan, “DeepServe: Serverless Large Language Model Serving at Scale,” in Proceedings of the 2025 USENIX Annual Technical Conference (ATC), Boston, MA, USA, Jul. 2025, pp. 57–73.

[2] E. Mabotha, N. E. Mabunda, A. Ali, and B. Khan, “Exploring dynamic RESTful API implementation in IoT environments using Docker,” Scientific Reports, vol. 15, Art. no. 34267, 2025.

[3] Y. Y. F. Panduman, N. Funabiki, P. Puspitaningayu, M. Kuribayashi, S. Sukaridhoto, and W. C. Kao, “Design and Implementation of SEMAR IoT Server Platform with Applications,” Sensors, vol. 22, no. 17, Art. no. 6436, 2022.

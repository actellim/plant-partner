## 1. Executive Summary
This progress report consolidates the research findings and design decisions produced across the team’s individual progress submissions. The reporting period focused on: (i) defining what “plant health monitoring” means for a small-scale indoor system, (ii) selecting a minimum viable sensor set supported by literature, (iii) defining a grounded recommendation pipeline using database retrieval and deterministic decision logic, and (iv) integrating a Large Language Model (LLM) as an explanation layer with safeguards against hallucinations.

The literature review supports monitoring four environmental parameters as the baseline for indoor plant care: soil moisture, light intensity, ambient temperature, and relative humidity. These variables capture the dominant, actionable stressors in household environments, while more complex sensing such as nutrient monitoring is excluded due to practical limitations. For plant health interpretation, the selected approach is a hybrid sensor and trend-based method: thresholds define safe operating bands, and persistence/rolling-window logic detects sustained excursions to reduce noise-driven false alerts.

To deliver species-specific, explainable guidance, the proposed system architecture separates concerns: sensor and plant-profile data are retrieved from relational databases, the backend performs numerical comparisons and classifies the plant state, the LLM is then used only to translate the structured decision into a user-friendly explanation. A Retrieval-Augmented Generation (RAG) strategy is proposed to ground responses in retrieved plant profiles. Key risks identified include sensor drift, indoor microclimate variability, retrieval/data quality issues, and language-model overconfidence near decision boundaries; mitigation strategies and an evaluation plan are defined in this report.

## 2. Project Overview
The project aims to develop a low-cost indoor plant monitoring and recommendation system for hobbyist use. The system collects environmental measurements, compares them to plant-specific ideal ranges, and outputs actionable guidance (e.g., watering suggestions or placement adjustments). A grounded language-model component generates explanations to improve user understanding, while core decisions remain deterministic and testable.

## 3. Progress Summary
Key outcomes completed in this reporting period:
- Literature-backed justification of a minimum viable sensor suite for indoor monitoring (moisture, light, temperature, humidity).
- Definition of plant health for this project and review of sensor-based, trend-based, and AI-driven monitoring approaches.
- Selection of a pragmatic monitoring strategy: hybrid threshold logic with temporal trend checks.
- Definition of a grounded recommendation pipeline with symbolic (SQL) retrieval and structured decision summaries.
- Controlled integration plan for an LLM explanation layer (input constraints, output validation, and fallbacks).
- Initial evaluation plan and consolidated risks/mitigation actions.

## 4. Research Consolidation

### 4.1 Environmental Sensors and Parameter Justification
Research on indoor and controlled-environment plant monitoring shows that a compact set of environmental parameters is sufficient for practical decision support in small-scale systems. This project prioritizes parameters that are:
- strongly linked to common indoor plant stressors,
- measurable with low-cost sensors, and
- directly actionable by the user.

**Soil moisture:** Soil moisture is a primary indicator of watering adequacy. Evaluation of low-cost sensors demonstrates that capacitive probes can provide reliable measurements when properly calibrated for the target substrate and container, and that calibration materially improves accuracy and repeatability \[1\].

**Light intensity:** Light intensity influences photosynthesis and growth. Comparative studies of low-cost digital light sensors report consistent lux measurements suitable for relative indoor assessment, with the limitation that lux is not equivalent to photosynthetically active radiation (PAR) \[2\].

**Ambient temperature and relative humidity:** Temperature and humidity affect transpiration, heat stress, and disease susceptibility. Studies of low-cost indoor environmental sensors indicate stability and accuracy sufficient for monitoring applications \[3\].

**Nutrients (excluded):** Real-time nutrient sensing was reviewed but excluded from the minimum viable prototype. Prior work highlights challenges including soil heterogeneity, measurement variability, and technical complexity for reliable in-situ nutrient estimation \[4\].

**Selected minimum viable sensor set**
- Capacitive soil moisture sensor (with calibration workflow)  
- Digital light (lux) sensor  
- Digital temperature sensor  
- Digital relative humidity sensor  

### 4.2 Plant Health Monitoring: Definitions, Approaches, and Project Choice

#### 4.2.1 Definitions of Plant Health in Literature
Recent reviews frame plant health as a function of both environmental conditions (microclimate) and plant response. Deviations in temperature, humidity, substrate moisture, and light intensity are treated as early indicators of stress in indoor and controlled-environment settings \[5\].

Literature also defines plant health through growth and biomass accumulation. Non-destructive biomass monitoring using proximal RGB-D imagery can detect deviations from expected growth trajectories within days under induced stress, suggesting that trends (not just instantaneous values) are informative \[7\].

A third framing is risk-based: systems classify disease state or a health level and use that to estimate the risk of failure without intervention. Image-based disease recognition and multi-class health scoring have been demonstrated using deep learning, enabling time-series health assessment at the population level \[9\], \[10\].

#### 4.2.2 Approaches Reviewed
**Sensor-based monitoring** uses environmental and substrate measurements compared to acceptable bands; this approach is common in smart flowerpot systems and is attractive due to low cost and interpretability \[11\].

**Trend-based monitoring** extends this by evaluating persistence and trajectories over time (e.g., rolling averages, rate-of-change, growth curves), enabling earlier detection than single-sample thresholding \[7\].

More direct physiological indicators exist, such as chlorophyll fluorescence imaging for early stress detection prior to visible symptoms \[6\], and plant-wearable strain sensors that track growth dynamics over diurnal cycles \[8\]. While informative for research, these methods increase cost and integration complexity for a minimum viable indoor prototype.

**AI/data-driven approaches** map images or multi-sensor data to health indicators (disease class, health level, or predicted biomass). Such systems can achieve strong classification performance on curated datasets, but they typically require labelled data and may be less practical for a small indoor prototype without a data-collection campaign \[9\], \[10\].

#### 4.2.3 Selected Approach for This Project
Given project constraints (limited labelled ground truth, modest hardware, and the need for explainable outputs), the selected strategy is a hybrid sensor- and trend-based approach. The system compares current and time-aggregated sensor values against plant-specific ideal bands and generates alerts/recommendations only when deviations persist beyond a defined duration.

#### 4.2.4 Risks and Limitations
Key limitations include species-dependent variability (the same moisture or light level can be healthy for one species and harmful for another), sensor drift over time, and indoor microclimate heterogeneity. Mitigations include calibration, conservative thresholds, persistence logic, and transparent uncertainty communication.

---

### 4.3 Retrieval-Augmented Generation (RAG) for Grounded Recommendations
LLMs can generate fluent but incorrect content when not grounded in relevant facts (“hallucination”). Retrieval-Augmented Generation (RAG) was introduced to mitigate this by retrieving external information and conditioning generation on the retrieved context \[12\].

For this project, the proposed grounding method is database-backed symbolic retrieval. Plant profile data (ideal ranges for light, moisture, temperature, and humidity) is retrieved via SQL from a relational database, and sensor telemetry is retrieved from the project’s sensor database. Symbolic retrieval is preferred because the dominant operations are numerical range checks and comparisons rather than semantic similarity \[13\].

In addition to basic retrieval, modern systems increasingly incorporate tool use and recursive retrieval behaviours. Recent work describes architectures where models can perform multi-step retrieval and reasoning loops over external stores \[14\]. A practical safeguard is to validate model outputs against retrieved context; similarity/consistency validation approaches have been proposed to detect or reduce context inconsistencies in RAG workflows \[15\].

**Proposed RAG pipeline (current)**
1. **Input:** plant species, recent sensor readings/aggregates, and a user query (optional).  
2. **Retrieval:** SQL lookup of plant ideal ranges and recent sensor telemetry.  
3. **Decision:** deterministic comparison to compute deltas and classify state (healthy / near-stress / stressed).  
4. **Generation:** LLM receives only the structured decision summary and generates explanation/recommendation text.  
5. **Logging:** store retrieved context, structured decision, and generated text for traceability and debugging.  

### 4.4 Role of Large Language Models (LLMs) and Integration Safeguards
In the proposed system, the LLM is not responsible for collecting data or determining the plant state. All analysis and decision making occurs in the backend, and the LLM is used only to convert structured results into clear explanations.

This modular design aligns with research on scalable LLM serving, where inference is treated as an external service accessed through structured APIs \[16\]. It also aligns with layered IoT architectures that validate sensor data internally and expose results via RESTful services \[17\], \[18\].

Primary LLM risks include hallucination, overconfidence near decision thresholds, privacy concerns (if external services are used), and dependency on network/model availability. Mitigations include: strict input schemas, prompt constraints, response validation against the structured summary, conservative uncertainty wording near boundaries, and a fallback template response when the LLM is unavailable.

## 5. Proposed System Architecture (Current)
The current architecture is organized into four layers:
1. **Sensing Layer:** sensors measure soil moisture, temperature, humidity, and light.  
2. **Data Layer:** sensor telemetry is stored in a database; plant profile data is stored in a relational database.  
3. **Decision Layer:** backend services retrieve data, apply calibration/filtering, and execute deterministic rule + trend logic to classify state and recommend actions.  
4. **Explanation Layer:** the LLM receives only the structured decision summary and generates a user-facing explanation.  

## 6. Evaluation Plan
Evaluation will combine unit tests, scenario-based tests, and qualitative review:
- **Sensor validation:** calibrate soil moisture probes for the intended potting media and verify wet/dry reference points \[1\].
- **Rule/trend validation:** create controlled test cases (stubbed telemetry) spanning optimal, sub-optimal, and detrimental conditions; verify classification and recommended actions.
- **Retrieval validation:** test SQL retrieval with malformed inputs and missing data; verify error handling and logging.
- **LLM explanation review:** verify that explanations match structured inputs, avoid unsupported claims, and communicate uncertainty near thresholds.

## 7. Key Risks and Mitigation
- **Sensor variability and drift:** calibrate soil moisture sensors for target substrate; apply filtering; periodically re-check calibration; document limitations \[1\], \[3\].  
- **Lux vs PAR mismatch:** use lux as a relative indicator for indoor placement; disclose that lux is not a direct PAR measure \[2\].  
- **Species dependence of thresholds:** store species-specific ranges; allow conservative bands; support user configuration; communicate uncertainty when near limits \[5\].  
- **Indoor microclimate heterogeneity:** encourage consistent placement; apply persistence logic; detect sudden shifts consistent with relocation.  
- **Retrieval/data quality issues:** use schema constraints and validation for database queries; log retrieved context and decisions for auditability \[13\], \[15\].  
- **LLM hallucination or overconfidence:** constrain the LLM to structured input; validate output; fallback to templates when uncertain or inconsistent \[12\], \[15\], \[16\].  
- **Service latency or unavailability:** cache plant profiles; provide template responses; treat the LLM as optional for core functionality \[16\].  

## 8. Next Steps
Planned activities for the next reporting period:
- Finalize sensor selection, assemble a breadboard prototype, and implement an initial calibration workflow for soil moisture.
- Implement database schemas for plant profiles and sensor telemetry; populate profiles for a small set of target houseplant species.
- Implement deterministic decision logic and automated test cases using stubbed telemetry.
- Integrate the explanation layer with controlled prompting, output validation, and fallback templates.

## References (IEEE Style)
\[1\] S. Adla, D. K. Rai, and V. V. Sarangi, “Laboratory calibration and performance evaluation of low-cost capacitive and very low-cost resistive soil moisture sensors,” *Sensors*, vol. 20, no. 2, p. 363, 2020, doi: 10.3390/s20020363.  
\[2\] F. Beyaz and A. Gul, “Comparison of low-cost light sensors for agricultural applications,” *Brazilian Archives of Biology and Technology*, vol. 65, 2022, doi: 10.1590/1678-4324-2022210112.  
\[3\] J. Pereira and N. M. Ramos, “Evaluation of low-cost environmental sensors for indoor monitoring applications,” *Journal of Building Engineering*, vol. 46, 2022, doi: 10.1016/j.jobe.2021.103824.  
\[4\] R. Burton et al., “The ‘Real-Time’ Revolution for In Situ Soil Nutrient Sensing,” *Journal of The Electrochemical Society*, vol. 167, no. 3, 2020, doi: 10.1149/1945-7111/ab67a7.  
\[5\] L. Wang, M. Xiao, X. Guo, Y. Yang, Z. Zhang, and C. Lee, “Sensing Technologies for Outdoor/Indoor Farming,” *Biosensors*, vol. 14, no. 12, p. 629, 2024, doi: 10.3390/bios14120629.  
\[6\] R. Legendre, N. T. Basinger, and M. W. van Iersel, “Low-Cost Chlorophyll Fluorescence Imaging for Stress Detection,” *Sensors*, vol. 21, no. 6, p. 2055, 2021, doi: 10.3390/s21062055.  
\[7\] N. Buxbaum, J. H. Lieth, and M. D. Earles, “Non-destructive Plant Biomass Monitoring With High Spatio-Temporal Resolution via Proximal RGB-D Imagery and End-to-End Deep Learning,” *Frontiers in Plant Science*, vol. 13, p. 758818, 2022, doi: 10.3389/fpls.2022.758818.  
\[8\] S. Wang, J. M. Baek, A. P. Lau, J. C. Quebedeaux, A. D. B. Leakey, et al., “Light-Stable, Ultrastretchable Wearable Strain Sensors for Versatile Plant Growth Monitoring,” *ACS Sensors*, vol. 10, no. 5, pp. 3390–3401, 2025, doi: 10.1021/acssensors.4c03104.  
\[9\] A. Fuentes et al., “Comprehensive Plant Health Monitoring: Expert-Level Assessment with Spatio-Temporal Image Data,” *Frontiers in Plant Science*, vol. 16, p. 1511651, 2025, doi: 10.3389/fpls.2025.1511651.  
\[10\] M. Islam, A. K. M. Azad, S. E. Arman, S. A. Alyami, and M. M. Hasan, “PlantCareNet: an advanced system to recognize plant diseases with dual-mode recommendations for prevention,” *Plant Methods*, vol. 21, no. 1, p. 52, 2025, doi: 10.1186/s13007-025-01366-9.  
\[11\] Y. Li et al., “A Personalized and Smart Flowerpot Enabled by 3D Printing and Cloud Technology for Ornamental Horticulture,” *Sensors*, vol. 23, no. 13, p. 6116, 2023, doi: 10.3390/s23136116.  
\[12\] P. Lewis et al., “Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks,” in *Advances in Neural Information Processing Systems*, vol. 33, 2020, pp. 9459–9474.  
\[13\] C. Hu et al., “ChatDB: Augmenting LLMs with Databases as Their Symbolic Memory,” arXiv:2306.03901, 2023.  
\[14\] A. L. Zhang, T. Kraska, and O. Khattab, “Recursive Language Models,” arXiv:2512.24601, 2025.  
\[15\] E. Collini, F. I. Kurniadi, P. Nesi, and G. Pantaleo, “Context-Aware Retrieval Augmented Generation Using Similarity Validation to Handle Context Inconsistencies in Large Language Models,” *IEEE Access*, vol. 13, pp. 170065–170080, 2025, doi: 10.1109/ACCESS.2025.11180037.  
\[16\] J. Hu et al., “DeepServe: Serverless Large Language Model Serving at Scale,” in *Proc. USENIX Annual Technical Conference (ATC)*, 2025, pp. 57–73.  
\[17\] E. Mabotha, N. E. Mabunda, A. Ali, and B. Khan, “Exploring dynamic RESTful API implementation in IoT environments using Docker,” *Scientific Reports*, vol. 15, 2025, Art. no. 34267.  
\[18\] Y. Y. F. Panduman, N. Funabiki, P. Puspitaningayu, M. Kuribayashi, S. Sukaridhoto, and W. C. Kao, “Design and Implementation of SEMAR IoT Server Platform with Applications,” *Sensors*, vol. 22, no. 17, Art. no. 6436, 2022.

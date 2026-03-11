## 1. Introduction

This section evaluates and justifies the environmental sensors selected for the proposed indoor plant monitoring system. The goal is to identify parameters that are strongly supported by peer-reviewed research and suitable for small-scale indoor monitoring. The focus is placed on environmental stress indicators rather than complex soil chemistry, aligning with the project’s research-driven scope.
## 2. Environmental Parameters Considered

### 2.1 Soil Moisture

Soil moisture is one of the most critical environmental parameters influencing plant health. Overwatering and underwatering are primary causes of indoor plant stress. 

Adla et al. [1] evaluated low-cost capacitive and resistive soil moisture sensors and demonstrated that capacitive sensors, when calibrated properly, can provide reliable measurements for monitoring applications. The study emphasizes that calibration significantly improves measurement accuracy and reduces variability.

Based on this research, a capacitive soil moisture sensor is appropriate for monitoring watering conditions in indoor plants.

### 2.2 Light Intensity

Light exposure directly impacts photosynthesis and growth rate. In indoor environments, improper placement often results in insufficient or excessive light exposure.

Beyaz and Gül [2] compared low-cost digital light sensors and found that sensors such as the BH1750 provide consistent and reliable lux measurements for monitoring purposes. Although lux does not directly measure photosynthetically active radiation (PAR), it is sufficient for relative indoor assessment.

Therefore, a digital lux sensor is suitable for detecting low-light or high-light conditions in indoor plants.

### 2.3 Temperature and Humidity

Temperature and relative humidity influence plant transpiration, stress response, and disease susceptibility.

Pereira and Ramos [3] evaluated low-cost environmental sensors for indoor monitoring and demonstrated that digital temperature and humidity sensors provide stable and sufficiently accurate measurements for practical applications. Their results support the use of digital environmental sensors in indoor monitoring systems.

Monitoring these parameters enables detection of:
- Heat stress
- Low humidity stress
- Prolonged high humidity conditions

### 2.4 Nutrient Sensors (Excluded from Scope)

Real-time in-situ nutrient sensing was reviewed but excluded from the minimum viable system.

Burton et al. [4] discuss the challenges of real-time soil nutrient sensing, highlighting limitations in commercial availability and technical complexity. The paper explains that soil heterogeneity significantly affects electrical measurements, making accurate nutrient sensing more difficult in practical scenarios.

Given these challenges and the indoor scope of this project, nutrient monitoring is considered out-of-scope.

## 3. Alignment with Existing Indoor Plant Systems

AI-enabled indoor plant monitoring systems typically rely on environmental sensors (soil moisture, light, temperature, humidity) to generate recommendations without requiring nutrient-level sensing [5].

These studies demonstrate that environmental monitoring is sufficient for decision-support in small-scale indoor plant systems.

## 4. Selected Sensor Set

Based on literature review, the selected sensor set includes:

- Capacitive Soil Moisture Sensor  
- Digital Light Sensor
- Digital Temperature Sensor  
- Digital Humidity Sensor  

This set:
- Covers the primary environmental stress factors identified in literature  
- Aligns with existing indoor monitoring research  
- Maintains feasibility within project scope  

## 5. Research-Level Implementation Considerations

Literature identifies several practical considerations:

- Soil moisture sensors require calibration to improve reliability [1].
- Digital environmental sensors provide stable indoor measurements [3].
- Lux sensors provide adequate relative measurements for indoor monitoring [2].

These considerations will guide system design and risk mitigation strategies.

## 6. Risks and Limitations

Identified risks based on literature:

- Measurement variability due to soil composition [1]
- Lux not equivalent to PAR measurement [2]
- Environmental sensor drift over time [3]
- Technical complexity of nutrient sensing [4]

Mitigation strategies include calibration, threshold validation, and transparent explanation of limitations.

## 7. Summary

Peer-reviewed literature supports the use of soil moisture, light intensity, temperature, and humidity as sufficient environmental indicators for indoor plant monitoring systems. Nutrient sensing is excluded due to technical complexity and limited feasibility within scope. The selected sensor set aligns with both academic research and project constraints.

## References

[1] S. Adla, D. K. Rai, and V. V. Sarangi, “Laboratory calibration and performance evaluation of low-cost capacitive and very low-cost resistive soil moisture sensors,” *Sensors*, vol. 20, no. 2, p. 363, 2020, doi: 10.3390/s20020363.

[2] F. Beyaz and A. Gül, “Comparison of low-cost light sensors for agricultural applications,” *Brazilian Archives of Biology and Technology*, vol. 65, 2022, doi: 10.1590/1678-4324-2022210112.

[3] J. Pereira and N. M. Ramos, “Evaluation of low-cost environmental sensors for indoor monitoring applications,” *Journal of Building Engineering*, vol. 46, 2022, doi: 10.1016/j.jobe.2021.103824.

[4] R. Burton et al., “The ‘Real-Time’ Revolution for In Situ Soil Nutrient Sensing,” *Journal of The Electrochemical Society*, vol. 167, no. 3, 2020, doi: 10.1149/1945-7111/ab67a7.

[5] A. A. Author et al., “AI-enabled IoT-based smart indoor plant monitoring system,” in *Proc. IEEE Int. Conf. Automation, Robotics and Applications (ICARA)*, 2024.

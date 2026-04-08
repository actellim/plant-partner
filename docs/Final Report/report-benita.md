# Benita – Sensor Simulation

## 1. Sensor Data Generation

Since the project is research-based and no physical prototype was implemented, environmental sensor data was **simulated** to represent realistic indoor plant conditions. The parameters used in the simulation were **soil moisture, light intensity, temperature, and relative humidity**, as these were identified in the literature review as the most relevant environmental indicators for indoor plant monitoring [1]–[3].

The simulated values were based on typical indoor environmental ranges and plant care needs. For example, soil moisture values were adjusted to represent dry, optimal, and overwatered conditions, while light intensity values reflected low-light and well-lit indoor spaces. Temperature and humidity values were varied to represent common indoor fluctuations. 

This allowed the frontend prototype to behave as if real sensors were connected, making it possible to test how environmental input would move through the system and support recommendation generation without requiring actual hardware.

## 2. Simulation Scenarios

To demonstrate system behavior, three main scenarios were created:

- **Healthy Condition**  
  All environmental parameters remain within expected ranges for the plant. In this case, the system should recognize that the plant is in a stable state and return little or no corrective action.

- **Slightly Stressed Condition**  
  One or more parameters slightly deviate from the preferred range, such as lower light exposure or slightly dry soil. In this case, the system should generate mild and actionable suggestions, such as adjusting placement or watering.

- **Stressed Condition**  
  Multiple parameters fall outside acceptable ranges, such as very dry soil combined with higher temperature. In this case, the system should return clearer recommendations indicating that user intervention is needed.

These scenarios were used to show how the system responds to different plant conditions in a structured and understandable way.

## 3. Example Sensor Values

Due to time constraints and the incomplete prototype stage, a finalized table of exact sensor values is still under development. However, representative value ranges were considered during simulation:

- **Soil Moisture:** low (dry) to high (saturated)
- **Light Intensity:** low indoor lighting to bright indirect light
- **Temperature:** typical indoor range (approximately 18°C–30°C)
- **Humidity:** low to moderate indoor humidity levels

These ranges were sufficient for testing the frontend simulation and demonstrating how different conditions would be interpreted by the system. A more structured numerical table can be added later if the prototype is extended further.

## 4. Role in the System

The simulated sensor data replaces real-time sensor input and acts as the **primary environmental input** to the system pipeline. These values are passed into the processing layer, where they are combined with plant-specific information retrieved through the RAG component.

The AI model then interprets the simulated environmental conditions and generates plant care recommendations. This allows the system to demonstrate its sensing-to-decision workflow even in the absence of physical hardware.

Overall, this approach validates the core logic of the monitoring system while remaining consistent with the project scope. It also reflects one of the project’s key design choices: the system does not rely entirely on the language model for core decisions, but instead uses structured environmental input to support reliable recommendations.

## References

[1] S. Adla, D. K. Rai, and V. V. Sarangi, “Laboratory calibration and performance evaluation of low-cost capacitive and very low-cost resistive soil moisture sensors,” *Sensors*, vol. 20, no. 2, p. 363, 2020, doi: 10.3390/s20020363.

[2] F. Beyaz and A. Gül, “Comparison of low-cost light sensors for agricultural applications,” *Brazilian Archives of Biology and Technology*, vol. 65, 2022, doi: 10.1590/1678-4324-2022210112.

[3] J. Pereira and N. M. Ramos, “Evaluation of low-cost environmental sensors for indoor monitoring applications,” *Journal of Building Engineering*, vol. 46, 2022, doi: 10.1016/j.jobe.2021.103824.

[4] A. A. Author et al., “AI-enabled IoT-based smart indoor plant monitoring system,” in *Proc. IEEE Int. Conf. Automation, Robotics and Applications (ICARA)*, 2024.

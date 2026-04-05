# Benita – Sensor Simulation

## 1. Sensor Data Generation

Since the project is research-based and no physical prototype was implemented, environmental sensor data was **simulated to replicate realistic indoor plant conditions**. The parameters considered were **soil moisture, light intensity, temperature, and relative humidity**, as these are widely supported in literature for indoor plant monitoring.

The simulated data was generated using predefined value ranges based on typical indoor environments and plant care requirements. For example, soil moisture values were varied to represent dry, optimal, and overwatered conditions, while light intensity values reflected low-light and well-lit indoor spaces. Temperature and humidity values were adjusted to represent common indoor fluctuations.

This approach allowed the system to behave as if real sensors were connected, enabling testing of the decision-making pipeline without requiring hardware implementation.

## 2. Simulation Scenarios

To demonstrate system behavior, three main scenarios were defined:

- **Healthy Condition**  
  All environmental parameters fall within optimal ranges for the plant. The system should recognize this state and provide minimal or no corrective recommendations.

- **Slightly Stressed Condition**  
  One or more parameters slightly deviate from optimal values, such as low light or slightly dry soil. The system should generate mild, actionable suggestions such as adjusting placement or watering.

- **Stressed Condition**  
  Multiple parameters fall outside acceptable ranges, such as very dry soil and high temperature. The system should generate clear recommendations indicating that intervention is required.

These scenarios help evaluate how the system responds to different environmental conditions in a structured manner.

## 3. Example Sensor Values

Due to time constraints and the incomplete prototype stage, a finalized dataset of sensor values is still under development. However, representative value ranges were considered during simulation:

- **Soil Moisture:** low (dry) to high (saturated)
- **Light Intensity:** low indoor lighting to bright indirect light
- **Temperature:** typical indoor range (approximately 18°C–30°C)
- **Humidity:** low to moderate indoor humidity levels

A structured table of exact numerical values will be incorporated in the final version of the prototype to demonstrate system evaluation across different scenarios.

## 4. Role in the System

The simulated sensor data replaces real-time sensor input and acts as the **primary input to the system pipeline**. These values are passed into the processing layer, where they are combined with plant-specific information retrieved through the RAG component.

The AI model then interprets the simulated environmental conditions and generates recommendations for plant care. This allows the system to demonstrate its full functionality—from sensing to decision-making—even in the absence of physical hardware.

This approach ensures that the **core logic of the system is validated**, while keeping the project aligned with its research-focused scope.

## Managerial Process Plans.

### Start-up Plan.

#### Estimation Plan. 
The project is planned for a total duration of 10 weeks, aligned with the Unified Process workflows already defined for this course project. The estimate is based on expert judgment and analogy with previous student software projects of similar scope, and it is expressed primarily in time (person-hours) rather than money because this is a course project. The work is divided into requirements, analysis, design, implementation, and testing, and each workflow has clear deliverables (use cases, architecture/design artifacts, a working prototype, and a tested final system). To reduce schedule risk, the plan includes a buffer by completing integration early and reserving the last phase for testing, fixes, and documentation polishing.

#### Staffing Plan. 
The project will be completed by a four-member team. To keep responsibilities clear and prevent overlap, each member will have a primary role and a secondary support role:

- Project Coordinator / Integration Lead: manages weekly planning, ensures milestones are met, and owns system integration.
- Hardware & Sensor Lead: responsible for Raspberry Pi setup, wiring, sensor reading code, calibration approach, and reliability checks.
- Backend & Data Lead: responsible for the API, database schema, plant profile storage/retrieval, and recommendation logic.
- Frontend & Documentation Lead: responsible for the UI/dashboard, clarity of “what to do” outputs, and maintaining the written deliverables.

All members participate in testing and review. If a team member becomes unavailable, the secondary support role ensures coverage so that critical tasks (sensor data pipeline, backend API, and UI) can still progress.

#### Resource Acquisition Plan. 
The project requires basic hardware for data collection and standard software development tools. Hardware includes a Raspberry Pi (or equivalent), a soil moisture sensor (preferably capacitive), a temperature/humidity sensor, and a light sensor. Optional sensors such as EC (nutrient proxy) and pH may be added if time allows, but they are not required for the minimum viable system. Additional items include a breadboard, resistors (if needed), and a stable power supply.

Software resources include Git and a Git hosting platform for version control, a code editor (e.g., VS Code), and a lightweight database. The backend will be implemented in Python, and the project will maintain clear setup instructions so the system can be run on another machine.

#### Project Staff Training Plan.
No formal external training is required, but the team will complete targeted onboarding during Week 1. This includes learning sensor interfacing basics (GPIO/I2C), reading and validating sensor data, and establishing a shared coding standard for the repository. The team will also review how to structure plant profiles and how to convert raw readings into actionable recommendations. Any unfamiliar tools (e.g., Markdown documentation, Git workflow, or simple API development) will be learned through small prototypes early, before the main build begins.

### Work Plan.

#### Work Activities and Schedule Allocation.
The work is organized into five workflows across 10 weeks:

- Week 1 (Requirements): finalize scope, define plant species input method, define sensor list, write use cases and acceptance criteria.
- Weeks 2–3 (Analysis): define system architecture, define data model for plant profiles, define recommendation rules and failure cases.
- Weeks 4–5 (Design): design the API endpoints, database schema, UI wireframes, and hardware/software integration plan; create a test plan for sensors and recommendations.
- Weeks 6–8 (Implementation): implement sensor reading and logging, backend API and recommendation engine, plant profile database integration, and UI/dashboard; start integration early and iterate.
- Weeks 9–10 (Testing & Finalization): perform end-to-end testing, verify recommendations against plant profiles, fix defects, finalize documentation, and prepare the final demo.

#### Resource Allocation. 
Team members will work in parallel but integrate continuously. The Hardware & Sensor Lead will provide stable sensor readings and a documented interface (e.g., JSON payload format) so the Backend & Data Lead can implement the API and logic without waiting for the UI. The Frontend & Documentation Lead will build the dashboard using mock data first and then switch to real API calls once available. The Project Coordinator / Integration Lead will ensure that all components are merged frequently and will manage integration milestones to prevent “last week integration” problems.

Weekly coordination will include a short team meeting to confirm progress, update tasks, and identify blockers. Task tracking will be done using Git issues (or an equivalent board).

#### Budget Allocation. 
Because this is a student project, the budget is mainly limited to low-cost sensors and basic electronics accessories. The plan is to reuse any available lab equipment and purchase only essential components. The minimum hardware set is kept intentionally small (Raspberry Pi + moisture + temperature/humidity + light) so the project remains feasible even if optional sensors (EC/pH) are not acquired or are unreliable. Any costs will be tracked and kept minimal, and the software stack will use free/open-source tools.

### Control Plan. 
Project control will be handled through milestone-based tracking and strict version control practices. Each workflow has defined outputs (requirements artifacts, architecture and data model, design artifacts, working prototype, and tested system). Changes to scope must be agreed upon by the full team and only accepted if they do not threaten the schedule.

All code and documentation changes will be made through Git commits, and major changes will be made on feature branches and merged via pull requests with at least one reviewer. The integration lead will ensure that the main branch remains buildable and that unfinished work is isolated to branches. Weekly checkpoints will confirm that progress matches the schedule and that the project remains aligned with the stated objectives.

### Risk Management Plan. 
Key risks and mitigation strategies are as follows:

- Sensor inaccuracy or instability: mitigate by using a capacitive moisture sensor, validating readings over time, and documenting calibration assumptions. Implement sanity checks (out-of-range detection) to prevent bad recommendations.
- Data availability for species-specific guidance: mitigate by using a plant profile dataset that can be downloaded or curated, and limiting the first release to a defined set of plant species with reliable references.
- Scope creep (too many sensors or features): mitigate by defining an MVP (moisture + temperature/humidity + light + species profiles) and treating extra sensors/features as stretch goals.
- Integration delays: mitigate by integrating early (Week 6 onward) and using mocked data so the UI and backend can progress while hardware is being stabilized.
- Recommendation errors causing misleading advice: mitigate by making recommendations explainable (show the measured value, the target range for the species, and the action) and adding conservative messaging when confidence is low.
- Hardware procurement delays or failures: mitigate by ordering early and keeping a software-only simulation mode to continue development without hardware.

### Project Close-out Plan. 
Project close-out will include a final integrated build, a demonstration of sensor-to-recommendation functionality, and a complete repository containing the code, setup instructions, and documentation. The team will tag a final release in the repository and ensure that the README provides step-by-step instructions to run the system. A brief post-project review will capture lessons learned (what worked well, what was difficult, and what could be improved in a future iteration).

## Additional Plans. 
- Security: the system will avoid storing sensitive personal data. If user accounts are implemented, passwords will be stored securely (hashed), and API keys/secrets will not be committed to the repository.
- Data/licensing: plant databases and any external datasets used will be cited, and licensing constraints will be respected. If a dataset cannot be legally reused, the team will replace it with an approved alternative or a curated set with proper references.



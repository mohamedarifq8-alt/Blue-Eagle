# Blue Eagle: Autonomous Quadcopter Control in Webots

**Blue Eagle** is a custom-designed drone project developed within the **Webots** robotics simulator. Inspired by the Mavic 2 Pro, this project features a ground-up implementation of a **PID Control System** written in **Python** to achieve stable autonomous flight and altitude hold.

## 🛸 Project Overview
The project focuses on building a robust flight controller for a quadcopter. As a **Computer and Control Engineer**, the implementation emphasizes the mathematical modeling of flight dynamics, sensor fusion, and precise motor speed modulation to maintain equilibrium and reach target altitudes.

---

### 📸 Visual Documentation

#### 1. Drone Design (Blue Eagle)
The customized model design within Webots, specifically configured with a custom Inertial Unit and Propeller physics.
![Blue Eagle Design](./protos/Screenshot%202026-04-24%20031539.png)

#### 2. Autonomous Flight Test
The drone maintains a stable hover at a target altitude of 20 meters, demonstrating the effectiveness of the PD control loop.
![Blue Eagle In Flight](./protos/Screenshot%202026-05-02%20001558.png)

---

## 🏗 Control System Architecture

The flight controller is built using a Class-based structure (`Mavic2ProController`) that manages the sense-think-act cycle:

### 1. Sensor Integration
The system stabilizes itself by fusion of data from three primary sensors enabled at the basic time step:
* **Inertial Unit (IMU):** Provides Roll, Pitch, and Yaw angles for orientation feedback.
* **Gyroscope:** Measures angular velocity to calculate the derivative (D) term of the PID.
* **GPS:** Used for real-time Z-axis (Altitude) monitoring.

### 2. Altitude PD Controller (Vertical Control)
A specialized vertical control logic was developed to manage take-off and hovering:
* **Velocity Estimation:** The system calculates `vertical_velocity` by differentiating the altitude over time ($v = \Delta h / \Delta t$), acting as a "brake" to prevent overshooting.
* **Error Saturation:** A `MAX_ALT_ERROR` of 1.5m is implemented to ensure the drone rises smoothly without aggressive surges.
* **Base Lift:** A constant base thrust (68.5 units) is used as the equilibrium point, adjusted dynamically by the PD error.

### 3. Attitude & Balance Controller
To maintain a level flight, the drone uses Proportional-Derivative (PD) control for Roll and Pitch:
* **P-Term ($K_p=30.0$):** Corrects the angle based on the current deviation from zero.
* **D-Term ($K_d=2.0$):** Dampens the movement using the Gyro rate to prevent oscillations.

---

## 🛠 Motor Mixing & Actuation
The controller translates high-level logic into individual motor velocities using a mixing matrix. This ensures that the altitude, roll, and pitch inputs are combined correctly for each of the four BLDC motors:

| Motor | Position | Mixing Formula |
| :--- | :--- | :--- |
| **m1** | Front Left | `vertical + roll - pitch` |
| **m2** | Front Right | `vertical - roll - pitch` |
| **m3** | Rear Left | `vertical + roll + pitch` |
| **m4** | Rear Right | `vertical - roll + pitch` |

*Note: Motor directions are accounted for in the `setVelocity` commands to handle torque compensation (Yaw).*

## 📈 Optimization & Safety Logic
* **Saturation Management:** Motor inputs are clamped between 50.0 and 85.0. This prevents the motors from stalling during descent and ensures there is always "control headroom" for stabilization during high-speed climbs.
* **Velocity-Based Braking:** By incorporating the `vertical_velocity` into the altitude input, the drone can "feel" its own momentum and slow down as it approaches the 20m target.

---

### 💡 Engineering Insights:
1. **Mathematical Tuning:** The constants ($K_p=30.0, K_d=2.0$) were derived through iterative testing in Webots to achieve a "critically damped" response.
2. **Dynamic Equilibrium:** The system uses 68.5 as the `vertical_input` base, which is the calculated power needed to counteract gravity for this specific drone mass.
3. **Sensor Sampling:** All sensors are enabled using `self.time_step`, ensuring the PID loop runs in sync with the physics engine for maximum stability.

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
The system stabilizes itself by fusion of data from three primary sensors:
* **Inertial Unit (IMU):** Provides Roll, Pitch, and Yaw angles for orientation feedback.
* **Gyroscope:** Measures angular velocity to calculate the derivative (D) term of the PID.
* **GPS:** Used for real-time Z-axis (Altitude) monitoring.

### 2. Altitude PD Controller (Vertical Control)
* **Velocity Estimation:** The system calculates `vertical_velocity` ($v = \Delta h / \Delta t$), acting as a "brake" to prevent overshooting.
* **Error Saturation:** A `MAX_ALT_ERROR` of 1.5m ensures smooth take-offs.
* **Base Lift:** A constant base thrust (68.5 units) is used as the equilibrium point.

### 3. Attitude & Balance Controller
* **P-Term ($K_p=30.0$):** Corrects the angle based on the current deviation.
* **D-Term ($K_d=2.0$):** Dampens the movement using the Gyro rate to prevent oscillations.

---

## 🛠 Motor Mixing & Actuation
| Motor | Position | Mixing Formula |
| :--- | :--- | :--- |
| **m1** | Front Left | `vertical + roll - pitch` |
| **m2** | Front Right | `vertical - roll - pitch` |
| **m3** | Rear Left | `vertical + roll + pitch` |
| **m4** | Rear Right | `vertical - roll + pitch` |

---

## 👨‍💻 Author
**Mohamed Arif Mahyoub Haider**
*Electrical Engineer - Computer and Industrial Control*

---

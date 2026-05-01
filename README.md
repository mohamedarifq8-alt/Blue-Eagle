# Blue Eagle: Autonomous Quadcopter Control in Webots

**Blue Eagle** is a custom-designed drone project developed within the **Webots** robotics simulator. Inspired by the Mavic 2 Pro, this project features a ground-up implementation of a **PID Control System** written in **Python** to achieve stable autonomous flight and altitude hold.

## 🛸 Project Overview
The project focuses on building an automated system capable of recognizing handwritten digits (0-9). As a **Computer and Control Engineer**, the implementation emphasizes not just accuracy, but also the stability of the training process and the robustness of the model architecture.

---

### 📸 Visual Documentation

#### 1. Drone Design (Blue Eagle)
This is the customized model design in the Webots environment, optimized for stability and physical accuracy.
![Blue Eagle Design](./images/drone_design.png)

#### 2. Autonomous Flight Test
The drone performing an autonomous take-off and maintaining a stable hover at a target altitude of 20 meters using the PID controller.
![Blue Eagle In Flight](./images/drone_flight.png)

---

## 🏗 Network Architecture & Engineering Design
The model was designed using a `Sequential` structure with a focus on feature extraction and regularization:
*   **Feature Extraction:** Utilized `Conv2d` layers to capture spatial hierarchies in the images.
*   **Stability:** Integrated `BatchNorm2d` layers after convolutions to stabilize the hidden state distributions and accelerate convergence.
*   **Non-Linearity:** Used `ReLU` activation functions to enable the model to learn complex patterns.
*   **Dimensionality Reduction:** Employed `MaxPool2d` for spatial downsampling while retaining essential features.
*   **Generalization (Regularization):** Applied `Dropout` layers to mitigate overfitting, ensuring the model performs well on unseen test data.

## 🛠 Technical Implementation & Tools
The project leverages the full power of the PyTorch ecosystem and Python data science stack:
*   **Core Framework:** `torch` & `torch.nn` for model building.
*   **Data Pipeline:** `DataLoader` and `TensorDataset` for efficient batching and memory management.
*   **Preprocessing:** `pandas` and `sklearn` for data splitting and normalization.
*   **Visualization:** `seaborn` and `matplotlib` for analyzing the training curves and error distribution.

## 📈 Optimization & Control Strategy
In line with control engineering principles, the training process was treated as an optimization problem:
*   **Optimizer:** Used the **Adam** optimizer for its adaptive learning rate capabilities.
*   **Loss Function:** **CrossEntropyLoss** was chosen as the objective function for multi-class classification.
*   **Dynamic Feedback:** Implemented a **Learning Rate Scheduler** (`ReduceLROnPlateau`). This mimics a closed-loop system where the "system" (the model) monitors the validation loss and automatically reduces the learning rate when the improvement stalls (plateaus), ensuring fine-tuned convergence.

## 📁 Dataset & Model Persistence
*   **Data Source:** [Kaggle Digit Recognizer](https://www.kaggle.com/competitions/digit-recognizer). 
*   **Model Weights:** The final trained state of the model is saved using `torch.save(model.state_dict(), 'model_weights.pth')`, allowing for easy deployment or further fine-tuning.
*   **Evaluation:** Detailed analysis was performed using a `confusion_matrix` to identify specific digit-class confusion (e.g., distinguishing between 4 and 9).

---

### 💡 Engineering Insights & Tips:
1. **Mathematical Tuning:** The constants ($K_p=30.0, K_d=2.0$) were derived through iterative testing to balance responsiveness and stability.
2. **Velocity Estimation:** By calculating `(altitude - prev_altitude) / time_step`, the system effectively estimates vertical speed without a dedicated variometer sensor.
3. **Hardware Compatibility:** The code is structured to be easily portable to real microcontrollers like **ESP32** or **Pixhawk** with minimal adjustments to the sensor API.
4. **Visual Showcase:** The images above demonstrate the system's ability to maintain equilibrium despite the complex physics of four independent rotors.

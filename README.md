# Group name: Fitness Guys
Repo for demo idea and code for ICT720 course 2025.

## A health-tracking application
This is a health monitoring application that tracks the status of gym trainers in real time. The system utilizes heart rate and motion sensors (IMU) to detect abnormal changes in trainers' physical health during workouts. The application advises trainers on modifying their training or taking a rest. In case of an accident, it functions as an SOS application, sending an SOS signal for help.

## Our members
1. Than Zaw Toe (SIIT,Thammasat)
2. Narodom Yatnimit (KU)
3. Luong Duc Nhat (Institute of Science Tokyo)

## User stories
1. As a **gymer**, I want to **know my limitation**, so that **I can stop at the right time**.
  - Acceptance Criteria #1 Enter the age
  - Acceptance Criteria #2 Calculate the average heart rate base on age
2. As a  **gymer**, I want to  **send an SOS signal when I have an accident or need weight support**, so that  **I can receive assistance or get timely help**.
  - Acceptance Criteria #1 Enter the emergency contact
  - Acceptance Criteria #2 Notify your medic.
3. As a **gymer**, I want to **monitor my heart rate and related health precautions while playing weight lifting**
  - Acceptance Criteria #1 I can see the status of my current heart beat
  - Acceptance Criteria #2 I can press the emergency button to call medic.

## Sequence diagram
![Flowchart of the application](Images/flow_chart.png)
![Hardware lists](Images/hw.png)

## Data format
```json
{
    "user": {
        "id": "dvadvfsd12@4egv",
        "name": {
            "last_name": "Luca",
            "first_name": "Luca"
        },
        "occupation": "SIIT",
        "height": 170,
        "age": 26,
        "telephone": 123456789,
        "email": "luca@gmail.com"
    },
    "guarantor": {
        "name": {
            "last_name": "Lucadad",
            "first_name": "Lucadad"
        },
        "relationship": "father",
        "telephone": 123456789,
        "email": "lucadad@gmail.com"
    },
    "weight_logs": [
        { "weight": 70, "timestamp": "2020-01-01 00:00:00" },
        { "weight": 71, "timestamp": "2020-01-02 00:00:00" },
        { "weight": 72, "timestamp": "2020-01-03 00:00:00" }
    ],
    "bmi_logs": [
        { "bmi": 70, "timestamp": "2020-01-01 00:00:00" },
        { "bmi": 71, "timestamp": "2020-01-01 00:00:00" },
        { "bmi": 72, "timestamp": "2020-01-01 00:00:00" }
    ],
    "heart_rate_logs": [
        { "val": 70, "timestamp": "2020-01-01 00:00:00" },
        { "val": 71, "timestamp": "2020-01-01 00:00:00" },
        { "val": 72, "timestamp": "2020-01-01 00:00:00" }
    ]
}
```
=======
## Build and Installation
1. Clone the repository:
2. Create a `.env` file by copying the example file:
3. Open the `.env` file and fill in the required environment variables.
4. Build the project:
5. Upload the project:

** Make sure to configure your `.env` file with the correct values before running the application.
## How to use the data
1) **Name**
2) **Age**
3) **BMI** ->> four catagories : 
-**Underweight** = < 18.5
-**Normal weight** = 18.5 - 24.9
-**Overweight** = 25-29.9
-**Obesity** = BMI of 30 or greater
	 
4) **Recommended Workout plan**

| BMI Category    | BMI Range       | Workout Focus |
|---------------|-----------------|------------------------------------------------|
| **Underweight** | < 18.5          | Building muscle mass and strength. |
| **Normal Weight** | 18.5 - 24.9   | Maintaining fitness, improving cardiovascular health, and building strength. |
| **Overweight** | 25 - 29.9        | Losing weight, improving cardiovascular health, and building strength. |
| **Obesity** | ≥ 30             | Gradual weight loss, improving cardiovascular health, and increasing mobility. |


# suspicious Activity Detection
Suspicious activity detected in recorded and live surveillance

A Python project that detects suspicious activity in **recorded videos and live surveillance feeds** using **head movement** cues and a simple web UI for running inference and viewing results. 

The system uses a rule based on the **detected face distance** to decide the next step:
- If the face distance is **≤ 200** → mark as **suspicious** (head-movement based)
- If the face distance is **> 200** → proceed to **activity detection** 

---

## How it works (decision rule)

For each processed segment/frame, the pipeline computes a **face distance** value from the detected face.

- **Face distance ≤ 200**  
  Flag as **suspicious** based on head movement.

- **Face distance > 200**  
  Trigger **activity detection** (deeper analysis of the ongoing activity).



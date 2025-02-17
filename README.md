**Automated Inspection & Counting System for Oil Cans**  

## **1. Introduction**  
This industrial project is developed for **BL Agro Industries**, an **edible oil and food manufacturing company based in Bareilly, India**. 
Founded in the 1950s, BL Agro has grown from an **oil trading business to a high-quality edible oil producer**.  

The system is designed to **automatically inspect and count oil cans** in a container. Each container should hold **six cans**. If any cans's caps are missing, the system generates an **"NG" (Not Good) signal**, otherwise, it is marked as **"OK"**.  

## **2. System Workflow**  

### **Step 1: Container Image Capture**  
- The **production lane inspection system** captures images of ** A containers carrying 6 oil cans**.  
- The image is processed in real time to check for missing cans's caps .  

### **Step 2: Object Detection & Counting**  
 **Input image 1 OK Image **

 
 ![ok_image](https://github.com/user-attachments/assets/0183a61a-9b3a-4488-8e7f-5b1339866fde)

 
 **Input image 2 NG Image **

 
 ![ng_image](https://github.com/user-attachments/assets/7f46fffa-755a-4efa-b5d7-13717f4413b8)

 
******************************************************************************************************************
##  **Output image 1  OK Image **


![detection__image1_frame](https://github.com/user-attachments/assets/4ce6f432-4b0f-47dc-9856-91e53cdd022c)


##  **Output image 2  NG Image **


![detection__image2_frame](https://github.com/user-attachments/assets/4c9ee09c-bad7-41d1-9521-5efb484a6bd5)


******************************************************************************************************************
 
- The system uses **computer vision (OpenCV) and YOLO object detection** techniques to count the total 6 number of cans in each container.  
- It classifies the **cans's caps as either "Open" (missing) or "Closed" (present)**.  

### **Step 3: Status Determination**  
- Based on the count, the system determines the **status**:  
  - **"OK"** → If **all 6 cans's caps ** are detected.  
  - **"NG (Not Good)"** → If **any cans's caps are missing**.  

### **Step 4: Response Generation**  
### **Responses Snapshots**


![image](https://github.com/user-attachments/assets/5a892488-6d4a-469d-80d8-d6afbe932daa)


![image](https://github.com/user-attachments/assets/35c800f1-ab3a-4c98-aa5b-8bdac3de35a6)



![image](https://github.com/user-attachments/assets/a8768085-f0fa-4332-9abb-82cc1323f87d)



- The **annotated image is encoded to Base64** format for easy transmission.  
- A **JSON response** is generated with:  
  - **Image (Base64)**  
  - **Inspection Status (OK/NG)**  
  - **Open Count (Missing Cans)**  
  - **Closed Count (Detected Cans)**  

### **Step 5: Alarm & Monitoring System**  
- If the **status is "NG"**, the system **triggers an alarm** to alert operators.  
- The inspection results are displayed on a **real-time dashboard** over the **LCD Display monitor**.  

## **3. Code Logic Overview**  
```python
# Determine status
status = "Ok" if open_count == 0 or closed_count == 6 else "Not Ok"

# Encode annotated image to base64
_, img_encoded = cv2.imencode('.jpg', frame)
img_base64 = base64.b64encode(img_encoded).decode('utf-8')

# Response data
response_data = {
    "image": img_base64,
    "status": status,
    "open_count": open_count,
    "closed_count": closed_count
}

return JSONResponse(content=response_data)
```

## **4. Technologies Used**  
- **Hardware:** Industrial Cameras[ Hikvision ], PLC ,IR Sensor
- **Software:** OpenCV, FastAPI, Uvicorn  
  

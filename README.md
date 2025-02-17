**Automated Inspection & Counting System for Oil Cans**  

## **1. Introduction**  
This industrial project is developed for **BL Agro Industries**, an **edible oil and food manufacturing company based in Bareilly, India**. Founded in the 1950s, BL Agro has grown from an **oil trading business to a high-quality edible oil producer**.  

The system is designed to **automatically inspect and count oil cans** in a container. Each container should hold **six cans**. If any cans's caps are missing, the system generates an **"NG" (Not Good) signal**, otherwise, it is marked as **"OK"**.  

## **2. System Workflow**  

### **Step 1: Container Image Capture**  
- The **production lane inspection system** captures images of **containers carrying oil cans**.  
- The image is processed in real time to check for missing cans.  

### **Step 2: Object Detection & Counting**  
- The system uses **computer vision (OpenCV) and object detection** techniques to count the number of cans in each container.  
- It classifies the **cans's caps as either "Open" (missing) or "Closed" (present)**.  

### **Step 3: Status Determination**  
- Based on the count, the system determines the **status**:  
  - **"OK"** → If **all 6 cans's caps ** are detected.  
  - **"NG (Not Good)"** → If **any cans's caps are missing**.  

### **Step 4: Image Encoding & Response Generation**  
- The **annotated image is encoded to Base64** format for easy transmission.  
- A **JSON response** is generated with:  
  - **Image (Base64)**  
  - **Inspection Status (OK/NG)**  
  - **Open Count (Missing Cans)**  
  - **Closed Count (Detected Cans)**  

### **Step 5: Alarm & Monitoring System**  
- If the **status is "NG"**, the system **triggers an alarm** to alert operators.  
- The inspection results are displayed on a **real-time dashboard** over the **local LAN network**.  

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
- **Hardware:** Industrial Cameras, PLC (if applicable)  
- **Software:** OpenCV, FastAPI, Uvicorn  
- **Database:** Can be integrated for logging results  
- **Display:** Real-time monitoring on Display monitor  

import cv2
import numpy as np
import base64
import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from typing import List


class ImageRequest(BaseModel):
    image: str
    threshold_val: int
    user_message: str
    # dummy_array: List[int]
    

def load_model(model_path='best.onnx'):
    return cv2.dnn.readNetFromONNX(model_path)

def load_classes(file_path='detectionn.names'):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def perform_detection(frame, net, classes, confidence_threshold=0.5, nms_threshold=0.5):
    height, width, _ = frame.shape
    blob = cv2.dnn.blobFromImage(frame, scalefactor=1/255, size=(640, 640), mean=[0, 0, 0], swapRB=True, crop=False)
    net.setInput(blob)
    detections = net.forward()[0]

    class_ids = []
    confidences = []
    boxes = []

    x_scale, y_scale = width / 640, height / 640

    for row in detections:
        confidence = row[4]
        if confidence > confidence_threshold:
            classes_score = row[5:]
            class_id = np.argmax(classes_score)
            if classes_score[class_id] > confidence_threshold:
                class_ids.append(class_id)
                confidences.append(confidence)
                cx, cy, w, h = row[:4]
                x1 = int((cx - w/2) * x_scale)
                y1 = int((cy - h/2) * y_scale)
                width = int(w * x_scale)
                height = int(h * y_scale)
                box = np.array([x1, y1, width, height])
                boxes.append(box)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, nms_threshold)
    return [(boxes[i], classes[class_ids[i]], confidences[i]) for i in indices]


def draw_boxes(frame, detections):
    label_color = {
        'Open': (0, 0, 255),   # Red
        'Closed': (0, 255, 0),  # Green
    }
    cords = []
    lab_list = []

    for box, label, confidence in detections:
        x1, y1, w, h = box
        lab = label
        lab_list.append(lab)
        bgr = label_color.get(lab, (0, 0, 0))
        cor = [lab, [int(x1), int(y1), int(x1 + w), int(y1 + h)]]
        cords.append(cor)
        frame = cv2.rectangle(frame, (int(x1), int(y1)), (int(x1 + w), int(y1 + h)), bgr, 1)

        text_size = cv2.getTextSize(lab, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
        text_width = text_size[0]

        text_x = max(int(x1) - 5, 0)
        text_x = min(text_x, frame.shape[1] - text_width - 5)

        frame = cv2.putText(frame, lab, (text_x, int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            label_color.get(lab, (0, 0, 0)), 2, cv2.LINE_AA)

    # Count "Open" and "Closed" instances
    open_count = lab_list.count("Open")
    closed_count = lab_list.count("Closed")
    count_color = (255, 255, 255)  # White for count values

    # Define text properties
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    thickness = 2
    line_type = cv2.LINE_AA

    # Get text size for positioning "Closed" count
    text_size_open = cv2.getTextSize(f'Open:{open_count}', font, font_scale, thickness)[0]
    text_size_closed = cv2.getTextSize(f'Closed:{closed_count}', font, font_scale, thickness)[0]

    # Draw "Open" count at the top left corner
    cv2.putText(frame, f'Open:{open_count}', (10, 30), font, font_scale, (0, 0, 255), thickness, line_type)

    # Calculate position for "Closed" count
    closed_text_y = 35 + text_size_open[1] + 10  # Below the "Open" count with some spacing

    # Draw "Closed" count below the "Open" count
    cv2.putText(frame, f'Closed:{closed_count}', (10, closed_text_y), font, font_scale, (0, 255, 0), thickness,
                line_type)

app = FastAPI()

net = load_model()
classes = load_classes()

@app.get("/ServerCheck")
async def server_check():
    return JSONResponse(
        status_code=200,
        content={
            "message": "Server is Running",
            "status_code": 200,
            "reason": "OK"
        }
    )

@app.post('/predict')
async def predictions(request: ImageRequest):
    try:
        # Decode base64 image
        image_data = base64.b64decode(request.image) 
        nparr = np.frombuffer(image_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            raise HTTPException(status_code=400, detail="Failed to load the image. Please provide a valid image.")

        # Perform object detection
        detections = perform_detection(frame, net, classes)
        draw_boxes(frame, detections)
        # save image after detection 
        #processed_img_path = "annotated_image.jpg"   
        #processed_img= cv2.imwrite(processed_img_path, frame)

        # print type of processed image
        #print(type(processed_img))
        #print(processed_img)
       
        # Count "Open" and "Closed" instances
        open_count = sum(label == "Open" for _, label, _ in detections)
        closed_count = sum(label == "Closed" for _, label, _ in detections)

        # Determine status
        status = "Ok" if open_count == 0 else "Not Ok"

        # Encode annotated image to base64
        _, img_encoded = cv2.imencode('.jpg',frame)
        img_base64 = base64.b64encode(img_encoded).decode('utf-8')
        # dummy_array = request.dummy_array
        user_message = request.user_message
        user_message = 'Congratulation You have done ->' + user_message
        threshold_val = request.threshold_val
        threshold_val += 5
       
        # Response data
        response_data = {
            "image": img_base64,
            "threshold_val":threshold_val,
            "user_message": user_message    
            
        }

        return JSONResponse(content=response_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    #uvicorn.run(app, host="127.0.0.1", port=5000)
    uvicorn.run("backend-server:app", host="127.0.0.1", port=5000 ,reload=True) #"backend-server:app"

import os
import sys
from ultralytics import YOLO

#Use the model to predict based on the source. 
cwd = os.getcwd()
# model = YOLO('yolov8s.pt')
model = YOLO('best_from_lab.pt')
results = model.predict(
   source=sys.argv[1], #you have to pass an image as the argument
   conf=0.25 #confidence level
)

# Save the predicted image with bounding boxes
for result in results:
    # Save the image with bounding boxes
    result.save()  # This saves to the default directory

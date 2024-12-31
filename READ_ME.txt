DO NOT TOUCH THIS. ANY WORK YOU WANT TO TRY, DO IN THE PROJECT COPY FOLDER. THIS FOLDER WORKS. DO NOT BREAK IT.
THIS WON'T WORK UNLESS YOU BRING IT TO YOUR DESKTOP, THAT'S WHERE THE ENVIRONMENT IS SET UP. BUT IT DOES WORK IN THE DESKTOP! I PUT IT AWAY FOR ORGANIZATION.
It works just fine where it is, but should future errors occur, refer back to this! ^

File system breakdown:
- recipegen is the folder that generates the recipe based on input ingredients. It contains all of the non-html app methods and whatnot. I own everything in there except for the recipes dataset.
- static is a folder containg the style css file for the website and one image: the results of yolov8 on the image input from the user. I don't know if I or the user own that image but I don't think it matters.
- templates contains only html stuff for the website. I own everything in there.
- yolov8 is a folder containing the yolov8 model, which I own none of. The only files in there I definitely own are myscript.py and notes.txt. The user's submitted image and the temporary results are in there too, as is the model I trained on the fridge dataset.
- yolov8fridgedata is a folder of refrigerator data formatted specifically for a yolov8 model. I do not own it, it's from https://universe.roboflow.com/computer-vision-group-ji0bm/group_work/dataset/3

More info:
- recipegen, templates, and yolov8 all have a txt file called notes.txt that gives more info about each folder.
- all code can be run in project directory (I think) but there's no code that has to be run from its own directory.
    - not all code will work if running in terminal, since lots relies on app input



To run: 
1. run app.py from terminal. I've been running it from the project folder which is 'python recipegen/app.py', but I don't think it matters where you run it.
2. Go to http://127.0.0.1:5000/ on a web browser and input an image! So far I think it supports filetypes: png, jpeg. It does NOT support Screenshots (I think because the files have spaces in the name) or HEIC.
3. Navigate through website. Don't forget to check the boxes!
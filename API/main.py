from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
import json
import base64
import io

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#Model Load
MODEL = tf.keras.models.load_model("model_api.h5")

CLASS_NAMES =['Apple___Apple_scab',
 'Apple___Black_rot',
 'Apple___Cedar_apple_rust',
 'Apple___healthy',
 'Blueberry___healthy',
 'Cherry_(including_sour)___Powdery_mildew',
 'Cherry_(including_sour)___healthy',
 'Corn_(maize)___Cercospora_leaf_spot',
 'Corn_(maize)___Common_rust_',
 'Corn_(maize)___Northern_Leaf_Blight',
 'Corn_(maize)___healthy',
 'Grape___Black_rot',
 'Grape___Esca_(Black_Measles)',
 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
 'Grape___healthy',
 'Orange___Haunglongbing_(Citrus_greening)',
 'Peach___Bacterial_spot',
 'Peach___healthy',
 'Pepper,_bell___Bacterial_spot',
 'Pepper,_bell___healthy',
 'Potato___Early_blight',
 'Potato___Late_blight',
 'Potato___healthy',
 'Raspberry___healthy',
 'Soybean___healthy',
 'Squash___Powdery_mildew',
 'Strawberry___Leaf_scorch',
 'Strawberry___healthy',
 'Tomato___Bacterial_spot',
 'Tomato___Early_blight',
 'Tomato___Late_blight',
 'Tomato___Leaf_Mold',
 'Tomato___Septoria_leaf_spot',
 'Tomato___Spider_mites',
 'Tomato___Target_Spot',
 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
 'Tomato___Tomato_mosaic_virus',
 'Tomato___healthy']
data = json.load(open("data.json"))

@app.get("/ping")
async def ping():
    return "Hello, I am Abhishek"

def read_file_as_image(data) -> np.ndarray:
    im = Image.open(BytesIO(data))
    dt = io.BytesIO()
    im.save(dt, "JPEG")
    global encoded_img_data 
    encoded_img_data = base64.b64encode(dt.getvalue())
    image = np.array(Image.open(BytesIO(data)).resize((240,240)))
    return image

@app.post("/predict", response_class=HTMLResponse)
async def predict(
    file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)
    
    predictions = MODEL.predict(img_batch)

    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    plant = data[predicted_class]["plant"]
    disease = data[predicted_class]["disease"]
    remedy = data[predicted_class]["remedy"]
    #confidence  in percentage
    confidence = '{:.3f}'.format(np.max(predictions[0]*100))
    return """
    <!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link
        href="https://fonts.googleapis.com/css2?family=Mochiy+Pop+One&family=Prompt:wght@300&family=Roboto&display=swap"
        rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">
    <link rel="stylesheet" href="https://abhishekkandel45.github.io/Plant-Disease-Front-END/style-index.css">
    <title>Document</title>
</head>

<body>
    <div class="header-box">
        <div class="hackathon-div">
            <img src="https://abhishekkandel45.github.io/Plant-Disease-Front-END/hackathon_logo.png" class="hackathon-logo">
        </div>

        <h2 class="heading">Plant Disease Recognition System</h2>
        <div class="sharda-div">
            <img src="https://abhishekkandel45.github.io/Plant-Disease-Front-END/sharda_logo.png" class="sharda-logo">
        </div>

    </div>

    <div class="container-box">
        <div class="text">
            <p><b>Plant:</b> {plant}</p>
            <p><b>Predicted Disease:</b> {disease}</p>
            <p><b>Accuracy:</b> {confidence}%</p>
            <p><b>Prescribed Remedy:</b> {remedy}</p>
        </div>
        <div class="input">
            <div class="selected-image-box">
                <img class = "selected-image-next" id="output" width="300" src="data:image/jpeg;base64,{image}">
            </div>
        </div>
    </div>
    
        

</body>

</html>
    """.format(predicted_class=predicted_class, confidence=confidence, plant=plant, disease=disease, remedy=remedy, image=encoded_img_data.decode('utf-8'))

@app.get("/", response_class=HTMLResponse)
async def upload():
    return """
    <!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link
        href="https://fonts.googleapis.com/css2?family=Mochiy+Pop+One&family=Prompt:wght@300&family=Roboto&display=swap"
        rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">
        <link href="https://abhishekkandel45.github.io/Plant-Disease-Front-END/style-index.css" rel="stylesheet">
    <title>Document</title>
</head>

<body>
    <div class="header-box">
        <div class="hackathon-div">
            <img src="https://abhishekkandel45.github.io/Plant-Disease-Front-END/hackathon_logo.png" class="hackathon-logo">
        </div>

        <h2 class="heading">Plant Disease Recognition System</h2>
        <div class="sharda-div">
            <img src="https://abhishekkandel45.github.io/Plant-Disease-Front-END/sharda_logo.png" class="sharda-logo">
        </div>

    </div>

    <div class="container-box">
        <div class="text">
            <h1>What it does ?</h1>
            <p>Every year huge numbers of farmers commit suicide beacuse of bad yield of crops which is cause due to infected plants.</p>
            <p>Farmers couldn't recognize the disease of their crops or even if they recognize the disease they do not know the remedy of cure for it.</p>
            <p>Therefore, We came with a solution which can recognize the infected and uninfected leaves and if they are infected, It can provied a remedy to cure it.</p>
        </div>
        <div class="input">
            <h1>Submit an image : </h1>
            <form action="/predict" enctype="multipart/form-data" method="post">
                <input name="file" type="file" accept="image/*" onchange="loadFile(event)" class="choose-btn">
                <input type="submit" class="btn submit-btn btn-outline-success">
            </form>
            <div class="selected-image-box">
                <img class = "selected-image" id="output" width="200" />
            </div>
        </div>
    </div>

    <script>
        var loadFile = function(event) {
            var image = document.getElementById('output');
            image.src = URL.createObjectURL(event.target.files[0]);
            document.getElementById('output').style.cssText = 'border: 0.3rem solid white; border-radius: 1.5rem';
        };
    </script>
        

</body>

</html>
    """

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000, root_path="\web")

# <form action="/predict" enctype="multipart/form-data" method="post">
#     <input name="file" type="file">
#     <input type="submit">
#     </form>

# <h1>Class: {predicted_class} | Confidence: {confidence} % </h1>
#     <h2>Plant: {plant}</h2>
#     <h2>Disease: {disease}</h2>
#     <h2>Remedy: {remedy}</h2>
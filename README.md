# Plant Disease Recognition System.
![Plant_Diseases_Recognition_System](https://user-images.githubusercontent.com/38427430/172302053-57bb9f70-6323-44b0-8142-716af7a2304d.png)



# Block Diagram of WebApp:
![Plant_Diseases_Recognition_System](https://user-images.githubusercontent.com/38427430/172546277-11142a6d-ac64-433c-953c-bed16d0d1c3a.png)

Any supervised machine learning project starts with data collection, which we can use as a training data set in our case. We need to collect images of healthy plant leaves and the plant with diseases, so we will cover how we do that, but we have covered all these images. Then comes the data cleaning and pre-processing step, for which we will be using the tf data sets and data augmentation. Data augmentation because we might not have enough diverse images, so we need to rotate and flip, and we know edges contrast to create more training samples. Once we have that, we will use model building using a Convolutional Neural Network. CNN is a standard way of doing image classification as of 2021. Therefore, we will use CNN and export the trained model onto our disk. Then we will cover some of the ML (Machine Learning) OPs concepts using TF serving. We will have a tf serving server running on top of these exported models, which can serve different versions of these models, and TF serving will be called from FAST API. Then will build a website in ReactJS. ReactJS is a hot technology today for doing a website app development, and that will be calling the fast APIs server where we can drag and drop the image, and it will tell us the label where it is healthy or not.










# Collaboration are always Welcome


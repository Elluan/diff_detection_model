# Informed methods for deepfake speech detection

**Author:** Vojtěch Staněk ([vojteskas](https://github.com/vojteskas)), xstane45@vutbr.cz ([Elluan](https://github.com/Elluan))

**Abstract:**Docker for this modele : https://github.com/vojteskas/Differential-Detection/tree/master


## Requirements

docker 

## Usage

Create the image 
```
docker build -t model .
```

Run the container 
```
docker run -p 8000:8000 model
```

Making POST request with 2 audio : real one and suspected one to http://localhost:8000/ will return the result of the Deepfake detection 



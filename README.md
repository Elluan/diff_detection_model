# Informed methods for deepfake speech detection

**Author:**
 Vojtěch Staněk ([vojteskas](https://github.com/vojteskas)), xstane45@vutbr.cz, 
 Thel9 ([Elluan](https://github.com/Elluan))

**Content:**
Docker for this modele : https://github.com/vojteskas/Differential-Detection/tree/master


## Requirements

 - Docker
 - FFConcat3_MHFA_finetune_7.pt model avaiable here :  https://drive.google.com/file/d/1FM-WowOpWLpgTFIzPFjpu_6amcMhctp0/view?usp=drive_link

## Usage

First, you need to place the FFConcat3 model into the main diff_detection_model folder.

The following commands should be executed in the main diff_detection_model folder.

Create the image 
```
docker build -t model .
```

Run the container 
```
docker run -p [port in your server]:8000 model
example : docker run -p 8888:8000 model
```

Making POST request with 2 audio : real as the key real and suspected as the key fake to http://localhost:[port in your server]/diff-model/ (in ou case : http://localhost:8888/diff-model/ ) will return the result of the Deepfake detection 

Run the container for NABOSO app
```
docker run -p 8888:8000 model
```

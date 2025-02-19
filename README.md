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

First you need to put the FFConcat3 model into the folder.

Create the image 
```
docker build -t model .
```

Run the container 
```
docker run -p 8000:8000 model
```

Making POST request with 2 audio : real one and suspected one to http://localhost:8000/ will return the result of the Deepfake detection 



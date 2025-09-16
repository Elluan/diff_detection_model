# Informed methods for deepfake speech detection

**Author:**
 Vojtěch Staněk ([vojteskas](https://github.com/vojteskas)), xstane45@vutbr.cz, 
 Thel9 ([Elluan](https://github.com/Elluan))

**Content:**
Docker for this modele : https://github.com/vojteskas/Differential-Detection/tree/master


## Requirements

 - Docker version 28.0.1 or higher
 - FFConcat3_MHFA_finetune_7.pt model avaiable here :  https://drive.google.com/file/d/1FM-WowOpWLpgTFIzPFjpu_6amcMhctp0/view?usp=drive_link

## Usage
First, you need to place the FFConcat3 model into the root of this folder.

To run this model it is necessary to have these repositories:
- backend : clone the repo and switch to the naboso branch
    - `git clone https://<username>@bitbucket.org/replaywell-ws/backend.git`
    - `cd backend`
    - `git checkout naboso`
- naboso-frontend:
    - `git clone https://github.com/simonfie/naboso-frontend.git`
- (optional) single_input_model: not necessary to run diff_detection_model but a part of naboso
    - `git clone https://github.com/simonfie/single_input_model.git`
  
Folder structure:
- backend/
- diff_detection_model/
- naboso-frontend/
- single_input_model/

## Usage (OLD)

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

# realestate10k
A tool used for download Dataset RealEstate10k



## About [RealEstate10k](https://google.github.io/realestate10k/)
RealEstate10K is a large dataset of camera poses corresponding to 10 million frames derived from about 80,000 video clips, gathered from about 10,000 YouTube videos. For each clip, the poses form a trajectory where each pose specifies the camera position and orientation along the trajectory. These poses are derived by running SLAM and bundle adjustment algorithms on a large set of videos. 

## Installation
```bash
git clone https://github.com/Iann1978/realestate10k.git
cd realestate10k
conda create -n realestate10k python=3.10
conda activate realestate10k
pip install -r requirements.txt
```

## How to use this project

* Download [RealEstate10K.tar.gz](https://storage.cloud.google.com/realestate10k-public-files/RealEstate10K.tar.gz), unzip it and replace the context in folder RealEstate10K.

* Export your youtube's cookie and save it as cookies.txt under the current folder.

* Run the follow
```bash
python download.py
```
* The result will be store under downloaded

## How to deal with interrupt
Run the follow
```bash
python download.py
```

## How to redownload
* Remove context under trajectories folder(./RealEstate10K/).
* Remove downloaded folder(./downloaded). 
* Remove tempory folder(./temp).
* Remove downloading database file(downloading.sqlite).
* Do follow 'How to use this project.'

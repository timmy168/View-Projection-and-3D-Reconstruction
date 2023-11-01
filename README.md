# View Projection And 3D Reconstruction

## Environment Set up
Using Habitat Simulation Environment and Replica Dataset to create a navigation simulation environment.

## Requirements
OS : Ubuntu Desktop 18.04, 20.04
Anaconda
Python 3.7 ( You can use conda to create new environment )

## Installation

### Setting ssh
(1) ssh-keygen -t rsa  
(2) cat ~/.ssh/id_rsa.pub 
(3) Go to your github account and add the ssh keys.

### Clone the repos and Create & Setup the Environment
(1) git clone git@github.com:HCIS-Lab/pdm-f23.git 
(2) cd pdm-f23/hw0
(3) git submodule update --init --recursive
(4) conda create -n habitat python=3.7 (assuming you've set up anoconda)
(5) conda activate habitat

### Download dataset
(1) Download dataset from: https://drive.google.com/file/d/1zHA2AYRtJOmlRaHNuXOvC_OaVxHe56M4/view 
(2) Put it under the directory under the foder "replica_v1"

### Compile
(1) cd pdm-f23/hw0
(2) pip install -r requirements.txt
(3) cd habitat-sim && pip install -r requirements.txt && python setup.py  install --bullet --headless && cd ..
(4) cd habitat-lab && pip install -r requirements.txt && python setup.py develop && cd ..

## Preparation
(1) Follow the instruction of to setup the simulation environment Habitat and download the Replica dataset.
(2) Put all the files (the data set, bev.py, load.py ,reconstruct.py into the folder pdm-f23/hw1)

## BEV projection
(1) Run the code "bev.py", the program will open a window a of bird eye view picture. Click on the picture, the program will mark red dots on the position you clicked.

(2) Press any key, the program will continue, and show the projection area in the front view image.

(3) Press any key to exit the code.

(4) First projection results
![image](https://github.com/timmy168/View-Projection-and-3D-Reconstruction/blob/main/bev_result_1.png)

(5) Second projection results
![image](https://github.com/timmy168/View-Projection-and-3D-Reconstruction/blob/main/bev_result_2.png)

## 3D Scene Reconstruction
(1) Run the code "load.py" to collect the data, using the key board to control the robot moving in the simulate scene.

(2) To reconstruct the scene, execute the "reconstruction.py" code. While the program is running, it will provide updates on the total number of pictures being processed, including the currently processed picture. Additionally, it will display the time taken for both global registration and ICP for each picture. Upon completion, the code will print the total reconstruction time and the mean L2 distance.

(3) Users can customize the reconstruction process by providing arguments to the code. For instance, to reconstruct the first floor using the implemented ICP method, you can run the following command in the terminal:

(4) python reconstruct.py -f 1 -v my_icp 
(This command allows you to specify the floor level ("-f 1") and the version of ICP to use ("-v my_icp") for the reconstruction process.)

(5) First floor reconstruction result
![image](https://github.com/timmy168/View-Projection-and-3D-Reconstruction/blob/main/first_floor.png)

(6) Second floor recondstruction result
![image](https://github.com/timmy168/View-Projection-and-3D-Reconstruction/blob/main/second_floor.png)

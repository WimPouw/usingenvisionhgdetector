# Using Envision's Automatic Hand Gesture Detection PyPi package (envisionhgdetector)

<br>
<div align="center">Wim Pouw (wim.pouw@donders.ru.nl), Bosco Yung, Sharjeel Shaikh, James Trujillo, Gerard de Melo, Babajide Owoyele (Babajide.Owoyele@hpi.de) </div>

<img src="Images/envision_banner.png" alt="isolated" width="300"/>

<img src="Images/ex.gif"  width="300"/>

<img src="Images/dashboard.gif" alt="isolated" width="300"/>

## Info
In the following notebook, we are going to use an envisionbox python package. This package is called "envisionhgdetector" and contains functions to automatically annotate gesture, to perform kinematic analysis, and to produce a visualization dashboard. In some other envisionbox module on training a gesture classifier we exhibited an [end-to-end pipeline](https://github.com/WimPouw/envisionBOX_modulesWP/tree/main/UsingEnvisionHGdetector_package) for training a model on particular human behaviors, e.g., head nodding, clapping; and then producing some inferences on new videos.  We also already presented how to do DTW analyses for exploring gesture similarity embedding spaces [embedding spaces](https://envisionbox.org/embedded_Gesture_kinematic_spaces.html), and we have an introduced [dashboards](https://envisionbox.org/embedded_dynamicvisualizer.html) for visualizing gestures alongside static data. This package builds on this work.

Firstly we have trained a convolutional neural network to differientate no gestures, self-adaptors (or non-communicative "move" actions), and a co-speech gesture. We do this based on the SAGA dataset, the Zhubo dataset, and the TED M3D dataset. Given that we have trained it on a bit of variability in terms of datasets and angles, and more than 9000 gestures, we can use this gesture detector to a little bit more varied settings than we could do would we have trained on a single dataset.

Now, don't get too excited! The performance is not extraordinary or anything, and it still awaits proper testing and further updating with better trained models (we are working on it...). Currently not differientating types of gestures (as far as that is possible; we are working on it...). But it is good enough for some purposes to have a quick pass over on a set of videos and get some prominent gestures out. Once we have the gestures, we can do all kinds of other interesting things, e.g., generate gesture kinematic statistics, or generate gesture networks. But now all automatically!

## Preprint (FORTHCOMING)
For more information we will refer to a preprint here. Still under development.

## Package info
https://pypi.org/project/envisionhgdetector/

### What does envisionhgdetector do
* It tracks upper body, hands, and face landmarks (generating 29 features)
* It makes an inference based on 25 frames of data, whether it labels no gesture (default implicit label), gesture (label: Gesture), or some kind of movement that is not a gesture (label: Move).
* It outputs a labeled video, an ELAN file, a confidence timeseries, and a gesture segment list (with labels and start and end times).
* It then allows you to retrack the gestures with metric pose world landmarks, which allows us to compare gestures as theire positions are given in meters rather than pixels
* Then we compute kinematic features, produced DTW distances between the gestures
* Then we create a visualization dashboard that summarizes the gesture kinematics

## Installation
It is best to install in a conda environment. 

conda create -n envision python = 3.9

conda activate envision

Then proceed: 

pip install -r requirements.txt

## Errors?
1. Make sure you c++ redistributables installed for tensorflow to work: https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170#latest-microsoft-visual-c-redistributable-version

## Citation
If you use this package, please cite:
* Pouw, W., Yung, B., Shaikh, S., Trujillo, J., de Melo, G., & Owoyele, B. (2024). envisionhgdetector: Hand Gesture Detection Using a Convolutional Neural Network (Version 0.0.5.2) [Computer software]. https://pypi.org/project/envisionhgdetector/

### Citations for the packages and datasets, and work that this builds on
Original Noddingpigeon Training code:
* Yung, B. (2022). Nodding Pigeon (Version 0.6.0) [Computer software]. https://github.com/bhky/nodding-pigeon

Zhubo dataset (used for training):
* Bao, Y., Weng, D., & Gao, N. (2024). Editable Co-Speech Gesture Synthesis Enhanced with Individual Representative Gestures. Electronics, 13(16), 3315.

SAGA dataset (used for training)
* Lücking, A., Bergmann, K., Hahn, F., Kopp, S., & Rieser, H. (2010). The Bielefeld speech and gesture alignment corpus (SaGA). In LREC 2010 workshop: Multimodal corpora–advances in capturing, coding and analyzing multimodality.

TED M3D:
* Rohrer, Patrick. A temporal and pragmatic analysis of gesture-speech association: A corpus-based approach using the novel MultiModal MultiDimensional (M3D) labeling system. Diss. Nantes Université; Universitat Pompeu Fabra (Barcelone, Espagne), 2022.

MediaPipe:
* Lugaresi, C., Tang, J., Nash, H., McClanahan, C., Uboweja, E., Hays, M., ... & Grundmann, M. (2019). MediaPipe: A framework for building perception pipelines. arXiv preprint arXiv:1906.08172.

DTW:
* Giorgino, T. (2009). Computing and visualizing dynamic time warping alignments in R: the dtw package. Journal of statistical Software, 31, 1-24.

Soft-DTW:
* Cuturi, M., & Blondel, M. (2017, July). Soft-dtw: a differentiable loss function for time-series. In International conference on machine learning (pp. 894-903). PMLR.

Creating Elan Files (and a good paper on classification on gestures)
* Ienaga, Naoto, Alice Cravotta, Kei Terayama, Bryan W. Scotney, Hideo Saito, and M. Grazia Busa. "Semi-automation of gesture annotation by machine learning and human collaboration." Language Resources and Evaluation 56, no. 3 (2022): 673-700.

Kinematic features & DTW
* Trujillo, J. P., Vaitonyte, J., Simanova, I., & Özyürek, A. (2019). Toward the markerless and automatic analysis of kinematic features: A toolkit for gesture and movement research. Behavior Research Methods, 51, 769-777.
* Pouw, W., & Dixon, J. A. (2020). Gesture networks: Introducing dynamic time warping and network analysis for the kinematic study of gesture ensembles. Discourse Processes, 57(4), 301-319.
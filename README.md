<h1 align="center">Driving Assistance System in GTA V</h1>

## :innocent: Motivation
We all enjoy playing GTA games be it for mission, online or for the open world experience. In recent times, it has become famous in computer vision community to show some concepts w.r.t to autonomous driving. In this repo, I try to add some assisted driving features with the use of computer vision in Python.

## :framed_picture: Some Screenshots

![](https://github.com/SahilChachra/ADAS_GTAV/blob/main/assets/adas_ss_1.png)
![](https://github.com/SahilChachra/ADAS_GTAV/blob/main/assets/adas_ss_2.png)

## :star: What is actually happening
So, the vehicle chosen is a truck (as assistive breaking makes more sense in highway for trucks in case driver doesn't reacts in time). The horizontal line which you see is a reference line from where distance (pixel distance) is measured w.r.t detected objects. For now breaks are applied only if a person, car or truck comes very close to the ego vehicle. Above the bounding box you see name of the class and the distance (in pixels). Also, the car is NOT driving itself, the user drives it and where necessary the model's output decide the assistive breaks. (Tried to make the car drive on it's own inside the lane using OpenCv, seriously results weren't good xD)

## :key: Features
<ol>
    <li>Automatically break/slow down if the car ahead of yours is very close</li>
</ol>

## :eyes: Future add-ons
<ul>
    <li>Use depth maps to measure distance instead of pixel distance</li>
    <li>Automatically stop the truck if traffic light is red</li>
    <li>Improve/add lane detection (gtav_laneDetect is not accurate hence cannot drive automatically)</li>
    <li>V2V communication (Can't be done in 'Story mode')</li>
</ul>

## :dizzy: How to use?
<ol>
    <li>Start GTA V and enter story mode. Get a truck and change camera to First-per view (by pressing V) (preferred)</li>
    <li>In settings, change the resolution to 800x600 and place the window on top-left corner of your screen</li>
    <li>Clone the repo and install dependencies (requirements.txt provided)</li>
    <li>Run od_gtav.py and you will see a OpenCv window popping up. Enjoyy...</li>
</ol>

## :heart: Reference
Inspired by [Sendex](https://github.com/Sentdex)

## :hammer_and_wrench: Extras
Readme will be updated with more info...

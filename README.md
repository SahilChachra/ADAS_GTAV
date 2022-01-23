<h1 align="center">Assisted Driving in GTA V</h1>

## :innocent: Motivation
We all enjoy playing GTA games be it for mission, online or for the open world experience. In recent times, it has become famous in computer vision community to show some concept w.r.t to autonomous driving. In this repo I try add some assisted driving features with use of computer vision in Python

## :hourglass: Some Screenshots

![](https://github.com/SahilChachra/ADAS_GTAV/blob/main/assets/adas_ss_1.png)
![](https://github.com/SahilChachra/ADAS_GTAV/blob/main/assets/adas_ss_2.png)

## :star: What is actually happening
So, the vehicle chosen is a truck (as assistive breaking makes more sense in highway for trucks in case driver doesn't reacts in time). The horizontal line which you see is a reference line from where distance (pixel distance) is measured w.r.t detected objects. For now breaks are applied only if a person, car or truck comes very close to the ego vehicle. Above the bounding box you see name of the class and the distance (in pixels). Also, the car is NOT driving itself, the user drives it and where necessary the model's output decide the assistive breaks. (Tried to make the car drive on it's own inside the lane using OpenCv, seriously results weren't good xD)

## :key: Results
<ol>
    <li>Automatically break/slow down if the car ahead of yours is very close</li>
</ol>

## :eyes: Future add-ons
<ol>
    <li>Use depth maps to measure distance instead of pixel distance</li>
    <li>Automatically stop the truck if traffic light is red</li>
    <li>Improve/add lane detection (gtav_laneDetect is not accurate hence cannot drive automatically)</li>
    <li>V2V communication (Can't be done in 'Story mode')</li>
</ol>

## :heart: Reference
Inspired by [Sendex](https://github.com/Sentdex)
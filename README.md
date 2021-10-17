![Logo](web/public/favicon.ico?raw=true) We're Team Arson and we're using 
the power of predictive modeling to combat wildfires.

![Screenshot](</SCE-Hacks-png/SCEhacks Arson Project.jpg>)

## Inspiration
There’s been a lot of wildfires in California in recent years, and a lot of 
the most recent wildfires have been uncontained. The government does not 
have the capacity to deal with such a huge amount of wildfires so it has to 
pick and choose which fires to bring under control. This picking and 
choosing should be done based on wildfire and wind data in order to minimize 
the damage caused by wildfires We should also prioritize mitigating fires 
that can spread across many counties/ have a large chance of spreading 
further

## What it does
Our project consists of a web app with an interactive map. We represent our wildfire as a MDP and determine how at risk counties are based on the fire location(s). 

## How we built it
We split the project into 2 main parts: web app and AI

### Website
- Built with React, and uses React-Plotly.js for generating dynamic and 
user-friendly maps of 10 local counties.
- The GeoJSON of counties were collected from https://eric.clst.org/tech/usgeojson/
- Uses Bootstrap 5 for improving UI
- Updates map data by calling a predictive model in an AWS Lambda function which uses wind data to assess fire risk.
- Deployment: http://sce-hacks-arson-deployment.s3-website-us-west-1.amazonaws.com/

### Artificial Intelligence
- Represent the wildfire as a MDP (Markov Decision Process)
    - States: Counties
    - Actions: Traversing Counties
    - Probability distribution: generated from wind data
    - Transition Model: generated from wind data
    - Reward function: Uniform for every county burned (prone to change if 
    scaled up)
- Use bellman equation to iterate through counties and propagate the fire
    - Utility values ranging between 0 and 1 represent how at risk a county
    is
    - ![Screenshot](</SCE-Hacks-png/bellman-iteration.png>)
    - Run until utility values reach equilibrium or until 100 iterations are 
    run
    - Gamma = 0.8
- Represent the map as a graph
    - Counties are nodes
    - Wind speeds are edges
    - Assign each county with a risk (for reward function)
    - Spawn fires on specific counties

## Challenges we ran into
Our project has a pretty large scope. We needed to develop a model and 
integrate it with a web app. This required extensive knowledge on AWS 
utilities and crisp communication between team members. The machine learning 
portion of this hackathon was difficult as we had to decide on what type of 
model to use for the wildfire and how to assign reward and utility values. 

## Accomplishments that we're proud of
We were able to integrate the web app with the model really quickly. This 
was surprising since usually connecting the pieces together will have a lot 
of bugs. It was also Austin, Raaj, and Romuz's first hackathons and this was
a fairly complex project compared to a standard web app.

## What we learned
This hackathon was a first for many of us. This was the first time any of us 
had implemented a machine learning model and connected it to a web app. 

## What's next for Arson
- Scale up to entire California to generate a better map during wildfire 
season
- Generate more accurate Reward values for each county burned
- Incorporate type 2 rewards based on R(state, action)
    - Wildfire gets bigger as it burns more land
    - Wildfire gets smaller in the presence of firefighters
- Automatically train and deploy models by integrating real-time data for 
wind and wildfires



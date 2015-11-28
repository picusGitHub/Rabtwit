# Rabtwit
Rabtwit is a Python tool for hashtag hijacking with fun on Twitter. It sends lovely (rab)tweets filled with a random Google image of cute bunnies (customizable) and randomly chosen hashtags from a file. The hashtag #rabtwit is added to every tweet to recognize normal tweets from (rab)tweets. The posting frequency is customizable.
Let's flood twitter with tenderness ;)

## Warning
Do not use your personal information/Twitter account with this program.

## Requirements
The following python modules are needed:
* `requests`
* `simplejson`

## Setup
* Edit `hashtags.txt` to add/edit the hashtags to use for tweets
* Edit `searchterms.txt` to add/edit the search terms for images

## Usage
`python rabtwit.py -u <Twitter username> [--tmin=<min minutes between tweets> --tmax=<max minutes between tweets>]`

If not specified, `<min time between tweets>` is set to 5 and `<max time between tweets>` is set to 10. The actual time between tweets is chosen randomly between the two numbers.


#Contributors
picus and all the rabbits out there. 

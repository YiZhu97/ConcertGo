# ConcertGo

## Table of Contents

1. [Motivation](README.md#motivation)
1. [File Overview](README.md#file-overview)
1. [Architecture](README.md#architecture)
1. [User Guide](README.md#user-guide)
1. [Contact Information](README.md#contact-information)

## Motivation

The pain of finding parking space in increasingly overcrowded cities is shared by every car owner, especially during busy events such as game and concert. Many concert-goers experience a common frustration when they arrive early at the venue yet still cannot find an available parking spot, and end up spending much more time on the parking and less on enjoying the show. Needless to say, this can be a major buzzkill and does not have an easy solution.

ConcertGO is a platform that provides concert-goers with nearest parking lot options and recommendation on when they should arrive prior to the concerts so they can find a parking space using data analytics. It calculates the recommendation time for each parking lot based on past parking data during past concert events that happened within a 2 kilometer radius. ConcertGO not only helps users with their parking problem, it also sheds light on how crowded events like concerts can affect the performance of parking lots.


## File Overview

### backend

`backend/` contains all the files that are in charge of retrieving data, creating the database, calculating the recommendation time based on past events, monitoring future events, updating the database and updating the recommendation time, etc.


#### data_gen.py and script.py
`data_gen.py` and `script.py` collect concert data in JSON files through Songkick API requests and write the data into MySQL database. Since the past concert data can only be collected by specifying the Event_ID or Artist_ID of that event, and both IDs are not provided to API users in an easily collectable way, the approach here is to iterate through all possible Artist IDs from 1 to 10,000,000 and distribute the tasks on multiple EC2 instances to speed up the process. All the data collected contain the event_id, name of the event, datetime of the event, location of the event in coordinates and the city where the event took place.

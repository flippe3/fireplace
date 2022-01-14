# Design decisions

This document provides further information on the decision process of the project. It covers why we used which methods, tools and libraries and which external APIs.

## Napkin sketch
![Napking sketch](https://github.com/flippe3/fireplace/blob/main/references/napkin_sketch.jpg?raw=true)
## Idea
We decided to not do the exemplary project but to come up with an idea on our own. When thinking about a good idea for a dynamic website, I needed to think about my recent problem to find a fireplace in Luleå with wood, because my friends and I nearly always chose the same. It would be cool, to easily see which fireplaces exist and whether they are free and have wood.

After having this broad idea, we narrowed it down to a specific task namely to present users locations of fireplaces. To do this in a visual way, because just listing longitude and latitude values seems hard to understand for a human, we decided to base our application on a fullscreen map.

## Python
When creating a website, a javascript framework is probably the most intuitive first choice. Nevertheless, over the last few years, python gained a lot of popularity. We decided to use python because we wanted to try how good it really is for our website and how easy it is to connect a backend in python with a nice frontend. This is mainly reasoned because we both used python in the past and are more familiar with it than with javascript. Nevertheless, we never created a full website with a frontend, but mainly backends with it. This project was the ideal opportunity to try it out.

## Flask
Flask is a simple and lightweight framework for python. Thereby, it is the ideal choice for our project. We want to build a website from scratch and do not bother with too many additional functionalities that are not necessary. Therefore the very simple basis of flask is very nice for the project. Nevertheless, flask can also be very powerful. It starts very simple, but pretty much everything is possible to implement if necessary.

## Werkzeug
Werkzeug is a web server gateway interface or more commonly known as a WSGI library. Werkzeug is what flask implements to provide the simple and easy to use routing out of the box. Yet part of our task was to implement a low-level version of our API so we chose to use werkzeug. In werkzeug, we had to do our own routing and change some parts which made it a bit more tedious and therefore we chose to only do this for the simulator communication API calls and have the rest of the API work with the standard high-level that comes with flask. 

## Database
When creating a dynamic web system that relies on data, it is always necessary to manage it in some way and the most intuitive one is to use a normal database. Other approaches like NoSQL databases or the amount of data is not too much to be handled by one computer and the amount of requests is also limited. Therefore, we do not need any advanced concepts here but can use a normal relational database. Therefore we also have ensured, that all transactions follow the ACID concept which makes it much easier for us to work with the data.

For the question, which SQL database, we use, we went with MySQL because it is an open-source SQL database that is widely used, well documented and has an integration for python. Therefore, it seems to be an ideal option for us. Those criteria of course also meet for other databases so this decision is kind of arbitrary and there is not only one right option.

### Entities

The two main entities in our database are the table with users consisting of names and roles and the table with fireplaces consisting of the location and additional attributes like whether they have wood. Both entities also have an id. For the fireplaces, it is an artificially created one and for the users, it is just their name. The name could be taken, because it is not supposed, that two users with the same username exist. For fireplaces, it would be ok if two fireplaces with the same name exist.

### Dataflow
![Dataflow](https://github.com/flippe3/fireplace/blob/main/diagramdatabase.png?raw=true)
If data is inserted into the database or taken from the database, this works with the database. So in the first step, a user would trigger something on his screen. Then our website would process it and create an API call to get the things done. The API would receive the request, establish a connection to the database and would then run the necessary query.

The only exception for this process is the user authentication. For this, the website directly accesses and verifies the login credentials from the database and no API call is done.

## Security

### User login with salt
For our project, there were no requirements on security from the instructions but we still did not want our users' passwords to be directly accessible in plain text. Hence we used the cryptographic [salt](https://en.wikipedia.org/wiki/Salt_(cryptography)) method. So when a user registers on our website we store two attributes, the salt and the hash generated with the salt and the user's password. This then makes us able to check that the password a user logs in with together with the salt is the same as the stored hash. Yet we are never able to see the user's password and since each hash is generated randomly two hashes will never be the same. That means that even if users have the same password users will never share the same hash.

### API securing with jwt
To use all functions of our application, a user needs to be logged in. But that is not enough to secure that nobody is misusing the API. Therefore, the API needs to be protected separately. Otherwise, people could just directly send the requests and thereby ignore the security of our login.

To secure the API, we chose to use the industrial standard jwt. With it, tokens can be created and those tokens are sent with the API requests. The tokens are just available after login and if there is no token sent with an API request or the token is invalid, a user cannot for example create/delete a fireplace.

### API-key securing for the map
Our code can be seen in our GitHub repository. Therefore also our API-key can be seen there. That is of course unfortunate because people could see it there and misuse it. Luckily, Here provides the option to secure the API key by just allowing requests from certain URLs. Therefore it is no problem to store it in Git and to directly start the Jenkins pipeline with the git repository because nobody can misuse it.

## Map API
To use a dynamic map, we decided to use a map API. We do not have a map on our own and downloading one takes a lot of space and effort to manage. With map APIs, it is easy to use the service of the map and to add own features.

While searching for the right map API for our purpose, we mainly found one by google, one by [here](https://www.here.com/) and one by [leaflet](https://leafletjs.com/). We decided earlier, that we are most familiar with python and want to base our project on flask. Additionally, we do not get money for the course. Therefore a free version of an API was necessary. Leaflet is mainly used for javascript and the one by google is expensive. This made the here API favourable. After trying out the API a bit, we quickly realised, that our requirements can easily by fulfilled and that it would be free for our purposes. We also found a very good guide for a python integration and therefore chose the here map API for our website.

## Weather API
Since our entire application is highly dependent on the location of users we wanted to be able to provide accurate weather data to the location of every fireplace. Hence we found a global [weather api](https://www.weatherapi.com/) where we could get accurate data for all of our fireplaces. This API also had good documentation and was simple to integrate with python. The only problem was that we needed to use an API key, we were not able to protect the API key in a similar way to the Here API and hence we needed a new solution to not store the key publicly in GitHub. We looked at git hooks and also linters but the easiest solution for our problem was to store the API key in a file on the server. Hence we only needed to read that file when loading our weather API and this solved the problem.

## Jenkins
We used Jenkins so that we would not be required to log into our server and then pull our code to the server every time. We just needed to log into Jenkins and build our project and that would pull the code to our server and run a quick test. Hence simplifying our development process. Jenkins could further be used for unit-testing and more advanced features but for this project we did not use these features.

## Simulator
In the project description, we needed to add a simulator that was running on the server at all times. We needed a simulator that fit our project and hence we added created a simulator that took in the weather data from our weather API and generated a percentage value of how likely it was that someone was at the fireplace. This, of course, would generate very similiar values if this was updated once every second, therefore we added some noise in form of a normal distribution. This then runs as a server at all times and saves the value once every second. To not overload the weather API with API-requests we also made sure to only update the weather every 10 minutes. When anyone makes an API-request to get our simulated data all that our API then needs to do is look at the latest entry in the saved file.

## Frontend (Bootstrap)
Design is a very relevant aspect to have an intuitive user interface and to make the experience of usage nice. For this reason, we decided to use Bootstrap, which provides a lot of basic designs and functionality for our needs. With it, we could choose one of the basic templates and use them for all our sites in the front end. We believe the result to be quite nice for not having the work of creating a whole design on our own. Therefore we could concentrate on the API and other functions. Additionally, the decision of putting a map in the center of our application created a nice first impression

## Grade Discussion
We both saw the course as an opportunity to try out as many different tools and techniques as possible. Therefore, we already started in the beginning to go our own path and to decide against doing the exemplary project and came up with an idea of our own. This was a very nice experience because we actually did everything from scratch and in every step of work, we actually had to decide, what we would do next and which technologies we wanted to use. Nevertheless, this also involved a lot of work for every task. The discussion, getting of information took a lot of time to have sophisticated decisions for every path. This stopped us to go too deep in some aspects.

Overall we think that a four would be a reasonable grade regarding our additional work by finding and implementing an idea of our own and because we tried using a lot of different tools.

The last thing to mention is, that our work distribution was very equal and we usually met each other to discuss the further progression and the splitting of the tasks. It was a nice atmosphere and fun to work together and we would suggest receiving the same grades.
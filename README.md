# sqlalchemy-challenge
Module_10_Challenge_ SQLalchemy

This challenge consists of using SQLAlchemy and Python libraries to analyze the climate for a holiday vaction in Hawaii.
After analyzing that data I was then tasked with creating a Flask API to reflect the database schema.

In the 'climate_starter.ipynb' you can see the csv files provided in the 'Resources' folder being reflected using SQLAlchemy queries.
I then designed a query to retreive the last 12 months of precipitation data and then used matplotlib to plot the results.
I then designed a query to find the most active stations in Hawaii. Using the data I the queried the last 12 months of temperature data into a histogram.

In the 'app.py' file I created a Flask API that had routes that referenced tables in the 'climate_starter.ipynb' file.
All of the references were applied in the '@app.routes' and would return in a JSON format.
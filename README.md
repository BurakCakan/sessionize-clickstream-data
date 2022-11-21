# Xccelerated-de-assignment-submission

## Step 1: Sessionize

This step consists of few actions: 

      a. Reading data from a Web API:** 
        - In this assesment, I will use 'https://storage.googleapis.com/xcc-de-assessment/events.json' as datasource.  
        - dataPrep.py file has some functions which are used to get a JSON object with multiple arrays, 
          transform it into a pandas Dataframe object, do manipulations on data.
        - Records that have a null CustomerId value are eliminated in validation() function of dataPrep.py.

      b. Sessionize:
        - Sessionization is done in calculate_sessionid() function of dataPrep.py. Because it is an industry standard 
          accorging to Google Analytics, 30 minutes of time interval for unavailability between logs for a customerId is taken as session interval. 
          (https://support.google.com/analytics/answer/2731565?hl=en#zippy=%2Cin-this-article)

      c. IO operations to PostgreSQL:
        - Writing and reading operations are executed on postgreConnector.py file. 
        - Before running, postgresql latest version should be downloaded to the computer (docker, website etc.)
        - pg_auth() function should be updated according to the connection string of other users

## Step 2: Publish your results

      a. Calculating metrics on PostgreSQL:
        
        Aim is to calculate the metrics of median visit before order and median session duration minutes before order. 
        These metrics are calculated on postgresql (num_session_before_order.sql and time_until_order.sql)
        And the final table is created to combine the results of both metrics (results.sql)
        API response will be derived from results table.

        Assumptions on the calculation of metrics
        
        num_session_before_order: 
            - If an order happens in a session, counting the previous sessions without placed_order event 
              excluding the current session. 
            - For example, if placed_order came in session 7 for a ustomer at first time
              number of sessions before order equals 6. 
            - For example, if placed_order came in session 8 but there is also an order in session 7 for a customer
              number of sessions before order equals 0. 

        time_until_order
            - If an order happens in a session, adding the number of seconds spent in the previous sessions 
              without placed_order event excluding the current session. 
            - To exclude sessions with placed order in calculations, I assigned 0 second as session time in query.
            - Logic is the same with num_session_before_order.

      b. Publishing results on API
        
        FastAPI is used for publishing results on API payload.
        To run the API;
            - Go to the right folder which has the app = FastAPI() command on terminal window 
              (Xccelerated>src>main>python for this case)  
            - Run the command below (if app variable is not in main.py change main:app part as filename:app)
              $ uvicorn main:app --reload
            - After running the command above, the terminal would be like below
        
![Terminal](../../Pictures/Photos Library.photoslibrary/resources/derivatives/masters/5/5980B7EA-FCE6-45BA-A591-70E08E56A7ED_4_5005_c.jpeg)

            - On terminal, there is IP:Port information. Take this and add GET command as IP:Port/mertics/order

![API Payload](../../Pictures/Photos Library.photoslibrary/originals/8/8314922C-D4CA-44F5-9CFA-0DA7D4946B28.jpeg)

            - According to these results (0 and 0), whenever customers visit they give an order!

            - Besides that, Swagger UI can be used by writing IP:PORT/docs (27.0.0.1:8000/docs) to test the API

![Swagger UI - GET Test](https://github.com/BurakCakan/Xccelerated-de-assignment-submission/blob/f89d1b5a35fc56f8b57f29afc052211e8e270c16/swagger.jpg)


## Step 3: Plan for the future

        a. "Assume the dataset is static, rather than data coming in on a more regular (hourly) basis;"

            There are a few ways to handle this kind of situation:

            - This python script should be transformed into a job and this job should be scheduled with a job scheduler 
              (like Apache Airflow etc.) after a few change (running all queries inside python script).
            - As a more appropriate way when considered the increasing size of data, using distributed data procession 
              tools should be adopted
            - For micro batch data pipeline, we can use spark instead of pandas. Data should be extracted from source 
              to Apache Kafka by using Apache Ni-fi or a Spark merger job. Then all calculations should be executed 
              on spark/pyspark instead of pandas dataframe. To have a streaming data pipeline, some tools 
              (Spark Streaming, Apache Flink, Kafka Streaming etc.) could be used but a micro batch pipeline like above 
              is enough for hourly basis. If the requirement changes as near real time data, this option 
              could be reasonable and logical.

        b. "Don't attempt to sessionize anonymous events by using their ip address or user-agent;"

            - A lookup table could be created to keep customerId and ip information. If null value in customerId occurs 
              and ip column is not null, we can look for the customerId value of this ip address.
            - For the ip addresses which have no customerId information in advance, dummy customerId could be assigned 
              in the lookup table. In that way, anonymous sessions could be tracked

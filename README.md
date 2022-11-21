# Xccelerated-de-assignment-submission

## Step 1: Sessionize

This step consists of few actions: 

    **a. Reading data from a Web API:** 
        - In this assesment, I will use 'https://storage.googleapis.com/xcc-de-assessment/events.json' as datasource.  
        - dataPrep.py file has some functions which are used to get a JSON object with multiple arrays, transform it into a pandas Dataframe object, 
          do manipulations on data.
        - Records that have a null CustomerId value are eliminated in validation() function of dataPrep.py.

      b. Sessionize:
        - Sessionization is done in calculate_sessionid() function of dataPrep.py. Because it is an industry standard accorgin to Google Analytics,
          30 minutes of time interval is taken as session interval. (https://support.google.com/analytics/answer/2731565?hl=en#zippy=%2Cin-this-article)

      c. Writing to PostgreSQL:


## Step 2: Publish your results

      a. Calculating metrics on PostgreSQL:


      b. Publishing results on API

![](../../Pictures/Photos Library.photoslibrary/resources/derivatives/masters/5/5980B7EA-FCE6-45BA-A591-70E08E56A7ED_4_5005_c.jpeg)


![](../../Pictures/Photos Library.photoslibrary/originals/8/8314922C-D4CA-44F5-9CFA-0DA7D4946B28.jpeg)


## Step 3: Plan for the future

a. "Assume the dataset is static, rather than data coming in on a more regular (hourly) basis;"

There are a few ways to handle this kind of situation:

This python script should be transformed into a job and this job should be scheduled with a job scheduler (like Apache Airflow etc.) after a few change (running all queries inside python script).
As a more appropriate way when considered the increasing size of data, using distributed data procession tools should be adopted

For micro batch data pipeline, we can use spark instead of pandas. Data should be extracted from source to Apache Kafka by using Apache Ni-fi or a Spark merger job. Then all calculations should be executed on spark/pyspark instead of pandas dataframe.
To have a streaming data pipeline, some tools (Spark Streaming, Apache Flink, Kafka Streaming etc.) could be used but a micro batch pipeline like above is enough for hourly basis. If the requirement changes as near real time data, this option could be reasonable and logical.

b. "Don't attempt to sessionize anonymous events by using their ip address or user-agent;"
A lookup table could be created to keep customerId and ip information. If null value in customerId occurs and ip column is not null, we can look for the customerId value of this ip address.
hiç gelmeyen customerid için iplere dummy customerid atanıp o şekilde takip edilebilir
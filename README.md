# apache-spark-on-lambdas
apache-spark-on-lambdas
![Screenshot 2023-11-05 at 9 53 20 AM](https://github.com/soumilshah1995/apache-spark-on-lambdas/assets/39345855/c389e77e-4bb6-4fbe-8828-7d18b09e6d22)



# Steps 

# Step 1:  Upload Code to S3 
```
Upload File accommodations.csv sample-accommodations-to-hudi.py to AWS S3 Bucket 

```

# Step 2:  Edit the Docker File and change this env var
```
ENV AWS_ACCESS_KEY_ID="XX"
ENV AWS_SECRET_ACCESS_KEY="XXX"
ENV AWS_REGION="us-east-1"
```

# Step 2:  Build Docker Image 
```
docker build --no-cache --build-arg FRAMEWORK=HUDI -t sparkonlambda-spark-on-lambda-image-builder .

```



# Step 3: Run Docker locally 
```
docker run -p 9000:8080 sparkonlambda-spark-on-lambda-image-builder:latest
```

# Step 4: Fire Lambda Functions 

```
curl --location 'http://localhost:9000/2015-03-31/functions/function/invocations' \
--header 'Content-Type: text/plain' \
--data '{
    "input_path": "s3a://XXXX/accommodations.csv",
    "output_path": "s3a://XXX/silver/",
    "BUCKET_NAME": "XXX",
    "SCRIPT_PATH": "sample-accommodations-to-hudi.py"
}'

```


## Acknowledgments

This project is based on the work of John Cherian, Emerson Antony, and Kiran Anand as originally published in the article "Spark on AWS Lambda: An Apache Spark runtime for AWS Lambda" on October 30, 2023, which can be found [here](https://aws.amazon.com/blogs/big-data/spark-on-aws-lambda-an-apache-spark-runtime-for-aws-lambda).

We would like to extend our gratitude to the original authors for their contributions.



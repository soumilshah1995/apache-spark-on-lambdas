import boto3
import sys
import os
import subprocess
import logging
import json

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def s3_script_download(s3_bucket_script: str, input_script: str) -> None:
    s3_client = boto3.client("s3")

    try:
        logger.info(f'Now downloading script {input_script} in {s3_bucket_script} to /tmp')
        s3_client.download_file(s3_bucket_script, input_script, "/tmp/spark_script.py")
        print("Download complete ****** ")

    except Exception as e:
        logger.error(f'Error downloading the script {input_script} in {s3_bucket_script}: {e}')
    else:
        logger.info(f'Script {input_script} successfully downloaded to /tmp')


def spark_submit(s3_bucket_script: str, input_script: str, event: dict) -> None:
    for key, value in event.items():
        os.environ[key] = value
    try:
        logger.info(f'Spark-Submitting the Spark script {input_script} from {s3_bucket_script}')
        subprocess.run(["spark-submit", "/tmp/spark_script.py", "--event", json.dumps(event)], check=True,
                       env=os.environ)
    except Exception as e:
        logger.error(f'Error Spark-Submit with exception: {e}')
        raise e
    else:
        logger.info(f'Script {input_script} successfully submitted')


def lambda_handler(event, context):
    logger.info("******************Start AWS Lambda Handler************")
    print("event")
    print(event)

    bucket_name = event.get('BUCKET_NAME', '')
    script_path = event.get('SCRIPT_PATH', '')
    os.environ['INPUT_PATH'] = event.get('INPUT_PATH', '')
    os.environ['OUTPUT_PATH'] = event.get('OUTPUT_PATH', '')

    s3_script_download(bucket_name, script_path)

    # Set the environment variables for the Spark application
    spark_submit(bucket_name, script_path, event)



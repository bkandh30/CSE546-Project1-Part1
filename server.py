import os
import boto3
from flask import Flask, request, Response

S3_BUCKET = "1229592821-in-bucket"
SIMPLE_DB_DOMAIN = "1229592821-simpleDB"
REGION = "us-east-1"

s3 = boto3.client("s3", region_name=REGION)
sdb = boto3.client("sdb", region_name=REGION)

# Initialize Flask app
app = Flask(__name__)

@app.route("/", methods=["POST"])
def upload_file():
    try:
        # Ensure a file is provided
        if "inputFile" not in request.files:
            return Response("No file provided", status=400, mimetype="text/plain")

        # Get the uploaded file
        inputFile = request.files["inputFile"]
        imageName = inputFile.filename.split(".")[0]
        imageNameWithExtension = inputFile.filename

        # Upload file to S3
        s3.upload_fileobj(inputFile, S3_BUCKET, imageNameWithExtension)

        # Query SimpleDB for classification results
        classification_query = f"SELECT Results FROM `{SIMPLE_DB_DOMAIN}` WHERE itemName() = '{imageName}'"
        response = sdb.select(SelectExpression=classification_query)

        # Return classification results
        if "Items" in response and response["Items"]:
            prediction = response["Items"][0]["Attributes"][0]["Value"]
            return Response(f"{imageName}:{prediction}", mimetype="text/plain")
        else:
            return Response(f"{imageName}:No prediction found", mimetype="text/plain")

    except Exception as e:
        return Response(f"Error: {str(e)}", status=500, mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

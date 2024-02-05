from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from io import StringIO
from utils import evaluate_NPI_expression
from pymongo import MongoClient
from dtos import Expression
import csv
import os

# read environment variables
user = os.environ.get("MONGO_ROOT_USERNAME")
password = os.environ.get("MONGO_ROOT_PASSWORD")

# create the FastAPI app
app = FastAPI(
   # docs_url=None, # Disable docs (Swagger UI)
   # redoc_url=None, # Disable redoc
)

# allow CORS for the client
app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],
   allow_methods=["*"],
   allow_headers=["*"],
)

# MongoDB connection settings
try:
   mongo_uri = f"mongodb://{user}:{password}@database:27017"
   client = MongoClient(mongo_uri)
except Exception as e:
   raise Exception(f"Failed to connect to MongoDB: {str(e)}")

# set up references to used database and collection
database = client.get_database("NPICalculator")
calculations_collection = database.get_collection("calculations")

# get a greeting
@app.get("/hello")
def read_root(who: str | None = None):
   return f"Hello {who}!" if who else "Hello AYOMI!"

# ! we should use the StreamingResponse object if we're dealing with a lot of data; see https://github.com/tiangolo/fastapi/issues/1277
# get all expressions calculated and their corresponding results in a '.csv' file
@app.get("/calculations")
def get_calculations():
   # read all calculations from database; 
   calculations = calculations_collection.find()

   # put calculations in a list formated to be used with the 'csv' module
   csv_data = []
   for doc in calculations:
      csv_data.append([doc['expression'], doc['result']])
   
   # write CSV data in a buffer
   buffer = StringIO()
   csv_writer = csv.writer(buffer, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
   csv_writer.writerow(['Expression', 'Result'])
   csv_writer.writerows(csv_data)
   
   return PlainTextResponse(
      buffer.getvalue(),
      media_type="text/csv", 
      headers={ "Content-Disposition": "attachment; filename=calculations.csv" } # I don't know if this header is necessary
   )

# post an expression and get its result, store both in a database
@app.post("/calculate")
def calculate(expression: Expression):
   try:
      # calculate the expression
      result = evaluate_NPI_expression(expression.expression)

      # add the expression and its result in the database
      calculations_collection.insert_one({
         "expression": expression.expression,
         "result": result,
      })

      return { "result": result }
   except Exception:
      raise HTTPException(status_code=400, detail="Invalid expression")

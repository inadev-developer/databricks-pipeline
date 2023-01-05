# pyspark functions
from pyspark.sql.functions import *
# URL processing
import urllib
# Check if the AWS S3 bucket was mounted successfully
display(dbutils.fs.ls("/mnt/experiments"))


# File location and type
file_location = "/mnt/experiments/allergies.csv"
file_type = "csv"
# CSV options
infer_schema = "true"
first_row_is_header = "true"
delimiter = ","
# The applied options are for CSV files. For other file types, these will be ignored.
df = spark.read.format(file_type) \
.option("inferSchema", infer_schema) \
.option("header", first_row_is_header) \
.option("sep", delimiter) \
.load(file_location)
display(df)

# Allow creating table using non-emply location
spark.conf.set("spark.sql.legacy.allowCreatingManagedTableUsingNonemptyLocation","true")

# Save the CSV in table format
df.write.format("parquet").saveAsTable("Allergies")
# df.write.format("parque").mode("Overwrite").saveAsTable("Allergies")

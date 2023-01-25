# pyspark functions
from pyspark.sql.functions import *
# URL processing
import urllib

mountPath = "update_mount_path"
# Check if the AWS S3 bucket was mounted successfully
display(dbutils.fs.ls(mountPath))


# File location and type
file_location = mountPath + "/allergies.csv"
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
# df.write.format("parquet").saveAsTable("Allergies")
# df.write.format("parque").mode("Overwrite").saveAsTable("Allergies")

df.write.mode("overwrite").format("parquet").saveAsTable("Allergies")
spark.catalog.refreshTable("Allergies")

# Connect to the database
		USERNAME =  "postgres"
		PASSWORD=  "L3d38L6NlTXFuFnA"
		HOST =  "esis-lite-testing-one-postgres.c69qhpco3e5q.us-east-1.rds.amazonaws.com"
		DATABASE_NAME= 'databricks'
#Postgres Jdbc URL
		jdbcURL = "jdbc:postgresql://{}/{}".format(HOST,DATABASE_NAME)
#Create connection properties with USERNAME & PASSWORD
		connProperties = {
				'user' :USERNAME,
				'password' : PASSWORD
			}
#LOAD Postgraql Driver
	%scala
		Class.forName("org.postgresql.Driver")
#Reading Table from AWS POstgreSQL

		get_df =Spark.read.jdbc(url=jdbcURL ,table= ‘table name’ , properties = connProperties)

		Display(get_df)
#Write DATA Into the Postgres from DATAbricks

# Now get the allergies dataset first. 
		allergies_df = spark.read.format('csv').option('header','true').option('inferschema','true')\
		.load('/mnt/sample-databricks-demo1/allergies.csv')
		display(allergies_df)

		allergies_df.write.jdbc(jdbcURL,table = 'allergies', properties=connProperties)

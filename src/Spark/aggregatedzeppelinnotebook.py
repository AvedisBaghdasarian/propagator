"""
this is a amalgamation of the zeppelin notebook I used to transform the text
data. It is for display purposes, as you need zeppelin running to read
the zeppelin notebook file in a legible way. I did not actually run this .py
file

"""

from pyspark import SparkFiles
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DateType

spark = SparkSession \
    .builder \
    .appName("texttransform") \
    .getOrCreate()



#read in data to dataframe
from pyspark.sql.functions import col
from  pyspark.sql.functions import input_file_name

spark.read.text("s3://arxivmanifest/**/*.txt", wholetext=True).explain()

text_df = spark.read.text("s3://arxivmanifest/**/*.txt", wholetext=True).select(col("value").alias("content")).withColumn("filename", input_file_name())
text_df.cache()


#add the filename to the dataframe
from  pyspark.sql.functions import input_file_name
text_df2 = text_df.withColumn("filename", input_file_name())


#tokenize document
from pyspark.ml.feature import HashingTF, IDF, Tokenizer
from pyspark.sql import SparkSession
from pyspark.ml.feature import CountVectorizer
import time

t = time.time()

#tokenize data
tokenizer = Tokenizer(inputCol="content", outputCol="words")
wordsData = tokenizer.transform(text_df)

print("tokenizer", time.time() - t)
t = time.time()

#hashingTF counts term frequency
hashingTF = HashingTF(inputCol="words", outputCol="rawFeatures", numFeatures=65536)
featurizedData = hashingTF.transform(wordsData)
featurizedData.cache()

print("hashingtf", time.time() - t)
t = time.time()

##you could also use CountVectorizer instead of HashingTF, but at a performance cost

# cv = CountVectorizer(inputCol="words", outputCol="rawFeatures", vocabSize=65536, minDF=2.0)
# model = cv.fit(wordsData)

# print("countvec fit", time.time() - t)
# t = time.time()


# featurizedData = model.transform(wordsData)

# print("countvec transform", time.time() - t)
# t = time.time()


idf = IDF(inputCol="rawFeatures", outputCol="features")
idfModel = idf.fit(featurizedData)

print("idf fit", time.time() - t)
t = time.time()

rescaledData = idfModel.transform(featurizedData)
rescaledData.write.parquet('s3://parquets/data.parquet')

print("idf transform", time.time() - t)
t = time.time()

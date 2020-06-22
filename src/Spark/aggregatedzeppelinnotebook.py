"""
this is a amalgamation of the zeppelin notebook I used to transform the text
data. It is for display purposes, as you need zeppelin running to read
the zeppelin notebook file in a legible way. I did not actually run this .py
files

I have left in the magic commands to denote block breaks
"""

%pyspark
from pyspark import SparkFiles
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DateType

spark = SparkSession \
    .builder \
    .appName("texttransform") \
    .getOrCreate()



%pyspark
from pyspark.sql.functions import col

#read in data to dataframe
spark.read.text("s3://pdflake/**/*.txt", wholetext=True).explain()

text_df = spark.read.text("s3://pdflake/**/*.txt", wholetext=True)
text_df = text_df.select(col("value").alias("content"))


%pyspark
from  pyspark.sql.functions import input_file_name
#add the filename to the dataframe
text_df2 = text_df.withColumn("filename", input_file_name())


%pyspark
from pyspark.ml.feature import HashingTF, IDF, Tokenizer
from pyspark.sql import SparkSession
from pyspark.ml.feature import CountVectorizer
import time


#tokenize document
t = time.time()
tokenizer = Tokenizer(inputCol="content", outputCol="words")
wordsData = tokenizer.transform(text_df2)
print("tokenizer", time.time() - t)
t = time.time()

#Apply hashingTF to count tf
hashingTF = HashingTF(inputCol="words", outputCol="rawFeatures", numFeatures=65536)
featurizedData = hashingTF.transform(wordsData)
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

#compute idf
idf = IDF(inputCol="rawFeatures", outputCol="features")
idfModel = idf.fit(featurizedData)
print("idf fit", time.time() - t)
t = time.time()


rescaledData = idfModel.transform(featurizedData) 
print("idf transform", time.time() - t)
t = time.time()

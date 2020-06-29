# propagator

Propogator is an ETL pipeline to take raw pdf files and turn them into vectorized data, ready for machine learning applications. This is done in a completely scalable way, demonstrated on terrabytes of data.
![Pipeline](/images/pipeline.png)


# How it works

Data starts as tar files in the Arxiv requester-pays bucket. They are copied, extracted, then converted to text with a series of lambda functions, then stored in another s3 bucket. From there, they are loaded into EMR, and transformed into feature vectores with sparks TF-IDF implementation. From there, they are stored as parquet files in s3 for easy retrieval. 

#  Repository Structure

All system code is contained Within `src`, which is split into code that runs in lambda, and code that runs in Spark. Additionally, outside of these folders, there is a python script called `copyscript.py` that is meant to assist you with copying files from a requester pays bucket using `s3api` (for the aws s3 command, the `--request-payer requester` tag does not work, even though in the documentation it says it should). 

within `src`, `Lambda` contains code that is run within lambda functions. `Untar` contains code that is run in a lambda function to untar tar files on scale, and `PdfConverter` contains code that is run in a lambda function to convert pdf files to text files on scale. 

Within `src`, Spark contains Spark code that is run to featurize the text files. You can either run it as a zeppelin notebook from `zeppelinnotebook.json` or as a spark job with the .py file that is made from the contents of the notebook, `aggregatedzeppelinnotebook.py`




# How is it installed?

## Lambda Stack

Lambda stack works on a rolling basis, responding to s3 put events. In essence, it automatically triggers when the tar files are placed in the s3 bucket. [/src/Lambda/untar/untar.py](https://github.com/AvedisBaghdasarian/propagator/blob/master/src/Lambda/Untar/untar.py) is the lambda function that will handle untarring, simply make a new lambda function and replace the default lambda_handler() with that one. Make sure to specify the source and destination buckets you will be using within untar.py. Next configure s3 to send an event notification to untar function when there is a file creation in that bucket. 

Next, create another lambda function with the resources in [/src/Lambda/PdfConverter](https://github.com/AvedisBaghdasarian/propagator/tree/master/src/Lambda/PdfConverter)

For this function, you must create a layer in Lambda containing the PDFMiner module. Once again, enter the source and destination buckets in the lambdafunction.py file. Your source should be the bucket that was untarred to. Once again create an event notification for file creation in the source bucket, sent to this lambda function

The untar lambda function should have 1048MB memory allocated. The `PdfConverter` lambda function should have 256MB allocated.

Finally you have to get the tar files into your own bucket.If you want to use arXiv, you can use copyscript.py to help you copy, since requester pays buckets are a bit tricky to work with. If you don't have tar files, and just have pdfs, you can put them straight into the pdf bucket. 

## EMR

I used zeppelin to run my spark code, but you could just as easily turn this into a regular spark job. I chose a cluster of 16 m4.xlarge instances but its up to you what you use. When creating your cluster, specify the config file [as shown by the docs](https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-spark-configure.html)

The rest of the conifg is up to you, but I got some small benefits from 


`spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version  2 `

`spark.speculation false`

Then import the [zeppelin notebook](https://github.com/AvedisBaghdasarian/propagator/blob/master/src/Spark/zeppelinnotebook.json) into your zeppelin, and specify the source and ouput location. At this point, you can run the notebook to compute.


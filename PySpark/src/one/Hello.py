
if __name__ == '__main__':
    pass
 
from pyspark import SparkConf, SparkContext
import  os 

# Configure the Spark environment
sparkConf = SparkConf().setAppName("WordCounts").setMaster("local")
sc = SparkContext(conf = sparkConf)
 # The WordCounts Spark program
file_path="file:///C:/SOFT/JOB/PySpark/ml-100k/"
rating_data = sc.textFile(file_path+"u.data")
print rating_data.first()
num_rating=rating_data.count()
print "Rating:%d" % num_rating
sc.stop()


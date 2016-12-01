
if __name__ == '__main__':
    pass
 
from pyspark import SparkConf, SparkContext
import  os 

# Configure the Spark environment
sparkConf = SparkConf().setAppName("WordCounts").setMaster("local")
sc = SparkContext(conf = sparkConf)
 # The WordCounts Spark program
file_path="file:///E:/spark/learn/ml-100k/"
rating_data = sc.textFile(file_path+"u.data").map(lambda line :line.split("\t"))
num_rating=rating_data.count()
print rating_data.first()
print "Rating:%d" % num_rating

ratings =rating_data.map(lambda fields:int(fields[2]))
max_ratings=ratings.reduce(lambda x,y:max(x,y))
min_ratings=ratings.reduce(lambda x,y:min(x,y))









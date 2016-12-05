#coding=UTF-8
'''
Created on 2016年12月5日

@author: BuleSky
'''
from pyspark import SparkConf, SparkContext
# Configure the Spark environment
sparkConf = SparkConf().setAppName("WordCounts").setMaster("local")
sc = SparkContext(conf = sparkConf)

from pyspark.mllib.recommendation import ALS, Rating
file_path="file:///C:/SOFT/JOB/PySpark/ml-100k/"

 
rawRatings = sc.textFile(file_path+"u.data").map(lambda line :line.split("\t")[0:3])
 
 
ratings=rawRatings.map(lambda fields:Rating(int(fields[0]),int(fields[1]),int(fields[2])))
 
print ratings.first()
 
model=ALS.train(ratings,50,10,0.01);
userFeaturesCount= model.userFeatures().count()
productFeaturesCount=model.productFeatures().count()
 
print "userCount {0} productCount {1}".format(userFeaturesCount, productFeaturesCount)
 
predicted=model.predict(789, 123)
print predicted
 
userId=789
k=10
topPredict=model.recommendProducts(userId, k)
 
for i in range(0,len(topPredict)):
    print topPredict[i]
    
    
moviesForUser = ratings.groupBy(lambda x : x.user).mapValues(list).lookup(789)
# moviesForUser=ratings.keyBy(lambda ob:ob.user).lookup(789)
# moviesForUser.sort(key=ratings, reverse=False)
print '用户对%d部电影进行了评级'%len(moviesForUser[0])
print '源数据中用户(userId=789)喜欢的电影(item)：'
for i in sorted(moviesForUser[0],key=lambda x : x.rating,reverse=True):
    print  '源数据中用户(userId=789)喜欢的电影(item)：{0}'.format( i.product)

# movies=sc.textFile(file_path+"u.item").map(lambda line:line.split("|")[0:2]).map(lambda line:(int(line[0]),line[1]))
# print movies.toDebugString()
# print movies.take(10)

movies = sc.textFile(file_path+"u.item")
titles = movies.map(lambda line: (int(line.split('|')[0]),line.split('|')[1])).collectAsMap()
print titles[1]
for i,rec in enumerate(topPredict):
    print 'rank:'+str(i)+' \t '+str(titles[rec.product])+' \t'+str(rec.rating)


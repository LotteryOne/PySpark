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
#file_path="hdfs://blue:9000/data/md/u.data"
file_path="file:///E:/spark/learn/ml-100k/"
 
rawRatings = sc.textFile(file_path).map(lambda line :line.split("\t")[0:3])
 
 
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



import numpy as np
def cosineSlmilarity(x,y):
    return np.dot(x,y)/(np.linalg.norm(x)*np.linalg.norm(y))
testx=np.array([1.0,2.0,3.0])
print cosineSlmilarity(testx,testx)

itemId=567
itemFactor=model.productFeatures().lookup(itemId)

actual=moviesForUser[0][0]
actualRating=actual.rating  
predictedRating=model.predict(789,actual.product)
squairedError=np.power(actualRating-predictedRating,2)


userProducts = ratings.map(lambda rating:(rating.user,rating.product))
print '实际的评分:',userProducts.take(5)

#预测所有用户对电影的相应评分
print model.predictAll(userProducts).collect()[0]
predictions = model.predictAll(userProducts).map(lambda rating:((rating.user,rating.product), rating.rating))
print '预测的评分:',predictions.take(5)

ratingsAndPredictions = ratings.map(lambda rating:((rating.user,rating.product),rating.rating)).join(predictions)
print '组合预测的评分和实际的评分:',ratingsAndPredictions.take(5)

MSE = ratingsAndPredictions.map(lambda ((x,y),(m,n)):np.power(m-n,2)).reduce(lambda x,y:x+y)/ratingsAndPredictions.count() 
print '模型的均方误差:',MSE 
print '模型的均方根误差:',np.sqrt(MSE)




def avgPrecisionK(actual, predicted, k): 
    if len(predicted) > k:
        predK = predicted[:k]
    else:
        predK = predicted
    score = 0.0
    numHits = 0.0
    for i,p in enumerate(predK):
        if p in actual and p not in predK:
            numHits = numHits + 1
            score = score + numHits/(i+1)
    if not actual:
        return 1.0
    else:
        return score/min(len(actual),k)

topKRecs=topPredict   


actualMovies = [rating.product for rating in moviesForUser[0]]
predictMovies = [rating.product for rating in topKRecs]
print '实际的电影：',actualMovies
print '预测的电影：',predictMovies

MAP10 = avgPrecisionK(actualMovies,predictMovies,10)
print MAP10

itemFactors = model.productFeatures().map(lambda (id,factor):factor).collect()
itemMatrix = np.array(itemFactors)
print itemMatrix
print itemMatrix.shape

imBroadcast = sc.broadcast(itemMatrix)
#    fd = _os.open(file, flags, 0600)
# SError: [Errno 2] No such file or directory
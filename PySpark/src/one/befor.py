
# pyspark.cmd --master spark://blue:7077 --executor-memory 888M
# 
# %pylab

from pyspark import SparkConf ,SparkContext
sparkConf = SparkConf().setAppName("WordCounts").setMaster("local")
sc=SparkContext(conf=sparkConf)
file_path="file:///E:/spark/learn/ml-100k/"
user_data=sc.textFile(file_path+"u.user")

user_data.first()

user_fields=user_data.map(lambda line:line.split("|"))
num_user=user_fields.map(lambda fields:fields[0]).count()
num_genders=user_fields.map(lambda fields:fields[2]).distinct().count()
num_occupation=user_fields.map(lambda fields:fields[3]).distinct().count()

num_zipcodes=user_fields.map(lambda fields:fields[4]).distinct().count()

print "User:%d, genders:%d, occupations:%d, zip Codes:%d" % (num_user,num_genders,num_occupation,num_zipcodes)

ages=user_fields.map(lambda x:int(x[1])).collect()
# hist(ages, bins=20,color='lightblue',normed=True)
# fig =matplotlib.pyplot.gcf()
# fig.set_size_inches(16,10)

count_by_occupation =user_fields.map(lambda fields:(fields[3],1)).reduceByKey(lambda x,y:x+y).collect()
print dict(count_by_occupation)

# x_axis1=np.array([c[0] for c in count_by_occupation])
# y_axis1=np.array([c[1] for c in count_by_occupation])
# 
# x_axis=x_axis1[np.argsort(x_axis1)]
# y_axis=y_axis1[np.argsort(y_axis1)]
#coding=UTF-8
list1 = [1, 2, 3, 4, 5, 6, 7 ];
list2 = [u'196', u'242', u'3', u'881250949']
def delList(fields):
    dlst = [0,0,0]
    if len(fields)>3:
        dlst[0]=int(fields[0])
    return dlst

print  list2.map(lambda line:(int(line[0]),int(line[1])))

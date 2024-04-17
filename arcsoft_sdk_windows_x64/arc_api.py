import os
import arc_sdk


'''
获取图片中的人脸特征
仅限图片中一个人脸
成功返回 {'code':1, 'message':'success', 'data':'...'}
'''
def feature_fetch(file=None):

    #对图片的检查, 参数是否为空, 文件是否存在, 是否为jpg图片, 等等
    if file == None:
        return {'code':0, 'message':'image file cannot None'}
    if not os.path.exists(file):
        return {'code':0, 'message':'image file not exist'}
    
    if type(file) != type(''):
        return {'code':0, 'message':'image file name is not string'}
    
    position = file.rfind('.')
    if position == -1:
        return {'code':0, 'message':'image file not have suffix'}
    suffix = file[position+1:]
    if suffix!='jpg' and suffix!='jpeg':
        return {'code':0, 'message':'image file is not jpg or jpeg'}
    
    data = arc_sdk.feature_fetch(file)
    
    return data


'''
获取图片中的人脸特征
支持图片出现多个人脸
成功返回 {'code':1, 'message':'success', 'data':'...'}
'''
def feature_fetch_multipleface(file=None):

    #对图片的检查, 参数是否为空, 文件是否存在, 是否为jpg图片, 等等
    if file == None:
        return {'code':0, 'message':'image file cannot None'}
    if not os.path.exists(file):
        return {'code':0, 'message':'image file not exist'}
    
    if type(file) != type(''):
        return {'code':0, 'message':'image file name is not string'}
    
    position = file.rfind('.')
    if position == -1:
        return {'code':0, 'message':'image file not have suffix'}
    suffix = file[position+1:]
    if suffix!='jpg' and suffix!='jpeg':
        return {'code':0, 'message':'image file is not jpg or jpeg'}
    
    data = arc_sdk.feature_fetch_multipleface(file)
    
    return data


'''
人脸特征比对
成功返回 {'code':1, 'message':'success', 'data':...}
data为0~1的浮点数, 如果大于等于0.8, 则可以认为两张人脸数据是同一个人
'''
def feature_compare(feature1, feature2):

    if type(feature1) != type(''):
        return {'code':0, 'message':'feature1 is not string'}
    if len(feature1) == 0:
        return {'code':0, 'message':'feature1 empty'}

    if type(feature2) != type(''):
        return {'code':0, 'message':'feature1 is not string'}
    if len(feature2) == 0:
        return {'code':0, 'message':'feature1 empty'}
    
    data = arc_sdk.feature_compare(feature1, feature2)
    return data


'''
人脸特征比对, 参数为两张图片
成功返回 {'code':1, 'message':'success', 'data':...}
data为0~1的浮点数, 如果大于等于0.8, 则可以认为两张人脸数据是同一个人
'''
def feature_compare_image(file1=None, file2=None):

    #对图片的检查, 参数是否为空, 文件是否存在, 是否为jpg图片, 等等
    if file1 == None:
        return {'code':0, 'message':'image file1 cannot None'}
    if not os.path.exists(file1):
        return {'code':0, 'message':'image file1 not exist'}
    if type(file1) != type(''):
        return {'code':0, 'message':'image file1 name is not string'}
    position = file1.rfind('.')
    if position == -1:
        return {'code':0, 'message':'image file1 not have suffix'}
    suffix = file1[position+1:]
    if suffix!='jpg' and suffix!='jpeg':
        return {'code':0, 'message':'image file1 is not jpg or jpeg'}
    
    if file2 == None:
        return {'code':0, 'message':'image file2 cannot None'}
    if not os.path.exists(file2):
        return {'code':0, 'message':'image file2 not exist'}
    if type(file2) != type(''):
        return {'code':0, 'message':'image file2 name is not string'}
    position = file2.rfind('.')
    if position == -1:
        return {'code':0, 'message':'image file2 not have suffix'}
    suffix = file2[position+1:]
    if suffix!='jpg' and suffix!='jpeg':
        return {'code':0, 'message':'image file2 is not jpg or jpeg'}

    data = arc_sdk.feature_compare_image(file1, file2)
    return data

import os
import cv2
import ctypes
import base64
import hashlib
import time, datetime


APP_ID              = b"8X7FPa7dwmHcXKhwsBqauYB1uUvoCNJGHfiRz2WFUtXK"
SDK_KEY             = b"BHcZ4sV2Zt3Jg97g6GJeRAkUauX1cQF1Nw5CVMcE1aNQ"
LIB_FACE            = ctypes.cdll.LoadLibrary( os.path.abspath('.') + "/windows_dll/libarcsoft_face.dll" )
LIB_FACE_ENGINE     = ctypes.cdll.LoadLibrary( os.path.abspath('.') + "/windows_dll/libarcsoft_face_engine.dll" )


ASF_DETECT_MODE_IMAGE   = 0xFFFFFFFF    #检测模式, Image模式
ASF_OP_0_ONLY           = 0x1           #检测时候人脸角度, 常规预览下正方向
ASF_OP_ALL_OUT          = 0x5           #检测时候人脸角度, 全角度
NSCALE                  = 16
FACENUM                 = 3             #检测到的人脸数
FACENUM2                = 5             #检测到的人脸数, 用于feature_fetch_multipleface()


ASF_FACE_DETECT         = 0x00000001    #此处detect可以是tracking或者detection两个引擎之一，具体的选择由detect mode 确定
ASF_FACERECOGNITION     = 0x00000004    #人脸特征
ASF_AGE                 = 0x00000008    #年龄
ASF_GENDER              = 0x00000010    #性别
ASF_FACE3DANGLE         = 0x00000020    #3D角度
ASF_LIVENESS            = 0x00000080    #RGB活体
ASF_IR_LIVENESS         = 0x00000400    #IR活体


ASVL_PAF_RGB24_B8G8R8   = 0x201         #图像格式


#激活文件信息
class ASFActiveFileInfo(ctypes.Structure):
    _fields_ = [
        (u'startTime',  ctypes.c_char_p),
        (u'endTime',    ctypes.c_char_p),
        (u'activeKey',  ctypes.c_char_p),
        (u'platform',   ctypes.c_char_p),
        (u'sdkType',    ctypes.c_char_p),
        (u'appId',      ctypes.c_char_p),
        (u'sdkKey',     ctypes.c_char_p),
        (u'sdkVersion', ctypes.c_char_p),
        (u'fileVersion',ctypes.c_char_p)
    ]


#人脸框, python调用C++时用于构造体数据的传递
class MRECT(ctypes.Structure):
    _fields_ = [
        (u'left',   ctypes.c_int32),
        (u'top',    ctypes.c_int32),
        (u'right',  ctypes.c_int32),
        (u'bottom', ctypes.c_int32),
    ]


#多人脸信息, python调用C++时用于构造体数据的传递
class ASFMultiFaceInfo(ctypes.Structure):
    _fields_ = [
        (u'faceRect',   ctypes.POINTER(MRECT)),
        (u'faceOrient', ctypes.POINTER(ctypes.c_int32)),
        (u'faceNum',    ctypes.c_int32)
    ]


#单人脸信息, python调用C++时用于构造体数据的传递
class ASFSingleFaceInfo(ctypes.Structure):
    _fields_ = [
        (u'faceRect',   MRECT),
        (u'faceOrient', ctypes.c_int32)
    ]


#人脸特征, python调用C++时用于构造体数据的传递
class ASFFaceFeature(ctypes.Structure):
    _fields_ = [
        ('feature',     ctypes.c_void_p), 
        ('featureSize', ctypes.c_int32)
    ]


#内存操作的定义
malloc  = ctypes.cdll.msvcrt.malloc
malloc.restype = ctypes.c_void_p
memcpy  = ctypes.cdll.msvcrt.memcpy
free    = ctypes.cdll.msvcrt.free
free.argtypes   = (ctypes.c_void_p, )
free.restype    = None


class Image:
    def __init__(self):
        self.width      = 0
        self.height     = 0
        self.imageData  = None


#加载图片
def loadImage(file):
    image   = cv2.imread(file)
    shape   = image.shape
    image   = cv2.resize(image, (shape[1]//4*4, shape[0]))
    image2  = Image()
    image2.width    = image.shape[1]
    image2.height   = image.shape[0]
    image2.imageData= image
    return image2


#---------------------------------------------


#获取图片中的人脸特征
def feature_fetch(file):

    #检查激活文件, 如果不存在, 则进行在线激活操作; 如果存在, 判断是否过期
    active_file_info    = ASFActiveFileInfo()
    result              = LIB_FACE_ENGINE.ASFGetActiveFileInfo(ctypes.byref(active_file_info));
    if result == 0:
        endtime         = int(str(active_file_info.endTime, encoding="utf-8"))
        nowtimestamp    = int(time.time())
        if nowtimestamp > endtime:
            return {"code":0, "message":"SDK有效期失败"}
    elif result == 90138:
        LIB_FACE_ENGINE.ASFOnlineActivation.argtypes = (ctypes.c_char_p, ctypes.c_char_p)
        result = LIB_FACE_ENGINE.ASFOnlineActivation(APP_ID, SDK_KEY)
        if result!=0 and result!=90114:
            return {"code":0, "message":"SDK激活失败, 错误码: %d" % (result)}

    #初始化引擎
    LIB_FACE_ENGINE.ASFInitEngine.argtypes = (ctypes.c_long, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.POINTER(ctypes.c_void_p))
    mask    = ASF_FACE_DETECT | ASF_FACERECOGNITION | ASF_AGE | ASF_GENDER | ASF_FACE3DANGLE | ASF_LIVENESS | ASF_IR_LIVENESS;
    engine  = ctypes.c_void_p()
    result  = LIB_FACE_ENGINE.ASFInitEngine(ASF_DETECT_MODE_IMAGE, ASF_OP_0_ONLY, NSCALE, FACENUM, mask, ctypes.byref(engine))
    if result != 0:
        return {"code":0, "message":"初始化引擎失败, 错误码: %d" % (result)}

    #人脸检测
    image           = loadImage(file)
    image_bytes     = bytes(image.imageData)
    image_ubytes    = ctypes.cast(image_bytes, ctypes.POINTER(ctypes.c_ubyte))
    multiple_face   = ASFMultiFaceInfo()
    LIB_FACE_ENGINE.ASFDetectFaces.argtypes = (ctypes.c_void_p, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ASFMultiFaceInfo))
    result          = LIB_FACE_ENGINE.ASFDetectFaces(engine, image.width, image.height, ASVL_PAF_RGB24_B8G8R8, image_ubytes, ctypes.byref(multiple_face))
    if result != 0:
        return {"code":0, "message":"人脸识别失败, 错误码: %d" % (result)}
    
    #特征提取
    if multiple_face.faceNum == 0:
        print('{"code":0, "message":"图片中不存在人脸图像"}')
        return False
    if multiple_face.faceNum > 1:
        print('{"code":0, "message":"仅允许图片中存在一张人脸, 当前图片中的人脸有多个: %d"}' % (multiple_face.faceNum))
        return False
    single_face             = ASFSingleFaceInfo()
    single_face.faceRect    = multiple_face.faceRect[0]
    single_face.faceOrient  = multiple_face.faceOrient[0]
    face_feature            = ASFFaceFeature()
    LIB_FACE_ENGINE.ASFFaceFeatureExtract.argtypes = (ctypes.c_void_p, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, 
                                                ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ASFSingleFaceInfo), ctypes.POINTER(ASFFaceFeature))
    result  = LIB_FACE_ENGINE.ASFFaceFeatureExtract(engine, image.width, image.height, ASVL_PAF_RGB24_B8G8R8, image_ubytes, single_face, ctypes.byref(face_feature))
    if result != 0:
        print('{"code":0, "message":"人脸特征提取失败, 错误码: %d"}' % (result))
        return False
    
    #特征复制
    face_feature2               = ASFFaceFeature()
    face_feature2.featureSize   = face_feature.featureSize
    face_feature2.feature       = malloc(face_feature.featureSize)
    memcpy(ctypes.c_void_p(face_feature2.feature), ctypes.c_void_p(face_feature.feature), face_feature2.featureSize);
    
    #二进制数据, 生成base64的字符串
    featureContent  = ctypes.create_string_buffer(face_feature2.featureSize)
    memcpy( ctypes.cast(featureContent, ctypes.c_void_p), ctypes.c_void_p(face_feature2.feature), face_feature2.featureSize )
    if featureContent==None or len(featureContent)==0:
        return {"code":0, "message":"feature empty"}
    base64byte      = base64.b64encode(featureContent)
    base64string    = str(base64byte, encoding="utf-8")
    
    free(ctypes.c_void_p(face_feature2.feature))
    
    return {'code':1, 'message':'success', 'data':base64string}


#---------------------------------------------


#获取图片中的人脸特征, 支持图片出现多个人脸
def feature_fetch_multipleface(file):

    #检查激活文件, 如果不存在, 则进行在线激活操作; 如果存在, 判断是否过期
    active_file_info    = ASFActiveFileInfo()
    result              = LIB_FACE_ENGINE.ASFGetActiveFileInfo(ctypes.byref(active_file_info));
    if result == 0:
        endtime         = int(str(active_file_info.endTime, encoding="utf-8"))
        nowtimestamp    = int(time.time())
        if nowtimestamp > endtime:
            return {"code":0, "message":"SDK有效期失败"}
    elif result == 90138:
        LIB_FACE_ENGINE.ASFOnlineActivation.argtypes = (ctypes.c_char_p, ctypes.c_char_p)
        result = LIB_FACE_ENGINE.ASFOnlineActivation(APP_ID, SDK_KEY)
        if result!=0 and result!=90114:
            return {"code":0, "message":"SDK激活失败, 错误码: %d" % (result)}

    #初始化引擎
    LIB_FACE_ENGINE.ASFInitEngine.argtypes = (ctypes.c_long, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.POINTER(ctypes.c_void_p))
    mask    = ASF_FACE_DETECT | ASF_FACERECOGNITION | ASF_AGE | ASF_GENDER | ASF_FACE3DANGLE | ASF_LIVENESS | ASF_IR_LIVENESS;
    engine  = ctypes.c_void_p()
    result  = LIB_FACE_ENGINE.ASFInitEngine(ASF_DETECT_MODE_IMAGE, ASF_OP_0_ONLY, NSCALE, FACENUM2, mask, ctypes.byref(engine))
    if result != 0:
        return {"code":0, "message":"初始化引擎失败, 错误码: %d" % (result)}

    #人脸检测
    image           = loadImage(file)
    image_bytes     = bytes(image.imageData)
    image_ubytes    = ctypes.cast(image_bytes, ctypes.POINTER(ctypes.c_ubyte))
    multiple_face   = ASFMultiFaceInfo()
    LIB_FACE_ENGINE.ASFDetectFaces.argtypes = (ctypes.c_void_p, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ASFMultiFaceInfo))
    result          = LIB_FACE_ENGINE.ASFDetectFaces(engine, image.width, image.height, ASVL_PAF_RGB24_B8G8R8, image_ubytes, ctypes.byref(multiple_face))
    if result != 0:
        return {"code":0, "message":"人脸识别失败, 错误码: %d" % (result)}
    
    #特征提取
    if multiple_face.faceNum == 0:
        print('{"code":0, "message":"图片中不存在人脸图像"}')
        return False
    
    total   = multiple_face.faceNum;

    rows    = []
    for i in range(multiple_face.faceNum):
        single_face             = ASFSingleFaceInfo()
        single_face.faceRect    = multiple_face.faceRect[i]
        single_face.faceOrient  = multiple_face.faceOrient[i]
        face_feature            = ASFFaceFeature()
        LIB_FACE_ENGINE.ASFFaceFeatureExtract.argtypes = (ctypes.c_void_p, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, 
                                                    ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ASFSingleFaceInfo), ctypes.POINTER(ASFFaceFeature))
        result  = LIB_FACE_ENGINE.ASFFaceFeatureExtract(engine, image.width, image.height, ASVL_PAF_RGB24_B8G8R8, image_ubytes, single_face, ctypes.byref(face_feature))
        if result != 0:
            print('{"code":0, "message":"人脸特征提取失败, 错误码: %d"}' % (result))
            return False
        
        #特征复制
        face_feature2               = ASFFaceFeature()
        face_feature2.featureSize   = face_feature.featureSize
        face_feature2.feature       = malloc(face_feature.featureSize)
        memcpy(ctypes.c_void_p(face_feature2.feature), ctypes.c_void_p(face_feature.feature), face_feature2.featureSize);
    
        #二进制数据, 生成base64的字符串
        featureContent  = ctypes.create_string_buffer(face_feature2.featureSize)
        memcpy( ctypes.cast(featureContent, ctypes.c_void_p), ctypes.c_void_p(face_feature2.feature), face_feature2.featureSize )
        if featureContent==None or len(featureContent)==0:
            return {"code":0, "message":"feature empty"}
        base64byte      = base64.b64encode(featureContent)
        base64string    = str(base64byte, encoding="utf-8")
        
        free(ctypes.c_void_p(face_feature2.feature))
        rows.append(base64string)
    
    return {'code':1, 'message':'success', 'data':{'total':total, 'rows':rows}}


#---------------------------------------------


#两个人脸特征进行比对
def feature_compare(feature1, feature2):
    feature1_binary             = base64.b64decode( bytes(feature1, encoding='utf-8') )
    face_feature1               = ASFFaceFeature()
    face_feature1.featureSize   = len(feature1_binary)
    feature1_data               = ctypes.create_string_buffer(feature1_binary)
    face_feature1.feature       = malloc(face_feature1.featureSize)
    memcpy(ctypes.c_void_p(face_feature1.feature), ctypes.cast(feature1_data, ctypes.c_void_p), face_feature1.featureSize);

    feature2_binary             = base64.b64decode( bytes(feature2, encoding='utf-8') )
    face_feature2               = ASFFaceFeature()
    face_feature2.featureSize   = len(feature2_binary)
    feature2_data               = ctypes.create_string_buffer(feature2_binary)
    face_feature2.feature       = malloc(face_feature2.featureSize)
    memcpy(ctypes.c_void_p(face_feature2.feature), ctypes.cast(feature2_data, ctypes.c_void_p), face_feature2.featureSize);

    #检查激活文件, 如果不存在, 则进行在线激活操作; 如果存在, 判断是否过期
    active_file_info    = ASFActiveFileInfo()
    result              = LIB_FACE_ENGINE.ASFGetActiveFileInfo(ctypes.byref(active_file_info));
    if result == 0:
        endtime         = int(str(active_file_info.endTime, encoding="utf-8"))
        nowtimestamp    = int(time.time())
        if nowtimestamp > endtime:
            return {"code":0, "message":"SDK有效期失败"}
    elif result == 90138:
        LIB_FACE_ENGINE.ASFOnlineActivation.argtypes = (ctypes.c_char_p, ctypes.c_char_p)
        result = LIB_FACE_ENGINE.ASFOnlineActivation(APP_ID, SDK_KEY)
        if result!=0 and result!=90114:
            return {"code":0, "message":"SDK激活失败, 错误码: %d" % (result)}

    #初始化引擎
    LIB_FACE_ENGINE.ASFInitEngine.argtypes = (ctypes.c_long, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.POINTER(ctypes.c_void_p))
    mask    = ASF_FACE_DETECT | ASF_FACERECOGNITION | ASF_AGE | ASF_GENDER | ASF_FACE3DANGLE | ASF_LIVENESS | ASF_IR_LIVENESS;
    engine  = ctypes.c_void_p()
    result  = LIB_FACE_ENGINE.ASFInitEngine(ASF_DETECT_MODE_IMAGE, ASF_OP_0_ONLY, NSCALE, FACENUM, mask, ctypes.byref(engine))
    if result != 0:
        return {"code":0, "message":"初始化引擎失败, 错误码: %d" % (result)}
    
    #特征比对
    confidence  = ctypes.c_float()
    LIB_FACE_ENGINE.ASFFaceFeatureCompare.argtypes = (ctypes.c_void_p, ctypes.POINTER(ASFFaceFeature), ctypes.POINTER(ASFFaceFeature), ctypes.POINTER(ctypes.c_float))
    result      = LIB_FACE_ENGINE.ASFFaceFeatureCompare(engine, face_feature1, face_feature2, confidence)
    
    free(ctypes.c_void_p(face_feature1.feature))
    free(ctypes.c_void_p(face_feature2.feature))
    
    return {"code":1, "message":"success", "data":confidence.value}


#---------------------------------------------


#两个人脸特征进行比对, 参数为两张图片
def feature_compare_image(file1, file2):

    #检查激活文件, 如果不存在, 则进行在线激活操作; 如果存在, 判断是否过期
    active_file_info    = ASFActiveFileInfo()
    result              = LIB_FACE_ENGINE.ASFGetActiveFileInfo(ctypes.byref(active_file_info));
    if result == 0:
        endtime         = int(str(active_file_info.endTime, encoding="utf-8"))
        nowtimestamp    = int(time.time())
        if nowtimestamp > endtime:
            return {"code":0, "message":"SDK有效期失败"}
    elif result == 90138:
        LIB_FACE_ENGINE.ASFOnlineActivation.argtypes = (ctypes.c_char_p, ctypes.c_char_p)
        result = LIB_FACE_ENGINE.ASFOnlineActivation(APP_ID, SDK_KEY)
        if result!=0 and result!=90114:
            return {"code":0, "message":"SDK激活失败, 错误码: %d" % (result)}

    #初始化引擎
    LIB_FACE_ENGINE.ASFInitEngine.argtypes = (ctypes.c_long, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.POINTER(ctypes.c_void_p))
    mask    = ASF_FACE_DETECT | ASF_FACERECOGNITION | ASF_AGE | ASF_GENDER | ASF_FACE3DANGLE | ASF_LIVENESS | ASF_IR_LIVENESS;
    engine  = ctypes.c_void_p()
    result  = LIB_FACE_ENGINE.ASFInitEngine(ASF_DETECT_MODE_IMAGE, ASF_OP_0_ONLY, NSCALE, FACENUM, mask, ctypes.byref(engine))
    if result != 0:
        return {"code":0, "message":"初始化引擎失败, 错误码: %d" % (result)}
    
    #人脸检测
    image           = loadImage(file1)
    image_bytes     = bytes(image.imageData)
    image_ubytes    = ctypes.cast(image_bytes, ctypes.POINTER(ctypes.c_ubyte))
    multiple_face   = ASFMultiFaceInfo()
    LIB_FACE_ENGINE.ASFDetectFaces.argtypes = (ctypes.c_void_p, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ASFMultiFaceInfo))
    result          = LIB_FACE_ENGINE.ASFDetectFaces(engine, image.width, image.height, ASVL_PAF_RGB24_B8G8R8, image_ubytes, ctypes.byref(multiple_face))
    if result != 0:
        return {"code":0, "message":"人脸识别失败, 错误码: %d" % (result)}
    
    #特征提取
    if multiple_face.faceNum == 0:
        print('{"code":0, "message":"face not exist in image"}')
        return False
    if multiple_face.faceNum > 1:
        print('{"code":0, "message":"仅允许图片中存在一张人脸, 当前图片中的人脸有多个: %d"}' % (multiple_face.faceNum))
        return False
    single_face             = ASFSingleFaceInfo()
    single_face.faceRect    = multiple_face.faceRect[0]
    single_face.faceOrient  = multiple_face.faceOrient[0]
    face_feature            = ASFFaceFeature()
    LIB_FACE_ENGINE.ASFFaceFeatureExtract.argtypes = (ctypes.c_void_p, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, 
                                                ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ASFSingleFaceInfo), ctypes.POINTER(ASFFaceFeature))
    result  = LIB_FACE_ENGINE.ASFFaceFeatureExtract(engine, image.width, image.height, ASVL_PAF_RGB24_B8G8R8, image_ubytes, single_face, ctypes.byref(face_feature))
    if result != 0:
        print('{"code":0, "message":"人脸特征提取失败, 错误码: %d"}' % (result))
        return False
    
    #特征复制
    face_feature1               = ASFFaceFeature()
    face_feature1.featureSize   = face_feature.featureSize
    face_feature1.feature       = malloc(face_feature.featureSize)
    memcpy(ctypes.c_void_p(face_feature1.feature), ctypes.c_void_p(face_feature.feature), face_feature1.featureSize);
    
    #人脸检测2
    image2          = loadImage(file2)
    image_bytes2    = bytes(image2.imageData)
    image_ubytes2   = ctypes.cast(image_bytes2, ctypes.POINTER(ctypes.c_ubyte))
    multiple_face2  = ASFMultiFaceInfo()
    LIB_FACE_ENGINE.ASFDetectFaces.argtypes = (ctypes.c_void_p, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ASFMultiFaceInfo))
    result          = LIB_FACE_ENGINE.ASFDetectFaces(engine, image2.width, image2.height, ASVL_PAF_RGB24_B8G8R8, image_ubytes2, ctypes.byref(multiple_face2))
    if result != 0:
        return {"code":0, "message":"人脸识别失败, 错误码: %d" % (result)}
    
    #特征提取2
    if multiple_face2.faceNum == 0:
        print('{"code":0, "message":"face not exist in image"}')
        return False
    if multiple_face2.faceNum > 1:
        print('{"code":0, "message":"仅允许图片中存在一张人脸, 当前图片中的人脸有多个: %d"}' % (multiple_face2.faceNum))
        return False
    single_face2            = ASFSingleFaceInfo()
    single_face2.faceRect   = multiple_face2.faceRect[0]
    single_face2.faceOrient = multiple_face2.faceOrient[0]
    face_feature2           = ASFFaceFeature()
    LIB_FACE_ENGINE.ASFFaceFeatureExtract.argtypes = (ctypes.c_void_p, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, 
                                                ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ASFSingleFaceInfo), ctypes.POINTER(ASFFaceFeature))
    result  = LIB_FACE_ENGINE.ASFFaceFeatureExtract(engine, image2.width, image2.height, ASVL_PAF_RGB24_B8G8R8, image_ubytes2, single_face2, ctypes.byref(face_feature2))
    if result != 0:
        print('{"code":0, "message":"人脸特征提取失败, 错误码: %d"}' % (result))
        return False

    #特征比对
    confidence  = ctypes.c_float()
    LIB_FACE_ENGINE.ASFFaceFeatureCompare.argtypes = (ctypes.c_void_p, ctypes.POINTER(ASFFaceFeature), ctypes.POINTER(ASFFaceFeature), ctypes.POINTER(ctypes.c_float))
    result      = LIB_FACE_ENGINE.ASFFaceFeatureCompare(engine, face_feature1, face_feature2, confidence)
    
    free(ctypes.c_void_p(face_feature1.feature))
    
    return {"code":1, "message":"success", "data":confidence.value}


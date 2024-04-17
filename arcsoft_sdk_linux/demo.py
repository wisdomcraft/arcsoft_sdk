import arc_api


'''
示例, 参数为图片路径与名称, 返回人脸特征的base64字符串, 返回值举例
{'code': 1, 'message': 'success', 'data': 'AID6RAAAoEHr0FQ8IQp3PFIe3z1VM+m8AT+mvMwN4bxQKMG9/5GRPffEZL2y26c8gwYQPTl4DT3t1We8NF4lveCIKDwymkS9ZWwGPX8Sb71teZ+9UhkGPh1KvbxS1zE9b2ZTvXcioL09YJM9jozEPCp1Hr3CSuy9rS4vPJz1iD3Rir89Te0OvY+YbT33fMK9gUj/vBKKxT3JSLA9VGQ2PeVxfT2NpfG7rKhmPNZ6dL0Cr+28bKKbvW4gFLvCvRg9y39DPKc65jyieaw9yfykPQa6eL1sf1q914W8PR3PaL3x8w8+rreDPRNfEr7Njvi7n9icvdNj+Tw7buM737SsvWa1QTulgK49ZDUmvWfUcL3rOza7TdyZPKT3Rr3GQQE9udyGPcfCAD6Hajc9V8FpPDyEWLy3N5W8PQeHPVMwzrxAjpC8ry4PPG4UEL5aBoa9tzBtOqTeCDwh/cO9a3A7O6yn5b2UhIc8XIoYvoqkTr1HaxQ964zqPHbnsr1xNOO9tsDBvT+03Dztn1+9R9G5O4Qp3L1/raK9LkFiPNYT7rwF46E9Jcb6vDYosr1HBQs+SobjvOXJd70Fm6s9DvpjPStzrT3a2rq9AmWJPb5/nDs2tnM9fI4uvgLRyD1dHM88xGQYPpKHxb2mLNe8T/IBu5qPmT3Q3k89BjGmPY/igb3K7tA9EPjSPefkTD08aMS8c3VDvWTKxj0haGA982BtvcUSpDuTz/g9hOctvQ4yAjpskxI7TZQ+PeXRLj010nO9odCVvSXPAL3b0kG9FRQMPao9GbssDAY9VWTiPMr0ArwfF629GwjKuw3TgD3wRoC98KnWPKW2PT3r3LG9KsqAPFrBUD7xzR493sk5PQDmjzw05CI8ElbiPZthQztMuNM9obVXvQFbxjzQy0k+quAZvZKm07ynM7E8R9ixPdNMab3CB7Y9nM05vYX1XT2RCUI+LxBGvO6UIz2AlO08uYlMvaZ5ZLxOSzE99YD3PFIZoz1Uefm7Vp2JPU+uyD2xaFK92k39PMCo9zzENgU92qx/PeDYkzzfOm68IRflPHxWC73yU2k9Gsu+vUAyIDzpk7K9Fe1vPLG/673mOU089XjovAmkIT2dHlu9h9v8PMQqjD3wZv688VjDPQPe/7wQwoA9YSyJvdV6mD0vApm9oa1sO7sj5jwrziM9gFxovUvINbw1UcC9IF+EvfxZurwkPIe9GTX6POSihD0utw49ohKXvclVVb3FakI9cbXVvHeNjD3g4NA8hkaDvaYgWr0SSbA7iccVPjqXCTyZPjQ9dYWfPWePtz02Iys98i9aPTmnEL0AvOg9DG1evauhOT3TNT49FR5vvNE+Lbw8Af87DnSgvYtQoL1VeBi9'}
'''

data    = arc_api.feature_fetch('image_demo/480_400.jpg')
print( data, '\n' )

data2   = arc_api.feature_fetch('image_demo/640_480.jpg')
print( data2, '\n' )


#-----------------------------------------

'''
示例, 参数为图片路径与名称, 获取图片中的多张人脸
{'code': 1, 'message': 'success', 'data':{'total':, 'rows'['','',...]}}
'''

data3   = arc_api.feature_fetch_multipleface('image_demo/multiple_1.jpg')
print( data3, '\n' )

data4   = arc_api.feature_fetch_multipleface('image_demo/multiple_3.jpg')
print( data4, '\n' )


#-----------------------------------------

'''
示例, 特征比较, 参数为两个人脸特征的base64字符串, 返回值举例
{'code': 1, 'message': 'success', 'data': 0.9624579548835754}
'''

feature1 = 'AID6RAAAoEHr0FQ8IQp3PFIe3z1VM+m8AT+mvMwN4bxQKMG9/5GRPffEZL2y26c8gwYQPTl4DT3t1We8NF4lveCIKDwymkS9ZWwGPX8Sb71teZ+9UhkGPh1KvbxS1zE9b2ZTvXcioL09YJM9jozEPCp1Hr3CSuy9rS4vPJz1iD3Rir89Te0OvY+YbT33fMK9gUj/vBKKxT3JSLA9VGQ2PeVxfT2NpfG7rKhmPNZ6dL0Cr+28bKKbvW4gFLvCvRg9y39DPKc65jyieaw9yfykPQa6eL1sf1q914W8PR3PaL3x8w8+rreDPRNfEr7Njvi7n9icvdNj+Tw7buM737SsvWa1QTulgK49ZDUmvWfUcL3rOza7TdyZPKT3Rr3GQQE9udyGPcfCAD6Hajc9V8FpPDyEWLy3N5W8PQeHPVMwzrxAjpC8ry4PPG4UEL5aBoa9tzBtOqTeCDwh/cO9a3A7O6yn5b2UhIc8XIoYvoqkTr1HaxQ964zqPHbnsr1xNOO9tsDBvT+03Dztn1+9R9G5O4Qp3L1/raK9LkFiPNYT7rwF46E9Jcb6vDYosr1HBQs+SobjvOXJd70Fm6s9DvpjPStzrT3a2rq9AmWJPb5/nDs2tnM9fI4uvgLRyD1dHM88xGQYPpKHxb2mLNe8T/IBu5qPmT3Q3k89BjGmPY/igb3K7tA9EPjSPefkTD08aMS8c3VDvWTKxj0haGA982BtvcUSpDuTz/g9hOctvQ4yAjpskxI7TZQ+PeXRLj010nO9odCVvSXPAL3b0kG9FRQMPao9GbssDAY9VWTiPMr0ArwfF629GwjKuw3TgD3wRoC98KnWPKW2PT3r3LG9KsqAPFrBUD7xzR493sk5PQDmjzw05CI8ElbiPZthQztMuNM9obVXvQFbxjzQy0k+quAZvZKm07ynM7E8R9ixPdNMab3CB7Y9nM05vYX1XT2RCUI+LxBGvO6UIz2AlO08uYlMvaZ5ZLxOSzE99YD3PFIZoz1Uefm7Vp2JPU+uyD2xaFK92k39PMCo9zzENgU92qx/PeDYkzzfOm68IRflPHxWC73yU2k9Gsu+vUAyIDzpk7K9Fe1vPLG/673mOU089XjovAmkIT2dHlu9h9v8PMQqjD3wZv688VjDPQPe/7wQwoA9YSyJvdV6mD0vApm9oa1sO7sj5jwrziM9gFxovUvINbw1UcC9IF+EvfxZurwkPIe9GTX6POSihD0utw49ohKXvclVVb3FakI9cbXVvHeNjD3g4NA8hkaDvaYgWr0SSbA7iccVPjqXCTyZPjQ9dYWfPWePtz02Iys98i9aPTmnEL0AvOg9DG1evauhOT3TNT49FR5vvNE+Lbw8Af87DnSgvYtQoL1VeBi9'

feature2 = 'AID6RAAAoEEP6u08Ma79PbUj6jp2e4q8Njt2vTMyoD2M9IO8l9BFPumN67x0YCi9ocZIPcXwj7w5wOW8MeynvZ1c8LzyoAw90SmQPJTEDL32fb28REiaPRKqNb3yt6S9Y9mfvN00Ub16CKw9QCSZPRUuarwujuO9BWONPWnlaT0ahc49lj2mvGDDyT2yn7y7ukdJvFS/vz0/ME08JAyKPUzZAr1DAtm9NkkWvDZiGb2CtO49wlYFPEnpDDp207e9qnS1PBAKGj0Tx5E9EppbPaH6Qb1BmrC9nnVHPdwyP71XvRM+AokAvWIiGb4OMwA9x7V9vesZcL1vkG69lAolPDnIuj1CpUQ9NQnZvT7Nw7xDExW9Cea0PJzcEb02TCI99keFPPzzmTyL6cO83oTdvAvcmzwHZqG9Q0qGPTWqJjuQhd28P5nWO/6FyL2qks29PidrPWB6Er2Hn/i9xMZKvHzS0r1juvc8N2jrvcOPh73MsoW9krEVPTHAjTspSva9eS8UvfaSET01S688vMAVvPLcTj1GDLq99uktPfLcbb2WcYQ8odS7vauhLr3MZQY+3S9zPY422rwjMLY93KWrPT9H3T30DGG9fMAKPaUDNLxVzSg93FUoviG1vj3LOqK7UxvYPRqOrr3csds8MxDXvD371j2/U2C906/JPbUz6rzLxO06v+mgPCqwZbzJQlU9MhTFvSpGoz3eSA68L/CTPTClIzx/J5C8+hK/vQbcED3bMOs8M3MEPrYamrxNOIC7H5x1vbpfs7xkgry9DO/xvLqz0jxEhw+9rZdiPe/oBrzUcM+9YRWYvaJ0kz3d3BE9zDBYPbUT0j3XiRS8pBK6PA2X+z33gHI9l2hrPbxTCrxzaxu9O+DcPe0Iyj3syK49CuyWOjSnYz2jICI+xy8rvTT4z7wLie87DOLkPXDP2LvD+F88hDIOvTDob731lq098SbtvYzffzyAvui83NQPvXMIG70K8fU8UjmOPM7nmT0WeA88cLHTPf+G6D1u0ku9LR5aPdAikrxfjKK9C8FYvJm+hrqmNZI8Dga3PJlVTzyWynU8WxlrvSGDnb2pUz+9myY+PaQZ4b3vtpo8mYQhvVtNd7z1Ny2+tlD+vHt2TT1K6Z+830NqPZSr2zzDvxo98KuPveUAkT1iDsy9LFITPOQ0T7lJaok5HrGTvbrjObzNDbG9E29RveZzjD2M4+S9zEztvOe3/Duumpm9xdJXvY5sRLy23o49ft7qvHoz8zxVHvI89ri4PF6QAr2LqCe8S7XrPewBHLw72Hm8AHwmvDGH5TwQ8zY97sElPel+kry6U8U9di3VvR2aRby05Qy9dT9/vIJjGj3wgBo9yk22vFC4dL2qVE89'

compare = arc_api.feature_compare(feature1, feature2)
print( compare, '\n' )


#-----------------------------------------


'''
示例, 特征比较, 参数为两张图片, 返回值举例
{'code': 1, 'message': 'success', 'data': 0.9624579548835754}
'''

compare2 = arc_api.feature_compare_image('image_demo/480_400.jpg', 'image_demo/640_720.jpg')
print( compare2, '\n' )



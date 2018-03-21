# -*- coding: utf-8 -*-
# flake8: noqa
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
#需要填写你的 Access Key 和 Secret Key
access_key = 'NY9KTZh636R5UMRAbVNXnL7G2gVhHK7stFYwpH0G'
secret_key = 'SQYZAeyQkYwvfM6nRIy_GW1765NYy5ZvfbDBoIxD'
#构建鉴权对象
q = Auth(access_key, secret_key)
#要上传的空间
bucket_name = 'scope'
def upload(uploadfile,localfile):
    #上传到七牛后保存的文件名
    key = uploadfile;
    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)
    #要上传文件的本地路径
    localfile = localfile
    ret, info = put_file(token, key, localfile)
    print(info)
    assert ret['key'] == key
    assert ret['hash'] == etag(localfile)


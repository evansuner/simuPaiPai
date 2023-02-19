## 私募排排网数据加密加密
### 适用于如下接口:
+ GET https://sppwapi.simuwang.com/sun/member/getUserInfoApi
+ GET https://sppwapi.simuwang.com/sun/Ranking/hotSearchApi
+ GET https://sppwapi.simuwang.com/pub/pubRanking/fund
+ GET/POST https://sppwapi.simuwang.com/sun/ranking/fund
+ GET https://sppwapi.simuwang.com/sun/chart/fundNavTrend
+ POST https://sppwapi.simuwang.com/sun/fund/getNavData (该接口涉及到html内容的混淆, 目前未解决该混淆)
+ ...

### 使用方式
express服务只提供一个解密的接口 `http://127.0.0.1:7799/decryptor`
请求方式: POST
参数: 
+ data   
 response获取到的对应加密data `response["data"]["data"]`
+ key    
 解密密钥

python代码只使用来解析出对应的加密data, 密钥, 以及向express服务发送请求, 获取到的response就是解密后的数据.

### 安装方式
+ Node安装   
 ```bash
npm i --registry=https://registry.npmmirror.com
npm start

再运行`request.py`提供对应的私募ID即可得到对应的解密数据
 ```

+ Docker部署
```bash


```
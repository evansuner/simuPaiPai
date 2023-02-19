import execjs
import requests
import re
import json

def parse(id='HF00007JYB'):
    """
    发送请求， 获取response， 以及对response做一些处理
    """
    # url = 'https://sppwapi.simuwang.com/sun/fund/getNavData'
    url = 'https://sppwapi.simuwang.com/sun/ranking/fund'

    headers = {
        'cookie': 'Hm_lvt_c3f6328a1a952e922e996c667234cdae=1676189389; certification=1; qualified_investor=1; evaluation_result=0; focus-certification-pop=-1; smppw_tz_auth=1; http_tK_cache=be30891c25f660f013638fc66b75c60228a3a854; cur_ck_time=1676782044; ck_request_key=5nWK8IURkXCavOjRnprhFhOCQBGTui7Wby6VBlDC%2FFU%3D; passport=2350372%09u2267599810781%09BQUFBQwAAQldUwQBWlBWDFJcAQEGCgkJAFZeXgYHAVY%3D9710d4c4e7; rz_rem_u_p=yEbSnZ1rzOf04nG44hMkf%2FJWXOvTZ1Q0nTTdkclYpto%3D%24BlQFOpWZaxQEVw%2Feud7Rn6R7taW6YYpd0dZKbjb2m80%3D; Hm_lpvt_c3f6328a1a952e922e996c667234cdae=1676782050',
        'host': 'sppwapi.simuwang.com',
        'origin': 'https://dc.simuwang.com',
        'Referer': 'https://dc.simuwang.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }

    payload = {
        # 'id': id,
        'USER_ID': '2350372',
        'sort_name': 'ret_incep_a',
        'condition': 'raise_type:1;fund_type:1,6,4,3,8,2;first_strategy:1001;rate_year:incep;maxdrawdown_year:incep;subscription_fee_conf:;rating_year:1;',
        'page': 1,
        'sort_asc': 'desc',
        'size': 5,
        'keyword': '',
        'ENCODE': 1,
        'pool_type': 1,
        
    }
    # payload = {
    #     'page': 1,
    #     'condition': 'raise_type:1;fund_type:1,6,4,3,8,2;first_strategy:1001;rate_year:incep;maxdrawdown_year:incep;subscription_fee_conf:;rating_year:1;',
    #     'size': 50,
    #     'sort_name': 'ret_incep_a',
    #     'sort_asc': 'desc',
    #     'pool_type': 1,
    #     'keyword': '',
    #     'ENCODE': 1,
    #     'USER_ID': '2350372'
    # }

    response = requests.post(url, headers=headers, data=payload).json()
    full_code = response["data"]["key"]
    regex = re.compile(r'\)\)\}\((.*?)\)\)', re.DOTALL)
    swap_code = re.findall(regex, full_code)[0].split(",")
    p = []
    for i in swap_code:
        p.append(eval(i))

    return response, full_code, p


def process_js_code(result, string):
    first_step = result.split(string[0])[0][:-2]
    second_step = first_step.split("eval(")[-1][8:]
    third_step = first_step.split("eval(")[0] + "function key" + second_step
    return third_step


def get_key(data, key):
    if data["data"] and data["data"]["encode"]:
        code = data["data"]["encode"]
        k = eval(key.split("=")[-1])
        js_code = """function key(k, code) {
    return 3 === code ? key = k.split("").reverse().join("") : 4 === code ? key = k.slice(2) : 5 === code ? key = k.slice(0, k.length - 2) : 6 === code ? key = k.slice(1, k.length - 1) : 7 === code ? key = k.slice(2, k.length - 1) : 8 === code ? key = k.slice(1, k.length - 2) : 9 === code ? key = k[0] + k.slice(2, k.length) : 10 === code && (key = k.slice(0, k.length - 2) + k[k.length - 1]),
        key
}"""
        ctx = execjs.compile(js_code)
        token = ctx.call('key', k, code)
        return token

def request_data(data, key) -> json:
    """
    params: data: 初步请求返回的加密数据 ["data"]["data"]
    params: key: 对应的密钥
    return: json
    """
    payload = {
        'data': data,
        'key': key
    }
    url = 'http://127.0.0.1:7799/decryptor'
    response = None
    try:
        response = requests.post(url, data=payload).json()
    except Exception as e:
        response = e
    return response

def main():
    id_list = ['HF00007JYB', 'HF000062TE', 'HF00005UXZ', 'HF00006WJD']
    for id in id_list[:1]:
        res, full, params = parse(id)
        js_code = process_js_code(full, params)
        ctx = execjs.compile(js_code)
        swap_key = ctx.call('key', *params)
        key = get_key(res, swap_key)
        # print(swap_key, key)
        # print(res["data"]["data"])
        result = request_data(res["data"]["data"], key)
        # json.loads(result)
        print(result)


if __name__ == '__main__':
    main()
import hashlib
# import random
import json
import re


def md5(data):
    md5_obj = hashlib.md5()
    md5_obj.update(data.encode('utf-8'))
    return md5_obj.hexdigest()


def str_find_last_index(content, target_string):
    if target_string is None:
        return -1
    index = -1
    res = 0
    while res != -1:
        res = content.find(target_string, res)
        if res != -1:
            index = res
            res += 1
    return index


class enc_function:
    def __init__(self, js_code):

        _temp = self.encA1_js_parser(js_code)
        self.seed = _temp['seed']
        self.seed_at = _temp['at_where']

    def encA1_js_parser(self, js_code):
        # http://bus.kuas.edu.tw/API/Scripts/a1
        seed_from_first_regex = re.compile(r"encA2\('((\d|\w){0,32})'")
        seed_from_last_regex = re.compile(
            r"encA2\(e(\w|\d|\s|\W){0,3}'((\d|\w){0,32})'\)")
        f_match = seed_from_first_regex.findall(js_code)
        l_match = seed_from_last_regex.findall(js_code)

        first_value = None
        last_value = None
        if len(f_match) > 0:
            first_value = f_match[-1][0]
        if len(l_match) > 0:
            last_value = l_match[-1][1]
        if str_find_last_index(js_code, first_value) > str_find_last_index(js_code, last_value):
            return {
                "seed": first_value,
                "at_where": "First"
            }

        return {"seed": last_value, "at_where": "Last"}

    def encA1(self, data):
        # Only use last encrypt seed, other command just let us confuse.
        if self.seed_at == 'Last':
            return md5(data+self.seed)
        return md5(self.seed+data)


def encrypt(enc_function: enc_function, username: str, password: str):

    # Just random value
    # g = int(1163531501*random.uniform(0, 1))+15441
    # i = int(1163531502*random.uniform(0, 1))+0
    # j = int(1163531502*random.uniform(0, 1))+0
    # k = int(1163531502*random.uniform(0, 1))+0
    g = 419191959
    i = 930672927
    j = 1088434686
    k = 260123741

    g = md5("J"+str(g))
    i = md5("E"+str(i))
    j = md5("R"+str(j))
    k = md5("Y"+str(k))
    username = md5(username+enc_function.encA1(g))
    password = md5(username+password+"JERRY"+enc_function.encA1(i))

    l = md5(username+password+"KUAS"+enc_function.encA1(j))
    l = md5(l + username+enc_function.encA1("ITALAB")+enc_function.encA1(k))
    l = md5(l + password+"MIS"+k)

    return json.dumps({
        "a": l,
        "b": g,
        "c": i,
        "d": j,
        "e": k,
        "f": password
    })


if __name__ == "__main__":

    js_code = "function encA1(e) {var r = e;r = encA2(e+ '73623');r = encA2(e+ '2001061D7FF8025AEABBFA078359B49D');r = encA2('1B2AE1ABC7405FB92168D400454C936C' + e);r = encA2(e+ 'C9571BAE638B1E00F6CE64325C44C285');r = encA2(e+ '56443A6997DC9A0F2D181B5D2D67256C');return r;};"
    enc_f = enc_function(js_code)
    print(enc_f.seed)
    print(enc_f.seed_at)

    answer = encrypt(enc_function=enc_f,
                     username="1106......", password=".....")
    print(answer)

    # content_ = """function encA1(e) {var r = e;r = encA2(e+ '69A278DF0E948BFA4FDFCFCBDA822C73');r = encA2(e+ '6495CF7CA745A9443508B86951B8E33A');r = encA2(e+ 'E3599F39F0D93DF31B632978CDC693C1');r = encA2(e+ '32881');r = encA2('91337' + e);return r;};function encA1(e) {var r = e;r = encA2(e+ '69A278DF0E948BFA4FDFCFCBDA822C73');r = encA2(e+ '6495CF7CA745A9443508B86951B8E33A');r = encA2(e+ 'E3599F39F0D93DF31B632978CDC693C1');r = encA2(e+ '32881');r = encA2('91337' + e);return r;};"""
    # print(content_.find("91337", 0))
    # r = str_find_last_index(content_, '91337')
    # print(r)

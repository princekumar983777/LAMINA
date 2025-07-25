def chibi_map(chibi_name):
    chibi_map = {   
        "ok": "chibi/0.png",
        "listen": "chibi/1.png",
        "talk": "chibi/2.png",
        "think": "chibi/3.png",
        "think_": "chibi/4.png",
        "sleep": "chibi/5.png",
        "happy": "chibi/6.png",
        "sad": "chibi/7.png",
        "confused": "chibi/8.png",
    }
    return chibi_map[chibi_name]
def chibi_map_list():
    return list(chibi_map.keys())
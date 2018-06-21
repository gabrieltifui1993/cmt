import os
import re

elastic_server = "localhost:9200"
script_name = "../client/twitter/scrapper/twint.py"
cmd_template = 'python {script} -s {text} --since {from_date} --until {until_date} -es {elastic_url} -c {elastic_index} -l {language}'

query_template = "{coin_name}%20OR%20%23{coin_name}%20OR%20{coin_code}%20OR%20%23{coin_code}%20OR%20%24{coin_code}%20OR%20%24{coin_name}"

lang = "en"

def load_tweets(from_date, until_date, coin):
    coin_name = re.sub('\s+', '%20', coin.name).strip().lower()
    coin_code = re.sub('\s+', '%20', coin.code).strip().lower()
    query = query_template.format(
        coin_name = coin_name,
        coin_code = coin_code
    )
    coin_name_cmd = build_cmd(query, from_date, until_date, coin.code.lower(), lang)
    os.system(coin_name_cmd)

def build_cmd(keyword_arg, from_arg, until_arg, es_index_arg, lang_arg):
    command = cmd_template.format(script=script_name, text=keyword_arg,
                                  from_date=from_arg, until_date=until_arg,
                                  elastic_url=elastic_server, elastic_index = es_index_arg, language=lang_arg)
    return command

if __name__ == "__main__":
    import re
    str = "ce face ee   bos "
    str = re.sub('\s+', '%20', str).strip()
    print(str)

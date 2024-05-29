import webbrowser
import os

import requests

def gen_file(parsing_info, products, title='Result'):

    data = ''
    body_items = ''

    for product in products:

        id, name, images, price, params, link, parsing_number = product.values()

        info_rows = [
            f'экран {params[0]['text']}, {params[1]['text']}, {params[2]['text']} Гц',
            f'{params[3]['text']} {params[4]['text']}',
            f'{params[5]['text']} Гб оперативной памяти',
            f'{params[len(params) - 1]['text'].replace('встроенная', 'встроенная графика')}'
        ]

        body_items += f'''
            <div class="products__item">
                <div class="products__item--photo">
                    <img src="{images['middle']}" alt="">
                </div>
                <div class="products__item--head">
                    <h1 class="products__item--title" title="{name}">{name}</h1>
                </div>
                <div class="products__item--info">

                    {''.join([f'<div class="products__item--info__row" title="{info_row}">{info_row}</div>' for info_row in info_rows])}
                
                </div>
                <div class="products__item--price">
                    
                    { f'<h1 class="products__item--price__old">{price['old']['value']} {price['old']['currency']}</h1>' if price.get('old', False) else ''}

                    <h1 class="products__item--price__new">{price['new']['value']} {price['new']['currency']}</h1>

                </div>
                <div class="products__item--bottom">
                    <a href="{link}" class="products__item--btn" target="_blank">В магазин</a>
                </div>
            </div>
        '''.replace('    ', '').replace('\n', '')
    
    with open("templates/index.html", "r", encoding='utf-8') as file:
        lines = file.readlines()

        for line in lines:
            data += f'{line.strip()}\n'
    
    data = data.replace('@TITLE@', title)
    
    data = data.replace('@PARSEDATE@', str(parsing_info[0]))
    data = data.replace('@PARSENUMBER@', str(parsing_info[1]))
    
    # data = data.replace('@PRODUCTSNUMBG@', str(parsing_info[2]))
    data = data.replace('@PRODUCTSNUMB@', str(len(products)))

    start_index_data = data.find("<!-- REPLACE -->")
    end_index_data = data.find("<!-- REPLACE -->", start_index_data + 1) + len("<!-- REPLACE -->")

    data = data[:start_index_data] + body_items + data[end_index_data:]

    start_index_js = data.find('<script>') + len('<script>')
    end_index_js = data.find('</script>', start_index_js + 1)

    js = data[start_index_js:end_index_js]

    min_js = requests.post('https://www.toptal.com/developers/javascript-minifier/api/raw', data=dict(input=js)).text

    data = data[:start_index_js] + "{}".format(min_js) + data[end_index_js:]

    data = data.replace('\n', '')

    dist_folder = 'dist'

    if not os.path.exists(dist_folder):
        os.makedirs(dist_folder)
        
    file_to_open = f'{dist_folder}/index.html'

    with open(file_to_open, 'w+', encoding='utf-8') as file:
        file.write(data)

    webbrowser.open(f'file://{os.path.abspath(file_to_open)}')
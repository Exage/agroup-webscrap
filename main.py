from async_webscrap import run_async
from sync_webscrap import run_sync
from add_to_db import get_parsing_dates, get_products_by_number
from generate_html import gen_file

from urls import url_full

from tkinter import *
from tkinter import ttk

items_in_category = 48
numb_of_pages = 4

urls = [
    f'{url_full}?state[pages][limit]=48&state[pages][offset]={i * items_in_category}' for i in range(numb_of_pages)
]

def update_tree():
    dates = get_parsing_dates()

    for children in tree.get_children():
        tree.delete(children)

    for date in dates:
        value = (date['date'], date['parsing_number'], date['products_in_catalog'])
        tree.insert('', END, values=value)

def on_double_click(event):
    item = tree.item(tree.focus())

    parsing_info = item['values']
    parsing_number = item['values'][1]

    products = get_products_by_number(parsing_number)

    gen_file(parsing_info, products, title=f'Результат отбора №{parsing_number}')

def run_sync_handler():
    run_sync(urls)
    update_tree()

def run_async_handler():
    run_async(urls)
    update_tree()

root = Tk()
root.title("Парсер нахуй")
root.geometry("500x300")
root.minsize(300,300)

btn_sync = Button(root, command=run_sync_handler, text='Синхронно')
btn_sync.pack(fill=X, padx=5)

btn_async = Button(root, command=run_async_handler, text='Асинхронно')
btn_async.pack(fill=X, padx=5)

columns = ('date', 'parsing_number', 'products_in_catalog')
 
tree = ttk.Treeview(columns=columns, show="headings")
tree.pack(fill=BOTH, expand=1)

tree.heading("date", text="Дата")
tree.heading("parsing_number", text="Порядковый номер отбора")
tree.heading("products_in_catalog", text="Кол-во товаров в категории")

tree.column("#1", stretch=YES, width=80)
tree.column("#2", stretch=YES, width=100)
tree.column("#3", stretch=YES, width=100)

update_tree()

tree.bind("<Double-1>", on_double_click)

root.mainloop()
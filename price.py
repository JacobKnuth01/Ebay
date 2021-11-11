import requests
import bs4
import matplotlib.pyplot as plt
import tkinter
import PIL.Image
import PIL.ImageTk
import io
import tkinter.tix

def getText(info):
    if info == None:
        return "Unavalable"
    info = str(info)
    s = info.rfind(">")
    info = info[:s]
    s = info.rfind(">")
    info = info[s:]
    return info[1:-4]
def byTag(info, tag):


    if info == None:
        return "Unavalable"
    info = str(info)
    p1 = info.find(tag)

    if p1 == -1:

        return "Unavalable"
    p2 = info.find("\"", p1+len(tag))
    info = info[p1:p2]

    return info[len(tag):]
def getInfo(r):
    items = []
    for listing in r:
        name = listing.find(class_="s-item__title")
        price = listing.find(class_="s-item__price")
        image = listing.find(class_="s-item__image-img")
        url = listing.find(class_="s-item__info clearfix")
        name = getText(name)
        price = getText(price)[1:-2]
        image = byTag(image, "src=\"")
        url = byTag(url, "href=\"")

        items.append(item(name=name, price=price, url=url, image=image))
    return items
def createHistogram(items, step):
    d = []
    for i in items:
        try:
            d.append(float(i.price))
        except ValueError:
            pass

    step = float(step)
    steps = []
    m = max(d)
    pre = m / step
    x = 0
    for _ in range(int(step) + 1):
        steps.append(x)
        x = x + pre

    plt.hist(x=d)
    plt.xticks(steps)
    plt.show()
def pricesLower(price, items):
    display = []
    for i in items:
        if i.price <= price:
            display.append(i)

    return display
class item:
    def __init__(self, name, price, image, url):
        self.price= price
        self.name = name
        self.image = image
        self.url = url
def getItemAtPrice(items):
    clearPage(root)

    tkinter.Label(root, text="low").pack()
    l = tkinter.Entry(root)
    l.pack()

    tkinter.Label(root, text="high").pack()
    h = tkinter.Entry(root)
    h.pack()

    b = tkinter.Button(text="submit", command=lambda: getItemAtPrice2(items, h, l))
    b.pack()






def getItemAtPrice2(items, hi, l):
    def copyToClip(e):
        w = e.widget
        i = bs.index(w)
        u = urls[i]
        root.clipboard_clear()
        root.clipboard_append(u)

    leave = False
    def goBack():
        global leave

        leave = True
        clearPage(root)
        Selection()
    try:
        low = float(l.get())
    except ValueError:
        low = float('-inf')
    try:
        high = float(hi.get())
    except ValueError:
        high= float("inf")


    clearPage(root)
    myscrollbar = tkinter.Scrollbar(root)

    myscrollbar.pack(side=tkinter.RIGHT,fill=tkinter.Y)
    c = 250

    back = tkinter.Button(root, text="Back", command=goBack)
    back.pack()
    f = tkinter.Canvas(root, width=500, height=500, scrollregion=(0,0,0,0))
    f.config(yscrollcommand=myscrollbar.set)
    myscrollbar.config(command=f.yview)
    f.pack()

    y = 250
    images = []

    urls = []
    bs = []

    for i in items:
        display = True

        try:
            p = float(i.price)
            if p < low:
                display = False
            if p > high:
                display = False

            if display:

                if i.image != "Unavalable":
                    r = requests.get(i.image)
                    image = r.content
                    image = PIL.Image.open(io.BytesIO(image))
                    image = PIL.ImageTk.PhotoImage(image)
                    images.append(image)
                    f.create_image(250, y, image=images[-1])
                    hight = image.height()

                    f.create_text(250, y+(hight/2), text=i.name)
                    f.create_text(250, y + (hight / 2)+10, text=i.price)


                    urls.append(i.url)
                    button1 = tkinter.Button( text="copy URL")
                    bs.append(button1)
                    bs[-1].bind("<Button-1>", copyToClip)
                    f.create_window(250, y+(hight / 2)+30, window=bs[-1])

                    y = y+hight+100




        except ValueError:
            pass
    f.configure(scrollregion=(0, 0, 0, y))
    while not leave:
        try:
            root.update()
        except tkinter.TclError:

            break


def getImage(url):
    c = requests.get(url)
    raw = c.content
    image = PIL.Image.open(io.BytesIO(raw))
    image = PIL.ImageTk.PhotoImage(image)
    return image
def displaySelection(image, root):
    l = tkinter.Label(root, image=image)
    l.pack()



def clearPage(root):
    widget_list = root.winfo_children()
    for item in widget_list:
        item.pack_forget()










def searchCommand():
    global search
    global url
    global items
    global refined
    s = search.get()
    url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=" + s + "&_sacat=0&rt=nc&LH_BIN=1"
    s = requests.Session()
    r = s.get(url)
    soup = bs4.BeautifulSoup(r.content, "html.parser")
    r = soup.find_all(class_="s-item")
    items = getInfo(r)
    found = False
    for i in items:
        try:
            float(i.price)
            found = True
        except ValueError:
            pass
    if not found:
        tkinter.Label(root, text="Nothing was found").pack()
        return
    refined = []
    clearPage(root)
    Selection()
def histogram():
    createHistogram(items, 15)
def refine():
    global items
    global refined
    global x
    def canc():
        global refined
        global x
        clearPage(root)
        refined = []
        Selection()
        x = 0



    while items[x].image == "Unavalable":
        x = x + 1
    i = items[x]
    clearPage(root)
    cancel = tkinter.Button(root, text="cancel", command=canc)
    cancel.pack()
    image = getImage(i.image)
    pic = tkinter.Label(root, image=image)
    pic.photo = image
    pic.pack()
    l = tkinter.Label(root, text=i.name)
    l.pack()
    l2 = tkinter.Label(root, text=i.price)

    l2.pack()
    b = tkinter.Button(root, text="yes", command= lambda: yes(i))
    b2 = tkinter.Button(root, text="no", command = next)
    b.pack()
    b2.pack()




def next():
    global x
    global items

    x = x + 1
    if x < len(items):
        refine()
    else:
        items = refined
        clearPage(root)
        Selection()


def yes(i):
    global refined
    refined.append(i)
    next()

def Selection():
    o1 = tkinter.Button(root, text="Create histogram", command=histogram)
    o2 = tkinter.Button(root,text="refine results", command=refine)
    o3 = tkinter.Button(root,text="view items", command=lambda: getItemAtPrice(items))
    o1.pack()
    o2.pack()
    o3.pack()

x = 0
url = ""
h = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
items = []
refined = []


root = tkinter.Tk()
search = tkinter.Entry(root)
go = tkinter.Button(root, text="Search", command=searchCommand)

search.pack()
go.pack()

while True:
    try:
        root.update()
    except tkinter.TclError:
        exit()

























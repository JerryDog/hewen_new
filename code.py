# -*- coding: utf-8 -*-
import web
import sys
import uuid
import json

reload(sys)
sys.setdefaultencoding('utf-8')
urls = (
  '/', 'index',
  '/about', 'about',
  '/hwt_prod', 'hwt_prod',
  '/services', 'services',
  '/news', 'news',
  '/news/(\d+)', 'single_news',
  '/books_item', 'books_item',
  '/books/(\d+)?', 'books',
  '/hr', 'hr',
  '/page_404', 'page_404',
  '/shortcodes', 'shortcodes',
  '/contact_us', 'contact_us',
  '/upload', 'upload'
)

render = web.template.render('templates/')
db = web.database(dbn='mysql', user='root', pw='Hewenchina2015', db='hewen')

class index:
    def GET(self):
        return render.index()

class about:
    def GET(self):
        return render.about()

class hwt_prod:
    def GET(self):
        return render.hwt_prod()

class news:
    def GET(self):
        news = db.select('cn_news')
        return render.news(news)

class single_news:
    def GET(self, news_id):
        news_list = db.select('cn_news', where='id=%s' % news_id)
        news = news_list[0]
        return render.news_item(news)

class services:
    def GET(self):
        return render.services()

class books_item:
    def GET(self):
        return render.books_item()

class books:
    def GET(self, page):
        books = db.select('books')
        if not page:
            pages = [1,]
            return render.books(books, pages)
        else:
            interval = 5
            if len(books) <= interval:
                pages = [1,]
            else:
                pages = [i for i in range(1, (len(books) - 1)/interval + 2)]
            page = int(page)
            start = (page - 1) * interval
            end = page * interval
            page_books = []
            for i in range(start,end):
                try:
                    page_books.append(books[i])
                except:
                    pass
            if page == 1:
                pre = 1
                next = pre + 1
                if next > len(pages):
                    next = len(pages)
            else:
                pre = page - 1
                next = pre + 1
                if next > len(pages):
                    next = len(pages)
            return render.books(page_books, pages, pre, next)

class hr:
    def GET(self):
        return render.hr()

class shortcodes:
    def GET(self):
        return render.shortcodes()

class contact_us:
    def GET(self):
        return render.contact_us()
    def POST(self):
        from utils import send_mail
        i = web.input()
        name = i.get('name')
        email = i.get('email')
        phone = i.get('phone', '')
        company = i.get('company', '')
        sub = i.get('subject')
        content = i.get('content')
        mix_content = '姓名: %s\n' \
                      '邮箱: %s\n' \
                      '电话: %s\n' \
                      '公司: %s\n' \
                      '内容: %s\n' % \
                      (name, email, phone, company, content)
        if send_mail(['564778704@qq.com'], sub, mix_content):
            message =  "发送成功"
        else:
            message =  "发送失败"
        pyDict = {"message": message}
        web.header('Content-Type', 'application/json')
        return json.dumps(pyDict)

class upload:
    def GET(self):
        return render.upload()

    def POST(self):
        i = web.input(picture={})
        book_name = i.get('book_name')
        content = i.get('content')
        filename = uuid.uuid1()
        file_path = 'static/book_images/%s.jpg' % filename
        f = open(file_path,'wb')
        f.write(i.picture.file.read())
        f.close()
        db.insert('books', book_name=book_name, file_path=file_path, content=content)
        raise web.seeother('/upload')


class page_404:
    def GET(self):
        return render.page_404()

#if __name__ == "__main__":
#app = web.application(urls, globals())
#application = app.wsgifunc()
app = web.application(urls, globals())
application = app.wsgifunc()

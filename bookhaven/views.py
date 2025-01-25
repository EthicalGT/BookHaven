from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
import pymysql
import pymysql.cursors

def homepage(req):
    return render(req,"homepage.html")

def booksinfo(req):
    conn=pymysql.connect(
        host='localhost',
        user='root',
        password=None,
        database='bookhaven',
        cursorclass=pymysql.cursors.DictCursor
    )
    booksdata=[]
    try:
        with conn.cursor() as cr:
            sql="""SELECT 
    b.book_id, 
    b.isbn, 
    b.title, 
    b.year, 
    b.price, 
    p.name AS publisher_name, 
    p.address AS publisher_address, 
    a.name AS author_name, 
    w.location AS warehouse_location, 
    bw.copies AS available_copies
FROM 
    Book b
JOIN 
    Publisher p ON b.publisher_id = p.publisher_id
JOIN 
    BookAuthor ba ON b.book_id = ba.book_id
JOIN 
    Author a ON ba.author_id = a.author_id
JOIN 
    BookWarehouse bw ON b.book_id = bw.book_id
JOIN 
    Warehouse w ON bw.warehouse_id = w.warehouse_id;
"""
            cr.execute(sql)
            res=cr.fetchall()
            if res:
                for i in res:
                    booksdata.append({
                        'bookid': i['book_id'],
                        'isbn': i['isbn'],
                        'title': i['title'],
                        'year': i['year'],
                        'price': i['price'],
                        'pname': i['publisher_name'],
                        'paddr': i['publisher_address'],
                        'authorname': i['author_name'],
                        'wareloc': i['warehouse_location'],
                        'availcopies': i['available_copies']
                    })
    except Exception as e:
        print(f"Error->{e}")
    finally:
        conn.close()
    return render(req,"books.html",{'books':booksdata})

def publishersinfo(req):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password=None,
        database='bookhaven',
        cursorclass=pymysql.cursors.DictCursor
    )
    publishersdata = []
    try:
        with conn.cursor() as cr:
            sql = """
            SELECT 
                p.publisher_id, 
                p.name AS publisher_name, 
                p.address AS publisher_address, 
                b.title AS book_title,
                b.isbn AS book_isbn,
                w.location AS warehouse_location,
                bw.copies AS available_copies
            FROM 
                Publisher p
            JOIN 
                Book b ON p.publisher_id = b.publisher_id
            JOIN 
                BookWarehouse bw ON b.book_id = bw.book_id
            JOIN 
                Warehouse w ON bw.warehouse_id = w.warehouse_id;
            """
            cr.execute(sql)
            res = cr.fetchall()
            if res:
                for i in res:
                    publishersdata.append({
                        'publisher_id': i['publisher_id'],
                        'publisher_name': i['publisher_name'],
                        'publisher_address': i['publisher_address'],
                        'book_title': i['book_title'],
                        'book_isbn': i['book_isbn'],
                        'warehouse_location': i['warehouse_location'],
                        'available_copies': i['available_copies']
                    })
    except Exception as e:
        print(f"Error->{e}")
    finally:
        conn.close()
    return render(req, "publisher.html", {'publishers': publishersdata})

def warehouseinfo(req):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password=None,
        database='bookhaven',
        cursorclass=pymysql.cursors.DictCursor
    )
    warehousesdata = []
    try:
        with conn.cursor() as cr:
            sql = """
            SELECT 
    w.warehouse_id, 
    w.location AS warehouse_location, 
    w.phone AS warehouse_phone,
    b.title AS book_title, 
    b.isbn AS book_isbn, 
    bw.copies AS available_copies
FROM 
    Warehouse w
JOIN 
    BookWarehouse bw ON w.warehouse_id = bw.warehouse_id
JOIN 
    Book b ON bw.book_id = b.book_id;

            """
            cr.execute(sql)
            res = cr.fetchall()
            if res:
                for i in res:
                    warehousesdata.append({
                        'warehouse_id': i['warehouse_id'],
                        'warehouse_location': i['warehouse_location'],
                        'warehouse_phone': i['warehouse_phone'],
                        'book_title': i['book_title'],
                        'book_isbn': i['book_isbn'],
                        'available_copies': i['available_copies']
                    })
    except Exception as e:
        print(f"Error->{e}")
    finally:
        conn.close()
    return render(req, "warehouse.html", {'warehouses': warehousesdata})

def adminlogin(req):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password=None,
        database='bookhaven',
        cursorclass=pymysql.cursors.DictCursor
    )
    if req.method=='POST':
        admin=req.POST.get('tb1')
        pwd=req.POST.get('tb2')
        try:
            with conn.cursor() as cr:
                cr.execute("select * from adminlogin where admin=%s and password=%s",(admin,pwd))
                res=cr.fetchall()
                if res:
                    return render(req,"admindashboard.html")
                else:
                    return HttpResponse("<html><body><script>alert('Invalid Credentials!'); window.location='adminlogin';</script></body></html>")
        except Exception as e:
            print("Error->",e)
        finally:
            conn.close()
    return render(req,"adminlogin.html")
    
def admindashboard(req):
    return  render(req,"admindashboard.html")

def add_book(req):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password=None,
        database='bookhaven',
        cursorclass=pymysql.cursors.DictCursor
    )
    if req.method == 'POST':
        isbn = req.POST.get('isbn')
        title = req.POST.get('title')
        year = req.POST.get('year')
        price = req.POST.get('price')
        publisher_id = req.POST.get('publisher_id')
        author_ids = req.POST.getlist('author_ids')
        warehouse_id = req.POST.get('warehouse_id')
        copies = req.POST.get('copies')

        try:
            with conn.cursor() as cr:
                cr.execute(
                    "INSERT INTO Book (isbn, title, year, price, publisher_id) VALUES (%s, %s, %s, %s, %s)",
                    (isbn, title, year, price, publisher_id)
                )
                book_id = conn.insert_id()
                for author_id in author_ids:
                    cr.execute(
                        "INSERT INTO BookAuthor (book_id, author_id) VALUES (%s, %s)",
                        (book_id, author_id)
                    )
                cr.execute(
                    "INSERT INTO BookWarehouse (book_id, warehouse_id, copies) VALUES (%s, %s, %s)",
                    (book_id, warehouse_id, copies)
                )
                conn.commit()
                return HttpResponse(
                    "<html><body><script>alert('Book added successfully!'); window.location='addbook';</script></body></html>"
                )
        except Exception as e:
            conn.rollback()
            print("Error:", e)
            return HttpResponse(
                f"<html><body><script>alert('An error occurred: {e}'); window.location='addbook';</script></body></html>"
            )
        finally:
            conn.close()
    else:
        publishers = []
        authors = []
        warehouses = []
        try:
            with conn.cursor() as cr:
                cr.execute("SELECT publisher_id, name FROM Publisher")
                publishers = cr.fetchall()
                cr.execute("SELECT author_id, name FROM Author")
                authors = cr.fetchall()
                cr.execute("SELECT warehouse_id, location FROM Warehouse")
                warehouses = cr.fetchall()
        except Exception as e:
            print("Error:", e)
        finally:
            conn.close()

        return render(req, 'addbook.html', {
            'publishers': publishers,
            'authors': authors,
            'warehouses': warehouses
        })

def add_publisher(req):
    if req.method == 'POST':
        name = req.POST.get('name')
        address = req.POST.get('address')
        pid = req.POST.get('id')

        conn = pymysql.connect(
            host='localhost',
            user='root',
            password=None,
            database='bookhaven',
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with conn.cursor() as cr:
                sql = "INSERT INTO Publisher (publisher_id, name, address) VALUES (%s,%s, %s)"
                cr.execute(sql, (pid,name, address))
                conn.commit()
                return HttpResponse("<html><body><script>alert('Publisher added successfully!'); window.location='addpublisher';</script></body></html>")
        except Exception as e:
            print(f"Error: {e}")
            return HttpResponse("<html><body><script>alert('Failed to add publisher. Try again.'); window.location='addpublisher';</script></body></html>")
        finally:
            conn.close()
    else:
        return render(req, 'addpublisher.html')


def add_author(req):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password=None,
        database='bookhaven',
        cursorclass=pymysql.cursors.DictCursor
    )
    if req.method == 'POST':
        name = req.POST.get('name')
        email = req.POST.get('email')
        aid = req.POST.get('id')
        try:
            with conn.cursor() as cr:
                sql = """
                INSERT INTO Author (author_id,name, email) 
                VALUES (%s, %s, %s)
                """
                cr.execute(sql, (aid,name, email))
                conn.commit()
                return HttpResponse("<html><body><script>alert('Author added successfully!'); window.location='addauthor';</script></body></html>")
        except Exception as e:
            print(f"Error -> {e}")
            return HttpResponse("<html><body><script>alert('Error adding author. Please try again!'); window.location='addauthor';</script></body></html>")
        finally:
            conn.close()
    return render(req, 'addauthor.html')

def add_warehouse(request):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password=None,
        database='bookhaven',
        cursorclass=pymysql.cursors.DictCursor
    )
    if request.method == 'POST':
        wid=request.POST.get('id')
        location = request.POST.get('location')
        phone = request.POST.get('phone')
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO Warehouse (warehouse_id,location, phone) VALUES (%s,%s, %s)"
                cursor.execute(sql, (wid,location, phone))
                conn.commit()
            return HttpResponse("<html><body><script>alert('Warehouse added successfully!'); window.location='addwarehouse';</script></body></html>")
        except Exception as e:
            print(f"Error: {e}")
            return HttpResponse("<html><body><script>alert('Error occurred while adding warehouse.'); window.location='addwarehouse';</script></body></html>")
        finally:
            conn.close()
    else:
        return render(request, "addwarehouse.html")
    
from django.shortcuts import render, redirect
from django.http import HttpResponse
import pymysql

from django.shortcuts import render
from django.http import HttpResponse
import pymysql

from django.shortcuts import render
from django.http import HttpResponse
import pymysql

def delete_book(request):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password=None,
        database='bookhaven',
        cursorclass=pymysql.cursors.DictCursor
    )

    if request.method == 'POST':
        book_id = request.POST.get('book_id')

        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM bookwarehouse WHERE book_id = %s", (book_id,))
                cursor.execute("DELETE FROM bookauthor WHERE book_id = %s", (book_id,))
                cursor.execute("DELETE FROM book WHERE book_id = %s", (book_id,))
                conn.commit()

                return HttpResponse("<html><body><script>alert('Book and its related records deleted successfully!'); window.location='deletebook';</script></body></html>")

        except Exception as e:
            print(f"Error: {e}")
            return HttpResponse("<html><body><script>alert('An error occurred while deleting the book.'); window.location='deletebook';</script></body></html>")
        finally:
            conn.close()

    return render(request, "deletebook.html")

def delete_author(request):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password=None,
        database='bookhaven',
        cursorclass=pymysql.cursors.DictCursor
    )

    if request.method == 'POST':
        author_id = request.POST.get('author_id')

        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM author WHERE author_id = %s", (author_id,))
                conn.commit()

                return HttpResponse("<html><body><script>alert('Author records deleted successfully!'); window.location='deleteauthor';</script></body></html>")

        except Exception as e:
            print(f"Error: {e}")
            return HttpResponse("<html><body><script>alert('An error occurred while deleting the author.'); window.location='deleteauthor';</script></body></html>")
        finally:
            conn.close()

    return render(request, "deleteauthor.html")

def delete_publisher(request):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password=None,
        database='bookhaven',
        cursorclass=pymysql.cursors.DictCursor
    )

    if request.method == 'POST':
        pub_id = request.POST.get('pub_id')

        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM publisher WHERE publisher_id = %s", (pub_id,))
                conn.commit()

                return HttpResponse("<html><body><script>alert('Publisher records deleted successfully!'); window.location='deletepublisher';</script></body></html>")

        except Exception as e:
            print(f"Error: {e}")
            return HttpResponse("<html><body><script>alert('An error occurred while deleting the Publisher.'); window.location='deletepublisher';</script></body></html>")
        finally:
            conn.close()

    return render(request, "deletepublisher.html")

def delete_warehouse(request):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password=None,
        database='bookhaven',
        cursorclass=pymysql.cursors.DictCursor
    )

    if request.method == 'POST':
        ware_id = request.POST.get('ware_id')

        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM warehouse WHERE warehouse_id = %s", (ware_id,))
                conn.commit()

                return HttpResponse("<html><body><script>alert('Warehouse records deleted successfully!'); window.location='deletewarehouse';</script></body></html>")

        except Exception as e:
            print(f"Error: {e}")
            return HttpResponse("<html><body><script>alert('An error occurred while deleting the Publisher.'); window.location='deletewarehouse';</script></body></html>")
        finally:
            conn.close()

    return render(request, "deletewarehouse.html")


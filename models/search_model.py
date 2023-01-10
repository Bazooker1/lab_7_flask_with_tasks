import pandas as pd


def get_publisher(conn):
    return pd.read_sql('''
        SELECT publisher_id, publisher_name, COUNT(book.book_id)
        FROM publisher
        JOIN book USING(publisher_id)
        GROUP BY publisher_name''', conn)


def get_genre(conn):
    return pd.read_sql('''
        SELECT genre_id, genre_name, COUNT(book.book_id)
        FROM genre
        JOIN book USING(genre_id)
        GROUP BY genre_name''', conn)


def get_author(conn):
    return pd.read_sql('''
        SELECT author_id, author_name, COUNT(book.book_id)
        FROM author
        JOIN book_author USING(author_id)
        JOIN book USING(book_id)
        GROUP BY author_name''', conn)


def convert(list):
    # Converting integer list to string list
    s = [str(i) for i in list]

    # Join list items using join()
    res = ",".join(s)

    return res

def card(conn, publishers, genres, authors):
    publishers = convert(publishers)
    authors = convert(authors)
    genres = convert(genres)
    return pd.read_sql(f'''
    SELECT Название,
    GROUP_CONCAT(Авторы),
    Жанр,
    Издательство,
    Год_издания,
    Количество,
    COUNT(*)
    FROM (SELECT
        	title AS Название,
        	author_name AS Авторы,
        	genre_name AS Жанр,
        	publisher_name AS Издательство,
            year_publication AS Год_издания,
            available_numbers AS Количество,
            book_id AS id
        FROM book
        JOIN genre USING(genre_id)
        JOIN publisher USING(publisher_id)
        JOIN book_author USING(book_id)
        JOIN author USING(author_id)
        WHERE (genre_id IN ({genres}) OR ({not genres}))
            AND (publisher_id IN ({publishers}) OR ({not publishers}))
            AND (author_id IN ({authors}) OR ({not authors})) ) AS q1
        INNER JOIN (SELECT book_id, COUNT(*) AS count_auth
        FROM book_author
        GROUP BY book_id) AS q2 ON id = book_id
    GROUP BY id
    HAVING COUNT(*) = count_auth    
    ''', conn)
from cassandra.cluster import Cluster
import uuid

# ==============================
# CQL Statements
# ==============================
CREATE_KEYSPACE = """
CREATE KEYSPACE IF NOT EXISTS movies
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
"""
CREATE_TABLE_MOVIE_BY_TITLE = """
CREATE TABLE IF NOT EXISTS movies.movie_by_title (
    movie_id UUID,
    title TEXT,
    release_year INT,
    genre TEXT,
    rating FLOAT,
    director TEXT,
    PRIMARY KEY (title, release_year)
);
"""
CREATE_TABLE_MOVIE_BY_GENRE = """
CREATE TABLE IF NOT EXISTS movies.movie_by_genre (
    movie_id UUID,
    title TEXT,
    release_year INT,
    genre TEXT,
    rating FLOAT,
    director TEXT,
    PRIMARY KEY (genre, rating, movie_id)
) WITH CLUSTERING ORDER BY (rating DESC, movie_id ASC);
"""
INSERT_MOVIE_TITLE = """
INSERT INTO movies.movie_by_title (movie_id, title, release_year, director, genre, rating)
VALUES (%s, %s, %s, %s, %s, %s);
"""
INSERT_MOVIE_GENRE = """
INSERT INTO movies.movie_by_genre (movie_id, title, release_year, director, genre, rating)
VALUES (%s, %s, %s, %s, %s, %s);
"""
DELETE_MOVIE_TITLE = ""
DELETE_MOVIE_GENRE = ""
SELECT_BY_TITLE = """
SELECT movie_id, title, release_year, genre, rating, director
FROM movies.movie_by_title
WHERE title = %s AND release_year = %s;
"""
SELECT_BY_GENRE = """
SELECT title, rating, release_year, director
FROM movies.movie_by_genre
WHERE genre = %s;
"""

# ==============================
# Funciones base
# ==============================
def create_keyspace_and_tables(session):
    session.execute(CREATE_KEYSPACE)
    session.execute(CREATE_TABLE_MOVIE_BY_TITLE)
    session.execute(CREATE_TABLE_MOVIE_BY_GENRE) 

def insert_movie(session, title, year, director, genre, rating):
    movie_id = uuid.uuid4()
    
    # Inserción en movie_by_title
    session.execute(
        INSERT_MOVIE_TITLE,
        (movie_id, title, year, director, genre, float(rating))
    )
    
    # Inserción en movie_by_genre
    session.execute(
        INSERT_MOVIE_GENRE,
        (movie_id, title, year, director, genre, float(rating))
    )
    print(f" Película '{title}' ({year}) agregada a ambas tablas.")  

def query_by_title(session, title, year):
    rows = session.execute(SELECT_BY_TITLE, (title, int(year)))
    row = rows.one()

    if row:
        print(f"\n{row.title} ({row.release_year}) | Director: {row.director} | Género: {row.genre} | Rating: {row.rating}")
    else:
        print("\nPelícula no encontrada.")

def query_by_genre(session, genre):
    rows = session.execute(SELECT_BY_GENRE, (genre,))
    results = list(rows)

    if results:
        print(f"\nPelículas del género '{genre}':")
        for row in results:
            print(f"- {row.title} ({row.release_year}) — {row.rating}")
    else:
        print(f"\nNo se encontraron películas para el género '{genre}'.")

def update_movie_director(session, title, genre, new_director):
    pass  

def delete_movie(session, title, genre, rating, release_year):
    pass
# ==============================
# Menú
# ==============================
def main():
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()

    create_keyspace_and_tables(session)

    while True:
        print("\n=== Movie Database Menu ===")
        print("1. Insertar película")
        print("2. Consultar por título")
        print("3. Consultar por género")
        print("4. Actualizar director")
        print("0. Salir")
        choice = input("Seleccione opción: ")

        if choice == "1":
            title = input("Título: ")
            year = int(input("Año: "))
            director = input("Director: ")
            genre = input("Género: ")
            rating = float(input("Rating: "))
            insert_movie(session, title, year, director, genre, rating)
        elif choice == "2":
            title = input("Título: ")
            year = int(input("Año: "))
            query_by_title(session, title, year)
        elif choice == "3":
            genre = input("Género: ")
            query_by_genre(session, genre)
        elif choice == "4":
            title = input("Título: ")
            genre = input("Género: ")
            new_director = input("Nuevo Director: ")
            update_movie_director(session, title, genre, new_director)
        elif choice == "5":
            # Eliminar de movie_by_title -> title, release_year
            # Eliminar de movie_by_genre -> genre, rating
            title = input("Título: ")
            genre = input("Género: ")
            rating = input("Rating: ")
            release_year = input("Año: ")
            delete_movie(session, title, genre, rating, release_year)
        elif choice == '0':
            # Cerrar conexión y salir
            pass
        else:
            print("Opción inválida")
            break

if __name__ == "__main__":
    main()
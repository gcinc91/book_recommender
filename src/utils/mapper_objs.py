
def  mapper_object_list(arr):
    
    res = []
    for i in arr:
        res.append({
            "book_id": i[0],
            "goodreads_book_id": i[1],
            "books_count":  i[2],
            "isbn": i[3],
            "isbn13": i[4],
            "authors": i[5],
            "original_publication_year": i[6],
            "original_title": i[7],
            "title": i[8],
            "language_code": i[9],
            "average_rating": i[10],
            "ratings_count": i[11],
            "ratings_1": i[12],
            "ratings_2": i[13],
            "ratings_3": i[14],
            "ratings_4": i[15],
            "ratings_5": i[16],
            "image_url": i[17],
            "small_image_url": i[18],
            "category": i[19],
            "f_categories":i[20]
        })

    return res

SELECT AVG(rating) FROM ratings
JOIN movies on ratings.movie_id = movies.id
WHERE year = 2012;

CREATE TABLE IF NOT EXISTS films(
  movie_id BIGINT PRIMARY KEY,
  title TEXT,
  watched BOOLEAN,
  lists TEXT[]
);

CREATE TABLE IF NOT EXISTS lists(
  list_id BIGINT PRIMARY KEY,
  name TEXT,
  films TEXT[]
);


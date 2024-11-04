CREATE TABLE IF NOT EXISTS films(
  film_id SERIAL PRIMARY KEY,
  title TEXT,
  watched BOOLEAN,
  lists TEXT[]
);

CREATE TABLE IF NOT EXISTS lists(
  list_id SERIAL PRIMARY KEY,
  name TEXT,
  films TEXT[]
);

ALTER TABLE lists ALTER COLUMN films SET DEFAULT array[]::text[];

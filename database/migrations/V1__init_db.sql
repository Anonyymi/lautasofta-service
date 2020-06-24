CREATE TABLE boards (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  path VARCHAR(16) NOT NULL,
  name VARCHAR(128) NOT NULL,
  description VARCHAR(1028) NULL,
  flag_hidden BOOLEAN NOT NULL DEFAULT false,
  flag_nsfw BOOLEAN NOT NULL DEFAULT false
);

INSERT INTO boards (path, name, description)
VALUES
  ('b', 'random', 'random stuff'),
  ('a', 'anime', 'weeb stuff'),
  ('v', 'vidya', 'video games')
;

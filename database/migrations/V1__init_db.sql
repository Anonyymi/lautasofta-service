CREATE TABLE boards (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  path VARCHAR(16) NOT NULL,
  name VARCHAR(128) NOT NULL,
  description VARCHAR(1028) NULL,
  flag_hidden BOOLEAN NOT NULL DEFAULT false,
  flag_nsfw BOOLEAN NOT NULL DEFAULT false
);

INSERT INTO boards (path, name, description, flag_hidden, flag_nsfw)
VALUES
  ('b', 'random', 'random stuff', false, true),
  ('a', 'anime', 'weeb stuff', false, false),
  ('v', 'vidya', 'video games', false, false)
;

CREATE TABLE posts (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  board_id INT NOT NULL,
  thread_id INT NULL DEFAULT NULL,
  data_message VARCHAR(4096) NOT NULL,
  data_filepath VARCHAR(1028) NULL DEFAULT NULL,
  datetime_created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  timestamp_edited TIMESTAMP NULL DEFAULT NULL,
  FOREIGN KEY (board_id) REFERENCES boards(id) ON DELETE CASCADE,
  FOREIGN KEY (thread_id) REFERENCES posts(id) ON DELETE CASCADE
);

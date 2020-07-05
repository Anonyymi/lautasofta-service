CREATE TABLE boards (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  path VARCHAR(16) NOT NULL,
  name VARCHAR(128) NOT NULL,
  description VARCHAR(1024) NULL,
  flag_hidden BOOLEAN NOT NULL DEFAULT false,
  flag_nsfw BOOLEAN NOT NULL DEFAULT false
);

INSERT INTO boards (path, name, description, flag_hidden, flag_nsfw)
VALUES
  ('b', 'random', 'random stuff', false, true),
  ('a', 'anime', 'weeb stuff', false, false),
  ('v', 'vidya', 'video games', false, false)
;

CREATE TABLE anons (
  ipv4_addr INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  timestamp_created_thread TIMESTAMP NOT NULL DEFAULT DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 1 DAY),
  timestamp_created_post TIMESTAMP NOT NULL DEFAULT DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 1 DAY)
);

CREATE TABLE posts (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  board_id INT NOT NULL,
  thread_id INT NULL DEFAULT NULL,
  data_message VARCHAR(4096) NOT NULL,
  data_filepath VARCHAR(1024) NULL DEFAULT NULL,
  data_thumbpath VARCHAR(1024) NULL DEFAULT NULL,
  datetime_created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  timestamp_edited TIMESTAMP NULL DEFAULT NULL,
  timestamp_bumped TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  ipv4_addr INT UNSIGNED NULL,
  deleted BOOLEAN NOT NULL DEFAULT false,
  FOREIGN KEY (board_id) REFERENCES boards(id) ON DELETE CASCADE,
  FOREIGN KEY (thread_id) REFERENCES posts(id) ON DELETE CASCADE,
  FOREIGN KEY (ipv4_addr) REFERENCES anons(ipv4_addr) ON DELETE CASCADE
);

-- NOTE: requires event_scheduler=ON configuration
CREATE EVENT AutoDeleteOldPosts
ON SCHEDULE EVERY 1 DAY STARTS CURRENT_TIMESTAMP
DO
  DELETE LOW_PRIORITY
  FROM posts
  WHERE
    thread_id IS NULL
  AND
    datetime_created < DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 1 MONTH)
;

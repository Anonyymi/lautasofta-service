      (
        SELECT
          t.id AS id,
          t.board_id AS board_id,
          t.thread_id AS thread_id,
          t.data_message AS data_message,
          t.data_filepath AS data_filepath,
          t.datetime_created AS datetime_created,
          t.timestamp_edited AS timestamp_edited
        FROM posts AS t
        WHERE t.board_id = %s AND t.thread_id IS NULL
        ORDER BY t.timestamp_edited DESC, t.datetime_created DESC
        LIMIT %s OFFSET %s
      )

      UNION

      (
        SELECT
          r.id AS id,
          r.board_id AS board_id,
          r.thread_id AS thread_id,
          r.data_message AS data_message,
          r.data_filepath AS data_filepath,
          r.datetime_created AS datetime_created,
          r.timestamp_edited AS timestamp_edited
        FROM (
          SELECT
            t.id AS id
          FROM posts AS t
          WHERE t.board_id = %s AND t.thread_id IS NULL
          ORDER BY t.timestamp_edited DESC, t.datetime_created DESC
          LIMIT %s OFFSET %s
        ) AS t
        JOIN posts AS r ON r.thread_id = t.id
      )
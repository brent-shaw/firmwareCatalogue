CREATE TABLE IF NOT EXISTS vendor (
    "id" INTEGER PRIMARY KEY,
    "name" TEXT
);

CREATE TABLE IF NOT EXISTS device (
    "id" INTEGER PRIMARY KEY,
    "model" TEXT,
    "vendor" INTEGER
);

CREATE TABLE IF NOT EXISTS firmware (
    "id" INTEGER PRIMARY KEY,
    "device" INTEGER,
    "vendor" INTEGER,
    "revision" TEXT,
    "entropy_plot" TEXT,
    "path" TEXT,
    "md5" TEXT
);

CREATE TABLE IF NOT EXISTS directory (
    "id" INTEGER PRIMARY KEY,
    "firmware" INTEGER,
    "parent" INTEGER,
    "directory_name" TEXT,
    "original_path" TEXT,
    "md5" TEXT
);

CREATE TABLE IF NOT EXISTS file (
    "id" INTEGER PRIMARY KEY,
    "directory" INTEGER,
    "firmware" INTEGER,
    "file_name" TEXT,
    "original_path" TEXT,
    "size" INTEGER,
    "md5" TEXT
);

CREATE TABLE IF NOT EXISTS link (
    "id" INTEGER PRIMARY KEY,
    "directory" INTEGER,
    "firmware" INTEGER,
    "file_name" TEXT,
    "original_path" TEXT,
    "end_location" TEXT
);

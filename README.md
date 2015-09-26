## Objective

If you have a Parse.com project, the data is stored on their servers and can be fetched to your local machine in one of two ways:
- Sending HTTP queries using Parse REST API
- Using "Export Data" tool to obtain a zipped archive of `*.json` files containing all your data (one `*.json` file for each Parse "class")

This repository contains Python code that allows copying Parse data into your own relational database. You might want to do so for the following reasons:
- Data warehousing:
 - Saving daily snapshots of Parse data
 - Maintaining a relational replica of Parse data for backup
- Running SQL queries for data analysis:
 - You might be more proficient with SQL than with the querying DSL proposed by Parse
 - You might need to use table joins with data that is *not* stored on Parse
 - You might want to use BI and Data Mining tools that do not "understand" Parse data (SPSS Modeler, Knime, Rapidminer, Excel)
- Migrating Parse data to another backend solution

## Features

Currently only PostgreSQL is supported.

Features ready:
- Type recognition and conversion into appropriate DB column type:
 - All columns can have NULL values by default! This is because Parse data does not guarantee non-empty cells for any column except `objectId`, `createdAt`, `updatedAt`.
 - Parse Date, `createdAt`, `updatedAt` => Timestamp without time zone
 - Parse GeoPoint(lat, long) => Text (`'%f %f' % (lat, long)`)
 - Parse Pointer => Text (containing `objectId`)
 - Parse Boolean => Boolean
 - Parse Numeric => Numeric
 - Everything else => Text
- **Directory-based snapshots**: Getting all `<class>.json` files from a directory, creating a new schema named `Snapshot_YYYY_MM_DD` and converting each file into a new table named `<class>`, rows filled with class instances.
- **Pandas DataFrame**: Converting result sets into Pandas DataFrames with appropriate column `dtype`s.

Future features:
- Http-based snapshots
- Http-based incremental inserts/updtes to a single live replica
- MySQL support

## Usage
```
cd <parse-tools-python directory>
virtualenv -p /usr/bin/python2.7 env
env/bin/pip install -r requirements.txt
env/bin/python test.py
```
[Todo 1: add sample data sets and explain test.py for Postgres usage]
[Todo 2: use IPython notebook for better illustration of working with Pandas DataFrame]


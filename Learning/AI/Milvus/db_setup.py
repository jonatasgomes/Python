from pymilvus import connections, db, Role, utility
from pymilvus import CollectionSchema, FieldSchema, DataType, Collection

connections.add_connection(
  learn={
    "host": "localhost",
    "port": "19530",
    "username": "",
    "password": ""
  }
)

# List all connections
connection_id = "learn"
connections.connect(connection_id)
print(connections.list_connections())

# List all databases and create a new database if not exists
current_dbs = db.list_database(using=connection_id)
print('Databases: ', current_dbs)
db_name = 'linkedin_db'
if db_name not in current_dbs:
  print('Creating database...', db_name)
  db.create_database(db_name, using=connection_id)
  print(f"Database {db_name} created.")
db.using_database(db_name, using=connection_id)
print(f"Using database {db_name}.")

# List all users and create a new user if not exists
current_users = utility.list_usernames(using=connection_id)
print('Users: ', current_users)
new_user = 'linkedin_user'
if new_user not in current_users:
  print('Creating user...', new_user)
  utility.create_user(new_user, "password", using=connection_id)
  print(f"User {new_user} created.")

  # Assign role to user
  public_role = Role(name="public", using=connection_id)
  print('Role public exists? ', public_role.is_exist())
  public_role.add_user(new_user)
  print(f"User {new_user} assigned to role {public_role.name}.")

# Define fields
course_id = FieldSchema(
  name="course_id",
  dtype=DataType.INT64,
  is_primary=True,
  max_length=32
)
title = FieldSchema(
  name="title",
  dtype=DataType.VARCHAR,
  max_length=256
)
description = FieldSchema(
  name="description",
  dtype=DataType.VARCHAR,
  max_length=2048
)
desc_embedding = FieldSchema(
  name="desc_embedding",
  dtype=DataType.FLOAT_VECTOR,
  dim=1536
)

# Define schema
wiki_schema = CollectionSchema(
  fields=[course_id, title, description, desc_embedding],
  description="Courses List",
  enable_dynamic_field=True
)
collection_name = 'courses_list'
wiki_collection = Collection(name=collection_name, schema=wiki_schema, using=connection_id, shards_num=2)
print('Collections: ', utility.list_collections(using=connection_id))

# Setup existing collection into another object
r_collection = Collection(collection_name, using=connection_id)
print('\n', r_collection.schema)

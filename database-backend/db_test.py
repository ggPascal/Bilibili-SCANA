from postersql_backend import *

cur = connect_db(has_con_config=False)
table_exists(con=cur,table_str='test')

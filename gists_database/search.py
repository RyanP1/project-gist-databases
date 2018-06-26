from .models import Gist
from datetime import datetime

'''
Your search_gists method should take a db_connection parameter (the database connection)
as well as two optional arguments

* github_id
* created_at

If no parameter is provided, all the gists in the database should be returned. 
If public_id or created_at parameters are provided, you should filter your SELECT 
query based on them.
'''

def search_gists(db_connection, **kwargs):
    
    search_query = "SELECT * FROM gists"
    
    if not kwargs:
        cursor = db_connection.execute(search_query)
    else:
        args = ['github_id', 'created_at', 'updated_at']    
        equality_ops = {'lte': '<=', 'lt': '<', 'gte': '>=', 'gt': '>'}
        params = {}
        addl_query = " WHERE "
        
        
        # assume passed on: created_at__gte=d
        for key, val in kwargs.items():
            equality_operator = '='
            param = key.split('__')
            
            if len(param) > 1:
                equality_operator = equality_ops[param[1]]
            
            if param[0] in args:
                params[param[0]] = kwargs[key]
                print (kwargs[key])
                
                if type(val) == datetime:
                    addl_query += "datetime({}) {} datetime(:{}) AND ".format(param[0], equality_operator, param[0])
                else:
                    addl_query += "{} {} :{} AND ".format(param[0], equality_operator, param[0]) 
        
        search_query+=addl_query[:-4]
        
        cursor = db_connection.execute(search_query, params)
    
    gists = []
    for row in cursor.fetchall():
        gists.append(Gist(row))
    
    return gists
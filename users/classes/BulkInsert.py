from itertools import repeat
from django.db import models, connections, transaction

class Bulk:
    def _modelFields(self, model):
        return [f for f in model._meta.fields
                if not isinstance(f, models.AutoField)]
    
    
    def _prepValues(self, fields, obj, con):
        return tuple(f.get_db_prep_save(f.pre_save(obj, True), connection=con) for f in fields)
    
   
    def _insertMany(self, model, objects, using="default"):
        if not objects:return
    
        con = connections[using]
    
        fields = self._modelFields(model)
        parameters = [self._prepValues(fields, o, con) for o in objects]
    
        table = model._meta.db_table
        col_names = ",".join(con.ops.quote_name(f.column) for f in fields)
        placeholders = ",".join(repeat("%s", len(fields)))
    
        sql = "INSERT INTO %s (%s) VALUES (%s)" % (table, col_names, placeholders)
        con.cursor().executemany(sql, parameters)
    
    def insertMany(self, *args, **kwargs):
        '''
            Bulk insert list of Django objects. Objects must be of the same
            Django model.
        
            Note that save is not called and signals on the model are not
            raised.
        
            :param model: Django model class.
            :param objects: List of objects of class `model`.
            :param using: Database to use.
    
        '''
        self._insertMany(*args, **kwargs)
        transaction.commit_unless_managed()
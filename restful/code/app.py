from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []

# the Student inherited from Resource
# class Student(Resource):
#     def get(self, name):   # name of the student
#         return {'student':name}

class Item(Resource):
    def get(self, name):
        '''for item in items:
            if item['name'] == name:
                return item'''
        # instead of the iteration above, use refresher
        item = next(list(filter(lambda x: x['name'] == name, items)), None) # next gives us the first item found by this filter function,
        return {'item':item}, 200 if item else 404     # however it can break our program if there are no items left so use None if the next does not find any item
                                                       # so we can use 'item':item instead of 'item':None
    def post(self, name):
        if next(list(filter(lambda x: x['name'] == name, items)), None) is not None: # to be sure that the item is unique
            return {'message' : "An item with name '{}' already exists.".format(name)}, 400
        data = request.get_json()
        item = {'name':name, 'price': data['price']}   # the price data will come from the request body not as default before... 'price':12.00
        items.append(item)
        return item, 201

class ItemList(Resource):
    def get(self):
        return {'items':items}

#api.add_resource(Student, '/student/<string:name>') # Student resource is gonna be accessible via our API with given path
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
app.run(port=5001, debug=True)
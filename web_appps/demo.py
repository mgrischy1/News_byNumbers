from flask import Flask, Markup, render_template
from irs_xls import *
import markdown
import os
from flask import Flask, g
from flask_restful import Resource, Api, reqparse
# kill -9 $(ps -A | grep python | awk '{print $1}')
app = Flask(__name__)
api = Api(app)
r = AwsRds()
lists = r.number_of_return()
labels = lists[0]
values = lists[1]

lists2 = r.tax_generated_at_marginal_rate()
labels2 = lists2[0]
values2 = lists2[1]
print(lists2)

@app.route("/")
@app.route('/bar')
def bar():
    bar_labels = labels
    bar_values = values
    bar_labels2 = labels2
    bar_values2 = values2
    return render_template('nav.html', title='Tax generated At marginal rate', max=max(bar_values),
                           labels2=bar_labels2, values2=bar_values2, labels=bar_labels, values=bar_values)


# @app.route("/index")
# def index():
#     """Present some documentation"""
#
#     # Open the README file
#     with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:
#         # Read the content of the file
#         content = markdown_file.read()
#
#         # Convert to HTML
#         return markdown.markdown(content)


class Tables(Resource):
    def get(self):
        tables = r.show_tables()

        return {'message': 'Success', 'data': tables}, 200

    # def post(self):
    #     parser = reqparse.RequestParser()
    #
    #     parser.add_argument('identifier', required=True)
    #     parser.add_argument('name', required=True)
    #     parser.add_argument('device_type', required=True)
    #     parser.add_argument('controller_gateway', required=True)
    #
    #     # Parse the arguments into an object
    #     args = parser.parse_args()
    #
    #     shelf = get_db()
    #     shelf[args['identifier']] = args
    #
    #     return {'message': 'Device registered', 'data': args}, 201


# class Device(Resource):
#     def get(self, identifier):
#         shelf = get_db()
#
#         # If the key does not exist in the data store, return a 404 error.
#         if not (identifier in shelf):
#             return {'message': 'Device not found', 'data': {}}, 404
#
#         return {'message': 'Device found', 'data': shelf[identifier]}, 200
#
#     def delete(self, identifier):
#         shelf = get_db()
#
#         # If the key does not exist in the data store, return a 404 error.
#         if not (identifier in shelf):
#             return {'message': 'Device not found', 'data': {}}, 404
#
#         del shelf[identifier]
#         return '', 204


api.add_resource(Tables, '/tables')
# api.add_resource(Device, '/device/<string:identifier>')
if __name__ == '__main__':
    app.run(debug=True)

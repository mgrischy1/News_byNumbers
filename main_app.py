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


@app.route("/")
@app.route('/bar')
def bar():
    bar_labels = labels
    bar_values = values
    bar_labels2 = labels2
    bar_values2 = values2
    return render_template('bar_chart.html', title='Tax generated At marginal rate', max=max(bar_values),
                           labels2=bar_labels2, values2=bar_values2, labels=bar_labels, values=bar_values)


@app.route("/API")
def index():
    return render_template('api_doc.html')


class Tables(Resource):
    def get(self):
        tables = r.show_tables()

        return {'message': 'Success', 'data': tables}, 200


class TaxGeneratedAtMarginalRate(Resource):
    def get(self):
        tax_gen_margin_rate = r.tax_generated_at_marginal_rate()
        res = dict(zip(tax_gen_margin_rate[0], tax_gen_margin_rate[1]))

        return {'message': 'Success', 'data': res}, 200


class AwardingAgency(Resource):
    def get(self):
        aa = r.awarding_agency()
        res = dict(zip(aa[0], aa[1]))
        return {'message': 'Success', 'data': res}, 200


api.add_resource(Tables, '/tables')
api.add_resource(TaxGeneratedAtMarginalRate, '/tax_generated_at_marginal_rate')
api.add_resource(AwardingAgency, '/awarding_agency')

# api.add_resource(Device, '/device/<string:identifier>')
if __name__ == '__main__':
    app.run(debug=True)

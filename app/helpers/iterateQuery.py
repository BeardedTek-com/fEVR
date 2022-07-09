from flask import jsonify

def iterateQuery(query):
    output={}
    if query:
        for q in query:
            output[q.id] = {}
            for item in q.__dict__:
                if not item.startswith('_') and item != "id":
                    output[q.id][item] = q.__dict__[item]
    return output
import logging

from flask import Flask, request, jsonify, json
from flask import after_this_request

from controller import Controller

app = Flask(__name__)

#   < --- Supplementary Libraries --- >
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


# from werkzeug.middleware.profiler import ProfilerMiddleware
# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, profile_dir="./profile")
#   < === End of Supplementary Libraries === >

@app.get('/api/change')
def change():
    @after_this_request
    def add_header(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    try:
        node_id = request.args.get('node_id')
        params = []
        for i in request.args:
            if i != "node_id":
                params.append([i, request.args[i]])
        node = mainController.get_node_by_id(node_id)
        if node is None:
            return jsonify({"reason": "Node not found"}), 404
        for key, data in params:
            exec("node." + str(key) + "=" + str(data))
        return jsonify({"status": "ok"}), 200
    except Exception as error:
        logging.info(str(error))
        return jsonify({"reason": "idk"}), 404


@app.post('/api/environment/add')
@app.post('/api/environment/delete')
def add_delete_environment_projectors():
    @after_this_request
    def add_header(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    try:
        node_id = request.args.get('node_id')
        projector_id = request.args.get('projector_id')
        current_node = mainController.get_node_by_id(node_id)
        if str(request.url_rule) == '/api/environment/add':
            current_node.add(projector_id)
            return jsonify({"status": "Projector successfully added to the environment"}), 200
        else:
            current_node.delete(projector_id)
            return jsonify({"status": "Projector successfully deleted from the environment"}), 200
    except Exception as error:
        logging.info("Unexpected error: " + str(error))
        return jsonify({'reason': "Unexpected error"}), 401


@app.post('/api/connect')
@app.post('/api/disconnect')
def connect_nodes():
    @after_this_request
    def add_header(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    try:
        from_node_id = request.args.get('from_node_id')
        to_node_id = request.args.get('to_node_id')
        logging.info("Connecting/Disconnecting: " + str(from_node_id) + " " + str(to_node_id))
        if str(request.url_rule) == '/api/connect':
            mainController.connect_nodes(from_node_id, to_node_id)
            return jsonify({'status': "Nodes connected successfully"}), 200
        else:
            mainController.disconnect_nodes(from_node_id, to_node_id)
            return jsonify({'status': "Nodes disconnected successfully"}), 200
    except Exception as error:
        logging.info("Unexpected error: " + str(error))
        return jsonify({'reason': "Unexpected error"}), 401


@app.get('/api/delete')
def delete_node():
    @after_this_request
    def add_header(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    try:
        node_id = request.args.get('node_id')
        mainController.delete_node(node_id)
        return jsonify({'status': "Node was deleted successfully"}), 200
    except Exception as error:
        logging.info("Unexpected error: " + str(error))
        return jsonify({'reason': "Unexpected error"}), 401


@app.get('/api/create_node')
def create_node():
    @after_this_request
    def add_header(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    try:
        node_type = request.args.get('type')
        new_node = mainController.create_node(node_type)
        return jsonify({'node_id': new_node.node_id}), 200
    except Exception as error:
        logging.info("Unexpected error: " + str(error))
        return jsonify({'reason': "Unexpected error"}), 401


is_on = False


# Flask is bruh btw
@app.get('/api/start')
def start():
    @after_this_request
    def add_header(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    global is_on
    if is_on is False:
        is_on = True
        mainController.start()
    else:
        pass
    return jsonify({"status": "i guess it's launched"}), 418


mainController = Controller()
app.run(host='localhost', port=8989, threaded=True)

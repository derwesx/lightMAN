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

@app.get('/api/ping')
def ping():
    @after_this_request
    def add_header(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    print(mainController.updates_counter)
    print(mainController.current_scene_id)
    print(mainController.get_node_by_id(mainController.current_scene_id).get_data())


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
            return jsonify({"status": "Projector successfully added to the environment"})
        else:
            current_node.delete(projector_id)
            return jsonify({"status": "Projector successfully deleted from the environment"})
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


@app.post('/api/delete')
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


@app.post('/api/create_plugin')
@app.get('/api/create_environment')
@app.get('/api/create_scene')
@app.get('/api/create_translator')
def create_node():
    @after_this_request
    def add_header(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    try:
        if str(request.url_rule) == '/api/create_plugin':
            plugin_type = request.args.get('type')
            new_plugin = mainController.create_plugin(plugin_type)
            return jsonify({'node_id': new_plugin.node_id}), 200
        elif str(request.url_rule) == '/api/create_environment':
            new_environment = mainController.create_environment()
            return jsonify({'node_id': new_environment.node_id})
        elif str(request.url_rule) == '/api/create_scene':
            new_scene = mainController.create_scene()
            return jsonify({'node_id': new_scene.node_id})
        elif str(request.url_rule) == '/api/create_translator':
            new_translator = mainController.create_translator()
            return jsonify({'node_id': new_translator.node_id})
        else:
            return jsonify({'reason': "Unknown node type"}), 404
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

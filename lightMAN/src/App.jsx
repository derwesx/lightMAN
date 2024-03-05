import {useState, useCallback, useRef} from 'react';
import ReactFlow, {
    MiniMap,
    Controls,
    Background,
    ReactFlowProvider,
    getOutgoers,
    useReactFlow,
    useNodesState,
    useEdgesState,
    updateEdge,
    addEdge,
} from 'reactflow';

import 'reactflow/dist/style.css';

import {nodes as initialNodes, edges as initialEdges} from './nodes-edges';
//<------------------NODES-------------------------->
import {default_node} from "./nodes/default_node.js";
import {blink} from "./nodes/blink.js";
import {scene} from "./nodes/scene.js";
import {set_color} from "./nodes/set_color.jsx";
import {ColorNode} from "./nodes/set_color.jsx"
import {translator} from "./nodes/translator.js";
import {environment} from "./nodes/environment.js";

const nodeTypes = {
    ColorNode: ColorNode,
};

//<------------------------------------------------->

function App() {
    const edgeUpdateSuccessful = useRef(true);
    const connectingNodeId = useRef(null);
    const {screenToFlowPosition} = useReactFlow();
    const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
    const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
    const {getNodes, getEdges} = useReactFlow();

    const isValidConnection = useCallback(
        (connection) => {
            // we are using getNodes and getEdges helpers here
            // to make sure we create isValidConnection function only once
            const nodes = getNodes();
            const edges = getEdges();
            const target = nodes.find((node) => node.id === connection.target);
            const hasCycle = (node, visited = new Set()) => {
                if (visited.has(node.id)) return false;

                visited.add(node.id);

                for (const outgoer of getOutgoers(node, nodes, edges)) {
                    if (outgoer.id === connection.source) return true;
                    if (hasCycle(outgoer, visited)) return true;
                }
            };

            if (target.id === connection.source) return false;
            return !hasCycle(target);
        },
        [getNodes, getEdges],
    );

    const connectNodes = (source_id, target_id) => {
        const request = new XMLHttpRequest();
        const req = "?" + "from_node_id=" + source_id + "&to_node_id=" + target_id;
        request.open("POST", "http://localhost:8989/api/connect" + req, false);
        request.send(null);
    };

    const disconnectNodes = (source_id, target_id) => {
        const request = new XMLHttpRequest();
        const req = "?" + "from_node_id=" + source_id + "&to_node_id=" + target_id;
        request.open("POST", "http://localhost:8989/api/disconnect" + req, false);
        request.send(null);
    };
    const onConnect = useCallback((params) => {
        console.log("Adding: ", params.source, params.target);
        connectNodes(params.source, params.target);
        connectingNodeId.current = null;
        setEdges((els) => addEdge(params, els))
    }, []);

    const onEdgeUpdateStart = useCallback(() => {
        edgeUpdateSuccessful.current = false;
    }, []);

    const onEdgeUpdate = useCallback((oldEdge, newConnection) => {
        edgeUpdateSuccessful.current = true;
        if (!(oldEdge.source === newConnection.source && oldEdge.target === newConnection.target)) {
            console.log("Removing: ", oldEdge.source, oldEdge.target)
            console.log("Adding: ", newConnection.source, newConnection.target)
            disconnectNodes(oldEdge.source, oldEdge.target);
            connectNodes(newConnection.source, newConnection.target);
        }
        setEdges((els) => updateEdge(oldEdge, newConnection, els));
    }, []);

    const onEdgeUpdateEnd = useCallback((_, edge) => {
        if (!edgeUpdateSuccessful.current) {
            console.log("Removing: ", edge.source, edge.target);
            disconnectNodes(edge.source, edge.target);
            setEdges((eds) => eds.filter((e) => e.id !== edge.id));
        }

        edgeUpdateSuccessful.current = true;
    }, []);

    const createNewNode = (event) => {

        const node_name = event.target.getAttribute('value');
        const request = new XMLHttpRequest();
        request.open("GET", `http://localhost:8989/api/create_node?type=${node_name}`, false);
        request.send(null);
        const node_id = JSON.parse(request.responseText)["node_id"];
        let newNode;
        try {
            newNode = eval(`${node_name}(node_id, screenToFlowPosition)`);
            // FIX ASAP
        } catch (e) {
            newNode = default_node(node_id, screenToFlowPosition, node_name)
        }
        setNodes((nds) => nds.concat(newNode));
    };
    const start = () => {
        const request = new XMLHttpRequest();
        request.open("GET", "http://localhost:8989/api/start", true);
        request.send(null);
    };

    return (
        <div style={{width: '100vw', height: '100vh'}}>
            {/*-------------------Nodes-----------------------*/}
            <button onClick={createNewNode} value="environment">Environment</button>
            <button onClick={createNewNode} value="scene">Scene</button>
            <button onClick={createNewNode} value="translator">Translator</button>
            <button onClick={createNewNode} value="turn_on">TurnOn</button>
            <button onClick={createNewNode} value="blink">Blink</button>
            <button onClick={createNewNode} value="set_color">SetColor</button>
            {/*-----------------------------------------------*/}
            <button onClick={start}>START</button>
            <ReactFlow
                nodes={nodes}
                edges={edges}
                onNodesChange={onNodesChange}
                onEdgesChange={onEdgesChange}
                onEdgeUpdate={onEdgeUpdate}
                onEdgeUpdateStart={onEdgeUpdateStart}
                onEdgeUpdateEnd={onEdgeUpdateEnd}
                onConnect={onConnect}
                isValidConnection={isValidConnection}
                nodeTypes={nodeTypes}
                fitView
                attributionPosition="top-right"
            >
                <Controls/>
                <MiniMap/>
                <Background variant="dots" gap={12} size={1}/>
            </ReactFlow>
        </div>
    );
}


export default () => (
    <ReactFlowProvider>
        <App/>
    </ReactFlowProvider>
);
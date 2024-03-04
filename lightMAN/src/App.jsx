import React, {useCallback, useRef} from 'react';
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
import {blink_node} from "./nodes/blink.js";

function App() {
    const reactFlowWrapper = useRef(null);
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
        var data = {
            "from_node_id": source_id,
            "to_node_id": target_id
        }
        request.send(null);
    };

    const disconnectNodes = (source_id, target_id) => {
        const request = new XMLHttpRequest();
        const req = "?" + "from_node_id=" + source_id + "&to_node_id=" + target_id;
        request.open("POST", "http://localhost:8989/api/disconnect" + req, false);
        var data = {
            "from_node_id": source_id,
            "to_node_id": target_id
        }
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
        console.log("Removing: ", oldEdge.source, oldEdge.target)
        console.log("Adding: ", newConnection.source, newConnection.target)
        if (!(oldEdge.source === newConnection.source && oldEdge.target === newConnection.target)) {
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

    // I HAVE NO IDEA HOW TO MAKE IT BEAUTY
    const createNewEnvironment = () => {
        const request = new XMLHttpRequest();
        request.open("GET", "http://localhost:8989/api/create_environment", false);
        request.send(null);
        const node_id = JSON.parse(request.responseText)["node_id"];
        const newNode = {
            id: node_id,
            type: "input",
            position: screenToFlowPosition({
                x: 100,
                y: 100,
            }),
            data: {label: `Environment ${node_id}`},
            origin: [0.5, 0.0],
            style: {
                background: '#FFFFFF',
                color: '#333',
                border: '1px solid #222138',
                width: 180,
            },
        };
        setNodes((nds) => nds.concat(newNode));
    };
    const createNewTranslator = () => {
        const request = new XMLHttpRequest();
        request.open("GET", "http://localhost:8989/api/create_translator", false);
        request.send(null);
        const node_id = JSON.parse(request.responseText)["node_id"];
        const newNode = {
            id: node_id,
            position: screenToFlowPosition({
                x: 100,
                y: 100,
            }),
            data: {label: `Translator ${node_id}`},
            origin: [0.5, 0.0],
            style: {
                background: '#2FFFFF',
                color: '#333',
                border: '1px solid #222138',
                width: 180,
            },
        };
        setNodes((nds) => nds.concat(newNode));
    };
    const createNewScene = () => {
        const request = new XMLHttpRequest();
        request.open("GET", "http://localhost:8989/api/create_scene", false);
        request.send(null);
        const node_id = JSON.parse(request.responseText)["node_id"];
        const newNode = {
            id: node_id,
            type: "output",
            position: screenToFlowPosition({
                x: 100,
                y: 100,
            }),
            data: {label: `Scene ${node_id}`},
            origin: [0.5, 0.0],
            style: {
                background: '#AAAAAA',
                color: '#333',
                border: '1px solid #222138',
                width: 180,
            },
        };
        setNodes((nds) => nds.concat(newNode));
    };
    const createNewPluginTO = () => {
        const request = new XMLHttpRequest();
        request.open("POST", "http://localhost:8989/api/create_plugin?type=turn_on", false);
        request.send(null);
        const node_id = JSON.parse(request.responseText)["node_id"];
        const newNode = {
            id: node_id,
            position: screenToFlowPosition({
                x: 100,
                y: 100,
            }),
            data: {label: `TurnOn ${node_id}`},
            origin: [0.5, 0.0],
            style: {
                background: '#F0F0F0',
                color: '#333',
                border: '1px solid #222138',
                width: 180,
            },
        };
        setNodes((nds) => nds.concat(newNode));
    };

    const createNewPluginB = () => {

        const request = new XMLHttpRequest();
        request.open("POST", "http://localhost:8989/api/create_plugin?type=blink", false);
        request.send(null);
        const node_id = JSON.parse(request.responseText)["node_id"];
        let name = "blink_node";
        const newNode = eval(`${name}(node_id, screenToFlowPosition)`);
        setNodes((nds) => nds.concat(newNode));
    };
    const createNewPluginSC = () => {
        const request = new XMLHttpRequest();
        request.open("POST", "http://localhost:8989/api/create_plugin?type=set_color", false);
        request.send(null);
        const node_id = JSON.parse(request.responseText)["node_id"];
        const newNode = {
            id: node_id,
            position: screenToFlowPosition({
                x: 100,
                y: 100,
            }),
            data: {label: `SetColor ${node_id}`},
            origin: [0.5, 0.0],
            style: {
                background: '#FAD0F0',
                color: '#333',
                border: '1px solid #222138',
                width: 180,
            },
        };
        setNodes((nds) => nds.concat(newNode));
    };
    const start = () => {
        const request = new XMLHttpRequest();
        request.open("GET", "http://localhost:8989/api/start", true);
        request.send(null);
    };
    //////////////////////////////////////////////////////

    return (
        <div style={{width: '100vw', height: '100vh'}}>
            <button onClick={createNewEnvironment}>Environment</button>
            <button onClick={createNewScene}>Scene</button>
            <button onClick={createNewTranslator}>Translator</button>
            <button onClick={createNewPluginTO}>TurnOn</button>
            <button onClick={createNewPluginB}>Blink</button>
            <button onClick={createNewPluginSC}>SetColor</button>
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
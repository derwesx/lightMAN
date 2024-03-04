export const environment = (node_id, screenToFlowPosition) => {
    return {
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
};
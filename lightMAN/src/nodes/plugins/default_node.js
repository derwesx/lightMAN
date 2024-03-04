export const default_node = (node_id, screenToFlowPosition, node_type) => {
    return {
        id: node_id,
        position: screenToFlowPosition({
            x: 100,
            y: 100,
        }),
        data: {label: `${node_type}`},
        origin: [0.5, 0.0],
        style: {
            background: '#FFFFFF',
            color: '#333',
            border: '1px solid #222138',
            width: 180,
        },
    };
};

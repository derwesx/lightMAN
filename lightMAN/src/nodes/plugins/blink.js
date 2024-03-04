export const blink = (node_id, screenToFlowPosition) => {
    return {
        id: node_id,
        position: screenToFlowPosition({
            x: 100,
            y: 100,
        }),
        data: {label: `Blink`},
        origin: [0.5, 0.0],
        style: {
            background: '#ff0000',
            color: '#333',
            border: '1px solid #222138',
            width: 180,
        },
    };
};

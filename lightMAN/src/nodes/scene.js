export const scene = (node_id, screenToFlowPosition) => {
    return {
        id: node_id,
        type: "output",
        position: screenToFlowPosition({
            x: 100,
            y: 100,
        }),
        data: {label: `Scene`},
        origin: [0.5, 0.0],
        style: {
            background: '#AAAAAA',
            color: '#333',
            border: '1px solid #222138',
            width: 180,
        },
    };
};
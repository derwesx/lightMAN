export const translator = (node_id, screenToFlowPosition) => {
    return {
        id: node_id,
        position: screenToFlowPosition({
            x: 100,
            y: 100,
        }),
        data: {label: `Translator`},
        origin: [0.5, 0.0],
        style: {
            background: '#2FFFFF',
            color: '#333',
            border: '1px solid #222138',
            width: 180,
        },
    };
};
import {Handle, Position, useNodesState} from 'reactflow';
import {nodes as initialNodes} from "../nodes-edges.js";

export const ColorNode = ({data, isConnectable}) => {
    return (
        <>
            <Handle
                type="target"
                position={Position.Top}
                isConnectable={isConnectable}
            />
            <div>
                Color Picker Node
            </div>
            <input className="nodrag" type="color" id={data.node_id} onChange={data.on_change}
                   defaultValue={data.color}/>
            <Handle
                type="source"
                position={Position.Bottom}
                isConnectable={isConnectable}
            />
        </>
    );
};

function hexToRgb(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}

const onChangeColor = (event) => {
    var rgb = hexToRgb(event.target.value);
    const request = new XMLHttpRequest();
    request.open("GET", `http://localhost:8989/api/change?R=${rgb.r}&G=${rgb.g}&B=${rgb.b}&node_id=${event.target.id}`, false);
    request.send(null);
};

export const set_color = (node_id, screenToFlowPosition) => {
    return {
        id: node_id,
        type: "ColorNode",
        position: screenToFlowPosition({
            x: 100,
            y: 100,
        }),
        data: {label: `set_color`, on_change: onChangeColor, color: '#000000', node_id: node_id},
        origin: [0.5, 0.0],
        style: {
            background: '#FFFFFF',
            color: '#333',
            border: '1px solid #222138',
            width: 180,
        },
    };
};

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class set_color : default_node
{
    public GameObject node_body;
    public Slider R;
    public Slider G;
    public Slider B;

    public void on_change()
    {
        int r = (int)(R.value * 255);
        int g = (int)(G.value * 255);
        int b = (int)(B.value * 255);
        node_body.GetComponent<Renderer>().material.color = new Color(R.value, G.value, B.value);
        data["R"] = r.ToString();
        data["G"] = g.ToString();
        data["B"] = b.ToString();
        api_handler.change(node_id, data);
    }
}

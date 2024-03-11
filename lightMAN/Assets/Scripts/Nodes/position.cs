using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class position : default_node
{
    public Slider Pan;
    public Slider Tilt;

    public void on_change()
    {
        int pan = (int)(Pan.value * 255);
        int tilt = (int)(Tilt.value * 255);
        data["pan"] = pan.ToString();
        data["tilt"] = tilt.ToString();
        api_handler.change(node_id, data);
    }
}
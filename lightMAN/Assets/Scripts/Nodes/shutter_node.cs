using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class shutter_node : default_node
{
    public GameObject node_body;
    public Slider slider_shutter;
    public Slider slider_rgb;
    public int shutter = 0, rgb = 0;
    public TextMeshProUGUI shutter_text;
    public TextMeshProUGUI rgb_text;

    public void on_change()
    {
        shutter = (int)(slider_shutter.value);
        rgb = (int)(slider_rgb.value);
        data["shutter"] = shutter.ToString();
        data["color"] = rgb.ToString();
        shutter_text.text = shutter.ToString() + " Shutter";
        rgb_text.text = rgb.ToString() + " RGB";
        api_handler.change(node_id, data);
    }
}
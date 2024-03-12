using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class ramp_up : default_node
{
    public GameObject node_body;
    public Slider slider;
    public TextMeshProUGUI time_text;
    public float timeS = 3;
    private float lastClickTime = -1;
    
    public void on_change() 
    {
        timeS = slider.value;
        data["time_per_cycle"] = timeS.ToString();
        time_text.text = timeS.ToString("#.##") + " Seconds";
        api_handler.change(node_id, data);
    }

    public void rhythm()
    {
        if (lastClickTime == -1)
        {
            lastClickTime = Time.time;
        }
        else
        {
            float new_time = Time.time - lastClickTime;
            lastClickTime = Time.time;
            new_time = Mathf.Min(new_time, (float)5.0);
            slider.value = new_time;
            timeS = new_time;
            on_change();
        }
    }
}
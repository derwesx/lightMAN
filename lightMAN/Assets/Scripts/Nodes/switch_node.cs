using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class switch_node : default_node
{
    public GameObject node_body;
    public Slider slider;
    public float timeS = 3;
    private float lastClickTime = -1;
    public TextMeshProUGUI time_text;

    public void on_change() 
    {
        timeS = slider.value;
        time_text.text = timeS.ToString("#.##") + " Seconds";
        data["time_per_switch"] = timeS.ToString();
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
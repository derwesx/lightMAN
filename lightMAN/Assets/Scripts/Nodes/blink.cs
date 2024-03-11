using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class blink : default_node
{
    public GameObject node_body;
    public Slider timecycle;
    public Slider brightness;
    public Slider groupsCounter;
    public TextMeshProUGUI time_text;
    public TextMeshProUGUI groups_text;
    public Toggle turn_one;
    public int groupsCount = 1;
    private float lastClickTime = -1;

    public void on_change() 
    {
        float timeS = timecycle.value;
        groupsCount = (int)groupsCounter.value;
        float coef = brightness.value;
        node_body.GetComponent<Renderer>().material.color = new Color(coef, coef, 0);
        data["brightness"] = ((int)(coef * coef * 255)).ToString();
        data["count_of_groups"] = groupsCount.ToString();
        ColorBlock cb = turn_one.colors;
        if (turn_one.isOn)
        {
            cb.normalColor = Color.yellow;
            cb.highlightedColor = Color.yellow;
            cb.selectedColor = Color.yellow;
            data["turn_one"] = "1";
        }
        else
        {
            cb.normalColor = Color.white;
            cb.highlightedColor = Color.white;
            cb.selectedColor = Color.white;
            data["turn_one"] = "0";
        }
        turn_one.colors = cb;
        data["time_per_cycle"] = timeS.ToString();
        time_text.text = timeS.ToString("#.##") + " Seconds";
        groups_text.text = groupsCount.ToString() + " Groups";
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
            timecycle.value = new_time;
            on_change();
        }
    }
}
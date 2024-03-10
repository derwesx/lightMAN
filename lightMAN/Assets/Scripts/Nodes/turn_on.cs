using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class turn_on : default_node
{
	public GameObject node_body;
	public Slider slider;
    public int brightness = 0;

	public void on_change() 
	{
		float coef = slider.value;
		brightness = (int)(coef * coef * 255);
		node_body.GetComponent<Renderer>().material.color = new Color(coef, coef, 0);
		data["brightness"] = brightness.ToString();
		api_handler.change(node_id, data);
	}
}

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class turn_on : MonoBehaviour
{
	public ApiHandler api_handler;
	public Slider slider;

    public int brightness = 0;
    public string node_id = "";
	private Dictionary<string, string> data = new Dictionary<string, string>();

	private void Start() 
	{
		api_handler = GameObject.Find("Api Handler").GetComponent<ApiHandler>();
		node_id = GetComponent<NodeController>().node_id;
	}

	public void on_change() 
	{
		float coef = slider.value;
		Debug.Log(coef);
		brightness = (int)(coef * coef * 255);
		data["brightness"] = brightness.ToString();
		api_handler.change(node_id, data);
	}
}

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Events;
using UnityEngine.EventSystems;

public class set_color : default_node
{
    public GameObject node_body;
    public Slider R;
    public Slider G;
    public Slider B;
	
    [SerializeField] Texture2D colorChart;
    [SerializeField] GameObject chart;
    [SerializeField] GameObject chosenPoint;

    public void PickColor()
    {
        Vector3 local_position = Camera.main.ScreenToWorldPoint(Input.mousePosition) - chart.transform.position;
		local_position.x += chart.transform.GetComponent<RectTransform>().rect.width / 2;
		local_position.y += chart.transform.GetComponent<RectTransform>().rect.height / 2;
    	Color pickedColor = colorChart.GetPixel((int)(local_position.x * (colorChart.width / chart.transform.GetComponent<RectTransform>().rect.width)), (int)(local_position.y * (colorChart.height / chart.transform.GetComponent<RectTransform>().rect.height)));
	    Vector3 new_point_position = Camera.main.ScreenToWorldPoint(Input.mousePosition);
	    new_point_position.z = -0.15f;
	    chosenPoint.transform.position = new_point_position;
	    node_body.GetComponent<Renderer>().material.SetColor("_EmissionColor", pickedColor);
        data["R"] = ((int)(pickedColor.r * 255)).ToString();
        data["G"] = ((int)(pickedColor.g * 255)).ToString();
        data["B"] = ((int)(pickedColor.b * 255)).ToString();
        api_handler.change(node_id, data);
    }
}

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class environment : MonoBehaviour
{
    public ApiHandler api_handler;
    public string node_id = "";

    public void Start()
    {
        api_handler = GameObject.Find("Api Handler").GetComponent<ApiHandler>();
        node_id = GetComponent<NodeController>().node_id;
    }
    public void change_projector(Toggle toggle)
    {
        int projector_id = int.Parse(toggle.name);
        if (toggle.isOn)
        {
            api_handler.add_projector(node_id, projector_id);
        }
        else
        {
            api_handler.delete_projector(node_id, projector_id);
        }
    }
}

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class default_node : MonoBehaviour
{
    public ApiHandler api_handler;
    public string node_id = "";
    public Dictionary<string, string> data = new Dictionary<string, string>();
    
    private void Start() 
    {
        api_handler = GameObject.Find("Api Handler").GetComponent<ApiHandler>();
        node_id = GetComponent<NodeController>().node_id;
    }
}

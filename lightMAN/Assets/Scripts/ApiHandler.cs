using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;
using UnityEngine.Networking;

public class ApiHandler : MonoBehaviour
{
    public void add_projector(string env_id, int projector_id)
    {
        WWWForm form = new WWWForm();
        UnityWebRequest uwr = UnityWebRequest.Post("localhost:8989/api/environment/add?node_id=" + env_id + "&projector_id=" + projector_id.ToString(), form);
        uwr.SendWebRequest();
    }
    public void delete_projector(string env_id, int projector_id)
    {
        WWWForm form = new WWWForm();
        UnityWebRequest uwr = UnityWebRequest.Post("localhost:8989/api/environment/delete?node_id=" + env_id + "&projector_id=" + projector_id.ToString(), form);
        uwr.SendWebRequest();
    }
    public void change(string node_id, Dictionary<string, string> data)
    {
        string send_data = "";
        foreach(var data_key in data)
        {
            send_data += "&" + data_key.Key + "=" + data_key.Value;
        }
        UnityWebRequest uwr = UnityWebRequest.Get("localhost:8989/api/change?node_id=" + node_id + send_data);
        uwr.SendWebRequest();
    }
    public void connect(string node_start_id, string node_end_id)
    {
        Debug.Log("Connecting: " + node_start_id + " - " + node_end_id);
        WWWForm form = new WWWForm();
        UnityWebRequest uwr = UnityWebRequest.Post("localhost:8989/api/connect?from_node_id=" + node_start_id + "&to_node_id=" + node_end_id, form);
        uwr.SendWebRequest();
    }
    
    public void create_node(string node_type)
    {
        Debug.Log("Creating new node with type " + node_type);
        UnityWebRequest uwr = UnityWebRequest.Get("localhost:8989/api/create_node?type=" + node_type);
        uwr.SendWebRequest();
        while (uwr.result != UnityWebRequest.Result.Success && uwr.result == UnityWebRequest.Result.InProgress)
        {
            continue;
        }
        string response = uwr.downloadHandler.text;
        response = response.Trim('[', ']');
        response = response.Replace("\"", "");
        response = response.Replace("{", "");
        response = response.Replace("}", "");
        response = response.Replace("\n", "");
        string[] keys = response.Split(',');
        string node_id = keys[0].Split(':')[1];
        // Creating an object
        GameObject new_node = (GameObject)Instantiate(Resources.Load("Prefabs/Nodes/" + node_type));
        new_node.GetComponent<NodeController>().node_id = node_id;
        Debug.Log("Created node with id: " + node_id);
    }

    public void start()
    {
        UnityWebRequest uwr = UnityWebRequest.Get("localhost:8989/api/start");
        uwr.SendWebRequest();
    }
}

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ConnectionHandler : MonoBehaviour
{
    public ApiHandler api_handler;
    
    private Dictionary<string, HashSet<string>> connections = new Dictionary<string, HashSet<string>>();
    private string node_start_id = "", node_end_id = "";
    
    private GameObject getChildGameObject(GameObject fromGameObject, string withName) {
        Transform[] ts = fromGameObject.transform.GetComponentsInChildren<Transform>();
        foreach (Transform t in ts) if (t.gameObject.name == withName) return t.gameObject;
        return null;
    }
    
    public List<LineRenderer> lines = new List<LineRenderer>();
    
	private GameObject get_node_by_id(string node_id)
	{
		GameObject[] allObjects = UnityEngine.Object.FindObjectsOfType<GameObject>();
		foreach(var node in allObjects) {
			try {
   				if (node.GetComponent<NodeController>().node_id == node_id) {
					return node;
				}
			} catch {}
		}
		return null;
	}
    private void DrawConnections()
    {
        int counter = 0;
        foreach (var node_connections in connections)
        {
            string node_from_id = node_connections.Key;
            HashSet<string> nodes_to_id = node_connections.Value;
            foreach(string node_to_id in nodes_to_id)
            {
                var node_from_obj = get_node_by_id(node_from_id);
                var node_to_obj = get_node_by_id(node_to_id);
				if (node_from_obj == null || node_to_obj == null) 
				{
					return;
				}
                var from_connection_out = getChildGameObject(node_from_obj, "connect_out");
                var to_connection_in = getChildGameObject(node_to_obj, "connect_in");
                if (lines.Count <= counter)
                {
                    var line = new GameObject().AddComponent<LineRenderer>();
                    line.SetWidth(0.04F, 0.04F);
                    Color c1 = Color.white;
                    Color c2 = new Color(0, 0, 0, 0);
                    line.material = new Material(Shader.Find("Sprites/Default"));
                    line.SetColors(c1, c2);
                    line.SetVertexCount(2);
                    lines.Add(line);
                }
                Vector2 from_v3_pos = new Vector3(from_connection_out.transform.position.x, from_connection_out.transform.position.y, -3);
                Vector2 to_v3_pos = new Vector3(to_connection_in.transform.position.x, to_connection_in.transform.position.y, -3);
                lines[counter].SetPosition(0, from_v3_pos);
                lines[counter].SetPosition(1, to_v3_pos);
                counter += 1;
            }
        }
		while (lines.Count > counter)
		{ 
			Destroy(lines[lines.Count - 1]);
			lines.RemoveAt(lines.Count - 1);
		}
    }
    void Update()
    {
        if (Input.GetMouseButtonUp(0))
        {
            Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
            RaycastHit2D hit = Physics2D.GetRayIntersection(ray, Mathf.Infinity);
			if((hit == null || hit.collider == null) && node_start_id != "")
			{
				string node_to_remove_from = node_start_id;

   	       		foreach(string node_to_id in connections[node_to_remove_from])
       	   		{
					api_handler.disconnect(node_to_remove_from, node_to_id);
				}
				HashSet<string> empty_hash_set = new HashSet<string>();
				connections[node_to_remove_from] = empty_hash_set;
                node_start_id = "";
                node_end_id = "";
				return;
			} else if (hit == null || hit.collider == null)
            {
                node_start_id = "";
                node_end_id = "";
                return;
            }
            else
            {
                if (hit.collider.name == "connect_out")
                {
                    string other_node_id = hit.collider.gameObject.transform.parent.gameObject.GetComponent<NodeController>().node_id;
                    node_start_id = other_node_id;
					Debug.Log("Got first point: " + node_start_id);
                } else if (hit.collider.name == "connect_in")
                {
                    string other_node_id = hit.collider.gameObject.transform.parent.gameObject.GetComponent<NodeController>().node_id;
                    node_end_id = other_node_id;
					Debug.Log("Got second point: " + node_end_id);
                }
                if (node_start_id != node_end_id && node_start_id != "" && node_end_id != "")
				{
                    if (connections.ContainsKey(node_start_id))
                    {
                        connections[node_start_id].Add(node_end_id);
                    }
                    else
                    {
                        HashSet<string> new_hash_set = new HashSet<string>();
                        new_hash_set.Add(node_end_id);
                        connections.Add(node_start_id, new_hash_set);
                    }
					Debug.Log("Connecting: " + node_start_id + " - " + node_end_id);
                    api_handler.connect(node_start_id, node_end_id);
                }
                node_start_id = "";
                node_end_id = "";
            }
        }
        if (Input.GetMouseButtonDown(0))
        {
            Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
            RaycastHit2D hit = Physics2D.GetRayIntersection(ray, Mathf.Infinity);
           
            if(hit.collider != null)
            {
                if (hit.collider.name == "connect_out")
                {
                    string other_node_id = hit.collider.gameObject.transform.parent.gameObject.GetComponent<NodeController>().node_id;
                    node_start_id = other_node_id;
					Debug.Log("Got first point: " + node_start_id);
                } else if (hit.collider.name == "connect_in")
                {
                    string other_node_id = hit.collider.gameObject.transform.parent.gameObject.GetComponent<NodeController>().node_id;
                    node_end_id = other_node_id;
					Debug.Log("Got second point: " + node_end_id);
                }
            }
        }

        DrawConnections();
    }
}

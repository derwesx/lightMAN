using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NodeController : MonoBehaviour
{
    public string node_id = "";
    private static bool is_moving = false;
    private string moving_object_id = "";
	private Vector3 correction, source;

    public ApiHandler api_handler;
    public ConnectionHandler connection_handler;
	
	void Start()
	{
        api_handler = GameObject.Find("Api Handler").GetComponent<ApiHandler>();
        connection_handler = GameObject.Find("Connection Handler").GetComponent<ConnectionHandler>();
	}

    void Update()
    {
		if (Input.GetMouseButtonUp(0))
        {
            is_moving = false;
            moving_object_id = "";
        }

        if (Input.GetMouseButtonDown(0) || is_moving)
        {
            if (is_moving && moving_object_id == node_id)
            {
                Vector3 target = Camera.main.ScreenToWorldPoint(Input.mousePosition);
                target.z = 0;
				correction.z = 0;
                transform.position = target - correction + source;
                return;
            } else if (is_moving && moving_object_id != node_id)
            {
                return;
            }

            Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
            RaycastHit2D hit = Physics2D.GetRayIntersection(ray, Mathf.Infinity);
            if(hit.collider != null && hit.collider.name == "header")
            {
				string other_node_id = hit.collider.gameObject.transform.parent.gameObject.transform.parent.gameObject.GetComponent<NodeController>().node_id;
                if (other_node_id == node_id)
                {
                    is_moving = true;
                    moving_object_id = node_id;
					source = transform.position;
                    correction = Camera.main.ScreenToWorldPoint(Input.mousePosition);
                }
            }
        }
    }
	public void delete_node(GameObject node)
    {
        connection_handler.delete_connections_from_node(node_id, true);
        connection_handler.delete_connections_from_node(node_id, false);
		api_handler.delete_node(node_id);
		Destroy(node);
	}	
}

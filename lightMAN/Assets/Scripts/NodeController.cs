using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NodeController : MonoBehaviour
{
    public string node_id = "";
    private static bool is_moving = false;
    private string moving_object_id = "";
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
                target.z = transform.position.z;
                transform.position = target;
                return;
            } else if (is_moving && moving_object_id != node_id)
            {
                return;
            }

            Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
            RaycastHit2D hit = Physics2D.GetRayIntersection(ray, Mathf.Infinity);
           
            if(hit.collider != null)
            {
                string other_node_id = hit.collider.gameObject.transform.parent.gameObject.transform.parent.gameObject.GetComponent<NodeController>().node_id;
                if (hit.collider.name == "header" && other_node_id == node_id)
                {
                    is_moving = true;
                    moving_object_id = node_id;
                    Vector3 target = Camera.main.ScreenToWorldPoint(Input.mousePosition);
                    target.z = transform.position.z;
                    transform.position = target;
                }
            }
        }
    }
}

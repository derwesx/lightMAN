using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ZoomHandler : MonoBehaviour
{
    public int click_to_move = 0, move_coef = 110;
    public float minimum_camera_size = 3, maximum_camera_size = 30;
    private float previous_x = 0, previous_y = 0;
    private bool is_moving = false;
    void Update()
    {
        if (Input.GetMouseButtonUp(click_to_move))
        {
            is_moving = false;
        }

        if (is_moving)
        {
            float current_x = Input.mousePosition.x;
            float current_y = Input.mousePosition.y;
            float d_x = (current_x - previous_x) / move_coef;
            float d_y = (current_y - previous_y) / move_coef;
            previous_x = current_x;
            previous_y = current_y;
            transform.position += new Vector3(-d_x, -d_y, 0);
        }
        Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
        RaycastHit2D hit = Physics2D.GetRayIntersection(ray,Mathf.Infinity);
        
        if(hit.collider != null)
        {
            return;
        }
        
        if (Input.GetMouseButtonDown(click_to_move))
        {
            previous_x = Input.mousePosition.x;
            previous_y = Input.mousePosition.y;
            is_moving = true;
        }
        
        float scrollDelta = Input.mouseScrollDelta.y;
        if (scrollDelta != 0)
        {
            Camera main_camera = GetComponent<Camera>();
            float new_orthographic_size = main_camera.orthographicSize + scrollDelta;
            if (new_orthographic_size < minimum_camera_size)
            {
                new_orthographic_size = minimum_camera_size;
            }

            if (new_orthographic_size > maximum_camera_size)
            {
                new_orthographic_size = maximum_camera_size;
            }
            main_camera.orthographicSize = new_orthographic_size;
            
        }
    }
}

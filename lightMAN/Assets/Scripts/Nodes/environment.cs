using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class environment : default_node
{
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

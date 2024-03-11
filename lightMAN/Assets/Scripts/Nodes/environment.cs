using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class environment : default_node
{
    public void change_projector(Toggle toggle)
    {
        int projector_id = int.Parse(toggle.name);
        ColorBlock cb = toggle.colors;
        if (toggle.isOn)
        {
            cb.normalColor = Color.yellow;
			cb.highlightedColor = Color.yellow;
			cb.selectedColor = Color.yellow;
            api_handler.add_projector(node_id, projector_id);
        }
        else
        {
            cb.normalColor = Color.white;
			cb.highlightedColor = Color.white;
			cb.selectedColor = Color.white;
            api_handler.delete_projector(node_id, projector_id);
        }
        toggle.colors = cb;
    }
}

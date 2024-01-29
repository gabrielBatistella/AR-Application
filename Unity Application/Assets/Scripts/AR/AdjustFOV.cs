using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(Camera))]
public class AdjustFOV : MonoBehaviour
{
    [SerializeField] private float rateOfAdjusting = 1f;

    private Camera sceneView;

    private void Awake()
    {
        sceneView = GetComponent<Camera>();
    }

    public void IncreaseFOV()
    {
        sceneView.fieldOfView += rateOfAdjusting;
    }

    public void DecreaseFOV()
    {
        sceneView.fieldOfView -= rateOfAdjusting;
    }
}

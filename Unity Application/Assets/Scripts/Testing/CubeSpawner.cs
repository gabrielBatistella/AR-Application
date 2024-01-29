using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CubeSpawner : MonoBehaviour
{
    [SerializeField] private GameObject cube;

    private bool flag = false;

    private void Update()
    {
        if (Input.touchCount == 1)
        {
            if (!flag)
            {
                GameObject instantiatedCube = Instantiate(cube, new Vector3(Random.Range(-10f, 10f), Random.Range(-10f, 10f), Random.Range(-10f, 10f)), Quaternion.identity, transform);
                instantiatedCube.GetComponent<Renderer>().material.color = new Color(Random.Range(0f, 1f), Random.Range(0f, 1f), Random.Range(0f, 1f));
                flag = true;
            }
        }
        else
        {
            flag = false;
        }
    }
}

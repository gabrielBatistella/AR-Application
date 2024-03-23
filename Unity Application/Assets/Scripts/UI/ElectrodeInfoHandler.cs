using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class ElectrodeInfoHandler : MonoBehaviour
{
    [SerializeField] private Transform electrodePoint;
    [SerializeField] private LineRenderer line;
    [SerializeField] private Transform entryPoint;

    [SerializeField] private Canvas infoCanvas;
    [SerializeField] private Text infoText;

    private void Update()
    {
        infoCanvas.transform.rotation = Quaternion.LookRotation(infoCanvas.transform.position - Camera.main.transform.position);
    }

    public void UpdateInfo()
    {
        infoText.text = "Posição do eletrodo: " + transform.parent.InverseTransformPoint(electrodePoint.position) + "\n" +
                        "Ponto de entrada: " + transform.parent.InverseTransformPoint(entryPoint.position);
    }

    public void SetElectrode(Vector3 electrodePosition, Vector3 entryPosition)
    {
        electrodePoint.position = electrodePosition;
        entryPoint.position = entryPosition;

        line.SetPosition(0, electrodePoint.localPosition);
        line.SetPosition(1, entryPoint.localPosition);
    }
}

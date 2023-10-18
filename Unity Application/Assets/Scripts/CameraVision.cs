using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

[RequireComponent(typeof(RawImage))]
public class CameraVision : MonoBehaviour
{
    private WebCamTexture cam;
    private Texture2D camImg;
    private RawImage display;

    private void Awake()
    {
        cam = new WebCamTexture();
        display = GetComponent<RawImage>();
    }

    private void OnDestroy()
    {
        Deactivate();
    }

    public byte[] GetFrameJPG(int quality)
    {
        camImg.SetPixels(cam.GetPixels());
        return camImg.EncodeToJPG(quality);
    }

    public void Activate()
    {
        if (!cam.isPlaying)
        {
            cam.Play();
            display.texture = cam;
            display.rectTransform.sizeDelta = new Vector2(cam.width, cam.height);

            camImg = new Texture2D(cam.width, cam.height, TextureFormat.ARGB32, false);
        }
    }

    public void Deactivate()
    {
        if (cam.isPlaying)
        {
            cam.Stop();
            display.texture = null;
            camImg = null;
        }
    }
}

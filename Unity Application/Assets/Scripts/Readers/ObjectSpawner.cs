using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class ObjectSpawner : MonoBehaviour
{
    [SerializeField] private string bundleFolder;
    [SerializeField] private string bundleName;
    [SerializeField] private Transform freeParent;

    public void LoadObject()
    {
        string bundleURL = bundleFolder + "/" + bundleName + "-";
        #if UNITY_ANDROID
            bundleURL += "Android";
        #else
            bundleURL += "Windows";
        #endif

        AssetBundle bundle = AssetBundle.LoadFromFile(bundleURL);
        //AssetBundle bundle = AssetBundle.LoadFromMemory(bytes);
        if (bundle != null)
        {
            GameObject obj = Instantiate(bundle.LoadAsset<GameObject>(bundleName), transform.position, transform.rotation, freeParent);
            bundle.Unload(false);
        }
    }
}